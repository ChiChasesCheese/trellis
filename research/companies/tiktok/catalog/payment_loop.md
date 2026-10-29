# Payment / backend SWE loop at TikTok-ByteDance (US), extended for Global Payment

Collected 2026-10-29; window 2025-10 .. 2026-10-29, older items marked **background**. Extends `loop.md`,
`system_design.md`, `CATALOG.md` (2026-10-24) and reuses their ids (`sources.md`); new sources are `[N*]` (section 5).
1P3A = 1point3acres; "summary" = 1P3A's public one-line summary at `/interview/thread/<tid>` (bodies are points-walled).
Confidence: high = 3+ independent reports, or first-hand text plus a second source; medium = one first-hand report or two
indirect ones; low = summary only, opinion, prep blog, or an inference.

## 1. Payment-team reports (Global Payment, payments, wallet, Shop / ads / monetisation billing)

Across ~540 interview-like titles in the 1P3A `bytedance` tag since 2025-10, Blind (`tiktok payment`: 107 hits, all
2021-2024), 208 Reddit posts, PracHub, Hello Interview and TrueInterview, only one in-window first-hand report names
Global Payment for a US SWE loop. The rest is older or adjacent.

| When | Team / place | What was reported | Src | Conf |
|---|---|---|---|---|
| 2025-11-11 | **Global Payment**, US, experienced | R1 coding = **LRU cache on HackerRank with no test cases supplied; candidate wrote and ran own tests**; Chinese interviewer, friendly; passed. Backend fundamentals (八股) were in **R2**. Candidate chose the language per round (R1 Chinese, R2 English). | [N1] | medium (first-hand, partly hidden) |
| 2026-10-13 | **USDS** onsite (team unnamed) | 3 rounds: two coding (R1 two problems incl. a logistics-themed LC; R2 an LC variant, tree problem took the hour), then SD. 1P3A summary: "a **detailed payment system design discussion**"; author: "SD was drilled more finely than expected". This is the 2026-10-13 sighting behind the bank record `payment-platform-design` (n=3, 2025-12-10 .. 2026-10-13) [A2]. | [N3][A2] | medium |
| 2026-01 | SG, backend 2-1, HM round | Projects, an LC problem, then **HLD of a payment system with 30 min left**; candidate forgot how the PSP's hosted UI appears on the vendor screen and ran out of time. | [R3b] | medium (reused) |
| 2025-12-10 | US, onsite, "hard" | "Design Payment System" (TrueInterview); infra guide: an **offer-winning SRE** designed "a payment platform like Stripe", discussion on **idempotency, transactions, data model, security**. | [G1] | medium (reused) |
| 2026-09-10 | ByteDance SWE onsite | Time-boxed payment-system HLD with follow-ups (section 4). | [P2] | high for the follow-up list (reused) |
| 2026-09 | SG backend (Glassdoor snippet) | discussion of past work, then high traffic, **idempotency, distributed consistency, indexing, data archiving, async processing, reconciliation** | [GD] | low-medium (reused) |
| 2026-09 (early) | US senior (Hello Interview) | **TikTok LIVE coin tracking and settlement**: real-time gifting, idempotency, per-session creator earnings, weekly settlement | [H1] | medium (reused) |
| 2026-04-13 | **国际支付 (international payments)**, backend, China, R1 | Project drill: service registry and inter-service calls; **DDD layers, how domain boundaries map to tables; distributed transactions across domains; reliable MQ producer delivery; Redis-DB consistency under overselling**; then ReentrantLock/AQS, G1 GC, MySQL index types, ACID, how RR is implemented; coding LC 567. | [N10] | medium (CN, mirror of Nowcoder) |
| 2026-03..04 | 国际支付 Java backend intern, China | 4 technical rounds + HR, offer: 八股, short-link SD, drill on an idempotent "unban" job (lock, ZSet vs MySQL atomicity, double-unban); LC 72, 42, 200, 151. | [N11] | low for a US senior loop |
| 2025-12 | Global Monetization (US) | Coding first: LC 438; tests passed but no 26-slot-array optimisation stated → fail. | [N26] | medium |
| 2025-10-20 | US SWE screen | collaboration BQ, a tree problem, SD on **task assignment + creator rewards** (reward granted when a creator completes a task, ~1k QPS) = TT-091 in `CATALOG.md`. | [N25] | medium |
| 2026-08 / 2026-10 | **E-commerce shipping & logistics / supply chain** backend | R1 = **AI-assisted coding** (own AI tool, screen share, build an `OrderValidator` with rule dependencies); tests unfinished → rejected same day. A 2026-10-06 candidate for the same org says one round is AI-assisted, "seems a new format". | [N17][G1] | medium-high |

