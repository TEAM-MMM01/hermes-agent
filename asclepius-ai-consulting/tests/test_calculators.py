import importlib.util, io, re, unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load(p, n):
    spec = importlib.util.spec_from_file_location(n, ROOT / p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


pricing = load('finance/pricing-calculator.py', 'pricing')
roi = load('finance/roi-calculator-for-prospects.py', 'roi')

# All numbers below are arbitrary test inputs, not prices.


class PricingTests(unittest.TestCase):
    def test_hourly_math(self):
        self.assertEqual(pricing.quote_hourly(20, 100, 1.5), (3000, 150))

    def test_fixed_fee_effective_rate(self):
        self.assertEqual(pricing.quote_fixed_fee(1200, 16), (1200, 75))

    def test_retainer_requires_hour_cap(self):
        q = pricing.quote_retainer(800, 8)
        self.assertEqual(q, {'monthly_price': 800, 'monthly_hour_cap': 8, 'effective_rate_at_cap': 100})
        with self.assertRaises(ValueError):
            pricing.quote_retainer(800, 0)

    def test_rejects_non_positive_inputs(self):
        with self.assertRaises(ValueError):
            pricing.quote_hourly(10, 0)
        with self.assertRaises(ValueError):
            pricing.quote_fixed_fee(0, 10)

    def test_cli_requires_rate(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            pricing.main(['hourly', '--tier', 'build', '--hours', '10'])

    def test_cli_retainer_requires_cap(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            pricing.main(['retainer', '--monthly-fee', '800'])

    def test_cli_fixed_output(self):
        out = io.StringIO()
        with redirect_stdout(out):
            pricing.main(['fixed', '--tier', 'build', '--fee', '1200', '--estimated-hours', '16'])
        self.assertIn('75.00/hour', out.getvalue())

    def test_no_hardcoded_prices_in_source(self):
        for path in ('finance/pricing-calculator.py', 'finance/roi-calculator-for-prospects.py'):
            src = (ROOT / path).read_text()
            self.assertNotIn('RANGES', src)
            self.assertNotIn('999', src)
            self.assertIsNone(re.search(r'\$[0-9]', src), path)


class RoiTests(unittest.TestCase):
    def test_roi_math(self):
        self.assertEqual(roi.calculate(6, 150, 1000), (46800, 46.8))

    def test_price_is_required(self):
        with self.assertRaises(TypeError):
            roi.calculate(6, 150)
        with self.assertRaises(ValueError):
            roi.calculate(6, 150, 0)

    def test_cli_requires_price(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            roi.main(['--hours-per-week', '6', '--hourly-value', '150'])


if __name__ == '__main__':
    unittest.main()
