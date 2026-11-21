card id | claim | source
src-scope-autonomy-impact | senior = autonomous, complex projects alone; two promotions to senior at Tier-3 vs four at Microsoft; terminal level; blast radius ~10 vs 100+; $1M vs $500M example | se-guidebook Part III intro; Part V intro
src-same-title-different-bar | same as above (ladder position, business impact, blast radius) | se-guidebook Part V intro "Why do titles vary"
src-taming-ambiguity | kickoff aligns why/what; throwaway prototypes, refuse to ship prototype, build on non-production stack | se-guidebook ch15 §2; ch16 §3
src-owning-outcomes | communicate roadblocks early + offer tradeoffs (cut scope, hack, have someone solve); long-term (test, monitoring, maintainable) | se-guidebook ch11 §1; Part III intro
src-design-doc | 10-20 pages for larger project, 1-3 page mini doc; section list; async/sync/hybrid review | industrialempathy.com Design Docs at Google; se-guidebook ch15 §1
src-when-no-design-doc | write when solution ambiguous; doc that is an implementation manual not needed | industrialempathy.com "When not to write a design doc"
src-goals-non-goals | non-goals are not negated goals (ACID example) | industrialempathy.com "Goals and non-goals"
src-alternatives-considered | section lists alternatives with tradeoffs; "one of the most important" | industrialempathy.com "Alternatives considered"
src-rfc-process | PEP statuses incl. Final, Provisional, Deferred; Rust subteam FCP with merge/close/postpone; KEP states provisional..replaced | peps.python.org/pep-0001 (read 2026-11-21); rust-lang/rfcs README; kubernetes/enhancements KEP-0000
src-adr | MADR template sections and status values incl. superseded by ADR-0123 | github.com/adr/madr template/adr-template.md; se-guidebook ch15 §1
src-status-updates | weekly status email, source of truth; kickoff; three ways to update stakeholders | se-guidebook ch18 §4; ch16 §5
src-work-breakdown | stories->tasks->subtasks, stop when clear; golden path first; prioritise closer to end-to-end; change tasks | se-guidebook ch7 §3
src-estimation | seven work categories; ideal vs worst-case estimate; prototype before estimating; timebox | se-guidebook ch7 §4
src-estimate-pushed-down | tradeoff examples: ship button capturing ticket; refuse top-down deadlines | se-guidebook ch16 §6 "Unrealistic timeline"
src-estimation-failure-modes | eight risk types; all estimates off by some degree | se-guidebook ch16 §6, §3
src-milestones | planning separate from milestones; milestones within a few weeks; no fixed date | se-guidebook ch16 §3
src-risk-first | prototype a day or two; spike = timeboxed research; refuse to start without context | se-guidebook ch16 §6
src-scope-negotiation | scope/time/people triangle; quality rarely negotiable in Big Tech; overtime raises errors | se-guidebook ch16 §4
src-adding-people | Brooks quote and conditions when adding people works | se-guidebook ch16 §4
src-one-way-two-way-doors / src-doors-that-harden | approved samples, node fixed; rule "at least as much work to reverse"; public stable API etc. | se-guidebook ch25 §4
src-build-vs-buy | third-party enrichment/first-party/hybrid tradeoffs; "Prefer vendors for commoditized functionality"; core function do it yourself | crafting ch19 Doc 19-1; ch4; joelonsoftware.com 2001/10/14 (read 2026-11-21). TCO/exit cost steps are general reasoning, no number
src-technical-debt | loan analogy, build-time multiplication formula, bundle with high-impact project, just enough debt | se-guidebook ch13 §3
src-intentional-debt | early-stage tech debt OK; quick fix then proper fix risk | se-guidebook ch13 §3; ch16 §6
src-migrations | shadow outputs found 2% payment diffs (not quoted on card); canary small %; staged rollout criteria; stale flags; data migrations in-between; dual-write NOT used | se-guidebook ch17 §4; ch11 §1; ch25 §4; crafting ch16
src-choose-boring-technology | innovation tokens (limited, ~3 early on — number left off card); stable unfashionable benefits | boringtechnology.club; se-guidebook ch25 §3 #4
src-incident-command | roles IC/Ops/Comms/Planning; Ops only ones modifying system; live incident doc; handoff phrase; declare conditions (second team, customer-visible, unsolved after an hour); mitigate before root cause | sre.google/sre-book/managing-incidents (read 2026-11-21); se-guidebook ch24 §6
src-when-declare-incident | three declare conditions | sre-book managing-incidents "When to Declare an Incident"
src-blameless-postmortem | postmortem triggers (5), review criteria (5), blameless assumptions; "no postmortem left unreviewed" | sre-book postmortem-culture; se-guidebook ch24 §6
src-human-error-root-cause | accountability vs blameless distinction | se-guidebook ch24 §6 #3
src-on-call-practice | 5 people min for once-a-month, 6 healthy, 10-12 with secondary; runbook contents; burnout factors; paging alerts actionable, aligned with SLO | se-guidebook ch24 §5; sre-book being-on-call
src-slos-error-budgets | SLI examples; 99.999% -> 0.001% budget; 0.0002% = 20% of quarterly budget; measured by monitoring; halt releases when exhausted | sre-book embracing-risk, service-level-objectives
src-budget-exhausted | releases halted; more subtle approaches exist | sre-book embracing-risk "Benefits"
src-influence-without-authority | five sources of trust capital; propose problem->solution->tradeoffs; support others, praise publicly/critique privately | se-guidebook ch22 §2
src-alignment-disagreement | perceptions: inflexible, pull rank; engineer-to-engineer before escalation | se-guidebook ch22 §1; ch16 §6
src-escalation-timing | engineer-to-engineer first quote | se-guidebook ch16 §6
src-disagree-and-commit | Amazon "have a backbone; disagree and commit", weaponized | se-guidebook ch22 §1
src-disagree-wrong-call | (derived practice; ADR as record) | se-guidebook ch22 §1; ch15 §1
src-cross-team-work | map of teams (5 lists); internal open source offer; mock; remove from critical path; escalate last | se-guidebook ch12 §5; ch16 §6
src-managing-up | 1:1s, tell don't assume, manager goals, deliver/notify | se-guidebook ch2 §5; ch22 §3
src-code-review-goals | review layers, nit, LGTM, single-purpose, urgent changes, same bar for all | se-guidebook ch12 §1
src-giving-receiving-review | tone, open-ended questions, talk when long back-and-forth, new joiners | se-guidebook ch12 §1
src-test-strategy | pyramid (Cohn 2009 not quoted), trophy "Write tests. Not too many. Mostly integration."; pyramid fits backend; no single best approach | se-guidebook ch14 §4
src-pyramid-or-trophy | same | se-guidebook ch14 §4
src-cost-of-quality | benefits/drawbacks of tests; verification layers; no numeric cost curve used | se-guidebook ch14 §7; ch17 §4; ch15 §1
src-mentoring | kickoff topics, cadence every two weeks 30-60 min, avoid silver platter, multiple solutions | se-guidebook ch12 §3
src-onboarding | onboarding doc seven items; new joiner edits doc; buddy; ship week one at small cos; 1/3/6-month goals | se-guidebook ch13 §4; ch6 §6
src-interviewing-others | structured interviewing: define attributes, vetted relevant questions (no brainteasers), record, common scale | rework.withgoogle.com guide (search excerpts only; page fetch 404 — LEAST SURE)
src-delegation | delegate generously; empower person with most info; distrust perception | se-guidebook ch16 §5; ch22 §1
src-business-value-framing | North Star/KPI/OKR definitions; OKR reliability example 99.8->99.9 | se-guidebook ch21 §1, §2
src-cloud-cost-awareness | FinOps definition, trade-offs speed/cost/quality; unit-cost steps general practice; OKR CPU 15->25 not quoted numerically | finops.org; se-guidebook ch21 §1
src-problem-before-solution | customer shoes, customer support, validation cycles | se-guidebook ch21 §2; ch5 §1
| src-interviewing-others | (orchestrator 2026-11-21) re:Work guide URLs return 200 but render client-side; steps not re-read in text. Card has no numbers. | https://rework.withgoogle.com/en/guides/hiring-use-structured-interviewing |
