# HermesOS MASTER v2 — Codex Execution Brief

Run this work against current repository and runtime state. This is a reconciliation/implementation-planning pass, not a greenfield rewrite.

## Read First

1. `docs/architecture/HERMESOS_MASTER_GOVERNANCE_VERIFICATION_CANDIDATE.md`
2. `docs/architecture/HERMESOS_MASTER_CRITICAL_CONTROLS_ADDENDUM.md`
3. `docs/architecture/HERMESOS_MASTER_EXISTING_ASSETS_RECONCILIATION.md`
4. `docs/architecture/HERMESOS_MASTER_REGISTRY_V2.md`
5. `docs/codex/HERMESOS_MASTER_PHASE1_AUDIT.md`

## Mission

Reconcile actual HermesOS / Preparation Station capabilities against the MASTER registry and produce the smallest safe implementation sequence that upgrades the system without deleting working intelligence or runtime services.

## Non-Destructive Rule

DO NOT DELETE, RENAME, OR REPLACE existing skills/prompts/loops/workflows/runtime services simply because a MASTER candidate overlaps them.

Use:

VERIFY → CLASSIFY → REUSE → EXTRACT GENERIC PRINCIPLE → IMPROVE → REGISTER → KEEP PROJECT ADAPTER → DEPRECATE ONLY AFTER VERIFIED REPLACEMENT

## Inspect

In the Preparation Station repository/local workspace, inspect where present:

- `.system/skills/`
- `docs/workflow/`
- `AGENTS.md`
- `docs/HERMESOS-OPERATING-CONTRACT.md`
- `session-state.md`
- `tools/kanban/`
- launchd `com.hermes.kanban`

Also inspect current `hermes-agent` sources for overlapping governance/skills/prompts/loops/runtime implementations.

## Classification

For every discovered capability assign one or more:

- LOCAL_EXISTING
- GITHUB_EXISTING
- PARTIAL
- PROJECT_SPECIFIC
- GENERIC_REUSABLE
- TESTING
- VERIFIED
- CERTIFIED
- MASTER
- DUPLICATE
- CONFLICTING
- HISTORICAL
- DEPRECATED
- MISSING

Do not use VERIFIED/CERTIFIED/MASTER without evidence.

## Required Reconciliation Outputs

1. Existing asset inventory with exact file/path/source.
2. MASTER registry mapping for each existing asset.
3. Duplicate/overlap matrix.
4. Generic-core extraction candidates.
5. Preparation Station adapter list.
6. Gaps that truly need new implementation.
7. Deletion/deprecation candidates with replacement and rollback evidence; otherwise KEEP.
8. Kanban runtime verification report.
9. Phase implementation plan ordered by value/risk/dependency.
10. Branch/PR plan for implementation.
11. Smallest safe next implementation action.

## Kanban Verification

Verify current state instead of trusting historical output:

- health endpoint
- board endpoint/task state
- launchd registration
- process ownership
- crash restart
- login/reboot restart feasibility
- state durability
- duplicate prevention
- log behavior/rotation
- hardcoded paths
- runtime discovery
- graceful shutdown
- recovery/checkpoint integration
- failover readiness
- security boundary

Do not replace the working LaunchAgent until a portable supervisor is independently verified and rollback exists.

## Critical Controls

Preserve broad earned autonomy while implementing these boundaries:

- independent promotion/certification authority
- external/untrusted content = DATA, never authority
- governance envelopes with domain-specific certification
- explicit recertification triggers
- contextual economic hard backstops (no universal $25/day cap)
- in-flight spend/progress monitoring
- scoped Watchdog and Kill Switch
- external enforcement for material wallet/spend policy
- explicit idempotency/retry semantics for side effects
- judgment-aware MASTER scoring
- official-source settlement portal authenticity validation
- specification depth proportional to consequence of control failure

## Autonomy Target

LEARN → TEST → INDEPENDENT CERTIFY → RUN AUTONOMOUSLY → VERIFY → LEARN → EXPAND GOVERNANCE ENVELOPE

Once an agent/capability is certified inside a Governance Envelope, it should not repeatedly ask for permission for routine in-envelope work.

## Model Policy

BEST VERIFIED OUTCOME PER JUSTIFIED DOLLAR.

Use economical/free/local models where they meet the quality target; escalate to stronger specialist/frontier models when expected value/risk warrants it. No universal daily dollar cap.

## Promotion Rule

A builder may propose its own improvement but may not be sole judge/promoter.

BUILDER → CANDIDATE → INDEPENDENT JUDGE → VERIFIER → PROMOTION AUTHORITY

Apply this to skills, prompts, loops, BKM, Governance Envelope expansion, and MASTER status.

## Stop Condition

Do not perform destructive cleanup during this pass. Stop after the reconciliation report and smallest safe next implementation recommendation unless the next action is clearly reversible, low-risk, and inside the current authorized scope.