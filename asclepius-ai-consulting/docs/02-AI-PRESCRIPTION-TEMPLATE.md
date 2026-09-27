# 02 — AI Prescription Template

## What this document is (and is not)

The AI Prescription prescribes **outcomes and priorities**: what to fix, in what order, the expected impact, and which option delivers it. It is a decision document for the owner.

It is **not** an implementation guide. Do not include:

- step-by-step setup or configuration instructions
- prompts, scripts, automations, or integration recipes
- vendor-specific click paths or account settings

You may name the *category* of solution (for example "shared FAQ response library" or "automated review request"), so the owner understands what they are choosing. How to build it is Build work, delivered under a Build agreement or by the client's own team.

## Client

- Business:
- Owner:
- Date:
- Diagnostic focus:
- Regulated business? (Y/N — which rules apply):

## Executive summary

Two or three sentences in plain English: where the business is losing time or revenue, the single most important outcome to target first, and why.

## What we found

| # | Bottleneck | Plain-language symptom | Business cost (conservative) |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## What we prescribe — outcomes and priorities

| Priority | Outcome to achieve | Why this, why now | Expected impact (range) | Confidence | Delivered by |
|---|---|---|---|---|---|
| 1 |  |  |  | High / Med / Low | Build / Retainer / Office Hours / Client team |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

Guidance:

- **Outcome** is a result the owner can check, e.g. "every web inquiry gets a first reply within one business hour," not a tool.
- **Expected impact** uses conservative ranges. Count owner hours separately from staff hours.
- **Delivered by** names the tier that fits. "Client team" is a legitimate answer; say so when it is.

## Risks, dependencies, and compliance flags

| Priority | Risk or dependency | Who must approve before go-live |
|---|---|---|
|  | e.g. touches customer texting (TCPA consent) | Client compliance officer / counsel |
|  | e.g. involves beneficiary or health data | Owner + client compliance; tool must be on the approved list |

See `docs/COMPLIANCE-AND-DATA-HANDLING.md`. Any outcome that touches restricted data or call/text outreach stays blocked until the named approver signs off.

## What we recommend NOT doing (yet)

List tempting ideas that are low-value, high-risk, or premature, with one line on why.

## Next step

"If you want help delivering Priority 1 (and optionally 2), I'll scope it and send a fixed-fee Build quote in writing. Nothing starts until you approve it. If you'd rather have your team deliver it, the priorities above still stand."

---

# Worked example — 12-person HVAC company

*Fictional. Illustrates format only.*

## Client

- Business: North Ridge HVAC
- Owner: Fictional example
- Date: August 2026
- Diagnostic focus: lead response, dispatch admin, customer communication, review generation
- Regulated business? N (but customer texting is subject to TCPA consent rules)

## Executive summary

North Ridge loses booked jobs because inquiries wait for the office manager, and staff lose several hours a week retyping the same answers. Fix response time first, then the repeated-answer load, then invoicing delays.

## What we found

| # | Bottleneck | Plain-language symptom | Business cost (conservative) |
|---|---|---|---|
| 1 | Slow lead follow-up | Web inquiries and voicemail callbacks wait until the office manager has a break. | Lost booked jobs and owner anxiety. |
| 2 | Repetitive customer questions | Staff retype answers about service windows, maintenance plans, and financing. | 5–8 staff hours/week. |
| 3 | Messy dispatch notes | Tech notes are inconsistent, making follow-up and invoicing slower. | Delayed invoices and callbacks. |
| 4 | Inconsistent review requests | Happy customers are not asked at the right time. | Missed local search and trust signals. |

## What we prescribe — outcomes and priorities

| Priority | Outcome to achieve | Why this, why now | Expected impact (range) | Confidence | Delivered by |
|---|---|---|---|---|---|
| 1 | Staff answer common customer questions from one approved answer set instead of retyping. | Lowest risk, fastest adoption, frees time for Priority 2. | About 5 staff hours/week. | High | Build (small) or Client team |
| 2 | Every inquiry gets a first human-approved reply within one business hour. | Largest revenue leak. | 2–4 additional booked jobs/month if the current missed-lead pattern holds. | Medium | Build |
| 3 | Tech notes reach the office invoice-ready the same day. | Speeds cash collection. | About 3 admin hours/week; faster invoicing. | High | Build (pilot with two technicians) |
| 4 | Satisfied customers are asked for a review at the right moment, every time. | Compounds local trust once 1–3 are stable. | 6–12 new reviews/quarter. | Medium | Retainer or Client team |

## Risks, dependencies, and compliance flags

| Priority | Risk or dependency | Who must approve before go-live |
|---|---|---|
| 2, 4 | Any texting requires documented prior consent and opt-out handling (TCPA). | Owner, with counsel if unsure. |
| 3 | Field staff adoption; pilot before rollout. | Owner and lead technician. |

## What we recommend NOT doing (yet)

- AI phone answering: high customer-experience risk and consent questions; revisit after Priority 2 is stable.

## Next step

Scope Priorities 1 and 2 as a fixed-fee Build, quoted in writing after scope and effort are estimated, with a 14-day tune-up window.
