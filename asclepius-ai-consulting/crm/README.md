# CRM README

Stdlib SQLite CRM for MMM Consulting. Run `python3 crm/crm.py --help` and each subcommand with `--help`.

## Pipeline stages (ladder order)

Lead status must be one of these keys (enforced by `crm.py`; run `list-stages` to print them):

| # | Key | Label |
|---|---|---|
| 1 | `lead` | Lead |
| 2 | `intro_booked` | Intro call booked |
| 3 | `intro_done` | Intro done |
| 4 | `diagnostic_proposed` | Diagnostic proposed |
| 5 | `diagnostic_signed` | Diagnostic signed |
| 6 | `diagnostic_delivered` | Diagnostic delivered |
| 7 | `build_proposed` | Build proposed |
| 8 | `build_signed` | Build signed |
| 9 | `build_delivered` | Build delivered |
| 10 | `retainer_active` | Retainer active |
| 11 | `office_hours_active` | Office Hours active |
| 12 | `closed_lost` | Closed-lost |

`pipeline` prints a count of leads per stage. Older databases with legacy statuses (e.g. `new`, `qualified`) still load; `pipeline` lists those as unrecognized so they can be moved with `update-status`.

## Prices

Engagement prices are entered per engagement with `--price`, taken from the signed quote. Nothing is defaulted.

## Data rule

Do not store PHI, Medicare Beneficiary Identifiers, SSNs, or a client's customer records in this CRM. It holds business-contact and deal data only. See `docs/COMPLIANCE-AND-DATA-HANDLING.md`.
