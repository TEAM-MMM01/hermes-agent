#!/usr/bin/env python3
"""MMM Consulting pricing calculator.

There are NO baked-in prices in this file. Every dollar figure is an explicit
input supplied by whoever is preparing the quote, after scope and effort have
been estimated. The calculator only does the math and sanity checks.

Three quoting modes:

  hourly     price = estimated hours x hourly rate x complexity multiplier
  fixed      a fixed fee already chosen for the scope; shows the effective
             hourly rate against the effort estimate so you can see whether
             the fee holds up
  retainer   monthly fee + an explicit monthly hour cap for "light support";
             shows the effective hourly rate if the full cap is used

Examples (substitute owner-approved numbers for <...>):
  python finance/pricing-calculator.py hourly --tier build --hours 20 --rate <RATE> --complexity 1.5
  python finance/pricing-calculator.py fixed --tier build --fee <FEE> --estimated-hours 30
  python finance/pricing-calculator.py retainer --monthly-fee <FEE> --monthly-hour-cap 8
"""
import argparse

TIERS = ('diagnostic', 'build', 'retainer', 'office-hours')


def _positive(name, value):
    if value is None or value <= 0:
        raise ValueError(f'{name} must be greater than zero')
    return value


def quote_hourly(hours, rate, complexity=1.0):
    """Hours x rate x complexity. Returns (price, effective_rate_per_hour)."""
    _positive('hours', hours)
    _positive('rate', rate)
    _positive('complexity', complexity)
    price = hours * rate * complexity
    return round(price, 2), round(price / hours, 2)


def quote_fixed_fee(fee, estimated_hours):
    """Fixed fee chosen for the scope. Returns (price, effective_rate_per_hour)."""
    _positive('fee', fee)
    _positive('estimated_hours', estimated_hours)
    return round(fee, 2), round(fee / estimated_hours, 2)


def quote_retainer(monthly_fee, monthly_hour_cap):
    """Retainer with an explicit monthly hour cap for light support.

    Returns a dict with the monthly price, the hour cap, and the effective
    hourly rate if the client uses the full cap.
    """
    _positive('monthly_fee', monthly_fee)
    _positive('monthly_hour_cap', monthly_hour_cap)
    return {
        'monthly_price': round(monthly_fee, 2),
        'monthly_hour_cap': monthly_hour_cap,
        'effective_rate_at_cap': round(monthly_fee / monthly_hour_cap, 2),
    }


def build_parser():
    p = argparse.ArgumentParser(
        description='MMM Consulting pricing calculator. All prices are inputs; nothing is hardcoded.')
    sub = p.add_subparsers(dest='mode', required=True)

    s = sub.add_parser('hourly', help='Quote as hours x rate x complexity')
    s.add_argument('--tier', choices=TIERS, required=True)
    s.add_argument('--hours', type=float, required=True, help='Estimated hours of effort')
    s.add_argument('--rate', type=float, required=True, help='Hourly rate (owner-approved)')
    s.add_argument('--complexity', type=float, default=1.0, help='Complexity multiplier (default 1.0)')

    s = sub.add_parser('fixed', help='Check a fixed fee against estimated effort')
    s.add_argument('--tier', choices=TIERS, required=True)
    s.add_argument('--fee', type=float, required=True, help='Fixed fee (owner-approved)')
    s.add_argument('--estimated-hours', type=float, required=True, help='Estimated hours of effort')

    s = sub.add_parser('retainer', help='Monthly retainer with an explicit light-support hour cap')
    s.add_argument('--monthly-fee', type=float, required=True, help='Monthly fee (owner-approved)')
    s.add_argument('--monthly-hour-cap', type=float, required=True,
                   help='Maximum light-support hours included per month')
    return p


def main(argv=None):
    p = build_parser()
    a = p.parse_args(argv)
    try:
        if a.mode == 'hourly':
            price, rate = quote_hourly(a.hours, a.rate, a.complexity)
            print(f'[{a.tier}] Hourly quote: ${price:.2f}')
            print(f'Effective rate: ${rate:.2f}/hour')
        elif a.mode == 'fixed':
            price, rate = quote_fixed_fee(a.fee, a.estimated_hours)
            print(f'[{a.tier}] Fixed-fee quote: ${price:.2f}')
            print(f'Effective rate vs. estimate: ${rate:.2f}/hour')
        else:
            q = quote_retainer(a.monthly_fee, a.monthly_hour_cap)
            print(f"[retainer] Monthly fee: ${q['monthly_price']:.2f}")
            print(f"Light-support hour cap: {q['monthly_hour_cap']:g} hours/month")
            print(f"Effective rate if cap is fully used: ${q['effective_rate_at_cap']:.2f}/hour")
    except ValueError as e:
        p.error(str(e))
    print('Reminder: quote in writing, with scope and exclusions, before any work starts.')


if __name__ == '__main__':
    main()
