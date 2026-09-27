# 00 — Doctrine

## Mission

Help owner-operated small businesses safely adopt AI where it saves real time, reduces expensive manual work, and improves customer responsiveness, without asking the owner to become technical. MMM Consulting is a consulting practice, not a software platform: Richie diagnoses, prescribes, implements, and trains.

## Positioning statement

**The AI Prescription:** a doctor-style diagnostic-then-treatment model for small business owners who feel behind on AI and need a trusted operator to identify practical, low-risk workflows.

## Ideal client profile

Owner-operated businesses with 3–50 employees, especially service-based or light-product operations where the owner has budget authority and feels the pain of messy admin. Examples:

- 8–25 person HVAC, plumbing, roofing, landscaping, or home-services companies.
- Clinics, dental offices, med spas, physical therapy practices, and wellness offices.
- Insurance agencies (including Medicare and life insurance), small law firms, accounting firms, agencies, and professional services shops.
- Local retailers or distributors with repetitive customer questions, ordering, and follow-up.

Regulated clients (insurance, healthcare, legal, financial) are welcome but always go through `docs/COMPLIANCE-AND-DATA-HANDLING.md` before any client data is touched.

## Pricing principle

**There are no published prices.** Every engagement is priced after we estimate scope and effort, and quoted in writing before any work starts. No dollar figure appears in marketing, scripts, templates, or the website until the owner approves it.

- Quotes may be fixed-fee (preferred for Diagnostic and Build) or hourly (Office Hours). The pricing calculator (`finance/pricing-calculator.py`) supports both; the price is always an input, never a built-in number.
- Retainers always state an explicit monthly hour cap for light support. Work beyond the cap is quoted separately or moved to a Build.
- A quote names scope, deliverables, exclusions, timeline, and price. No quote, no work.

## The offer ladder and rationale

### 0. Free intro call (not a tier; no charge)

A short fit conversation. It exists to decide whether a paid Diagnostic makes sense, not to deliver one. See "Free call boundary" below.

### 1. The Diagnostic

A structured discovery session and a written AI Prescription. Priced after we estimate scope and effort; quoted in writing before any work starts. The margin is secondary: this tier creates trust, exposes implementation work, and gives Richie permission to make a specific Build offer.

### 2. The Build

Fixed-fee implementation, quoted per prescription line item after scoping. Small setup projects and multi-workflow rollouts are quoted separately so the client always sees what each outcome costs. Fixed fees protect the client from hourly uncertainty and reward Richie for speed.

### 3. The Retainer

Turns one-time implementation into compounding support: quarterly re-diagnosis, tool evaluation, workflow tuning, new-hire onboarding, and light support up to a stated monthly hour cap. The goal is to convert 30–50% of Build clients within 90 days.

### 4. Office Hours / Overflow

For clients who need occasional expert help but do not want a retainer. Billed per hour in pre-booked blocks under the Office Hours agreement. Not the main revenue engine; a paid safety valve that prevents unpaid favors and keeps relationships alive.

## Free call boundary

The free intro call and the paid Diagnostic are different products. Hold the line.

| The free intro call covers | The free intro call does NOT cover |
|---|---|
| Fit: is this a business we can help, and is the owner the decision-maker? | Process mapping or walking through workflows step by step |
| Goals: what the owner wants to be true in 6–12 months | Tool or vendor recommendations, even "just a quick one" |
| Top pain points: the 2–3 problems the owner names, in their words | A written plan, summary of fixes, or implementation order |
| Regulatory flags: is the business regulated (e.g., Medicare, insurance, healthcare)? | Reviewing the client's data, screens, recordings, or documents |
| Next step: whether a Diagnostic is worth quoting | Estimating savings for specific workflows |

If the prospect pushes for recommendations on the free call: "That's exactly what the Diagnostic answers, and I'd rather give you a real answer in writing than a guess on a call."

## Compliance posture

- Client data is classified before it is handled (`docs/COMPLIANCE-AND-DATA-HANDLING.md`).
- By default, **no AI tool is approved for client data** until the owner adds it to the approved list in that document.
- For regulated clients, the client's compliance officer, carrier, or counsel signs off on any customer-facing workflow (calls, texts, marketing copy) before it goes live. We flag risks; we do not give legal or compliance advice.

## What we will never do

- We will not turn a free intro call or a Diagnostic call into free implementation or live tool shopping.
- We will not quote a price out loud or in writing before scope and effort are estimated.
- We will not work for free "to build the portfolio"; if a case study is useful, discount intentionally, document the exchange, and use the testimonial/case-study consent clause.
- We will not automate human judgment calls that require client context, ethics, legal review, or owner approval.
- We will not prescribe tools without verifying current pricing, privacy posture, and client fit.
- We will not put PHI, Medicare Beneficiary Identifiers, SSNs, or other restricted data into any tool that is not on the approved list.
- We will not build call, text, or voice outreach for a client without documented consent handling and the client's compliance sign-off.
- We will not accept open-ended "make us AI-powered" scopes; every Build has named deliverables and boundaries.