**Background (2024 - 2025-04), Global Payment by name** (shows what this org has asked before; not in window):
- 2024-04, **Global Payment 2-2**, two US-based rounds: **OOD "tax engine"**, a **payment system SD**, and a **CV deep dive focused on payment background**; candidate lacked payment background and complained the team only wanted payment people [N4]. medium.
- 2024-10, Global Payment VO R1: two BQs ("most challenging project" ...) + **LC 560**; not bug-free → fail; "all levels" interview [N5]. medium.
- 2024-09, Global Payment (Bay Area) R2: BQ "a project where you showed ownership" + coding (Merge K Sorted Lists per a reply); rejected after 2 days with a good feeling [N6]. medium.
- 2024-06/07, payments group SWE: US-based interviewers, coding only (search in rotated sorted array), no 八股; rejected at final review [N7]. medium.
- 2025-04, an infra-leaning SDE loop: two infra-heavy SD rounds, one a **POS backend payment system** [N8]. low.
- 2024-10, Global Payments **3-1 tech lead manager** (San Jose): first round is coding, comp discussed only after it; insiders: LC medium, no fixed bank [N13]. low.

**Hiring signals** (not interview content): international payments team "expanding, many reqs, Seattle / San Jose", payment experience "a plus" (2025-11, 2026-04/05); some payment reqs sit in the USDS JV ("Payment AI Platform - USDS") [N2]; 2024 Blind opinions: Global Payments "more political" / "better WLB than e-commerce" [N12]. low.

**Reading.** The payment org interviews like the rest of ByteDance (LC-medium coding with self-written tests, resume drill,
八股 from China-based interviewers), plus a **payment-domain design** (payment system / coins / settlement) and, at least
once, a **payment-flavoured OOD** (tax engine). Expect the CV drill to probe Chi's PayPal fee and settlement work as domain
knowledge, not just as a project. medium.

## 2. The US loop in 2026 for experienced backend SWE (what is new since `loop.md`)

`loop.md` §1-7 stands; below are additions and refinements from 2025-10 .. 2026-10-29.

**Number and order of rounds.** Still a chain of pass/fail gates booked one at a time [G1][A1] (high). New shapes seen:
- 2-2 loop (2026-10-13): recruiter books two 60-min technical rounds and warns R2 may be cancelled after R1; R1 = US tech
  lead, resume deep dive + domain knowledge (good role match helped); R2 = US senior, resume + 八股 + one coding problem; a
  few hours later two **more** 60-min rounds are added with **China-based interviewers at US evening**, format not disclosed [N16]. medium.
- USDS SWE (2026-10-13): coding, coding, SD [N3]; USDS loops booked as a batch of 3-4 rounds in ~2 weeks [A1][1P3A 1157562]. medium-high.
- 2026 Seattle senior SWE (Glassdoor snippets): 3 rounds, first two coding/system design, third HM [N28]. low.
- Fast 2-1 loop: two LC-style coding + one behavioural, then offer in days, **no system design** [N14]. medium.
- Final round can be a **skip-level manager**, followed by an extra China-based HR conversation on motivation, other offers and years of experience [N23]. low-medium.
- 2-1 vs 2-2 shape still holds: mid loops add a fundamentals or design hour; senior loops one or two design hours and a project defence [G1]. medium.

