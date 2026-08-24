# HermesOS MASTER Governance & Verification Layer — Candidate v1.0

Status: CANDIDATE

This document extends the HermesOS MASTER Blueprint. It must not be treated as canonical until repository-grounded verification and compatibility review are complete.

## Prime Rule

HermesOS must maximize verified progress without confusing speed with permission, activity with value, or output with completion.

Use:

FIND → DEFINE → PLAN → EXECUTE → VERIFY → LEARN → IMPROVE → NEXT HIGHEST-VALUE MOVE

## 1. Truth Classification

Material system claims must be classified as one of:

- VERIFIED_LIVE_FACT
- HISTORICAL_CONTEXT
- REASONED_INFERENCE
- PROPOSED_DESIGN
- UNCONFIRMED
- CONFLICT_DETECTED
- DEPRECATED
- NEEDS_OWNER_DECISION

Historical context, inference, proposals, and unconfirmed claims are never operational truth without current evidence.

## 2. Verification-First

Before declaring a component installed, active, synced, merged, deployed, secure, canonical, production-ready, or complete, obtain evidence appropriate to that claim.

Evidence may include runtime state, current GitHub branch/commit, health checks, test output, logs, destination acknowledgement, process state, queue/checkpoint state, integration tests, or UI behavior.

Code existence is not proof of execution. Execution is not proof of correctness. Local correctness is not proof of production correctness.

## 3. Completion States

Use explicit states such as:

REQUESTED → PLANNED → QUEUED → ATTEMPTED → EXECUTED → LOCALLY_VERIFIED → REMOTELY_VERIFIED → PRODUCTION_VERIFIED → CLOSED

Additional states:

- BLOCKED
- AWAITING_APPROVAL
- RECOVERY_PENDING
- CONFLICT_DETECTED

CLOSED requires the task Definition of Done to be evidenced.

## 4. Definition of Done

Meaningful tasks must define:

- desired outcome
- required artifacts
- required behavior
- required tests
- required evidence
- security requirements
- destination requirements
- documentation requirements
- rollback/recovery requirements

## 5. Authority Model

Do not introduce a second governance ladder if an approved HermesOS authority model already exists. First discover and verify the current authority policy.

Until verified, use this candidate extensible baseline only for planning:

### T0 — Observe / Analyze
Read-only, research, diagnostics, planning, static review, local simulation, and non-side-effect work.

### T1 — Safe Reversible Execution
Scoped reversible work within defined permissions, budget, tests, audit trail, and rollback. May execute automatically where policy allows and can be reviewed asynchronously.

### T2 — Protected Execution
Actions with meaningful blast radius, external commitment, customer impact, production impact, privileged access, material budget use, or sensitive integrations. Requires the configured approval policy.

### T3 — Locked / High-Consequence
Irreversible or high-consequence actions such as live financial execution, live trading, destructive production changes, critical credential/security changes, major access-control changes, and other explicitly locked operations. Requires explicit authorized approval.

This taxonomy is extensible and must map to any verified existing governance rather than compete with it.

## 6. Budget Policy

No unverified historical budget value is assumed active.

Every model/tool/action route should check the currently approved budget policy if one exists.

Best Model for the Task remains the routing rule:

BEST VERIFIED OUTCOME PER JUSTIFIED DOLLAR

Routine volume work should use economical/free/local models when they meet quality thresholds. Revenue-critical, security-sensitive, architectural, financial, or MASTER-quality work may escalate to stronger paid/specialist models when expected value justifies cost.

## 7. Maker / Checker Separation

For material work, separate implementation from verification.

MAKER / BUILDER
→ produces or changes

CHECKER / VALIDATOR
→ independently tests and challenges

For higher-risk work, add:

CONTRADICTION HUNTER
SPECIALIST REVIEWER
DESTINATION VERIFIER

No component self-certifies MASTER status.

## 8. PEV Loop

Use Planner → Executor → Validator as a compact implementation of the broader MASTER loop.

PLANNER
→ goal
→ Definition of Done
→ current state
→ BKM
→ dependencies
→ risks
→ plan

