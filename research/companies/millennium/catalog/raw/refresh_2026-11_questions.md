# Refresh 2026-11-27: coding and technical questions reported for Millennium (SWE / data)

> Collected 2026-11-27. Reachability: 200 = read in full; 摘要 = search snippet only; 403/429/login = body blocked.
> Confidence: high = first-hand or official; medium = aggregator whose details match a first-hand one; low = SEO or AI-written.
> Not cited: lodely, vervecopilot. Budget used: about 9 searches, 14 fetches, GitHub API calls.

## 1. GitHub: Millennium now has a company tag list (correction to the kit)

The kit file `vault/interviews/core/leetcode/companies/millennium.md` (2026-09-21) says no source has a Millennium directory. **That is wrong now, and probably was wrong then for snehasishroy.** All four mirrors below have it. `lc_company.py` should be re-run and checked for a case or path bug.

| Repo | Path | Read | Date (last commit on the path, best parse of the API output) |
|---|---|---|---|
| liquidslr/leetcode-company-wise-problems | `Millennium/` with 4 CSVs (30 days, 3 months, 6 months, more than 6 months) | 200 | 2026-10-21 (previous 2026-08-16) |
| snehasishroy/leetcode-companywise-interview-questions | `millennium/all.csv`, `six-months.csv`, `more-than-six-months.csv` | 200 (all.csv) | 2026-08-15 (previous 2026-05-24) |
| Br8ny/company-wise-problem, Rushikesh-Ambilwade/leetcode-companywise-interview-questions, Chetan-Chandra/leetcode-company-wise-problems | copies of the two above | listing only | repo pushed 2026-11-22 to 11-24 |
| ayush-that/codejeet | `data/companies/millennium.csv` (7 problems) + blog `how-to-crack-millennium-coding-interviews.md` (2026-08-27, SEO, says 11 questions: 2 Easy, 6 Medium, 3 Hard) | 200 | CSV 2026-06-28 |

Windows in liquidslr: **30 days, 3 months, 6 months are empty (header only). Everything is in "more than six months".** There are no recent sightings. Frequency is relative inside a sample of about 8 reports (100 = 8 of 8, 87.5 = 7 of 8, 75 = 6 of 8), so it carries little weight.

Merged list (snehasishroy `all.csv`, 12 rows, with liquidslr agreeing on the same 9 titles):

| LC | Slug | Diff | Freq | Kit's 15? |
|---|---|---|---|---|
| 121 | best-time-to-buy-and-sell-stock | E | 100 | already in kit |
| 2484 | count-palindromic-subsequences | H | 100 | **NEW** |
| 56 | merge-intervals | M | 87.5 | already in kit |
| 2603 | collect-coins-in-a-tree | H | 87.5 | **NEW** |
| 20 | valid-parentheses | E | 87.5 (snehasishroy) | already in kit |
| 301 | remove-invalid-parentheses | H | 75 | **NEW** |
| 139 | word-break | M | 75 | **NEW** |
| 437 | path-sum-iii | M | 75 | **NEW** |
| 98 | validate-binary-search-tree | M | 75 | **NEW** |
| 49 | group-anagrams | M | 75 | **NEW** |
| 622 | design-circular-queue | M | 75 | **NEW** (only in snehasishroy) |
| 146 | lru-cache | M | 75 | already in kit (QuantVault) |

codejeet (older snapshot, 2026-06) lists seven: 121 (6 months), 50, 1283, 991, 2035, 20, 647 (more than 6 months). These are the same seven as the kit's StealthCoder source, so it is one source, not two.

## 2. Reported questions, newest first

Round and location are "not stated" unless shown. PracHub dates are the card dates on its listing, not interview dates.