**Length and platform.** 45-60 min. HackerRank and the Lark/meeting code pad; **no test cases are supplied, you write and run your own** (Global Payment R1 [N1]; [A1][G1]) — high. Diagrams sometimes have to be typed into the pad [B6][G1]. HR's description of the rounds is unreliable: an e-commerce SDE told "two coding, no SD" got SD first [N19]; another commenter says the HM tells an interviewer the night before what to ask [N16] — high (4+ independent reports incl. [G1][B6]).

**Language rules.** Any mainstream language for code [G1]; spoken language is negotiable per round with Chinese interviewers (R1 Chinese, R2 English in the Global Payment loop) [N1]; China-based rounds open in Mandarin and a classic China-side opener is "have you done high-concurrency (高并发) work?" [N16]. medium.

**AI-assisted coding round.** Now reported by several teams, still not universal:
- Format: recruiter asks you to set up **your own IDE with AI assistance** and share the screen [B5]; any model allowed [N17].
- Tasks seen: build an `OrderValidator` whose rules form a dependency graph, then remove a rule and reconnect predecessors to successors (e-commerce shipping/logistics, 2026-08) [G1][N17]; **debug a Python thread pool and add priority support** (2026-07) [N17]; LRU cache listed in TrueInterview's AI-coding format with ByteDance among askers (2026-10-01) [G1]; time-based KV store "with production testing" (2025-10) [G1]; AI-enabled **system design** rounds where you write the design, then prompt an AI to implement it live (ByteDance, Chinese, 2026-09) [1P3A 1189821].
- Scoring: working code **and finished tests**; candidates who left tests unfinished were rejected the same day [G1][N17]. Candidates on 1P3A in 2026-08/10 ask how it is graded and call it "new" [N17].
- Confidence: the round exists — high (5 independent sightings); that a Payment loop will contain one — low (no payment sighting; ask the recruiter).

**Project deep dive.** Present in nearly every round (1P3A bank `project-deep-dive-round` n=56 [A2]). New detail: 45 of 60 minutes on resume including "why the org-level infra is designed this way", 10 min coding [1P3A 1185434]; resume drill covering **data schema, CAP, indexing, concurrency** before an LRU [N24]; a T&S senior screen spent ~45 min on projects + an AI system design, then Number of Islands [N21]. high.

**HM round.** Projects + BQ, often a coding problem or HLD [G1][R3b][1P3A 1188260]; a candidate who passed two coding + SD within hours was rejected after HM, the one weak answer being "conflict with a PM" [N18]. medium.

**System design format.** As in `system_design.md` §1; payment prompts are now confirmed in a 2026-10 USDS onsite [N3]. Ad-hoc HM-led SD "without a whiteboard" also reported (2026-06, integrity team) [1P3A 1181082]. medium.

**LLD / OOD (class design).** No dedicated OOD round in any in-window US report; class design shows up inside coding rounds: `PercentileFinder` (2025-10), a "brief OOD scenario" after Java + SQL (2026-05) [N24], snapshot/restore and time-based KV, task schedulers (`coding.md` §3), the AI-assisted `OrderValidator` [G1]. Background: Global Payment's **tax engine OOD** (2024) [N4]. So prepare one payment-flavoured OOD (fee/tax calculator with composable rules, ledger/account classes) — medium (inference).

**Backend fundamentals.** Asked orally, usually by China-based interviewers, often as the first 20-50 min of an hour (`CATALOG.md` §3). Payment-team specifics: distributed transactions across domains, MQ reliable delivery, Redis-DB consistency, AQS, G1, MySQL RR/MVCC [N10]; Java concurrency + LC 124 (2025-11) [1P3A 1155971 summary]; Kafka + concurrency (2026-06) [1P3A 1179071 summary]. US-based interviewers tend to skip 八股 (2024 payments report [N7]; 2026 US tech lead round was resume-only [N16]). medium-high.

**Behavioural / ByteStyle.** No report cites a ByteStyle value by name (`CATALOG.md` §4). Payment-team BQs seen: ownership project [N6], most challenging project [N5], conflict with PM [N18]. medium.