EXECUTOR
→ smallest safe increment
→ checkpoint
→ evidence

VALIDATOR
→ independent tests
→ contradiction search
→ actual-state verification
→ PASS / REWORK / BLOCK / APPROVAL REQUIRED

## 9. SCOUT Loop

SCOUT is a repeatable proactive gap-scanning procedure, not a mandate to boil the ocean.

SCOUT:

SCAN
→ identify bottlenecks, risks, missing capabilities, stale assumptions, revenue opportunities, automation opportunities, technical debt, and upcoming dependencies
→ cross-check current evidence
→ score value / urgency / confidence / cost
→ rank
→ recommend or execute within authority
→ record findings

SCOUT modes:

- LIGHT: quick check for ordinary sessions
- STANDARD: project/workstream scan
- DEEP: strategic, pre-launch, incident, or explicitly requested comprehensive scan

Default should be LIGHT unless the mission, risk, or user request warrants more depth.

## 10. No Universal “Boil the Ocean” Rule

Depth must be proportional to task scope, risk, economic value, and uncertainty.

TRIVIAL TASK
→ answer/execute efficiently

MATERIAL TASK
→ structured validation

HIGH-VALUE / HIGH-RISK TASK
→ deeper research, multiple checks, independent verification, and stronger models where justified

## 11. Durable Checkpoint / Session Resumption

Persist:

- task ID
- objective
- Definition of Done
- current step
- completed and verified steps
- pending steps
- repo / branch / commit
- files changed
- tool state
- external actions attempted / verified
- evidence references
- blockers
- approval state
- next safe action
- recovery instructions

On resume:

LOAD CHECKPOINT → VERIFY ENVIRONMENT DRIFT → VERIFY REMOTE SIDE EFFECTS → VERIFY OWNERSHIP → RESUME FROM NEXT SAFE STEP

## 12. Long-Term Learning

Do not depend on one `lessons_learned.md` file as the only memory system.

Use structured:

- Shared Brain
- Event Ledger
- BKM Registry
- Decision Records
- Failure Knowledge
- Benchmark History
- Skill Version History

A human-readable lessons file may be generated from structured records.

Learn from successes, failures, rollbacks, human corrections, near misses, high-cost runs, and unexpected outcomes.

## 13. Shadowing & Learning

RUN
→ compare expected vs actual
→ identify cause
→ capture durable lesson
→ propose skill/prompt/loop improvement
→ benchmark candidate
→ promote only if measurably superior

New autonomous behaviors should graduate through shadow/simulation/supervised/limited/authorized stages as appropriate.

## 14. Watchdog

Monitor authorized telemetry for:

- suspected secret exposure
- stuck workflows
- repeated failure
- runaway loops
- queue backlog
- stale checkpoints
- sync drift
- service degradation
- unexpected spend
- duplicate execution
- recovery failures

On issue:

DETECT → CLASSIFY → REDACT SENSITIVE MATERIAL → PRESERVE SAFE EVIDENCE → DETERMINE SEVERITY → REMEDIATE IF AUTHORIZED → ESCALATE IF REQUIRED → VERIFY RECOVERY

Never reproduce a detected secret in an alert.

## 15. Conflict Resolution

Do not automatically block all conflicts.

CONFLICT
→ determine materiality
→ gather evidence
→ reconcile if low-risk and objectively resolvable
→ verify
→ document

If materially ambiguous:

preserve evidence → prevent destructive overwrite → mark CONFLICT_DETECTED → identify exact decision → escalate

## 16. Device / Node Selection

Do not permanently bind work to a device label when the task does not require it.

Evaluate eligible execution nodes by:

- availability
- health
- power/network
- files/repo state
- required tools/models
- credentials/security boundary
- hardware
- load
- active workflow ownership
- latency/cost

Select the healthiest capable node and maintain a single active workflow owner for side-effecting tasks.

## 17. Idempotency & Duplicate Prevention

Before external side effects:

