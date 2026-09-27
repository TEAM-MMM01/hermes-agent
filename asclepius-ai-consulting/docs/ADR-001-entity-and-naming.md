# ADR-001 — Entity and Naming

## Status

Decision 1 LOCKED (2026-09-26). Decisions 2 and 3 PROPOSED — AWAITING RICHIE'S LOCK.

## Context

The consulting offer needs a market-facing name, a legal entity decision, and a future integration stance with HermesOS/RichieRichOS. These decisions affect contracts, invoices, domain names, and brand continuity.

## Decision 1 — Business name and brand

Status: LOCKED by owner, 2026-09-26. Market-facing name: **MMM Consulting**. Brand colors: orange and black. It replaces the earlier working name everywhere in client-facing content. The repository folder name (`asclepius-ai-consulting/`) is kept as-is to avoid breaking paths; it is internal only and never shown to clients. "The AI Prescription" remains the name of the Diagnostic deliverable.

## Decision 2 — Legal entity

Status: PROPOSED — AWAITING RICHIE'S LOCK. Agreements and invoices carry the placeholder `[LEGAL ENTITY — owner to confirm]` and `[GOVERNING LAW — owner to confirm]` until decided. Default recommendation: operate through a standalone LLC once revenue is imminent, unless Richie's attorney/CPA recommends housing it under an existing entity for tax, insurance, or administrative reasons. Errors & omissions (professional liability) insurance should be decided alongside this.

## Decision 3 — HermesOS integration

Status: PROPOSED — AWAITING RICHIE'S LOCK. Default recommendation: keep this fully decoupled now. Maintain the simple SQLite CRM so export is possible later, but do not build integrations until a real operating need appears.

## Consequences

- Contracts and invoices need the final legal entity name and governing law before the first paid engagement.
- Website booking link stays a placeholder until the Calendly URL is provided.
- Decoupling prevents this consulting launch from being delayed by product architecture.