**How level is decided.**
- HR may refuse to state a level before the loop: "graded by interview performance" [N14]; level is assessed from the resume drill and design rounds and checked against open headcount [G1]. high.
- A loop **without system design ends at 2-1**: 5+ YOE candidate got 2-1 after 2 coding + 1 BQ; HR refused to add an architecture round to re-level; an insider reply says 2-2 loops are run by 2-2 interviewers with different expectations and the bar "now starts around 8 years" [N14]. medium (one report + replies).
- Downlevels are common: 3-1 → 2-2 (2026-08) [N15]; 10-YOE ex-big-tech targeting 3-1 → USDS 2-2, ~$530k all cash (2026-10-23) [N15]; Amazon L6 → 2-2 [B2]. high.
- A 2-2 offer data point (2026-10-23): base $340k, 25% bonus, RSU $240k over **3 years 30/30/40**, $30k sign-on [N15]. medium. (Comp detail belongs to `payment_company.md`.)
- Implication: **ask for the 2-2 loop explicitly and make sure it includes a design round** [R1][N14]. medium.

**Timeline and feedback.** Next-round emails within hours to ~2 days [N16][N18]; rejections next day to ~8 working days [N21]; ghosting after "chat-only" rounds [1P3A 1183128]; "another candidate accepted, moved to a different team" (2026-10-27) [1P3A 1194630]. **No cooldown**: after a fail you can interview with another team, and feedback is visible to later loops [N20][G1]. high.

## 3. What besides DSA decided the outcome

Pass reasons (reported):
1. **Domain match on the resume drill** — the 2-2 R1 went well "because my background matches the role", mostly domain knowledge [N16]; Global Payment 2024 openly screened for payment background [N4]. medium.
2. **Finishing everything, with own tests** — the passing Global Payment R1 wrote and ran its own tests on HackerRank [N1]; USDS onsite "all finished" before a payment SD [N3]. medium.
3. **Concrete production numbers and mechanisms in design** ("Kafka + Redis, hot keys, 100k QPS per node" [1P3A 1156078]; a consistency design "that TikTok actually uses" [B1]). medium.

Fail reasons (reported):
1. **Not reaching the stated optimum or not explaining it** even with tests passing: LC 438 without the 26-slot array [N26]; quickselect complexity not derived [N20]; LC 560 not bug-free [N5]. high (3 reports).
2. **Unfinished tests in the AI-assisted round** [G1][N17]. medium-high.
3. **Little communication / edge cases**: calculator with validation and leading zeros, "little interaction" → fail [N22]. medium.
4. **HM round**: a weak conflict-with-PM answer; comp expectation above the band suspected [N18]; "HM decides everything" [R5]. medium.
5. **Payment HLD details**: hosted-checkout UI and running out of the 30-min slot [R3b]. medium.
6. **Level/headcount, not performance**: role filled, "only 2-2 wanted", re-routed after passing rounds [A1][1P3A 1194630][1P3A 1178773]. high.
7. **Lack of payment background** for a payment team (2024) [N4]. low-medium.

## 4. Payment-specific design and fundamentals prompts reported at ByteDance

Design prompts (all ByteDance/TikTok, any region; follow-ups where reported):