| Date | Question | Round | Role / location | Follow-ups | Source (reach) | Conf. |
|---|---|---|---|---|---|---|
| 2026-11-25 | Design an order book matching engine: limit orders, market orders, cancels; price-time priority; `placeOrder`, `cancelOrder`, `getExecutedTrades`, `getOrderQuantity`, `getBestBid/Ask`; up to 10^4 ops | Other | Software Engineer. The question page is tagged "General"; it appears on the Millennium company listing | (1) quantity at a price, top 5 levels; (2) amend price/qty, which keep queue position; (3) cancel-heavy traffic with millions of orders; (4) many symbols and crash recovery | https://prachub.com/interview-questions/design-an-order-book-matching-engine-with-limit-orders-market-orders-and-cancels (200) | low-medium |
| 2026-11-17 | Choose client-service communication protocols for scale | Technical Screen | Software Engineer; system design | not given | https://prachub.com/interview-guide/millennium-software-engineer-interview-guide-2026 (200) | medium |
| 2026-11-17 | Floating-point equality after decimal subtraction (`0.9 - 0.8`) | Technical Screen | Software Engineer | not given | same guide (200) | medium |
| 2026-11-17 | Unbounded session cache and thread stop flag (Python/Java concurrency, memory growth) | not stated | Software Engineer | not given | prachub company page (title only) | low-medium |
| 2026-11-17 | Mutable hash keys in HashSet and ArrayList (Java) | Technical Screen | Software Engineer | not given | guide (200) | medium |
| 2026-11-13 | Network device health checks and log-based root-cause analysis with ML; networking fundamentals (CIDR, routing vs switching, TCP vs UDP); overlapping fiber routes from KMZ files | not stated | ML Engineer intern | not given | https://prachub.com/companies/millennium (200, titles only) | low-medium |
| 2026-07-30 | Design a governed agent for portfolio rebalancing; evaluate an agentic decision system end to end | not stated | Data Scientist | not given | prachub company page (200, titles only) | low-medium |
| 2026-08 (Jul-Sep) | Agentic systems: key evaluation metrics and architecture discussion (video round, outcome "Fail") | video round | Forward Deployment AI Engineer | login wall | https://www.1point3acres.com/interview/thread/1185103 (login) | medium (existence), none (content) |
| 2026-07 (round level) | OA: PnL calculation, permutation divisible by 8, spreadsheet-column notation, sliding-window substring, OOP. Tech rounds: LeetCode-style coding, Python async debugging, streaming quote-buffer design. Data roles: SQL (GROUP_CONCAT, anti-joins), pandas, ML task | OA + technical | Quant Developer / SDE; Data Engineer / Data Scientist | not given | https://quantvault.org/millennium-interview-guide.html (200, updated 2026-10-20) | low-medium (aggregator, dates per round only) |
| 2026-04-26 | C++ atomics, memory ordering, safe publication; GCC/Clang/LLVM optimization; how a C++ mutex protects shared state; explain a project and its hardest challenge | Onsite (guide label) | Software Engineer intern, C++ | not given | prachub guide + company page (200) | medium |
| 2026-04 / 05 | Shared online editor, any language; two back-to-back interviews, slow feedback | not stated | location unclear | none | Glassdoor RVW103588540, RVW103798625 (403, 摘要 only) | low |
| 2026-02-12 | Design a data structure to store anagrams (maps to LC 49 Group Anagrams) | Technical Screen | Software Engineer | not given | prachub guide (200) | medium |
| 2026-02-12 | How would you model stock price prediction? (oral) | Technical Screen | Software Engineer | not given | same | medium |
| 2026-02 | Rust language question; 2026-02 Miami SWE report | not stated | Software Engineer, Miami | none | https://www.glassdoor.ca/Interview/Millenium-Management-Interview-E5713526-RVW102647075.htm (403, 摘要) | low |
| 2026-02-12 | How do you explain work to non-technical partners? | HR / Technical Screen | Software Engineer | not given | prachub guide (200) | medium |
| 2025-12-19 | Trapping Rain Water; Container With Most Water; subarrays with sum divisible by K; asyncio; multithreading + pandas aggregation; decorators; price-data design; probability (5 red 3 blue) | R1 to R5 | Quant Developer (Python) | see kit `coding_first_round.md` §1.1 | https://leetcode.com/discuss/post/7423863/ and https://www.1point3acres.com/interview/post/7423863 (login) | high (already in kit) |
| 2025-10-24 | Debug missing output in a Python async HTTP flow | Onsite (guide label) | Software Engineer | not given | prachub guide (200) | medium |
| 2025-09-06 | Implement paginated API ingestion | Online Assessment | Software Engineer, Python data manipulation | not given | prachub guide (200) | medium |
| undated | Top K elements in a massive data stream (coding); latency spikes in a data feed (other) | not stated | Software Engineer | not given | prachub guide (200) | medium |
| undated | Guide practice items (not reported questions): SQL end-of-day positions from execution reports; join fan-out in a desk report; order-book levels vs orders; tag-value (FIX) parser; signed drop-copy webhooks | practice | Software Engineer | listed on the guide page | prachub guide (200) | low (PracHub-authored practice) |