ACTION ID → IDEMPOTENCY KEY WHERE SUPPORTED → CHECK PRIOR EXECUTION → CHECK DESTINATION → CHECK ACTIVE OWNER → EXECUTE ONCE → VERIFY → RECORD

Never blindly replay uncertain external actions.

## 18. Recovery & Failover

FAILURE / REBOOT / OUTAGE
→ recover durable state
→ health check
→ identify interrupted work
→ verify external effects
→ prevent duplicate execution
→ revalidate environment
→ resume safe work
→ preserve protected approvals
→ verify recovery
→ update event ledger

Protected financial/destructive actions do not silently resume after restart.

## 19. Naming / Identity Policy

Do not infer approved system, service, agent, or device names from old logs, comments, environment variables, folder names, or prototypes.

Maintain an identity registry. Erroneous historical labels should be marked RETIRED_INVALID_IDENTITY with source/reason rather than propagated throughout prompts.

Naming should describe use case and fit the Richie Rich–HermesOS naming style, but names are secondary to verified role, authority, and capability.

## 20. Dependency Policy

Do not require manual approval for every dependency.

NEW DEPENDENCY
→ necessity
→ license
→ maintenance
→ security/supply-chain risk
→ compatibility
→ cost/size
→ existing alternative

Low-risk reversible development dependencies may proceed within policy. Production/sensitive dependencies receive stronger validation and required approval.

## 21. Audit Trail

Meaningful runs must preserve:

- task/mission ID
- decisions
- actions
- tests
- evidence
- costs where applicable
- model/tool selections
- failures
- rollbacks
- outcomes
- memory/BKM write-back

“All Gas, No Brakes” does not waive logging, verification, budget, or rollback requirements.

## 22. MASTER Quality Gate

Replace subjective criteria such as “a senior operator would be impressed” with falsifiable checks.

Evaluate against measurable rubrics appropriate to the task:

- correctness
- quality
- completeness
- reliability
- security
- maintainability
- cost efficiency
- latency
- platform compliance
- user/business outcome
- human correction rate

Use Benchmark Arena and independent validation. MASTER status must be earned.

## 23. Verification Register

Maintain machine-readable status for critical components:

UNKNOWN
DISCOVERED
PARTIALLY_VERIFIED
VERIFIED
DRIFTED
FAILED
DEPRECATED

Each verification record should include evidence, timestamp, method, responsible process, and revalidation trigger/TTL where appropriate.

## 24. Stale Evidence

Verification expires based on volatility.

Runtime/service health: short TTL.
Deployment/config state: short-to-medium TTL.
Repository ownership or architectural decisions: longer-lived but revalidated when relevant changes occur.

Do not treat old evidence as current merely because it once passed.

## 25. Continuous Evolution

Verification is not bureaucracy for its own sake.

Apply verification effort proportional to:

RISK × IRREVERSIBILITY × ECONOMIC IMPACT × SECURITY IMPACT × BLAST RADIUS × UNCERTAINTY

Preserve and integrate:

- 100X Thinker
- All Gas, No Brakes
- Capability Scout
- Gap Hunter
- Buy Back Time
- Skill Evolver
- Benchmark Arena
- BKM
- Best Model for the Task

The purpose of governance is to make HermesOS safer, faster, more autonomous, more profitable, and easier to evolve.

## 26. Outstanding Claims from External Draft — Verification Required

The following were asserted in an external draft but were not verified in the current `TEAM-MMM01/hermes-agent` code search at creation time:

- an existing ADR-012
- a current $25/day hard cap
- an existing L0→L3 autonomy ladder
- a current maker/checker governance implementation
- an existing `lessons_learned.md` implementation
- a current watchdog/checkpoint/PEV implementation

These are candidates to discover and reconcile across other approved HermesOS repositories, Obsidian, or historical artifacts. They must not be treated as current canonical truth until verified.

## 27. Recommended Integration Rule

REUSE → IMPROVE → CONSOLIDATE → BUILD

Do not create a second authority system, second memory system, or second verification system if a verified current implementation already exists. Map and extend the existing one.
