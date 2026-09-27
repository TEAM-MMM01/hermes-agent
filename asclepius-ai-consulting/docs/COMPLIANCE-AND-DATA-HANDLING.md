# Compliance and Data Handling Standard

**Internal operating standard for MMM Consulting. Not legal advice.** Regulations change, often annually. Before relying on anything below for a specific client, confirm current requirements with the client's compliance officer, carrier/FMO, or counsel, and with our own attorney. Referenced from every client agreement as the "Data Handling Standard."

Status: DRAFT — owner review required. Last reviewed: 2026-09-27.

## 1. Why this exists

Our first client is a Medicare and life-insurance business. That work touches federal marketing rules, consent rules for calls and texts, and sensitive personal and health-related data. A consultant who suggests an AI workflow that breaks those rules creates real liability for the client and for us. This standard keeps that from happening.

## 2. Our role and limits

- We identify workflow opportunities and flag compliance risk. We do **not** provide legal, regulatory, or compliance advice, and we do not certify that anything is compliant.
- The client (and its compliance officer, carriers, FMO, or counsel) decides whether a workflow is compliant and approves it in writing before go-live.
- We do not sign Business Associate Agreements (BAAs) or take custody of Protected Health Information by default. If a client needs us to, stop and escalate to the owner and our attorney before proceeding.

## 3. Medicare marketing rules (CMS) — awareness checklist

CMS regulates how Medicare Advantage and Part D plans, and the agents, brokers, and third-party marketing organizations (TPMOs) that sell them, market and communicate with beneficiaries (42 CFR Parts 422 and 423, Subpart V, and CMS's annual Medicare Communications and Marketing Guidelines). Carriers and FMOs add their own requirements on top. Before proposing any workflow that touches marketing or beneficiary contact, confirm with the client:

- **Unsolicited contact** is restricted (for example, cold calls, unsolicited texts, and door-to-door approaches to beneficiaries). Do not design outbound automation to beneficiaries without the client's compliance sign-off.
- **Scope of Appointment (SOA)** documentation and timing requirements before sales appointments.
- **Required disclaimers** (including TPMO disclaimers) on marketing materials, websites, and calls.
- **Call recording and retention** requirements for sales and enrollment calls.
- **Material approval**: carriers often require marketing materials, scripts, and templates to be reviewed or filed before use. AI-drafted copy is still marketing material.
- **Event and educational content** rules, which differ from sales rules.
- Annual enrollment period and other calendar-driven restrictions.

Life insurance and other lines are regulated by state insurance departments and carrier rules; ask which states and carriers apply.

## 4. TCPA — consent before calls and texts

The Telephone Consumer Protection Act and FCC rules restrict telemarketing calls and texts, especially those using automated systems or artificial/prerecorded voices. The FCC has stated that AI-generated voices count as "artificial" voices under the TCPA. State "mini-TCPA" laws can be stricter.

Our default rule for any workflow we design or recommend:

- **Prior express written consent is documented before any marketing call or text** is sent through an automated, AI-assisted, or prerecorded/artificial-voice system. We will not build it otherwise.
- Consent records (who, when, how, what language) are stored in the client's system of record, not ours.
- Opt-out ("STOP") handling is honored promptly and across channels.
- Lists are scrubbed against the National Do Not Call Registry and the client's internal DNC list.
- Calling-time windows and state rules are respected.
- The client's compliance officer or counsel approves the consent language and the workflow before go-live.

## 5. HIPAA-adjacent data handling

Depending on the arrangement, an insurance agency may handle data that is Protected Health Information under HIPAA, or data protected by other laws (for example GLBA and state privacy and insurance laws). We do not decide which applies. We treat all of the following as **Restricted** regardless:

- Medicare Beneficiary Identifiers (MBIs), Medicare/Medicaid numbers, policy numbers
- Social Security numbers, dates of birth tied to a named person, driver's license numbers
- Health conditions, medications, providers, claims, or any health information about a person
- Bank or payment account details
- Call recordings and transcripts with beneficiaries or applicants

Rules:

- **No PHI or beneficiary identifiers go into any tool that is not on the approved list in section 7**, including AI chat assistants, note-takers, transcription tools, or our own email.
- During the Diagnostic we work from descriptions, blank forms, and redacted or synthetic samples only. We do not ask for, view, or accept live customer records.
- If restricted data is sent to us by mistake: do not open further, do not forward, notify the client the same business day, delete it, and log the incident (date, what, who, action taken).

## 6. Data classification

| Class | Examples | Where it may go | AI tools allowed? |
|---|---|---|---|
| Public | Client's website copy, published brochures, public reviews | Anywhere | Any, subject to client's brand approval |
| Internal | Client's org chart, tool list, process descriptions, meeting notes without customer data | Our approved workspace; client-approved tools | Only tools on the approved list for Internal |
| Confidential | Pricing, contracts, financials, vendor terms, marketing scripts pending carrier approval | Our approved workspace, encrypted; need-to-know | Only tools on the approved list for Confidential |
| Restricted | PHI, MBIs, SSNs, DOBs tied to a person, health info, account numbers, call recordings | Client's own systems only; we do not store it | **None**, unless the owner and client both approve in writing and required agreements (e.g. BAA) are in place |

When unsure, classify one level higher.

## 7. AI tools approved for client data

**Default: none.** Until the owner fills in this table, no AI tool may process Internal, Confidential, or Restricted client data. Public data only.

| Tool | Plan / account type | Approved data classes | Data retention / training setting verified | BAA available/signed? | Approved by | Date |
|---|---|---|---|---|---|---|
| [TOOL — owner to fill] | [PLAN] | [CLASSES] | [Y/N + note] | [Y/N] | [OWNER] | [DATE] |

Before adding a tool, verify: the plan's data-use and training terms, retention and deletion, access controls, where data is stored, and whether a BAA or DPA is available. A client may impose a stricter list; the stricter list wins.

## 8. Engagement checklist for regulated clients

- [ ] Regulatory flags captured on the intro call and in the CRM
- [ ] Compliance questions in the Diagnostic script answered and recorded (answers only, no sensitive data)
- [ ] Client's compliance approver named in the agreement
- [ ] Prescription includes a risks/compliance-flags section
- [ ] Every customer-facing workflow (calls, texts, marketing copy) approved in writing by the client's approver before go-live
- [ ] Only approved tools used; no restricted data in our systems
- [ ] Offboarding: client credentials removed, our copies of Internal/Confidential data deleted, deletion confirmed in writing

## 9. Open items for the owner

- Fill in the approved AI tools table (section 7).
- Have our attorney review this standard and the agreements that reference it.
- Decide on errors & omissions (professional liability) and cyber insurance.
