# Final Checklist

## Built

- Doctrine, discovery script (free intro call + paid Diagnostic), AI Prescription template with HVAC worked example, upsell ladder, acquisition plan, tool stack reference, and ADR.
- Compliance and Data Handling Standard (`docs/COMPLIANCE-AND-DATA-HANDLING.md`).
- Client proposals, agreements (Diagnostic, Build/Retainer, Office Hours), intake, invoice, follow-up emails, Refund and Risk-Reversal Policy, and Testimonial/Case-Study Consent.
- Outreach copy for all seven acquisition channels.
- Stdlib SQLite CRM with ladder pipeline stages, pricing calculator, ROI calculator, and static landing page.

## Review fixes applied (owner decisions 2026-09-26)

- [x] **Rebrand:** "MMM Consulting" replaces the old working name in all client-facing content; website restyled deep teal (matching the shipped logo/form/Calendly assets, brand mark #175044; all text pairs pass WCAG AA — see `website/style.css` header). Folder name unchanged.
- [x] **Finding 1 — pricing:** all hardcoded prices removed from README, doctrine, agreements, proposals, email sequence, discovery script, Prescription example, calculators, and landing page. Replaced with scope-based pricing language. Calculators take price as a required input; pricing calculator supports hourly, fixed-fee, and retainer quoting; retainer has an explicit monthly hour cap.
- [x] **Finding 2 — free call vs. paid Diagnostic:** free call boundary added to doctrine and discovery script. Prescription template rewritten to prescribe outcomes, priorities, expected impact, and delivering tier, with no step-by-step how-to.
- [x] **Finding 3 — Diagnostic agreement:** expanded to full paper (scope, deliverables, timeline, client responsibilities, exclusions, change control, payment, confidentiality, data handling, limitation of liability, no guaranteed results, termination, signatures) with "Template — not legal advice" banner.
- [x] **Finding 4 — compliance:** new Compliance and Data Handling Standard (CMS marketing awareness, TCPA consent, HIPAA-adjacent handling, data classification, approved AI tools list defaulting to none). Compliance questions added to discovery script and intake form. Referenced from all agreements.
- [x] **Finding 6 — CRM and templates:** CRM pipeline stages (Lead → … → Closed-lost) enforced in `crm/crm.py` with tests; new Refund/Risk-Reversal Policy, Office Hours agreement, and Testimonial/Case-Study Consent.

## Validation results

- Test suite: 16 tests passing via `python3 -m unittest discover -s tests`.
- CRM: stage order, stage validation, missing-lead rejection, pipeline counts, required engagement price, revenue summary.
- Calculators: hourly, fixed-fee, and retainer math; required-price and required-hour-cap enforcement; no hardcoded prices in source.
- Landing page: static HTML/CSS; booking link and contact placeholders remain intentionally visible.

## OPEN — NEEDS RICHIE'S DECISION

- [ ] **Legal entity:** replace `[LEGAL ENTITY — owner to confirm]` in agreements, policy, and invoice.
- [ ] **Governing law and venue:** replace `[GOVERNING LAW — owner to confirm]`.
- [ ] **E&O (professional liability) insurance**, and whether cyber insurance is needed for regulated clients.
- [ ] **Final pricing:** approve Diagnostic, Build, Retainer (including monthly hour cap and overage terms), and Office Hours pricing approach. Nothing is published until approved.
- [ ] **Refund policy terms:** `templates/refund-and-risk-reversal-policy.md` is now a bare stub (owner rejected the earlier invented structure on 2026-09-27) — the owner needs to decide whether any risk-reversal/guarantee exists at all, then the specific terms; see that file's "Owner decisions needed" list.
- [x] **Calendly URL:** owner-confirmed and live on the landing page: `https://calendly.com/mmminvestment25/30min`.
- [ ] **Contact details:** replace `[CONTACT EMAIL]` and `[PHONE]`.
- [ ] **AI tools approved for client data:** fill in section 7 of `docs/COMPLIANCE-AND-DATA-HANDLING.md` (default is none).
- [ ] **Attorney review** of all agreements, the refund policy, the consent form, and the compliance standard before first use.
- [ ] Whether CRM ever exports into HermesOS/RichieRichOS; no integration is built now.