| Prompt | Where / when | Follow-ups and pushes | Src | Conf |
|---|---|---|---|---|
| **Payment system** (checkout, charge via external PSP, async confirmation) | SG HM 2026-01; US onsite 2025-12; PracHub onsite 2026-09; USDS onsite 2026-10 | Idempotency key on every retryable step; payment state machine + append-only ledger in integer minor units; webhooks lost/duplicated; crash between steps; reconciliation with PSP. **(1) seller payouts and how the ledger changes; (2) routing between two PSPs and failover; (3) payment pending for an hour — fix and what the user sees; (4) full and partial refunds without breaking reconciliation**; PSP tokenisation / no card data; hosted UI on the vendor screen. | [P2][R3b][G1][N3] | high |
| **Payment platform "like Stripe"** (SRE/infra flavour) | infra guide, offer case | idempotency, transactions, data model, security; graded on operating the system | [G1] | medium |
| **LIVE coin / virtual gift tracking and settlement** | US senior, 2026-09 | global, "highly accurate", idempotent gifting; per-session creator earnings; weekly settlement | [H1] | medium |
| **Currency exchange-rate system** (SD) and **currency conversion** (coding, LC 399 pattern) | US onsite 2026-10; phone 2026-01 | rate storage, queries, multi-hop conversion; coding returns rate or -1 | [1P3A 1193703][1P3A 1160243] | medium |
| **Task completion → creator reward** | US screen 2025-10 | ~1k QPS reward claims, PM-defined tasks, creator task view ~10k QPS | [N25] (= TT-091) | medium |
| **Account top-up / deduct API with idempotency** | CN intern R2, 2026-03 | "consider it in detail" | `raw/forums_cn.md` (mianlingai 2824606) | low |
| **Fund flow (资金流转) inside an agent + idempotency key and Redis key design** | CN AI full-stack R1, 2026-10 | why not let the model generate the key | `raw/forums_cn.md` (Nowcoder 942897472391684096) | low |
| **Money charged at the provider but order still unpaid; daily reconciliation for ~10M orders** | "a payment dept", 3rd round, director — second-hand, prep blog | T+1 bill pull vs orders from replica/warehouse; sharded sort + streaming two-pointer compare; long/short/amount-mismatch classes; cross-midnight buffer; safe auto-repair vs refund | [N27] | low |
| **Tax engine** (OOD) | Global Payment 2-2, 2024 | not visible | [N4] | medium (background) |
| **POS backend payment system** (infra SD) | 2025-04 | not visible | [N8] | low (background) |

Payment-flavoured fundamentals (oral) reported: idempotency key design and storage; TCC / SAGA / outbox / empty rollback
(`CATALOG.md` §3 row 6); cross-domain transactions under DDD, reliable MQ delivery, Redis-DB consistency under
overselling, AQS, G1, MySQL RR/MVCC/next-key locks [N10][N11]; Redis lock expiry at 10k QPS (`raw/forums_cn.md`).
**Not reported** for ByteDance but likely from a payment interviewer (inferred from postings listing reconciliation,
settlement, transaction monitoring; low): double-entry rules, FX rounding and minor units, chargebacks, PSP settlement
files, risk scoring in the payment path.

## 5. New sources in this file

1P3A thread URLs are `https://www.1point3acres.com/bbs/thread-<tid>-1-1.html`; summaries at
`https://www.1point3acres.com/interview/thread/<tid>`. Post dates as shown by 1P3A.

