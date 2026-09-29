# MMM Consulting

`PROJECT_NAME = MMM Consulting` (brand: deep teal, matching the shipped logo/form/Calendly assets). The repository folder is still named `asclepius-ai-consulting/` for path stability; that name is internal only.

**One-line pitch:** MMM Consulting sells "The AI Prescription": a doctor-style diagnostic and implementation service for owner-operated small businesses that want practical AI wins without becoming AI experts.

## Pricing

No prices are published. Every engagement is priced after we estimate scope and effort, and quoted in writing before any work starts. See `docs/00-DOCTRINE.md` ("Pricing principle").

## The offer ladder

0. **Free intro call**: fit, goals, and top pain points only. No process mapping, tool recommendations, or written plan (see the free call boundary in `docs/00-DOCTRINE.md`).
1. **The Diagnostic**: a structured discovery session and a written AI Prescription that names the outcomes to target, their priority, expected impact, and which tier delivers each.
2. **The Build**: fixed-fee implementation of approved Prescription items: setup, integrations, prompts, SOPs, and training.
3. **The Retainer**: ongoing AI ops, quarterly re-diagnosis, workflow tuning, tool evaluation, and staff onboarding, with an explicit monthly hour cap for light support.
4. **Office Hours / Overflow**: pre-booked blocks of ad hoc expert help for clients not ready for a retainer.

## Compliance

Regulated clients (our first client is a Medicare/life-insurance business) follow `docs/COMPLIANCE-AND-DATA-HANDLING.md`: CMS marketing awareness, TCPA consent before calls/texts, no PHI or beneficiary identifiers in unapproved tools, and an approved-AI-tools list that defaults to **none**.

## Templates

Agreements (Diagnostic, Build/Retainer, Office Hours), proposals, intake form, invoice, follow-up emails, Refund and Risk-Reversal Policy, and Testimonial/Case-Study Consent live in `templates/`. All agreements are templates, not legal advice; have a licensed attorney review before use.

## Quickstart

```bash
# Run all tests
python3 -m unittest discover -s tests

# Create and inspect a local CRM database (pipeline stages: python3 crm/crm.py list-stages)
python3 crm/crm.py --db crm/mmm_consulting.db add-lead --name "Jordan Lee" --business "Lee HVAC" --source "warm_referral"
python3 crm/crm.py --db crm/mmm_consulting.db list-leads
python3 crm/crm.py --db crm/mmm_consulting.db update-status --lead-id 1 --status intro_booked
python3 crm/crm.py --db crm/mmm_consulting.db pipeline
python3 crm/crm.py --db crm/mmm_consulting.db add-engagement --lead-id 1 --tier Diagnostic --price <QUOTED_PRICE> --status closed_won
python3 crm/crm.py --db crm/mmm_consulting.db revenue-summary

# Pricing calculator: every price is an input (owner-approved), never a default
python3 finance/pricing-calculator.py hourly --tier build --hours 20 --rate <RATE> --complexity 1.5
python3 finance/pricing-calculator.py fixed --tier build --fee <FEE> --estimated-hours 30
python3 finance/pricing-calculator.py retainer --monthly-fee <FEE> --monthly-hour-cap 8

# ROI calculator: the Diagnostic price from the written quote is required
python3 finance/roi-calculator-for-prospects.py --hours-per-week 6 --hourly-value 50 --diagnostic-price <QUOTED_PRICE>

# Open the landing page
python3 -m http.server 8000 --directory website
# then visit http://localhost:8000
```

## Design note

This is a standalone consulting venture, intentionally decoupled from HermesOS/RichieRichOS. The CRM schema is deliberately plain SQLite so it could later export into HermesOS if Richie chooses, but no integration is built now. That remains a future business/technical decision.
