#!/usr/bin/env python3
"""Local SQLite CRM for MMM Consulting.

Lead status is restricted to the pipeline stages below, which track the
offer ladder: free intro call -> paid Diagnostic -> Build -> Retainer /
Office Hours. Prices are always entered per engagement; none are hardcoded.
"""
import argparse, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = Path(__file__).with_name('schema.sql').read_text()

# (key, human label) in ladder order. Keys are what is stored in the DB.
PIPELINE_STAGES = (
    ('lead', 'Lead'),
    ('intro_booked', 'Intro call booked'),
    ('intro_done', 'Intro done'),
    ('diagnostic_proposed', 'Diagnostic proposed'),
    ('diagnostic_signed', 'Diagnostic signed'),
    ('diagnostic_delivered', 'Diagnostic delivered'),
    ('build_proposed', 'Build proposed'),
    ('build_signed', 'Build signed'),
    ('build_delivered', 'Build delivered'),
    ('retainer_active', 'Retainer active'),
    ('office_hours_active', 'Office Hours active'),
    ('closed_lost', 'Closed-lost'),
)
STAGE_KEYS = tuple(k for k, _ in PIPELINE_STAGES)
STAGE_LABELS = dict(PIPELINE_STAGES)
DEFAULT_STAGE = 'lead'

TIERS = ('Diagnostic', 'Build', 'Retainer', 'Office Hours')
ENGAGEMENT_STATUSES = ('open', 'closed_won', 'closed_lost')


def conn(path):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db


def add_lead(a):
    with conn(a.db) as db:
        db.execute('INSERT INTO leads(name,business,source_channel,status) VALUES(?,?,?,?)',
                   (a.name, a.business, a.source, a.status))
    print('Lead added')


def list_leads(a):
    with conn(a.db) as db:
        for r in db.execute('SELECT id,name,business,source_channel,status,created_at FROM leads ORDER BY id'):
            print(' | '.join(map(str, r)))


def update_status(a):
    with conn(a.db) as db:
        cur = db.execute('UPDATE leads SET status=? WHERE id=?', (a.status, a.lead_id))
        if cur.rowcount == 0:
            sys.exit(f'No lead with id {a.lead_id}')
    print(f'Status updated: {STAGE_LABELS[a.status]}')


def list_stages(a):
    for i, (key, label) in enumerate(PIPELINE_STAGES, 1):
        print(f'{i:2d}. {key} | {label}')


def pipeline(a):
    with conn(a.db) as db:
        counts = dict(db.execute('SELECT status, COUNT(*) FROM leads GROUP BY status').fetchall())
    for key, label in PIPELINE_STAGES:
        print(f'{label} | {counts.pop(key, 0)}')
    for key, n in counts.items():  # legacy statuses from older databases
        print(f'(unrecognized stage: {key}) | {n}')


def add_engagement(a):
    closed = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if a.status == 'closed_won' else None
    with conn(a.db) as db:
        db.execute('INSERT INTO engagements(lead_id,tier,price,status,closed_at) VALUES(?,?,?,?,?)',
                   (a.lead_id, a.tier, a.price, a.status, closed))
    print('Engagement added')


def revenue_summary(a):
    with conn(a.db) as db:
        rows = db.execute("SELECT tier, strftime('%Y-%m', COALESCE(closed_at, started_at)) month, SUM(price) "
                          "FROM engagements WHERE status='closed_won' GROUP BY tier, month ORDER BY month,tier").fetchall()
    total = sum(r[2] for r in rows)
    for tier, month, amt in rows:
        print(f'{month} | {tier} | ${amt:.2f}')
    print(f'TOTAL | ${total:.2f}')


def build_parser():
    p = argparse.ArgumentParser(description='Local SQLite CRM for MMM Consulting')
    p.add_argument('--db', default='mmm_consulting.db')
    sub = p.add_subparsers(required=True)
    s = sub.add_parser('add-lead', help='Add a lead')
    s.add_argument('--name', required=True)
    s.add_argument('--business', required=True)
    s.add_argument('--source', required=True)
    s.add_argument('--status', choices=STAGE_KEYS, default=DEFAULT_STAGE)
    s.set_defaults(func=add_lead)
    s = sub.add_parser('list-leads', help='List leads')
    s.set_defaults(func=list_leads)
    s = sub.add_parser('update-status', help='Move a lead to a pipeline stage')
    s.add_argument('--lead-id', type=int, required=True)
    s.add_argument('--status', choices=STAGE_KEYS, required=True)
    s.set_defaults(func=update_status)
    s = sub.add_parser('list-stages', help='List pipeline stages in ladder order')
    s.set_defaults(func=list_stages)
    s = sub.add_parser('pipeline', help='Count leads per pipeline stage')
    s.set_defaults(func=pipeline)
    s = sub.add_parser('add-engagement', help='Add engagement (price is always entered, never defaulted)')
    s.add_argument('--lead-id', type=int, required=True)
    s.add_argument('--tier', choices=TIERS, required=True)
    s.add_argument('--price', type=float, required=True)
    s.add_argument('--status', choices=ENGAGEMENT_STATUSES, default='open')
    s.set_defaults(func=add_engagement)
    s = sub.add_parser('revenue-summary', help='Print revenue by tier and month')
    s.set_defaults(func=revenue_summary)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    a.func(a)


if __name__ == '__main__':
    main()
