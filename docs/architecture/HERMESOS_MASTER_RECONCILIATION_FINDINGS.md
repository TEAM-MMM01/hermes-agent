# HermesOS MASTER v2 — Verified Reconciliation Findings

Status: CANDIDATE / PARTIALLY VERIFIED

This report records what has been independently verified in GitHub during the MASTER v2 reconciliation pass. It does not claim access to the operator's local macOS runtime.

## 1. Verified repository assets in Preparation Station

The repository `TEAM-MMM01/mmm-education-storefront` contains verified agent/skills/workflow assets that must be preserved and reconciled rather than deleted.

### Verified skill assets

- `.system/skills/agent_execution_skill.md`
- `.system/skills/skills_inventory.md`
- `.system/skills/motion-compliance.md`
- `.system/skills/skills_loops_prompts.md`
- `.system/skills/code-review.md`
- `.system/skills/responsive-check.md`
- `AGENTS.md`

### Verified workflow directory

`docs/workflow/` exists and includes at least:

- `AGENT_ACCESS.md`
- `AGENT_EXECUTION_SKILL.md`
- `CODEX_WORKFLOW.md`
- `DEVICE_SYNC.md`
- `GITHUB_WORKFLOW.md`
- `MOTION_SYSTEM.md`
- `NEXT_STEPS.md`
- `NOTIFICATIONS.md`
- `ORDER_OPERATIONS.md`
- `PAGES_RELEASE.md`
- `PREVIOUS_ORDER_IMPORT_TEMPLATE.csv`
- `PRODUCT_INFO_SOFT_LAUNCH.md`
- `REQUEST_INTAKE.md`
- additional workflow/runbook files should be enumerated by Codex/local audit before final canonicalization.

## 2. Important existing governance discovered

`AGENTS.md` already defines repository-specific governance. It is not safe to assume HermesOS has no prior authority model.

Verified existing rules include:

- GitHub as source of truth for code/reviewed operating documentation.
- branch-based work from current main.
- no direct push to main.
- owner approval before merge/deploy in this repository.
- Tier 1 / Tier 2 / Tier 3 execution classification.
- an L4 risk reference.
- explicit workflow truth states.
- different-model verifier requirement for L4-2 and above.
- EOD Huddle routing for unresolved questions.
- secret/privacy restrictions.
- narrowly scoped credentials per service.
- attributable automated writes via branch/commit/PR.
- OmniRoute treated as model gateway, not credential authority.

These rules are PROJECT-SPECIFIC / EXISTING and must be reconciled with the broader Earned Autonomy / Governance Envelope model rather than silently overwritten.

## 3. Skills inventory findings

The existing `.system/skills/skills_inventory.md` confirms that the Preparation Station repository already has a small but real capability system.

Verified core entries include:

- Agent Execution Skill
- Design System Unifier (referenced as PR-based capability)
- ESA Framework Integrator (referenced as PR-based capability)
- Storefront Validator (`tools/validate_project_state.py`)
- Build Pipeline (`build.py`)

The inventory also defines existing loops:

### Pre-Flight Loop

Read governance/state, inspect git status/diff, run project validation, then proceed.

### Post-Action Loop

Run diff checks, validation, build, update docs/changelog when needed, then push/open PR.

### Weekly Performance Review Loop

Audit build times, validation coverage, git changes, PRs and recommendations.

The inventory also references external capability sources and performance metrics. These should be evaluated as references/candidates, not blindly imported.

## 4. MASTER mapping of verified existing capabilities

