# HermesOS MASTER — Phase 1 Audit & Reconciliation Mission

## Mission

Review the current HermesOS repositories and architecture against the latest HermesOS MASTER Blueprint v1.0.

This is **NOT** a greenfield rebuild.

Do **NOT** begin implementing the entire blueprint yet.

The immediate objective is to determine the exact delta between the current system and the MASTER architecture, then define the smallest safe Phase 1 implementation.

---

## Source-of-Truth Policy

- **GitHub** is canonical for executable/configured system state: code, skills, prompts, loops, agent recipes, schemas, evaluations, benchmarks, BKM records, configuration, and version history.
- **Obsidian** is the synchronized human-readable knowledge/operations layer.
- If executable GitHub state conflicts with Obsidian, flag the drift, determine the correct current state, and reconcile documentation without silently overwriting useful history.

---

## Core Definitions

### Skills
Reusable jobs HermesOS knows how to perform.

### Prompts
Operating instructions defining role, objective, rules, tools, permissions, constraints, expected output, quality thresholds, and escalation behavior.

### Loops
Repeatable execution cycles such as Plan → Execute → Inspect → Judge → Correct → Retry → Verify. A loop does not stop merely because an output was generated.

### Agents
Workers assembled from model + prompt + skills + tools + memory + permissions + loops.

### Baby Agents
Temporary, tightly scoped subagents with one bounded objective, minimum necessary tools/context, explicit budget/permissions, completion criteria, and termination conditions.

---

## MASTER Model Policy

Use **Best Model for the Task**, not a blanket free-first policy.

Route according to:
- task difficulty
- expected economic value
- historical benchmark quality
- domain specialization
- tool reliability
- privacy/security
- latency
- context requirements
- cost

Use free/local or economical models for routine/high-volume work when they meet the quality threshold.

Use stronger paid/frontier/specialist models when revenue, financial impact, production architecture, security, major contracts, launches, or MASTER-quality output justify the incremental cost.

Optimize for:

**BEST VERIFIED OUTCOME PER JUSTIFIED DOLLAR**

---

## Audit Classification

For every blueprint component, classify it as one of:

- `EXISTS`
- `PARTIAL`
- `MISSING`
- `DUPLICATE`
- `CONFLICT`
- `DEPRECATED`

For each item provide:

1. Current implementation, if any
2. Exact repository/file/path
3. Current status/readiness
4. Overlapping or conflicting components
5. Dependencies
6. Risks
7. Recommended action
8. Implementation priority

---

## Systems to Audit

### Canonical Registries
- Skill Registry
- Prompt Registry
- Loop Registry
- Agent Recipe Registry
- Tool Registry
- Model Registry
- Evaluation Registry
- Benchmark Registry
- BKM (Best Known Method) Registry

### Reliability Kernel
- shared-brain / durable memory
- event-ledger
- execution-preflight
- builder-judge-verifier
- adaptive-retry
- checkpoint-resume
- contradiction-hunter
- compatibility-guardian
- agent-kill-switch
- rollback/recovery

### MASTER Performance
- best-model-for-task routing
- benchmark arena
- BKM engine
- platform-master / platform adapters
- software/API version awareness
- agent-performance scoring
- skill-evolver / mastery-evolver

### Self-Expansion / Meta Skills
- 100x-thinker
- all-gas-no-breaks
- capability-scout
- gap-hunter
- buy-back-time
- reference-to-system
- hermes-skill-factory
- agent-spawner
- bounded baby-agent framework

### Business / Revenue
- opportunity-radar
- service-first-opportunity
- productization-engine
- revenue-100x-engine
- zero-to-hero-business
- business-model-architect
- proof-before-scale
- kill-or-double-down
- asset-inventory
- cross-business-synergy
- revenue-leak-detector
- client-acquisition-engine
- offer-engineer
- growth-experiment-engine

### Financial / Capital
- master-financial-strategist
- financial-gap-hunter
- expense auditor
- subscription hunter
- debt optimizer
- cash-flow forecaster
- revenue analyst
- margin analyst
- pricing agent
- AR agent
- capital scout
- financing scout
- budget agent
- vendor-cost agent
- sba-capital-strategist
- capital-stack-optimizer
- agent-economics

### Government / Public Opportunities
- government-opportunity-scout
- grant-opportunity-scout
- public-sector-bid-builder
- eligibility/qualification scoring
- official-source validation
- deadline tracking
- compliance judge

### Settlement / Recovery
- settlement-opportunity-scout
- refund-recovery-scout
- eligibility verification
- deadline tracking
- claim-evidence ledger

Rule: never fabricate eligibility, purchases, dates, losses, receipts, or claims. “No documentation required” does not mean “no eligibility required.”

### E-Commerce / Trends
- ecommerce-trend-watcher
- product-gap-hunter
- trend-monetizer
- picks-and-shovels
- supply/demand gap detection
- trend lifecycle scoring

### Web / Software
- UI/UX
- frontend
- backend
- database
- APIs
- authentication
- payments
- security
- SEO
- accessibility
- performance
- analytics
- conversion optimization
- responsive design
- motion/animation
- browser QA
- visual regression
- deployment
- rollback
- production monitoring
- website-bottleneck-hunter

