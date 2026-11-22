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
| src-staff-archetypes | four archetypes Tech Lead / Architect / Solver / Right Hand with Larson's one-line definitions; behaviours can change; ivory tower architect | se-guidebook ch22 §4; ch25 §9; staffeng.com/guides/staff-archetypes (via book) |
| src-glue-work | "glue work" term (Reilly); capture it, work log; re-evaluate if mostly helping; seen as unfocused | se-guidebook ch3 §2 |
| src-being-the-strongest | pair when stuck for days; guide by questions not the fix; document for others; resolve external blockers; delay giving solutions | se-guidebook ch11 §3; ch12 §3 |
| src-picking-battles | "yes, BUT" script; finish #1 priority; being inflexible / pulling rank perception | se-guidebook ch7 §1; ch22 §1 |
| src-skip-design-doc-checklist | five questions, three or more yes -> worth a doc; implementation-manual doc not needed; prototype can justify design | industrialempathy.com Design Docs at Google (read 2026-11-21) |
| src-doc-review-lifecycle | four lifecycle steps; async/sync/hybrid review; central mailing list stopped scaling; update doc, link amendments; docs drift but stay entry point; RFC goal = shorter time to ship | industrialempathy.com; se-guidebook ch15 §1 |
| src-one-pager-for-leadership | status update email: progress, risks+mitigation, timeline changes, confidence; source of truth. Four-part one-pager = general synthesis, no book template | se-guidebook ch18 §4 |
| src-working-backwards-pr-faq | Customer Obsession first sentence quoted; PR/FAQ structure is general practice (book Working Backwards not ingested; page does not mention PR/FAQ) -- LEAST SURE | atoz.amazon leadership principles (read 2026-11-21) |
| src-dependencies | six mitigation options for engineering dependencies incl. mock, internal open source, escalate after engineer-to-engineer; non-engineering mitigation | se-guidebook ch16 §6 |
| src-kickoff-closeout | PRD why/what; engineering kickoff how; milestones separate; wrap-up elements; failed project wrap-up | se-guidebook ch16 §3, §7 |
| src-prioritization-frameworks | RICE factors, impact scale 3/2/1/0.5/0.25, confidence 100/80/50%, effort person-months; formula composed from description (page shows image) | intercom.com RICE blog (read 2026-11-21) -- formula inferred, LEAST SURE |
| src-technical-roadmapping | 2 months vs 20 payment methods example; tie architecture to business initiatives; good-enough | se-guidebook ch25 §7; ch21 §1 |
| src-software-project-physics | triangle; quality rarely negotiable in Big Tech; Brooks not universal conditions; new joiner onboarding day 2 vs 1-2 months; overtime -> errors | se-guidebook ch16 §4 |
| src-prototyping-poc | throwaway; no reviews/tests; refuse to ship; non-production stack trick; a day or two | se-guidebook ch15 §2; ch16 §6 |
| src-articulating-trade-offs | 2 months vs 20 payment methods example; offer product/engineering tradeoffs; help mentees articulate tradeoffs | se-guidebook ch25 §7; ch12 §3; ch11 §4 |
| src-over-engineering | start simple (whiteboards, no formal UML unless value); scalable = new use cases vs load; payment framework only if roadmap needs; complex easier than simple | se-guidebook ch25 §1, §6, §7 |
| src-rewrite-vs-refactor | full revert/rewrite = one-way door; bankruptcy = cheaper to rewrite; Khan Academy Py2->Go + split monolith + GraphQL; refactor steps. "Why rewrites fail" is derived from these, not a quoted statistic | se-guidebook ch25 §3, §4; ch13 §3; ch9 §3 |
| src-technical-strategy | Rumelt three pillars; five steps; strategies fail from avoidable errors; guiding policy must imply tradeoff | crafting ch1 "Adapting Rumelt"; ch5 |
| src-platform-economics | platform team characteristics and formation; cost allocation by revenue; services overhead vs shared monolith blast radius; payment framework example | se-guidebook ch5 §2; ch25 §6; crafting ch20 Doc 20-1 |
| src-readable-strategy-docs | inverted structure order; strategy refactoring; uninvolved reader; comment period; template metadata; disable comments after release | crafting ch11 |
| src-strategy-testing | narrowest deepest slice; examples; metrics not adoption; sponsor/guide; don't-test cases | crafting ch13 |
| src-systems-modeling | three scenarios; steps; LLM model and driver onboarding findings; cautions | crafting ch14; ch17 Docs 17-2, 17-4 |
| src-wardley-maps | users/needs/capabilities; x-axis genesis/custom/product/commodity; y visibility; steps; situational awareness | crafting ch15 |
| src-llm-adoption-strategy | three needs; policy: one vendor, refresh in six months; modeling shows reactivation lever; switching cost low; no numbers on card | crafting ch17 Doc 17-1 |
| src-blast-radius-of-decisions | 20 teams / 100,000 customers examples; adapter keeps endpoint alive; shrink blast radius | se-guidebook ch25 §5 |
| src-architecture-vs-tech-debt | four architecture-debt examples; stable unfashionable language benefit | se-guidebook ch25 §3 |
| src-simplicity | essential vs accidental complexity; dead code/flags; Knight Capital cited by chapter; minimal APIs; util/misc; 100 unrelated changes | sre.google/sre-book/simplicity (read 2026-11-21) |
| src-incident-communication | Comms role = public face; live doc editable concurrently, "messy but functional"; handoff phrase; war room/email for execs; known/unknown/next-update template = general practice | sre-book managing-incidents (read 2026-11-21); se-guidebook ch24 §6 |
| src-postmortem-action-items | review checks action plan and bug prioritisation; "unreviewed postmortem might as well never have existed"; follow-up deprioritised, staff+ create time; Allspaw quote paraphrased. Owner+deadline = general practice | sre-book postmortem-culture; se-guidebook ch24 §6 |
| src-change-risk | canary/flags/staged/automated rollback; stale flags; error budget pauses risky deploys; change-induced emergency case (Friday push, 5 min rollback, lax canary) | se-guidebook ch17 §4, §5; sre-book emergency-response |
| src-alert-quality | precision/recall definitions with 30% examples; urgency categories; good page = urgent, actionable, requires intelligence, novel; five questions | se-guidebook ch24 §4; sre-book monitoring-distributed-systems |
| src-pre-mortems | "Do a pre-mortem exercise"; rollout plan, bake, rollback; resilient-systems simulations (graceful degradation, retries, circuit breaker, failover, DR). Meeting procedure = general practice | se-guidebook ch15 §4; ch24 §7 |
| src-release-spectrum | YOLO vs thorough; selecting-approach questions; multi-tenancy cancels multiple environments | se-guidebook ch17 §1, §2, §5, §7 |
| src-eliminating-toil | six toil traits; <50% cap; 6-person rotation 2/6=33%, 8-person 25%; 0%-80% spread; interrupts top source; harms | sre-book eliminating-toil (read 2026-11-21) |
| src-embracing-risk | 99% phone vs 99.99/99.999; 100x cost increments; 2.5M req/day 99.99% => 250 errors; $1M revenue 0.09% => $900; private contacts example; error budget shared metric | sre-book embracing-risk (read 2026-11-21) |
| src-effective-troubleshooting | hypothetico-deductive; problem report; triage mitigate first; examine; diagnose; test/treat; negative results; hoofbeats | sre-book effective-troubleshooting (read 2026-11-21) |
| src-emergency-response | three case studies (one hour restore; 5-min rollback; 10-min incident declared; "sometimes zero does mean all") | sre-book emergency-response (read 2026-11-21) |
| src-tracking-outages | Escalator, Outalator, aggregation, tagging example cause:network:switch, analysis cautions | sre-book tracking-outages (read 2026-11-21) |
| src-testing-for-reliability | test types; "tests that are failing generally prove the absence of reliability"; zero MTTR argument; 8 GB->32 GB perf example; canary baking | sre-book testing-reliability (read 2026-11-21) |
| src-release-engineering | four principles; branch/cherry pick; hermetic; push on green; four config models; rollout "several days" for sensitive | sre-book release-engineering (read 2026-11-21) |
| src-sponsorship-vs-mentorship | sponsoring = advocating + leveraging position; five sponsorship forms; overlap with mentoring | se-guidebook ch22 §6 |
| src-feedback | concrete/sincere positive; ask before critique; situation+impact; no "you should"; in person; on their side; decode feedback (specific examples, impact, suggestions) | se-guidebook ch12 §4; ch2 §4 |
| src-difficult-conversations | observe first; talk privately; reduce negative interactions in groups; escalate to manager with suggestions; verbal for problematic cross-team. Situation+question script derived from feedback section | se-guidebook ch12 §4; ch20 §4, §5; ch22 §1 |
| src-meeting-hygiene | No agenda no attenda; invites+agendas 72h (min 24h); speedy meetings 25/50 min; single agenda; document live; cancel recurring; coffee chats exempt | handbook.gitlab.com all-remote/meetings (fetched via curl 2026-11-21) |
| src-async-remote | async definition; sync vs async guidance incl. 4 days/17 replies; async-only failure mode; new hires lonely; /all-remote/asynchronous/ URL from leaf is 404 -- replaced. 48-hour comment period on card is flagged as an example | handbook.gitlab.com communication/ and communication/sync-vs-async-culture/ |
| src-stakeholder-management | upstream/downstream/strategic; forgot RFC delayed two weeks; legal blocked after a month; three update ways; update email as source of truth | se-guidebook ch18 §3-§5 |
| src-internal-politics | influence vs political; problematic perceptions list; recusal example; feedback by relative seniority | se-guidebook ch22 §1 |
| src-team-health-dynamics | five healthy traits; unhealthy causes; growing pains; observe, talk privately, Team A/B, escalate | se-guidebook ch20 §1-§4 |
| src-observability-by-design | logging toolset; every event fields; events to log; p50/p95/p99; business metrics payments example; planning-phase SLI etc. | se-guidebook ch24 §2, §3, §7 |
| src-quality-metrics | five DORA metrics (throughput 3 / instability 2) with definitions; caveats (not targets, not for comparison, not silo); older "four" = leaf wording, current page lists five -- version drift, tag 时效; Orosz reservation | dora.dev/guides/dora-metrics (read 2026-11-21); se-guidebook ch17 §7 |
| src-design-review-as-reviewer | question list synthesised from RFC goals, rollout plan, pre-mortem, resilient-systems planning; no book checklist | se-guidebook ch15 §1, §4; ch24 §7 |
| src-testing-in-production | five safe approaches; benefits; challenges incl PII; performance/load (10x Black Friday, 1/10 infra)/chaos (Netflix Chaos Monkey)/smoke | se-guidebook ch14 §5, §6 |
| src-compliance-privacy-secure-dev | PII, GDPR, listed regimes (PCI DSS, HIPAA/ISO 27001, FERPA, FCRA, Section 508, EAA); logging PII; audits; OWASP; Log4j 2021; pentest; not legal advice | se-guidebook ch23 §5, §6 |
| src-raising-the-bar | engineering practices list; ask biggest shipping challenge first; post-commit review tradeoff | se-guidebook ch13 §5 |
| src-hard-feedback | managers owe early feedback; ask questions first; empathetic corrective feedback | se-guidebook ch3 §2; ch12 §4 |
| src-metrics-experiments | three questions on measurements; Uber 99.9% reliability and 500->200 gaming; CPU 15%->25% countermeasure; treatment/control; stale flags. Statistical pitfalls line is generic, flagged on card | se-guidebook ch21 §1; ch17 §4; ch23 §2; ch11 §3 |
| src-how-the-company-makes-money | unit economics; Uber revenue 10-20% of GMV, Stripe/Adyen 1-3% (numbers from book, no year given -- stale risk); earnings calls; startups transparency | se-guidebook ch21 §1, §3-§5 |
| src-customer-feedback-loop | PM-hat activities; shoes; customer support; B2B Shopify store example; comparison doc | se-guidebook ch21 §2; ch5 §1 |
