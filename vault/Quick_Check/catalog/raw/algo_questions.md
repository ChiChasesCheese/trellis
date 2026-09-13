# Stripe SWE interviews — LeetCode-style / algorithm / DS questions (frequency table)

Status: CHECKPOINT 1 (2026-08-25). Being appended as the sweep progresses.

## Access notes
- leetcode.com/discuss posts: mostly HTTP 403 via fetch; content recovered from search snippets + gists.
- 1point3acres thread pages: 403; 1point3acres.com/interview/problems/* question bank first screen accessible.
- Blind posts: fetchable.
- Glassdoor list pages: 403 (single-question pages sometimes OK).

## (C) LeetCode "Stripe" company tag — recovered lists

### liquidslr/leetcode-company-wise-problems, `Stripe/5. All.csv` (snapshot 2025-06-20)
Source: https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv

| Difficulty | Title | LC # | Frequency | Topics |
|---|---|---|---|---|
| Medium | Minimum Penalty for a Shop | 2483 | 100.0 | String, Prefix Sum |
| Easy | Calculate Amount Paid in Taxes | 2303 | 92.7 | Array, Simulation |
| Medium | Invalid Transactions | 1169 | 89.7 | Array, Hash Table, String, Sorting |
| Medium | Cheapest Flights Within K Stops | 787 | 82.0 | DP, DFS, BFS, Graph, Heap, Shortest Path |
| Medium | Brace Expansion | 1087 | 82.0 | String, Backtracking, Stack, BFS |
| Medium | Evaluate Division | 399 | 76.9 | Graph, DFS/BFS, Union-Find |
| Hard | Parallel Courses III | 2050 | 61.2 | Graph, Topological Sort, DP |
| Medium | One Edit Distance | 161 | 61.2 | Two Pointers, String |
| Medium | Number of Black Blocks | 2768 | 61.2 | Array, Hash Table |
| Medium | Alert Using Same Key-Card Three or More Times in a One Hour Period | 1604 | 61.2 | Array, Hash Table, String, Sorting |
| Medium | Simple Bank System | 2043 | 61.2 | Design, Simulation |
| Medium | Merge Intervals | 56 | 61.2 | Array, Sorting |
| Medium | Remove Covered Intervals | 1288 | 61.2 | Array, Sorting |

### liquidslr `Stripe/4. More Than Six Months.csv` (2025-06-20 snapshot; 30d/3mo/6mo files are empty = header only)
Source: https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv

| Difficulty | Title | LC # | Frequency |
|---|---|---|---|
| Easy | Calculate Amount Paid in Taxes | 2303 | 100.0 |
| Medium | Invalid Transactions | 1169 | 93.2 |
| Medium | Cheapest Flights Within K Stops | 787 | 88.8 |
| Medium | Brace Expansion | 1087 | 88.8 |
| Medium | Evaluate Division | 399 | 83.5 |
| Medium | Minimum Penalty for a Shop | 2483 | 76.7 |
| Hard | Parallel Courses III | 2050 | 67.1 |
| Medium | One Edit Distance | 161 | 67.1 |
| Medium | Number of Black Blocks | 2768 | 67.1 |
| Medium | Simple Bank System | 2043 | 67.1 |

### shreeratn/leetcode-company-wise-problems `Stripe/5. All.csv` (2025-05-13 snapshot)
Source: https://raw.githubusercontent.com/shreeratn/leetcode-company-wise-problems/main/Stripe/5.%20All.csv

| Difficulty | Title | LC # | Frequency |
|---|---|---|---|
| Medium | Minimum Penalty for a Shop | 2483 | 100.0 |
| Medium | Evaluate Division | 399 | 68.2 |
| Medium | Cheapest Flights Within K Stops | 787 | 56.4 |
| Hard | Optimal Account Balancing | 465 | 51.5 |
| Medium | Brace Expansion | 1087 | 51.5 |
| Hard | Parallel Courses III | 2050 | 44.6 |

(hxu296 2022 repo: companies/Stripe.md returns 404 — Stripe not in the 2022 list. snehasishroy repo uses lowercase folders; checking `stripe/`.)

## Aggregator sites (secondary; used only for statements, not counted as independent reports unless dated)
- prachub.com/companies/stripe (2026): Register Data Centers & route to nearest healthy region (2026-08-13); Schedule Weekly Deployment Windows (2026-05-09); Generate Account Email Notifications (2026-04-14); Calculate Transaction Fees (2026-04-09); Compute Transaction Fees from CSV string (2026-02-24); Assign Reviewers from Changed Files (2026-04-29); Build an Account Transfer Ledger (2026-03-13); Simulate Sticky Load Balancer with Shutdown (intern, 2026-02-12); Implement Validation and String Compression (Senior+, 2026-03-01).
- techprep.app/companies/stripe: lists LC 2483 Minimum Penalty for a Shop, LC 787 Cheapest Flights, CSV transaction parsing, log parsing, rate limiter (sliding window / token bucket), request replay / idempotency.
- linkjob.ai (2026-02-13): CSV of transactions -> filter by status -> total per user; HTTP request to mock payment API; refactor + tests.
- hackerprep.io/company/stripe: Balance Ledger Reconciliation, Invoicing, Payouts Flow, Chargebacks, HTTP Server design, Webhooks, Receivables, Dunning Email Reminder, **Bracket Expansion (Stack)** (= LC 1087 Brace Expansion).
- interviewing.io/stripe-interview-questions: "build simple IAM", "blur credit card numbers from logs", "design a rate limiter in any language".
- darkinterview.com/collections/stripe: Shipping Cost Calculator, Data Verification, Payment Invoice Reconciliation (high freq), Feature Flag SDK (design), Bike Map (integration), Mako Template Engine (debug).

### snehasishroy/leetcode-companywise-interview-questions `stripe/` (snapshot 2026-07-12 — most recent)
Sources: https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv , .../six-months.csv , .../more-than-six-months.csv
(Repo has no thirty-days / three-months file for Stripe → nothing tagged in the last 3 months.)

| LC # | Title | Difficulty | Acceptance | Freq (all) | Freq (>6mo) | Freq (6mo) |
|---|---|---|---|---|---|---|
| 2483 | Minimum Penalty for a Shop | Medium | 71.2% | 100.0 | 87.5 | — |
| 2303 | Calculate Amount Paid in Taxes | Easy | 69.5% | 87.5 | 100.0 | — |
| 399 | Evaluate Division | Medium | 64.4% | 87.5 | 100.0 | — |
| 1087 | Brace Expansion | Medium | 66.9% | 87.5 | 87.5 | — |
| 1169 | Invalid Transactions | Medium | 32.4% | 87.5 | 87.5 | **100.0 (only 6-month entry)** |
| 787 | Cheapest Flights Within K Stops | Medium | 42.2% | 75.0 | 87.5 | — |
| 2050 | Parallel Courses III | Hard | 66.8% | 62.5 | 62.5 | — |
| 161 | One Edit Distance | Medium | 34.6% | 62.5 | 62.5 | — |
| 2768 | Number of Black Blocks | Medium | 42.0% | 62.5 | 62.5 | — |
| 1604 | Alert Using Same Key-Card Three or More Times in a One Hour Period | Medium | 46.3% | 62.5 | — | — |
| 2043 | Simple Bank System | Medium | 69.7% | 62.5 | 62.5 | — |
| 56 | Merge Intervals | Medium | 52.3% | 62.5 | — | — |

Union across all mirrors (13 problems + LC 465 Optimal Account Balancing from shreeratn 2025-05 snapshot; LC 1288 Remove Covered Intervals from liquidslr 2025-06).

## Raw report log (independent reports; used for the counts in (A))

### Blind
- B1 https://www.teamblind.com/post/stripe-phone-interview-experience-ha4pxp3h — 2021-12 phone: "simple string/array processing, check conditions, output array", multiple levels; regex in part 2; unit tests expected. Rejected.
- B2 https://www.teamblind.com/post/stripe-phone-screen-interview-b34ftqso — 2023-08 phone (Berlin): no LC; verbose reading-comprehension programming problem; commenter: "request filtering or internationalization" (= HTTP header / Accept-Language class).
- B3 https://www.teamblind.com/post/stripe-phone-screen-ohnoejc2 — 2021-08 phone: 4-part problem; commenter: "the one about headers". Pass thresholds: 2–3 parts.
- B4 https://www.teamblind.com/post/stripe-phone-screen-8r8jb1c6 — 2025 phone: commenter did "parsing multiple JSON objects and performing calculations".
- B5 https://www.teamblind.com/post/stripe-phone-screen-interview-jcnxxpsh — 2025-09 phone (full-stack): "read in this JSON, transform it"; "design queues or caches for specific use cases".
- B6 https://www.teamblind.com/post/stripe-phone-screen-march-2025-oqru2jvw — 2025-03 phone: commenter got "shipping cost with order info" question.
- B7 https://www.teamblind.com/post/how-to-approach-the-stripe-on-site-coding-challenges-qb0yu0tx — 2022 onsite integration: read file of request array → HTTP POST → print response.
- B8 https://www.teamblind.com/post/stripe-onsite-2nvvaesr — 2021 onsite: coding "easy non-LC, code quality + unit tests".
- B9 https://www.teamblind.com/post/stripe-onsite-fstu61mn — 2024 onsite: "easy string manipulation + arrays question with 2 follow-ups".
- B10 https://www.teamblind.com/post/stripe-onsite-interview-experience-n4mqgn4g — 2024 onsite: coding 2 parts, long statement, no concurrency.
- B11 https://www.teamblind.com/post/stripe-interview-review-lj0bq5t3 — 2022: coding 2 parts (string.join), integration read JSON file.
- B12 https://www.teamblind.com/post/stripe-onsite-lfhrvh8n — 2022: phone non-LC multi-step; integration 3 parts; bug bash 3 bugs.
- B13 https://www.teamblind.com/post/bombed-stripe-interview-rdzlegue — 2023: tech screen 4 parts solved.
- B14 https://www.teamblind.com/post/stripe-interview-review-ine4wxoa — 2022-04 L2: 1 programming question 40 min; integration 5 parts.
- B15 https://www.teamblind.com/post/chances-in-stripe-interview-s55thedi — 2025 round 1: "real-world string parsing question, pretty huge", follow-up = one new method; "3/4 parts to qualify".
- B16 https://www.teamblind.com/post/stripe-onsite-interview-vwunpzkn — 2023 onsite: commenter mentions "top k most frequent elements" (hypothetical), integration = black-box APIs multi-part.

### LeetCode Discuss (via snippets / gists; pages 403)
- L1 https://leetcode.com/discuss/interview-question/2585038/Stripe-or-Phone-Screen-or-Senior-SE-or-Reject (2022, senior phone screen) + solution gist https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1 — **Best closing time / Minimum Penalty for a Shop** (LC 2483) part 1; part 2: log with BEGIN/END markers, multiple opening periods, best closing time per period.
- L2 https://leetcode.com/discuss/post/7384225/stripe-phone-screen-4-part-interview-exp-dhoy/ (2025?, phone, 4-part).
- L3 https://leetcode.com/discuss/post/1340172/ "Stripe [No offer]" (2021).
- L4 https://leetcode.com/discuss/post/5883672/stripe-phone-screen-by-anonymous_user-0kk5/ (2024, phone).
- L5 https://leetcode.com/discuss/post/7566910/ Stripe New Grad Interview Experience 2026.
- L6 https://leetcode.com/discuss/post/7595344/ Stripe onsite (2026) debug round details.

### 1point3acres (from cn_sources.md sweep; pages 403, snippets)
- P1 thread-1048313「Stripe 電面新題」— currency conversion (3 parts).
- P2 thread-1088332「Stripe滇缅」— currency conversion, "LC medium" (exchange-rate methods).
- P3 thread-817977「Stripe NG现场表演」— rate limiter (5 req / 2 s per user; sliding window).
- P4 thread-1081681「Stripe 過經 Senior」— rate limiter.
- P5 thread-1093485 — server allocate/deallocate.
- P6 1point3acres question bank: currency-conversion (phone), rate-limiter (onsite, last asked 2025-12-06), http-language-preference (phone, last asked 2025-10-22, 4 parts), shipping-cost-calculator (phone, 2025-12-19), AccountScheduler LRU (onsite, 2026-03-27), Matching Contacts (phone, 2026-06-10).
- P7 interviewdb.io/question/stripe (page 1 of 3): Card Parsing (phone), Closing Time (phone), Credit Card Number (phone), Currency Conversion (phone), Data Validation (phone), Expansion (phone, 6 days ago), Factory Cost (phone), Fraud Reports (phone); OA: Chat Billing, Collusion, Deployment.

### Glassdoor
- G1 https://www.glassdoor.ca/Interview/server-id-allocation-QTN_2174722.htm — "server id allocation" (Stripe SWE).
- G2 https://www.glassdoor.com/Interview/One-of-the-question-asked-me-to-implement-a-replay-test-with-a-pre-recorded-JSON-file-...-QTN_1885228.htm — replay test: parse JSON into HTTP requests, send, compare responses.
- G3 glassdoor list page (403): summary says OA HackerRank data-processing; onsite = coding, bug squash, integration, BQ.


### Blind (batch 2)
- B17 https://www.teamblind.com/post/stripe-technical-phone-screen-v37vsgvg — 2026 phone mid-level: multi-part (≤3 parts, "2a"); commenter: "3-4 parts per coding question; pass if 3 solved; Stripe has a small fixed set of questions".
- B18 https://www.teamblind.com/post/stripe-phone-screen-5titeaec — 2026-06 phone: rejections even after all 3 parts; commenter hint "Scalable solution. Graph BFS" (→ currency-conversion class).
- B19 https://www.teamblind.com/post/how-hard-at-technical-phone-screen-for-stripe-dlhvzujm — 2026-05 phone: "string parsing and data manipulation", "4 parter usually", "always very csv/dict oriented".
- B20 https://www.teamblind.com/post/can-someone-whos-ever-interviewed-at-stripe-for-mid-level-tell-me-what-to-expect-for-phone-screen-d4f50dzn — 2026-07 phone: questions named **Shipping Cost** and **Currency Conversion**.
- B21 https://www.teamblind.com/post/stripe-what-even-is-your-interview-bar-0hj2ltna — 2026-01 loop: 3 parts per round.
- B22 https://www.teamblind.com/post/stripe-swe-l3-interview-feedback-timeline-outcome-rbkumngu — 2026-08 L3 loop: AI programming (HackerRank AI assistant), bug squash 3 bugs, design, integration.
- B23 https://www.teamblind.com/post/stripe-onsite-interview-rajkrsgv — 2025: commenter "write json parser and write test" (engineering round).
- B24 https://www.teamblind.com/post/stripe-swe-phone-screen-dub4tnbn — 2026-04 phone: "classified as leetcode but emphasis on correctness/code quality/speed".

### interviewdb.io Stripe question bank (Aug 2026 snapshot; 3 pages) — https://www.interviewdb.io/question/stripe
Phone-screen coding: Card Parsing, Closing Time, Credit Card Number, Currency Conversion, Data Validation, Expansion (6 days ago), Factory Cost, Fraud Reports, Header Parsing, Linked User, Matching Contacts, Merging Transactions, Optimizing Money Transfer, Payment Invoices, Shipping Cost, Shipping Route, Transaction Fee, User Feature System, User Roles, Wishlist, Pattern Validator (frontend).
OA coding: Chat Billing, Collusion, Deployment, Join Dataset, Observability, Proximity Request Routing, Request Router, Stripepay Backend.
Onsite: 1p3a VO coding+design list, Bug Squash list, Integration list, Build an Interactive UI Element, Frontend System Design, ML Bug Squash / Integration / System Design.

### Search-engine snippets (Brave) — additional report URLs
- LeetCode: interview-question/5150083 "Stripe Technical Screen (Canada)"; post/7349079 "Stripe SDE Intern Phone Screen" ("for each product, start from first unit and iterate through quantity" → shipping-cost tiered pricing); post/7384225 ("system outputs up to two error codes according to priority" → data validation); interview-experience/5712510 "Stripe Phone Screen and Onsite" (string/array questions).
- Reddit r/leetcode: comments/1k1d2rl "Just had Stripe first coding round" (45 min, 3 parts, string parsing + prefix checking); comments/1d8ifef "SDE interview at Stripe" (string manipulation); comments/1m3ouod (string + JSON parsing).

### Blind (batch 3)
- B25 https://www.teamblind.com/post/stripe-interview-experience-sa3i71d8 — 2025-10: phone 2 parts; onsite programming part 1 "easy-medium question based on heaps" (→ top-k / priority-queue class), part 2 harder; integration 3 parts.
- B26 https://www.teamblind.com/post/stripe-onsite-interview-experience-jwdugpal — 2021 onsite: multi-part, lengthy description, arrays/hashmaps.
- B27 https://www.teamblind.com/post/stripe-onsite-x7beaq87 — 2025 onsite: coding 4 requirements built on JSON/test data; "LC easy-med".
- B28 https://www.teamblind.com/post/my-stripe-interview-gdmiywlu — 2025-08 L2: programming 3/4, integration 3/4.
- B29 https://www.teamblind.com/post/onsite-experience-at-stripe-umo0fobx — 2021 onsite: integration = parse JSON, HTTP call, business logic.
- B30 https://www.teamblind.com/post/phone-screen-at-stripe-ewqrtbt5 — 2024 phone: "multi-part, no topological sort, lots of string manipulation"; bar 2/3 → 3/4 parts.
- B31 https://www.teamblind.com/post/stripe-phone-screen-reject-rvwcuzdf — 2018 phone: 3-part problem, step 3 optimization hint; variables "min"/"minRecord" (→ minimum-cost / penalty style).

### Search snippets (Brave) batch 2 — 1point3acres & others
- P8 https://www.1point3acres.com/bbs/thread-1150184-1-1.html (2025-10-16) 电面: transaction fee from CSV-format string.
- P9 https://www.1point3acres.com/bbs/thread-1025478-1-1.html 电面: candidate prepped "Store, Server Remove, Mutual Wish List, User Feature", got a different one.
- P10 https://www.1point3acres.com/bbs/tag/stripe-2126-44.html tag page: phone questions listed "mutualrank, valid credit card, wishlist, server penalty, shop penalty, http header, money transfer".
- P11 https://www.1point3acres.com/bbs/thread-1029620-1-1.html Phone + Onsite: "Server Removal penalty" and "Money Transfer" with optimization follow-ups.
- P12 https://www.1point3acres.com/bbs/thread-817977-1-1.html NG onsite: Rate Limiter, ≤5 requests per 2 s.
- P13 https://www.1point3acres.com/bbs/thread-814077-1-1.html NG VO: "server task weights — route returns server with lowest workload" (load balancer).
- P14 https://www.1point3acres.com/interview/thread/1066090 phone: currency conversion.
- P15 https://www.1point3acres.com/interview/problems/25b1c004-aefc-4fc7-bdd5-d6b7dc7afcca question bank: "AUD:USD:0.7, AUD:JPY:100, USD:CAD:1.2 → direct conversion rate…"
- P16 https://www.1point3acres.com/bbs/thread-934403-1-1.html OA: exchange with bank_currency, subtract 2% Stripe fee.
- G4 https://www.glassdoor.com/Interview/Parse-a-string-in-the-format-USD-CAD-DHL-5-USD-GBP-FEDX-10-...-QTN_7989241.htm — "Parse 'USD:CAD:DHL:5,USD:GBP:FEDX:10' rates + shipping method" (shipping-route / currency graph variant).
- T1 https://www.jointaro.com/interviews/companies/stripe/experiences/software-developer-intern-memphis-tn-december-1-2024-no-offer-positive-5813ba11/ — intern Dec 2024: same "USD:CAD:DHL:5,USD:GBP:FEDX:10" parse question.
- M1 https://medium.com/nybles/stripe-software-engineering-intern-interview-experience-off-campus-a83b30aabed4 — intern: multi-part builds on previous.
- R1 https://www.reddit.com/r/Hack2Hire/comments/1rrsy56/stripe_screening_interview_design_rate_limiter/ — screening: rate limiter, rolling window.
- R2 https://www.reddit.com/r/leetcode/comments/1k1d2rl/just_had_stripe_first_coding_round/ — 2025: string parsing, existence check in master list, prefix matching ("LC easy").
- Aggregators: bigtechexperts.com/companies/stripe/swe-algorithm-questions/interview-question-1 (currency conversion BFS); techprep.app/blog/stripe-interview-process ("currency conversion via BFS/DFS commonly reported"); linkjob.ai/interview-questions/stripe-software-engineer-interview/ (currency graph); tryexponent guide ("LRU caches, scheduling constraints, interval overlaps, greedy optimization"); codinginterview.com (merge intervals, logger rate limiter, top-k, optimal account balancing, cheapest flights).

### 1point3acres phone-screen "high-frequency list" (search snippets, batch 3)
- P17 https://www.1point3acres.com/bbs/thread-873287-1-1.html (2022-03-26) 电面: prepped "mutual rank, valid credit card, wishlist, server penalty, shop penalty, http header, money transfer" → got a new one.
- P18 https://www.1point3acres.com/bbs/thread-851458-1-1.html 条纹电面: common problems "mutualRank / wishlist / airbnb-like rental service, http header parse, server remove penalty / store close".
- P19 https://www.1point3acres.com/bbs/thread-1028744-1-1.html (2023-11) 店面+高频题整理: "store open/close penalty", feature questions, mutual rank.
- P20 https://www.1point3acres.com/bbs/thread-804154-1-1.html (2021-10) 条纹店面: "Wishlist" with mutual-rank variants.
- G5 https://www.glassdoor.com/Interview/Write-a-function-compute-penalty-that-computes-the-total-penalty-given-a-server-log-as-a-string-AND-a-time-at-which-we-re-QTN_4434801.htm — "compute_penalty(server_log: str, remove_at)" server-removal penalty (Stripe SWE phone).

### bigtechexperts.com "Stripe SWE algorithm questions" (11 questions; 1–5 public) — statements captured in (B)
Q1 Currency Conversion (3 parts: direct / any path DFS / fewest hops BFS); Q2 Accept-Language header (3 parts: filter / q-values / wildcard); Q3 Idempotency keys & safe retries (3 parts: replay / TTL / conflict 409); Q4 Tiered pricing (volume / graduated / max units for budget); Q5 Flight/shipping routing "UK:US:FedEx:4,…" (direct / exactly one stop / any path DFS).

### programhelp.net / csoahelp / linkjob (dated candidate write-ups; each = 1 report unless clearly same candidate)
- H1 programhelp 2026-04-02 VO: PaymentLedger (idempotent add_payment/refund/get_payments_by_date); round 3 "algorithm": **min transactions to settle group debts (= LC 465 Optimal Account Balancing)** and **cheapest flight within k stops (= LC 787)**. https://programhelp.net/en/vo/stripe-vo-interview-questions-and-solutions/
- H2 programhelp 2026-03-31 intern VO: PaymentLedger; debug float-precision; integration idempotent POST /v1/charges. https://programhelp.net/en/vo/stripe-intern-vo-coding-debug-integration-guide/
- H3 programhelp 2026-02-27 SDE VO: account balance settlement (current→target balances; min transactions DFS; audit). https://programhelp.net/en/vo/stripe-sde-interview-vo-5-round-interview-experience/
- H4 programhelp 2026-01-26 intern VO: PaymentLedger. https://programhelp.net/en/vo/stripe-summer-intern-vo-coding-integration/
- H5 programhelp 2026-01-08 VO: transaction CSV → per-user fee; part 2 (country, provider) → rate + fixed fee. https://programhelp.net/en/vo/stripe-vo-real-coding/
- H6 programhelp 2026-04-13 intern VO: PaymentLedger 4 methods. https://programhelp.net/en/vo/stripe-intern-vo-coding-integration/
- H7 csoahelp 2026-07-22 coding: merchant linking — Part1 share any attribute; Part2 weighted confidence score ≥ threshold; Part3 indirect (1-hop) links. https://csoahelp.com/2026/07/22/...
- H8 csoahelp 2024-12-27 full interview: shippingCost("US:UK:FedEx:5,UK:US:UPS:4,...", src, dst, method) → cost or -1. https://csoahelp.com/2024/12/27/ace-your-stripe-interview-with-csoahelp-a-detailed-case-study/
- H9 linkjob 2025-12-08 phone: **user dedup / linked users** (weighted similarity on name/email/company, threshold; P2 1-hop transitive; P3 full connected component). VO: **AccountScheduler** (is_available / acquire(duration) / LRU auto-select). Intern VO: transaction balance ledger (balances, reject negative, platform reserve). NG VO: email subscription scheduler. https://www.linkjob.ai/interview-questions/stripe-technical-interview/
- H10 linkjob (2025-07 phone): shipping cost 3 parts; VO coding: subscription email schedule (welcome / 15-days-before-expiry / expiry; plan change; renewal). https://www.linkjob.ai/interview-questions/stripe-interview-questions/