| id | Source | Date | Type / what it gave |
|---|---|---|---|
| N1 | 1P3A 1154075 | 2025-11-11 | Global Payment R1: LRU on HackerRank, own tests; language per round |
| N2 | 1P3A 1157391, 1174524, 1153374 | 2025-11 .. 2026-05 | team hiring posts (international payments, Seattle/San Jose; USDS payment/risk); "Payment AI Platform - USDS" reply |
| N3 | 1P3A 1192940 (+ summary) | 2026-10-13 | USDS onsite: 2 coding + detailed payment SD |
| N4 | 1P3A 1063446 (+ summary) | 2024-04-25 | background: Global Payment 2-2, tax-engine OOD, payment SD, payment CV drill |
| N5 | 1P3A 1093909 (+ summary) | 2024-10-25 | background: Global Payment VO, BQ + LC 560 |
| N6 | 1P3A 1086549 | 2024-09-16 | background: Global Payment R2, ownership BQ + coding |
| N7 | 1P3A 1091424 | 2024-10-13 | background: payments SWE, coding only with US interviewers |
| N8 | 1P3A 1124415 (summary) | 2025-04-16 | background: infra SD incl. POS payment backend |
| N10 | Nowcoder mirror `mj.mianlingai.com/interview/bytedance-backend-interview-1-2833873` | 2026-04-13 | 国际支付 backend R1 (China) |
| N11 | `https://www.nowcoder.com/discuss/908737508467277824` | 2026-03/04 (posted 07-20) | 国际支付 Java backend intern, 4 rounds + HR (China) |
| N12 | Blind `tiktok-e-commerce-supply-chain-vs-bytedance-global-payments-isbs5tmw` | 2024-06-13 | background: opinions on Global Payments |
| N13 | Blind `tik-tok-3-1-first-interview-coding-tech-lead-manager-ut7mvs6a` | 2024-10-11 | background: Global Payments 3-1 TLM, coding first |
| N14 | 1P3A 1179430 | 2026 (≈06) | level set by performance; no-SD loop → 2-1; insider reply on 2-2 bar |
| N15 | 1P3A 1184911, 1194201, 1194139 | 2026-08-03, 2026-10-23 | downlevels 3-1 → 2-2; 2-2 offer numbers |
| N16 | 1P3A 1192965 (+ 1194630) | 2026-10-13 (10-27) | 2-2 loop: 2 US rounds then 2 China-based rounds; HR format unreliable; re-routing |
| N17 | 1P3A 1185242, 1185263, 1192150, 1183128 (+ summaries) | 2026-07 .. 2026-10-06 | AI-assisted coding: OrderValidator, thread-pool priority debug, "new format" |
| N18 | 1P3A 1152392 | 2025-10-30 | 2 coding + SD passed, rejected after HM |
| N19 | 1P3A 1151099 | 2025-10-21 | HR said coding-only, got SD |
| N20 | 1P3A 1188464 | 2026-09-04 | senior screen fail; no cooldown; team-specific bar |
| N21 | 1P3A 1180429 (+ summary) | 2026-06-16 | T&S senior screen: projects + AI SD + islands |
| N22 | 1P3A 1170977 | 2026-05-04 | USDS senior: validating calculator, follow-ups */ and () |
| N23 | 1P3A 1189592 | 2026-09-15 | skip-level final round, level "between two", extra China HR round |
| N24 | 1P3A 1150899, 1178394 (summary), 1185609 (summary) | 2025-10 .. 2026-08 | class design in coding rounds; schema/CAP/index/concurrency drill |
| N25 | 1P3A 1150865 | 2025-10-20 | task + creator reward SD (TT-091) |
| N26 | 1P3A 1156954 | 2025-12 | Global Monetization: LC 438, failed on optimum |
| N27 | `https://juejin.cn/post/7610636435847086095` | 2026-02-26 | prep blog, second-hand: payment-dept reconciliation question |
| N28 | Glassdoor search snippets (TikTok Senior SWE, Seattle) | 2026 H1 | 3 rounds: coding/SD, coding/SD, HM |

Nothing new from: Blind searches (`tiktok payment` = 2021-2024 posts only), Reddit via Arctic Shift (needs a subreddit;
space calls ≥10 s), PracHub, Hello Interview (same 5 of 13), TrueInterview mirror (2026-10-29), 1P3A bank (members-only),
1P3A forum search (login).

## Gaps

- **No in-window, US, first-hand report of a full Global Payment SWE loop.** Only R1 of one loop [N1] and a USDS payment SD
  without its body [N3]. The Global Payment loop shape (number of rounds, whether an OOD round exists, HM content) is
  inferred from 2024 reports [N4]-[N7] and the generic loop.
- Key 1P3A bodies (1154075 R2, 1192940 SD, 1063446 tax engine, 1185242 task) are behind the points wall; only visible
  fragments and public summaries were used.
- Whether the Payment req (A128193 / X6613) uses the AI-assisted round: unknown; ask the recruiter.
- Whether Global Payment interviewers for US reqs are mostly US-based or China-based (affects 八股 and Mandarin): mixed
  evidence (2024 US-based [N7]; 2025-11 Chinese interviewer [N1]).
- No ByteDance report of follow-ups on ledger schema, double-entry, FX rounding, chargebacks or PSP settlement files;
  the reconciliation-at-10M-orders prompt is a second-hand prep blog [N27].
- Glassdoor 403 (snippets only).
- Correction to the old catalogue: `CATALOG.md` §2 row 8 lists 1P3A 1192940 under "consistency / cache design"; its 1P3A
  summary says the SD was a **payment system**. Blind [B1]'s "consistency system design problem" is from a 2025
  ByteDance loop, a different event.