Dated 2024-2025 threads on 1point3acres (quant developer OAs 1103395, 1096305, 1095296, 1037380; HK intern phone screen 1148288, Jul-Sep 2025, "resume-based questions and in-depth follow-ups") are titles only behind a login. Source: https://www.1point3acres.com/interview/company/millennium-management/quant (200).

## 3. LeetCode originals

Reported only through the GitHub tag lists or the kit's earlier sources. Marked against the kit's 15 (42, 11, 974, 560, 56, 121, 50, 1283, 991, 2035, 20, 647, 146, 295, 221).

| LC | Slug | Status | Where it is reported |
|---|---|---|---|
| 301 | remove-invalid-parentheses | **NEW** (H) | liquidslr, snehasishroy |
| 2484 | count-palindromic-subsequences | **NEW** (H) | liquidslr, snehasishroy |
| 2603 | collect-coins-in-a-tree | **NEW** (H) | liquidslr, snehasishroy |
| 139 | word-break | **NEW** (M) | liquidslr, snehasishroy |
| 437 | path-sum-iii | **NEW** (M) | liquidslr, snehasishroy |
| 98 | validate-binary-search-tree | **NEW** (M) | liquidslr, snehasishroy |
| 49 | group-anagrams | **NEW** (M); also matches PracHub "store anagrams" (2026-02-12), so it is the one with two independent signals | liquidslr, snehasishroy, PracHub |
| 622 | design-circular-queue | **NEW** (M) | snehasishroy |
| 56, 121, 20, 146 | merge-intervals, best-time-to-buy-and-sell-stock, valid-parentheses, lru-cache | already in kit | tag lists confirm them |
| 42, 11, 974, 560, 295, 221, 50, 1283, 991, 2035, 647 | | already in kit; not in the tag lists except through codejeet's StealthCoder-equivalent set (50, 1283, 991, 2035, 647) | |

Not LeetCode but new and worth knowing: order book matching engine (2026-11-25), paginated API ingestion, top-K from a stream, mutable hash keys, float equality, Python async debugging.

## 4. What was not reached

- Glassdoor interview pages (403), Blind (403 in the kit; search snippets only now), 1point3acres thread bodies (login), Interview Query and TechPrep (429 / paywall), LeetCode Discuss (the search returned no 2026 Millennium post other than the 2025-12 one already in the kit).
- No report of a superday, team round, or hiring-manager round with questions. The only structure comes from kit sources (Blind: three 45-minute HackerRank technical rounds) and the PracHub guide's generic "deep-dive coding, system design, cultural fit".
- LEaD-specific question reports: none found.
- The three 2026-11-17 PracHub titles and the order book page carry no round, and the order book page carries no company on the page itself; treat attribution to Millennium as medium-low.