### Creative / Multimodal
- multimodal-director
- artifact-critic
- visual-continuity
- prompt-compiler
- cinematic-video-production
- motion-experience-designer
- voice-production
- speech-intelligence
- full-output verification

### Assessments / Development
- assessment-builder
- growth-score-engine
- personal development
- business
- leadership
- relationships
- financial habits
- communication
- productivity
- entrepreneurship
- AI readiness

Do not represent nonvalidated assessments as medical/clinical diagnostic instruments.

### Trading / Market Intelligence
- live-state-observer
- crypto-momentum-radar
- market-risk analyzer
- dynamic alerts
- event-ledger
- portfolio monitoring
- authorization layer
- execution adapter
- position monitor

Keep detection → analysis → risk → portfolio → authorization → execution → monitoring as distinct stages.

Pump.fun “callouts” are not a core HermesOS primitive. They may exist only as optional external signal inputs.

### Controlled Agent Wallets
Audit whether any wallet/economic-agent infrastructure already exists.

Required authority tiers:
- VIEW ONLY
- SIMULATE
- REQUEST TRANSACTION
- LIMITED SPEND
- AUTHORIZED AUTONOMY

Wallet ownership must not imply unrestricted spending authority.

---

## MASTER Performance Standard

Use the following quality maturity labels where evaluation data exists:

- `<70` Experimental
- `70–79` Working
- `80–89` Production
- `90–94` Advanced
- `95–97` Expert
- `98–100` MASTER

Do not self-declare MASTER. It must be benchmarked.

Evaluate correctness, output quality, reliability, task completion, verification, tool execution, cost efficiency, latency, maintainability, security, platform compliance, recovery behavior, cross-run consistency, and human correction rate.

---

## BKM — Best Known Method

Determine whether Hermes currently has a reliable way to track the best-performing combination of:

- skill
- prompt
- loop
- model
- platform/version
- tools
- settings
- benchmark result
- success rate
- average cost
- latency
- known failures
- last validation

If not, recommend the smallest Phase 1 BKM structure.

---

## All Gas, No Breaks

Interpret this as:

**No idle agent capacity when valuable, authorized work exists.**

It must NOT create:
- pointless work
- infinite loops
- repeated scans without changed conditions
- unnecessary model/API spend
- duplicate agents/docs
- changes to stable production systems without business value

When no useful authorized work is available, the agent state may be `AVAILABLE`.

---

## 100X Thinker

For meaningful systems/businesses/workflows ask:

- How could value increase dramatically?
- How could revenue move 10x/100x or as close as realistically possible?
- How could this take 1/10th the time?
- How could human involvement be reduced?
- How could this become reusable?
- Could this become a service, productized service, SaaS, license, data product, white-label capability, or recurring-revenue offer?
- What is the cheapest meaningful experiment?

Do not use 100X thinking to justify reckless spending or unsupported assumptions.

---

## Buy Back Time

Identify repetitive human work and classify it:

- DELETE
- AUTOMATE
- DELEGATE
- TEMPLATE
- BATCH
- AGENTIZE

Estimate hours returned and redeploy saved time toward higher-value work.

---

## Required Deliverables — AUDIT ONLY

Do not perform the full blueprint build yet.

Return:

### 1. Current-State Architecture Map
Show the real HermesOS architecture as it exists today.

### 2. MASTER Gap Matrix
For every major blueprint component:
- classification
- repo/path
- current state
- risk
- action
- priority

### 3. Retain
What already works and should stay.

### 4. Improve
What exists but needs hardening.

### 5. Consolidate
Duplicate/overlapping capabilities that should become one authoritative implementation.

### 6. Conflicts
Exact prompt/skill/loop/model-routing/permission conflicts that must be resolved.

### 7. Deprecate
Old functionality that should no longer be treated as authoritative.

### 8. Missing
Genuinely absent blueprint capabilities.

### 9. Phase 1 Foundation Plan
Define the smallest safe implementation for:
- GitHub canonical source-of-truth structure
- Obsidian synchronization rules
- Skill Registry
- Prompt Registry
- Loop Registry
- Agent Recipe Registry
- Evaluation/Benchmark structure
- BKM Registry

### 10. Complexity / Risk
Estimate relative implementation complexity and risk by Phase 1 workstream.

### 11. Branch / PR Strategy
Recommend a minimal, reversible branch/PR plan.

Suggested first branch name:

`feat/hermes-master-registry-foundation`

### 12. Smallest Safe Next Action
State the single highest-value next implementation step after the audit.

---

## Constraints

- Do not duplicate working functionality.
- Do not delete working functionality during the audit.
- Do not perform broad architectural rewrites yet.
- Do not silently change production behavior.
- Prefer REUSE → IMPROVE → CONSOLIDATE → BUILD.
- Ground all conclusions in the actual repository state.
- If another Hermes repo contains relevant infrastructure, inspect and reference it rather than assuming this repository contains everything.
- Separate confirmed facts from assumptions.
- Preserve rollback paths.

## Final Doctrine

**Find the gap. Define the opportunity. Verify reality. Solve the problem. Ship the result. Measure the outcome. Buy back the time. Productize what works. Find who will pay. Use the best intelligence where the value justifies it. 100X the leverage. Teach Hermes what was learned. Then execute the next highest-value move.**