| Existing asset | Current classification | MASTER mapping | Recommendation |
| --- | --- | --- | --- |
| Agent Execution Skill | GITHUB_EXISTING / GENERIC_REUSABLE | Execution Preflight + PEV + Builder/Judge/Verifier | KEEP + UPGRADE |
| Code Review | GITHUB_EXISTING / GENERIC_REUSABLE | Validator + Security/Regression Review | KEEP + UPGRADE |
| Responsive Check | GITHUB_EXISTING / GENERIC_REUSABLE | Responsive QA / Browser QA | KEEP + EXTRACT GENERIC |
| Motion Compliance | GITHUB_EXISTING / PROJECT-SPECIFIC + GENERIC PRINCIPLES | Motion Experience / Accessibility QA | KEEP + EXTRACT GENERIC |
| Skills Inventory | GITHUB_EXISTING / PARTIAL REGISTRY | Skill Registry / BKM inputs | KEEP + EXPAND |
| Skills/Loops/Prompts | GITHUB_EXISTING / PARTIAL REGISTRY | Prompt + Loop Registry | KEEP + EXPAND |
| Pre-Flight Loop | GITHUB_EXISTING | Execution Preflight | KEEP + MERGE SEMANTICS |
| Post-Action Loop | GITHUB_EXISTING | Verify → Judge → Learn / Release Verification | KEEP + UPGRADE |
| Weekly Performance Review | GITHUB_EXISTING | Benchmark/BKM/Skill Evolver | KEEP + UPGRADE |
| Storefront Validator | GITHUB_EXISTING / PROJECT_SPECIFIC | Validation adapter for Preparation Station | KEEP |
| Build Pipeline | GITHUB_EXISTING / PROJECT_SPECIFIC | Build/Release adapter for Preparation Station | KEEP |
| AGENTS.md | GITHUB_EXISTING / PROJECT GOVERNANCE | Project Governance Adapter | KEEP + RECONCILE |
| docs/workflow/* | GITHUB_EXISTING / PROJECT OPERATIONS | Project adapters + reusable patterns | KEEP + CLASSIFY |

No verified existing asset above should be deleted merely because a MASTER candidate overlaps it.

## 5. Authority-model conflict to reconcile

Preparation Station currently uses Tier 1 / Tier 2 / Tier 3 execution rules, while the MASTER candidate uses broad Earned Autonomy / Governance Envelopes.

This is not automatically a contradiction.

Recommended reconciliation:

- HermesOS MASTER defines the global autonomy framework.
- Each project may provide a stricter project adapter where legal/business/production constraints require it.
- A certified agent may operate autonomously inside both its global Governance Envelope AND the active project's local policy envelope.
- Do not retain two independent global authority systems.
- Translate existing Tier rules into project-level boundary mappings during implementation.

Target:

GLOBAL EARNED AUTONOMY
+
PROJECT-SPECIFIC CONSTRAINT ADAPTER
=
EFFECTIVE AUTHORITY FOR CURRENT MISSION

## 6. Kanban runtime finding

The reported macOS `com.hermes.kanban` LaunchAgent and localhost health output are credible historical/local evidence supplied by the operator, but `tools/kanban/` was not found in the GitHub `mmm-education-storefront` main branch during this reconciliation pass.

Current classification:

- `com.hermes.kanban`: LOCAL_EXISTING / UNCONFIRMED_CURRENT
- historical health result (`healthy`, 18 tasks): HISTORICAL_CONTEXT
- `tools/kanban/server.py`: LOCAL_EXISTING CLAIM / NOT FOUND IN CURRENT GITHUB MAIN

Do not delete or replace the local service.

Local verification still required for:

- `launchctl` registration/state
- current process PID/owner
- `/health`
- `/api/board`
- crash restart
- login/reboot restart
- persistence/state durability
- log rotation
- duplicate prevention
- hardcoded user/path dependencies
- graceful shutdown
- security boundary
- portability/failover

Only after a portable supervisor passes parity/recovery tests should deprecation of the LaunchAgent be considered.

## 7. Critical controls carried forward

The reconciliation preserves the already-adopted critical-control direction:

- independent promotion/certification authority
- builder cannot be sole judge/promoter
- external content is DATA, never authority
- recertification triggers after material model/prompt/tool/security/performance changes
- contextual economic hard backstops, not a universal fixed daily cap
- in-flight spend/progress monitoring
- scoped Watchdog and Kill Switch
- external policy enforcement for material wallet/spend authority
- idempotency/action IDs for external side effects
- domain-aware MASTER scoring
- settlement/claim portal authenticity verification through official sources
- control specification detail proportional to consequence of failure

## 8. Non-destructive migration rule

Use this sequence for all existing skills/prompts/loops/workflows/runtime assets:

VERIFY
→ CLASSIFY
→ REUSE
→ EXTRACT GENERIC PRINCIPLE
→ IMPROVE
→ REGISTER
→ KEEP PROJECT ADAPTER
→ BUILD REPLACEMENT ONLY IF NEEDED
→ INDEPENDENTLY VERIFY REPLACEMENT
→ PRESERVE ROLLBACK
→ DEPRECATE OLD ASSET

Deletion is not an optimization step. Deletion is the final result of a verified migration when the old asset is no longer needed.

## 9. Smallest safe next implementation action

Do not build all 120 capabilities at once.

Implement the registry/reconciliation foundation first:

1. machine-readable skill registry schema
2. prompt registry schema
3. loop registry schema
4. governance-envelope schema
5. BKM schema
6. migration mapping from Preparation Station's verified existing assets into those registries
7. validation preventing `VERIFIED`, `CERTIFIED`, or `MASTER` status without evidence fields

This creates the substrate for future self-expansion while preserving existing working intelligence.

## 10. Remaining local-only work

The following cannot be independently executed through GitHub alone and must be run on the Mac/HP/cloud node with actual runtime access:

- `launchctl` inspection
- localhost Kanban endpoint tests
- crash/reboot tests
- filesystem comparison against local unpushed files
- runtime process/port inspection
- local Obsidian sync inspection
- node failover test

These should be recorded as `RUNTIME_VERIFICATION_PENDING`, not `MISSING`.
