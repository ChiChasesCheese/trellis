# Skills matrix — what the Stripe OA tests, which problem drills it, which JD line it maps to

Skill ids S01–S24 come from `catalog/raw/process_and_jd.md` §E (each backed by candidate reports
or Stripe docs). S25 was added 2026-09-03 from the Bitfont family — see the note under the table
for why it is here and why its evidence is weaker than the rest. "Problems" = directories under `problems/`. JD lines = frequency across the 9
Stripe SWE JDs read (2025–2026) + the two JDs already evaluated in `career-ops` (Optimized
Checkout & Link 8075469; Credit Decisions 8084195).

| id | Skill / test target | Why Stripe tests it | Problems that drill it | JD line |
|---|---|---|---|---|
| S01 | Read the whole multi-part spec before coding; design for Part N+1 | Later parts extend the same program; "panic-implementing Part 1" → refactor → out of time | every q; especially q01 q04 q05 q07 q09 q10 | "navigate ambiguity, own problems end-to-end" (6/9) |
| S02 | Line-oriented parsing with delimiters (`,` `|` ` `), typed fields, malformed lines | Every reported OA starts with parsing; corrupted lines are a graded part (q16, q15) | q01 q02 q03 q06 q10 q12 q13 q14 q15 q16 q19 q20 | "debug production issues across the stack" (7/9) |
| S03 | Model the domain as small records + dicts keyed by id (state per merchant/user/connection) | Stripe employee on Blind: "creating classes, proper data structures, business logic" | q01 q09 q10 q11 q13 q24 q26 q27 | "design/build/maintain APIs, services" (9/9) |
| S04 | Group-by / aggregation and applying a rule once per group (not per row) | #1 failure in merchant scoring: double-counting additive rules | q02 q03 q14 q18 q20 | "large-scale financial tracking systems" (4/9) |
| S05 | Threshold semantics: strict vs non-strict, count vs ratio, minimum-volume gates | `>` vs `≥` flips hidden tests; fraud problem switches count→fraction | q01 q02 q08 q15 q23 | Radar / risk JDs |
| S06 | Money in integer minor units; explicit rounding (half-up vs banker's); 2-dp formatting | Stripe API = integer minor units; UGX/JPY zero-decimal; rounding drift fails tests | q03 q13 q16 q20 q21 q22 q27 | "financial products", Billing JD |
| S07 | Tiered / metered / prorated computations (graduated vs volume, allowance, proration) | Billing team problems mirror Stripe tier math | q03 q22 q20 | Billing JD: "pricing models, usage-based billing" (2/9) |
| S08 | Deterministic ordering with explicit tie-breaks | Almost every output is "sorted by X, ties by Y"; ordering mistakes fail tests | q01 q04 q05 q06 q07 q09 q17 q19 q24 q28 | — |
| S09 | Byte-exact output formatting (separators, padding, zero-pad 16 digits, tags) | "spacing/commas errors causing rejection" | q03 q04 q05 q10 q13 q16 q21 | "high code quality standards" (6/9) |
| S10 | Event streams + reversals (CHARGE→DISPUTE, plan change, renewal, shutdown re-route) | Parts 3–5 of fraud; parts 2–3 of scheduler; last failing group for a 22/25 candidate | q01 q07 q09 q10 q11 q25 | "real-time transaction processing… ledgering" |
| S11 | Idempotency / de-dup of repeated events (double disputes, duplicate ids, retries) | Explicit OA edge case; mirrors idempotency keys, webhook event ids | q01 q10 q16 q24 q27 | API JDs: "idempotency, retries" |
| S12 | Time & date handling (offsets, hour buckets, durations, month-end clamps, chronological merge) | Scheduler + hour-band penalty; billing anchors clamp to month end | q02 q07 q11 q23 q26 q27 q29 | — |
| S13 | Inclusive intervals, gap filling, off-by-one discipline | BIN obfuscation warns about inclusive endpoints | q04 q08 q29 | Issuing JD: "BIN sponsorship" |
| S14 | String normalization / canonicalization (case, punctuation, suffixes, Luhn walk, wildcards) | Atlas, card validation, email normalization | q05 q06 q19 q34 | — |
| S15 | Small combinatorics on masked input (`*` completions, `?` single-edit/swap) | Card validation parts 3–4 | q05 | — |
| S16 | Sliding-window / rate-limit counters, token bucket | Recurring OA/phone topic; Stripe's own 429/token-bucket guidance | q23 q02 (hour density) | Stripe API rate limits |
| S17 | Ledger-style balance tracking (credit/debit, never negative unless allowed, reserves) | "parse transaction logs → balances", Stripepay backend, money transfer | q10 q13 q25 q27 q32 | "financial tracking systems" (4/9) |
| S18 | Validation and error paths (missing keys, invalid numbers, unknown codes, nested markers) | Phone-screen rubric lists "dictionary key presence / number validity checks" | q08 q12 q15 q16 q19 q22 | "debug production" (7/9) |
| S19 | Incremental design: parse → model → compute → render as separate functions | "later parts build on earlier ones and bugs compound" | all; see each solution.py structure | "raise engineering standards" (6/9) |
| S20 | Self-testing discipline: run samples immediately, 2–3 own edge cases per part, lock parts | Testing instinct is a stated screen criterion; partial credit advances | drill protocol in README; every test_qNN.py shows the edge list | "testing, safe deploys" (6/9) |
| S21 | Speed in a concise language + stdlib fluency (dict/defaultdict/sorted key/heapq/Decimal/csv/datetime) | Stripe engineers advise against Java for speed; no extra time | q09 (heapq) q14 (csv) q16 q27 (datetime) q03 q21 (Decimal) | "strong coding skills in any language" (6/9) |
| S22 | Time-boxing: ~10–12 min/part, 5 min final format check | Reported outcomes 18/20, 22/25 pass; 14/20 fails | `drill.py time` | — |
| S23 | Print-debugging in a browser IDE, keep the tab focused | HackerRank logs tab switches; no breakpoints | CONVENTIONS: stderr only | — |
| S24 | Domain literacy: merchant/MCC/dispute/refund/payout/subscription/proration/tier/BIN/Luhn/idempotency | "reflects the real-world engineering work we do" | glossary in catalog/raw/process_and_jd.md §D; q01 q03 q04 q05 q10 q16 q20 | all payments JDs |
| S25 | Binary frame decoding: byte order, MSB-first bit and nibble extraction, RLE run-length decode, length-prefixed variable records | The Bitfont family decodes a made-up binary format: a big-endian 16-bit length header, one bit per pixel with the byte's high bit leftmost, COMPACT splitting a byte into two nibbles, and RLE runs that must sum to the declared size | cd09 (all three parts); cd10 part 3 (RLE only) | — (no JD line yet; see below) |

### S25 的收录理由与它的不确定性

S25 是 2026-09-03 那轮排查的产物。离它最近的两个是 **S02**（行式解析）和 **S09**（字节级精确
输出），但两者都停在"文本行 + 字段"这一层：S02 的原语是 `split` 和按名取列，S09 管的是打印出来
的那一串字符长什么样。**在一个字节内部按位取值、按字节序把几个字节拼成一个整数、把游程展开成
像素** —— 这三件事在现有 24 个编号里没有落点，硬塞进 S02 会让 S02 失去边界。

需要说清的是**它的证据强度**：S25 来自 `cd09_bitfont_binary_frames`，而那道题是**重建题**——
规格来自一个 GitHub 仓库里的转录文件，其唯一上游（一亩三分地）两轮排查都被 Cloudflare 挡住，
无法核实。所以：

- **技能本身是真的**：字节序、MSB-first 取位、nibble 切片、RLE 解码是确定存在的一类基本功，
  Stripe 考不考它，都值得会。
- **"Stripe 考这个"这件事没有被证实**。JD 列里留空就是这个意思——不像 S01–S24 每条都能指回
  一份候选人报告或一条 JD。
- 如果哪天能读到一亩三分地原文、或出现第二个独立来源，把这一行的证据补上；如果反过来证实
  cd09 那份规格是二次创作，**这一行应该降级或删掉**，不要留着它假装有依据。

判据是 `catalog/SOURCES.md` 那三条纪律里的第二条：不把猜测写成事实。收录一个技能，和声称
Stripe 考过它，是两件事。

## Algorithm / DS targets (phone screen + onsite; LeetCode Stripe tag)

| id | Target | LC / problem | Problems |
|---|---|---|---|
| A01 | Prefix sums + argmin with tie-break | LC 2483 Minimum Penalty for a Shop (tag freq 100) | q08 |
| A02 | Weighted graph path product / BFS-DFS on currency graph | LC 399 Evaluate Division (freq 77–88) | q21 |
| A03 | Shortest path with ≤K stops (Bellman-Ford / BFS by hops) | LC 787 Cheapest Flights Within K Stops (freq 56–89) | q22 (route version), qA02 |
| A04 | Stack / backtracking string expansion | LC 1087 Brace Expansion (freq 82–89; InterviewDB "Expansion — Phone, Aug 2026") | qA03 |
| A05 | Hash-table + sort validation of records | LC 1169 Invalid Transactions (only 6-month entry, freq 100) | qA04 |
| A06 | Tiered tax / graduated brackets | LC 2303 Calculate Amount Paid in Taxes (freq 87–100) | qA01, q22 |
| A07 | Sliding window over sorted timestamps per key | LC 1604 Alert Using Same Key-Card ≥3 in 1 h (freq 62) | q23, qA05 |
| A08 | Simulation / design with validation | LC 2043 Simple Bank System (freq 62–67) | q13, qA06 |
| A09 | Interval merge / covered intervals | LC 56, LC 1288 (freq 62) | q04, qA07 |
| A10 | Min transactions to settle debts (DFS + pruning / bitmask DP) | LC 465 Optimal Account Balancing (freq 52; programhelp VO 2026-04) | q32, qA08 |
| A11 | Topological order with weights | LC 2050 Parallel Courses III (freq 44–67) | qA09 |
| A12 | One-edit distance | LC 161 (freq 61–67; also q05 part 4 logic) | qA10, q05 |
| A13 | Grid/hash counting | LC 2768 Number of Black Blocks (freq 61–67) | qA11 |
| A14 | LRU / time-keyed cache | AccountScheduler LRU; MultiTimeMap (LC 981 Time Based Key-Value Store) | q26, q36 |
| A15 | Heap-based top-k / least-loaded selection | load balancer; "heaps" onsite report (Blind B25) | q09 q28 |
| A16 | Union-find / connected components | Six Degrees of Collusion, record linking | q18 |
