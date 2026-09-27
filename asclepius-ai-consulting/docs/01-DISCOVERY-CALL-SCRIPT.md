# 01 — Discovery Call Script

This file has two scripts. Use the right one.

- **Part A — Free intro call** (short, no charge): fit, goals, top pain points, regulatory flags. Ends with a Diagnostic quote or a polite no.
- **Part B — Paid Diagnostic session**: the full excavation. Only after the Diagnostic agreement is signed and paid.

---

## Free call boundary (read before every intro call)

| Covers | Does NOT cover |
|---|---|
| Fit and decision-maker | Process mapping or step-by-step workflow walkthroughs |
| Goals for the next 6–12 months | Tool or vendor recommendations |
| The 2–3 top pain points, in the owner's words | A written plan, fix list, or implementation order |
| Whether the business is regulated | Looking at the client's data, screens, recordings, or files |
| Whether a Diagnostic is worth quoting | Savings estimates for specific workflows |

If they push for answers: "That's exactly what the Diagnostic answers. I'd rather give you a real answer in writing than a guess on a call."

---

# Part A — Free intro call

## Opening

"Thanks for making time. This call is to see whether I can actually help, and whether a paid Diagnostic would be worth it for you. I won't be recommending tools today; that's what the Diagnostic is for."

## Fit and goals

1. "What made you take this call now?"
2. "What does the business sell, and roughly how many people work in it?"
3. "Who makes the final call on spending for something like this?"
4. "If this went well, what would be different in 6–12 months?"

## Top pain points (listen; do not solve)

5. "What are the two or three things that eat the most time or cost you the most business?"
6. "Which one bothers you most?"

## Regulatory screen (always ask)

7. "Is any part of the business regulated — for example Medicare, insurance, healthcare, legal, or financial services?"
8. "Do you or your team call or text customers or prospects? Do you keep records of their consent?"
9. "Does your team handle health information, Medicare numbers, Social Security numbers, or similar?"
10. "Do you have a compliance officer, carrier, FMO, or attorney who approves marketing or customer communications?"

If any answer is yes, note it in the CRM and flag the engagement as regulated. See `docs/COMPLIANCE-AND-DATA-HANDLING.md`.

## Close

"Based on what you've told me, I think a Diagnostic makes sense. I'll estimate the scope and send you a written quote with exactly what's included before anything starts. If it's not a fit, I'll tell you that too."

CTA: "Can I send the quote and the Diagnostic agreement over for you to review?"

CRM: move the lead to `intro_done`, then `diagnostic_proposed` when the quote goes out.

---

# Part B — Paid Diagnostic session

## Call goal

Find the 3–5 business bottlenecks where AI-assisted workflow changes can save measurable time or reduce preventable revenue leakage. Do not prescribe live; the paid deliverable is the written AI Prescription.

## 0:00–3:00 — Opening and rapport

"Thanks for making time. The goal today is not to throw AI tools at you. I'm going to understand where work gets stuck, where your team repeats itself, and where the owner's time is being consumed. After this, I'll write an AI Prescription with the outcomes to target, their priority, expected impact, and which option delivers each."

Ask:

1. "What has changed in the business in the last 6–12 months?"
2. "If this was worth your time, what would we have clarity on by the end?"

## 3:00–8:00 — Business overview

- "What does the business sell, and who is the best customer?"
- "How many employees and contractors are involved day to day?"
- "What tools run the business now: CRM, scheduling, bookkeeping, email, project management, phones?"
- "Where does work enter the business: calls, forms, referrals, walk-ins, email, DMs?"
- "What does a normal week look like for you personally?"

## 8:00–13:00 — Compliance and data (required for every client; go deeper for regulated clients)

Do not ask the client to show or send any customer records during this section. Describe, don't share.

1. "Which regulators, carriers, or plans set rules for your marketing and customer communications? (For Medicare: CMS marketing rules, plus your carriers and FMO.)"
2. "Does anyone have to approve marketing materials, scripts, or email/text templates before use? Who, and how long does it take?"
3. "How do you get and store consent before calling or texting someone? Written? Recorded? Where is it kept?"
4. "Do you scrub call lists against Do Not Call lists? Who owns that?"
5. "For Medicare: how do you handle Scope of Appointment, required disclaimers, and call recording today?"
6. "What sensitive data does your team touch: health information, Medicare Beneficiary Identifiers, SSNs, dates of birth, bank details, call recordings?"
7. "Which systems hold that data today? Do any vendors have a signed agreement (such as a BAA) covering it?"
8. "Is anyone on your team already pasting customer information into ChatGPT or similar tools?"
9. "Are there tools your carriers, FMO, or IT have banned or approved?"
10. "Do you have a written data retention or privacy policy we should follow?"

Record the answers in the Prescription's compliance section. Never record the sensitive data itself.

## 13:00–30:00 — Time-drain excavation

### Operations

1. "Which task gets repeated every day even though it feels like it should be systematized?"
2. "Where do jobs, orders, or requests get stuck waiting on a person?"
3. "What information does your team ask you for repeatedly?"
4. "Where do mistakes happen because information is copied from one place to another?"

### Marketing

5. "How consistently do you publish useful content or follow up with your audience?"
6. "What marketing task do you avoid because it takes too long?"
7. "Do you have customer reviews, FAQs, or job photos that are not being reused?"

### Sales

8. "How are new leads captured and followed up?"
9. "How long does it usually take to respond to a serious inquiry?"
10. "Where do prospects disappear in the process?"
11. "What questions do prospects ask before they buy?"

### Finance and admin

12. "What admin work piles up at the end of the week or month?"
13. "Where do invoices, estimates, receipts, or purchase orders slow people down?"
14. "What reports do you wish you had without manually building them?"

### Customer service

15. "What questions do customers ask repeatedly?"
16. "What updates do customers want that your team currently sends manually?"
17. "Where do handoffs break between sales, service, and billing?"
18. "What complaint shows up more than once a month?"

### Owner leverage

19. "If I gave you five hours back every week, what would you spend them on?"
20. "Which task would you most gladly pay someone to make disappear permanently?"

## 30:00–38:00 — Prioritization

"Of everything we discussed, I heard these themes: [repeat three bullets]. Which one feels most expensive right now?"

Capture urgency, budget sensitivity, decision-maker availability, implementation appetite, and any compliance approvals that would gate a change.

## 38:00–45:00 — Close

"I'm going to turn this into your AI Prescription. I'll send it within two business days, then we'll schedule a short delivery call to walk through priority, risk, and whether you want help delivering any of it."

CRM: move the lead to `diagnostic_delivered` after the Prescription is sent.

## What not to do

- Do not prescribe tools live on either call.
- Do not map processes or give recommendations on the free intro call.
- Do not quote a price on either call; quotes go out in writing after scope and effort are estimated.
- Do not diagnose from buzzwords; diagnose from repeated work, delay, errors, and owner bottlenecks.
- Do not promise exact savings; use conservative ranges.
- Do not accept implementation scope before the Prescription is written.
- Do not accept, view, or record customer PHI, Medicare numbers, SSNs, or recordings during discovery.
