#!/usr/bin/env python3
"""ROI calculator for prospects.

The Diagnostic price is a REQUIRED input. There is no default price in this
file; use the figure from the written quote you are sending this prospect.

Example (substitute the quoted price for <...>):
  python finance/roi-calculator-for-prospects.py --hours-per-week 6 --hourly-value 50 --diagnostic-price <QUOTED_PRICE>
"""
import argparse


def calculate(hours_per_week, hourly_value, diagnostic_price):
    """Returns (annualized cost of the problem, multiple of the quoted Diagnostic price)."""
    if diagnostic_price is None or diagnostic_price <= 0:
        raise ValueError('diagnostic_price must be greater than zero (use the quoted price)')
    if hours_per_week < 0 or hourly_value < 0:
        raise ValueError('hours_per_week and hourly_value cannot be negative')
    annual = hours_per_week * hourly_value * 52
    multiple = annual / diagnostic_price
    return round(annual, 2), round(multiple, 1)


def main(argv=None):
    p = argparse.ArgumentParser(description='Annualized cost of a bottleneck vs. the quoted Diagnostic price')
    p.add_argument('--hours-per-week', type=float, required=True)
    p.add_argument('--hourly-value', type=float, required=True)
    p.add_argument('--diagnostic-price', type=float, required=True,
                   help="The Diagnostic price from this prospect's written quote")
    a = p.parse_args(argv)
    try:
        annual, multiple = calculate(a.hours_per_week, a.hourly_value, a.diagnostic_price)
    except ValueError as e:
        p.error(str(e))
    print(f'Annualized cost of problem: ${annual:.2f}')
    print(f'That is {multiple}x the quoted Diagnostic price')
    print('Conservative estimate only; not a guarantee of savings.')


if __name__ == '__main__':
    main()
