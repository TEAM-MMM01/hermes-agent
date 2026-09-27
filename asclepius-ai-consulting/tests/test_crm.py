import importlib.util, subprocess, sys, tempfile, unittest
from pathlib import Path

CRM = Path(__file__).parents[1] / 'crm' / 'crm.py'
_spec = importlib.util.spec_from_file_location('crm', CRM)
crm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(crm)

EXPECTED_STAGES = [
    'Lead', 'Intro call booked', 'Intro done', 'Diagnostic proposed', 'Diagnostic signed',
    'Diagnostic delivered', 'Build proposed', 'Build signed', 'Build delivered',
    'Retainer active', 'Office Hours active', 'Closed-lost',
]


class CRMTests(unittest.TestCase):
    def run_crm(self, db, *args, check=True):
        return subprocess.run([sys.executable, str(CRM), '--db', str(db), *args],
                              text=True, capture_output=True, check=check)

    def test_stage_order_matches_ladder(self):
        self.assertEqual([label for _, label in crm.PIPELINE_STAGES], EXPECTED_STAGES)
        self.assertEqual(crm.DEFAULT_STAGE, 'lead')
        self.assertEqual(len(set(crm.STAGE_KEYS)), len(crm.STAGE_KEYS))

    def test_add_update_revenue(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 't.db'
            self.run_crm(db, 'add-lead', '--name', 'A', '--business', 'B', '--source', 'warm')
            out = self.run_crm(db, 'list-leads').stdout
            self.assertIn('A | B', out)
            self.assertIn('| lead |', out)
            self.run_crm(db, 'update-status', '--lead-id', '1', '--status', 'diagnostic_signed')
            self.assertIn('diagnostic_signed', self.run_crm(db, 'list-leads').stdout)
            # 100 is an arbitrary test fixture amount, not a price.
            self.run_crm(db, 'add-engagement', '--lead-id', '1', '--tier', 'Diagnostic',
                         '--price', '100', '--status', 'closed_won')
            out = self.run_crm(db, 'revenue-summary').stdout
            self.assertIn('Diagnostic | $100.00', out)
            self.assertIn('TOTAL | $100.00', out)

    def test_invalid_stage_and_missing_lead_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 't.db'
            self.run_crm(db, 'add-lead', '--name', 'A', '--business', 'B', '--source', 'warm')
            r = self.run_crm(db, 'update-status', '--lead-id', '1', '--status', 'qualified', check=False)
            self.assertNotEqual(r.returncode, 0)
            r = self.run_crm(db, 'update-status', '--lead-id', '99', '--status', 'intro_done', check=False)
            self.assertNotEqual(r.returncode, 0)

    def test_pipeline_counts_and_list_stages(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 't.db'
            self.run_crm(db, 'add-lead', '--name', 'A', '--business', 'B', '--source', 'warm')
            self.run_crm(db, 'add-lead', '--name', 'C', '--business', 'D', '--source', 'partner',
                         '--status', 'retainer_active')
            out = self.run_crm(db, 'pipeline').stdout
            self.assertIn('Lead | 1', out)
            self.assertIn('Retainer active | 1', out)
            self.assertIn('Closed-lost | 0', out)
            stages = self.run_crm(db, 'list-stages').stdout.splitlines()
            self.assertEqual(len(stages), 12)
            self.assertIn('office_hours_active | Office Hours active', stages[10])

    def test_engagement_price_required(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 't.db'
            self.run_crm(db, 'add-lead', '--name', 'A', '--business', 'B', '--source', 'warm')
            r = self.run_crm(db, 'add-engagement', '--lead-id', '1', '--tier', 'Build', check=False)
            self.assertNotEqual(r.returncode, 0)


if __name__ == '__main__':
    unittest.main()
