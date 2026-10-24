# TikTok / ByteDance catalog: what was reported, ranked, and what the decks are missing

Window 2025-10-01 .. 2026-10-24 (collected 2026-10-24). Inputs: every file in `catalog/` and `catalog/raw/`, and `../index.json` (the 278 LeetCode problems already in the decks). Companion file: `additions.json` (what to add to the decks). Counts below are produced by a script over hand-transcribed sightings; scratch lives in `/tmp/tiktok_catalog/` and is not kept.

## 0. How to read the numbers

- **Sighting** = one candidate report of one problem family in one interview. **#refs** = independent sightings after de-duplication.
- **De-duplication.** (1) The explicit duplicate map in `raw/aggregators_cn.md` sec 5 is applied first (PDF TT-056 = 1P3A 1162894, TT-050 = 1165436, TT-037 = 1172146, TT-028 = 1176917, TT-009 = 1183948, TT-012 = 1183355, TT-053 = 1163442, TT-019 = 1181934, TT-021 = 1181618, TT-036 = 1172524; TT-097 and TT-100 are the same report; Nowcoder reposts and the 面经-NN columns that re-list the same post are counted once). (2) Same family, different source among TrueInterview / 1P3A / PDF / PracHub / Hello Interview / LC Discuss, dates within 7 days: merged as one event (one-to-one). (3) 1P3A bank records give `n` independent threads per family with only the first and last date: when `n` exceeds the events found elsewhere, the difference is added as dated-by-last-date residual events. (4) The Chinese frequency table (`raw/forums_cn.md` sec 2) is used the same way for CN families. These residual events have no per-report id; each row says how many.
- **Region.** US = San Jose / Seattle / USDS / unspecified English-language reports (the aggregators do not say; most TrueInterview, PDF and 1P3A items are US); SG = Singapore; CN = Chinese-market posts (Nowcoder and its mirror, mostly campus and intern, many on Agent or Java backend roles). **Weight CN rows down for a US senior loop.**
- **Stages** count events touching a stage: OA, P = phone screen or first technical round, O = onsite or later technical round, HM = hiring-manager or manager round. Reports often do not say; a "?" means the stage is not recorded. CN 一面 is mapped to P, 二面/三面 to O.
- **Ranking** = sum over a row's sightings of 0.5^(age in days / 180) (half-life 6 months, age counted to 2026-10-24; month-only dates use the 15th). This is "refs x recency". Ties are broken by refs.
- **Confidence.** high = at least 3 refs from at least 2 source types; medium = 2 refs, or 1 ref from a first-hand text (PDF or 1P3A thread); low = 1 ref from an aggregator title, a prep-service post, a template post, or a Chinese-market post alone.
- **In decks** compares the LeetCode numbers in the row with `index.json` ids; `*` after a number means that problem is not in the decks. `[custom]` rows are TikTok-specific problems or heavily reworded ones; `[OA]` rows are new-grad or intern online assessments.
- **Unattributed.** 30 sightings name no identifiable problem ("a binary search", "a hot-100 problem", "two easy ones") and are excluded from every count below.
- Not counted: the 65 undated references and the "tiktok-leo-10/20" docx in `raw/aggregators_cn.md` sec 4 (undated), the pre-window items (LC Discuss 7150750 of 2025-09, job-compass NG-1/NG-2/o8aelo), and ombharatiya / lmiztbrv lists (derivative of TrueInterview, no per-report data).

## 1. Coding

### 1.1 Cut line (computed by script)

- 186 problem families, 464 sightings in total (186 of them CN). The long tail is real: 102 families have a single report.
- **Cut line, all regions: rank 102 of 186.** The top 102 rows (55% of the rows) cover 80.2% of the 464 sightings (80% needs 372). The top 20% of rows (38) cover only 56.2%, so the usual 20/80 rule does not hold here: reports are spread over many one-off problems.
- **Cut line, US + SG only: rank 92 of 147** families with at least one non-CN report (278 sightings); the top 20% (30 rows) cover 45.3%.
- Rows with at least 2 refs: 84 rows cover 78.0%; rows with at least 3 refs: 45 rows cover 61.2%. Using recency weights instead of raw counts, 80% of the weight is reached at rank 82.
- Practical reading: 45 families have 3 or more reports (cache, grids, graphs, sliding windows, linked lists, intervals, trees); 102 families are single reports and fill most of the lower half of the ranking.

### 1.2 Above the cut line (ranks 1 to 102)

| # | US rank | Family | Aliases | LC | How TikTok changed it | Stages (events touching) | #refs | Region | Last seen | Conf | In decks | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | **LRU Cache (+TTL / LFU / weighted / thread-safe)** | LRU with TTL, expiring LRU, LRU with time limit, local cache with expiry, LFU, 带过期时间的LRU | 146, 460 | TTL passed per call or uniform; expired entry deleted lazily and treated as absent; O(1); LFU after LRU; thread safety; "what if the miss rate is high"; some rounds run on HackerRank with no tests | P 12 / O 5 | 30 | US 12 / CN 18 | 2026-10 | high | yes | 1P3A 1192155; PracHub/TI 2026-10-04; TI 2026-09-06; TT-003; 1P3A 1180357; 1P3A 1178773 (+16 more, +8 counted from 1P3A bank / CN table (no per-report id)) |
| 2 | 3 | **Number of Islands family** | islands, 岛屿数量, max area, distinct islands, making a large island | 200, 695, 694, 711*, 827 | follow-ups: do not modify the grid; distinct shapes (694); rotations/flips (711); boundary/perimeter; grid too large for memory (split + union-find); streaming rows; 8 directions; BFS-only | P 11 / O 4 | 21 | US 13 / CN 8 | 2026-10 | high | partial | TT-004; TT-015; TT-016; 1P3A 1182260/TT-020; TI 2026-06-16; TI 2026-04-09 (+14 more, +1 counted from 1P3A bank / CN table (no per-report id)) |
| 3 | 9 | **Longest Substring Without Repeating Characters (+II)** | LC3 | 3 | output all longest substrings; II variant | P 6 | 19 | US 4 / CN 15 | 2026-10 | high | yes | PracHub; TT-008; TI 2026-03-06; TT-056; NC 2925493; NC 922661579517108224 (+6 more, +7 counted from 1P3A bank / CN table (no per-report id)) |
| 4 | 1 | **Course Schedule / topological sort family** | Course Schedule I/II, Parallel Courses III, build order, cycle detection, learning path | 207, 210, 2050* | output the shortest/learning path; print execution order of a DAG and detect cycles; lexicographically smallest order with min-heap; Parallel Courses III with weights | P 8 / O 5 | 15 | US 13 / CN 2 | 2026-10-15 | high | partial | 1P3A 1193703; 1P3A 1192024; PracHub; TT-001; TI 2026-06-15; TI 2026-06-06 (+9 more) |
| 5 | 4 | **Reverse Nodes in k-Group (+ variants)** | LC25, reverse even-length groups 2074 | 25, 2074* | reverse the incomplete tail too; from the tail; O(1) space; even-length group variant; first write a plain reversal | P 3 / O 2 | 13 | US 7 / CN 6 | 2026-10 | high | partial | 1P3A 1180698/TI 2026-06-25; TT-025; TT-066; TI 2025-12-11; NC 940039518206414848; NC 933056720308305920 (+1 more, +6 counted from 1P3A bank / CN table (no per-report id)) |
| 6 | 16 | **Longest Palindromic Substring** | LC5 | 5 | output all longest; Manacher; subsequence follow-up | P 3 / O 2 | 9 | US 3 / CN 6 | 2026-10 | high | yes | TT-005; TI 2026-06-16; TT-056; NC 2929548; NC 2923110; NC 930870582843805696 (+1 more, +2 counted from 1P3A bank / CN table (no per-report id)) |
| 7 | - | **Rate limiter implementation (token bucket / sliding window)** [custom] | distributed rate limiter, flag actors above a rate | - | hand-write a limiter; interviewer pushes token bucket after sliding window; Redis/distributed version | O 1 | 10 | CN 10 | 2026-08 | medium | - | NC 920379874269794304; NC ai-2849957 (+8 counted from 1P3A bank / CN table (no per-report id)) |
| 8 | - | **Binary tree level order / zigzag traversal** |  | 102, 103 | plain; CN uses zigzag often | P 2 / O 2 | 8 | CN 8 | 2026-10 | medium | yes | NC 2927700; NC 938145178114592768; NC 2916483; NC 922828057570709504; NC 2812231 (+3 counted from 1P3A bank / CN table (no per-report id)) |
| 9 | 6 | **Merge Intervals** | LC56, merge time windows | 56 | ads twist start > end; used as a 25-minute opener | P 5 | 8 | US 5 / CN 3 | 2026-10 | high | yes | 1P3A 1183894/TT-010; TI 2026-02-18; TI 2026-02-04; TI 2026-01-25; NC 2926169; NC 2918979 (+2 counted from 1P3A bank / CN table (no per-report id)) |
| 10 | 108 | **Best Time to Buy and Sell Stock family** | LC121/122/123/188 | 121, 122, 123, 188* | once, many times, twice, n times in one hour | P 2 | 7 | US 1 / CN 6 | 2026-09 | high | partial | TI 2026-03-09; NC 2913828; NC 2910816; NC 922663186854092800 (+3 counted from 1P3A bank / CN table (no per-report id)) |
| 11 | 10 | **Top K Frequent Elements** | LC347 | 347 | hashmap+sort, then quickselect/heap; interviewer insists on the heap | P 4 / O 1 | 7 | US 4 / CN 3 | 2026-10-17 | high | yes | job-compass; TI 2026-06-08; TI 2026-01-10; TT-107; NC 942897472391684096; NC 2929548 (+1 more) |
| 12 | 7 | **Kth Largest Element / QuickSelect** | LC215 | 215 | without a heap; quickselect average O(n) | P 2 / O 2 | 7 | US 4 / CN 3 | 2026-10-10 | high | yes | PracHub; TT-009/TI; TI 2026-05-06; TT-052; NC 922661003731406848; NC 922663186854092800 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 13 | 55 | **Reverse Linked List** |  | 206 | in place; what is wrong with this code | P 2 / O 1 | 5 | US 1 / CN 4 | 2026-10 | high | yes | 1P3A 1188918; NC 938540581574164480; NC 932058602422956032 (+2 counted from 1P3A bank / CN table (no per-report id)) |
| 14 | 77 | **Largest number below N from a digit set** [custom] | 用给定数字组成小于n的最大数, 数组中的数能构成的比n小的最大数 | 902 | digits from A may repeat; strictly below N; N=23415, A={2,4,9} -> 22999; greedy + backtracking | P 4 / O 1 | 5 | US 1 / CN 4 | 2026-10 | high | yes | TT-007/TI; NC 2926142; NC 940208627883761664; NC 930870582843805696; NC 932058602422956032 |
| 15 | - | **Deep merge of two nested JSON objects** [custom] | merge nested dict | - | recurse on equal keys, keep unique keys, concatenate lists; follow-ups: key conflict with different types, depth over 10k | P 4 | 4 | CN 4 | 2026-10 | medium | - | NC 938539037059567616; NC 939623386806751232; NC 931893943342465024; NC 932407145864130560 |
| 16 | 54 | **Multiply Strings (+ hex)** | LC43 | 43 | write own cases; hex big-number multiply in CN | P 2 / O 1 | 5 | US 2 / CN 3 | 2026-09 | high | yes | TT-026; TT-081; NC 2905763; NC 933056720308305920 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 17 | 74 | **Binary Tree Right Side View** |  | 199 | plain; ACM-style input in CN | OA 1 / P 3 / O 2 | 5 | US 2 / CN 3 | 2026-10 | high | yes | TI 2026-02-11; TT-053/TI; NC 940040254214389760; NC 2914727; NC 931568372028829696 |
| 18 | 19 | **Restore IP Addresses / valid IPv4** | LC93 | 93 | plain | P 1 | 4 | US 2 / CN 2 | 2026-09-04 | high | yes | TI 2026-09-04; NC 922663816993705984; NC 922666956514131968 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 19 | 8 | **Basic Calculator I / II / III** | LC224/227 | 224, 227, 772 | no parentheses (char array) then parentheses and unary minus; validate then evaluate | P 3 / O 2 | 6 | US 5 / CN 1 | 2026-08-26 | high | yes | TI 2026-06-24; TT-042; TI 2026-01-30; TT-076; NC 2830567 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 20 | 37 | **Merge K Sorted Lists** | merge k price streams | 23 | heap key choice, memory for huge lists | P 2 | 5 | US 3 / CN 2 | 2026-09 | high | yes | TI 2026-04-01; TI 2026-01-16; TT-075; NC 934756038690033664 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 21 | 5 | **Alien Dictionary** | infer alien alphabet | 269 | cycle / invalid input handling; in-degree guard explained | P 2 / O 3 | 4 | US 4 | 2026-09-02 | high | yes | 1P3A bank; 1P3A 1187366; TI 2026-08-15; TI 2026-03-04 |
| 22 | 29 | **Path Sum III (incl. N-ary and upward paths)** | count downward paths with target sum | 437 | N-ary tree; brute-force DFS rejected, prefix sums wanted | P 3 / O 2 | 6 | US 3 / CN 3 | 2026-05-30 | high | yes | TT-027; TI 2026-02-12; TI 2026-01-10; NC 2847755; NC 2827917; NC 2815363 |
| 23 | - | **Implement Trie** | LC208 | 208 | CN agent/backend rounds | P 2 / O 1 | 3 | CN 3 | 2026-10 | medium | yes | NC 940040254214389760; NC 2920851; NC 2914727 |
| 24 | 63 | **Valid Parentheses** | LC20 | 20 | plain | P 2 | 4 | US 2 / CN 2 | 2026-10 | high | yes | TT-045; TI 2026-02-07; NC 940040254214389760; NC 2916909 |
| 25 | - | **Merge Sorted Arrays** | LC88 | 88 | no built-in sort; descending output | P 2 | 3 | CN 3 | 2026-10 | medium | yes | NC 2925747; NC 2920851; NC 922828057570709504 |
| 26 | - | **Subtree of Another Tree** |  | 572 | null is not a subtree | P 1 | 3 | CN 3 | 2026-10 | high | yes | NC 2928138; NC 922662144535994368; 1P3A 1181025 |
| 27 | 48 | **Lowest Common Ancestor of a Binary Tree** |  | 236 | q may not exist in the tree | P 1 | 5 | US 2 / CN 3 | 2026-04-25 | high | yes | TT-034; TI 2026-02-26; NC 2830536 (+2 counted from 1P3A bank / CN table (no per-report id)) |
| 28 | 36 | **MinStack / MaxStack (+ streaming median)** | stack with getMax, min stack | 155 | bundled with MaxStack and streaming median; Java array-backed stack | P 3 / O 2 | 5 | US 3 / CN 2 | 2026-08 | high | yes | TI 2026-02-12; TI 2026-01-30; TI 2026-01-10; NC 2889950; NC 2815079 |
| 29 | 15 | **Search in Rotated Sorted Array / find min** | LC33/153/154 | 33, 153, 154* | with duplicates (154) | P 3 / O 2 | 4 | US 3 / CN 1 | 2026-08-21 | high | partial | TI 2026-08-21; TT-009; TT-095; NC 2812231 |
| 30 | 123 | **House Robber (incl. III on a tree)** | LC198/337 | 198, 337* | tree DP version | P 2 / O 2 | 4 | US 1 / CN 3 | 2026-09 | high | partial | TT-064; NC 2915254; NC 2830306; NC 2826107 |
| 31 | 34 | **Meeting Rooms II / III, max concurrent processes** | LC253/2402 | 253, 2402 | plain | OA 1 / P 1 | 3 | US 2 / CN 1 | 2026-10 | high | yes | TT-011; TI 2026-02-26; NC 2920943 |
| 32 | 11 | **Grid shortest path with obstacle removal / fuel and recharge cells** | LC1293, gas-tank grid reachability | 1293 | k obstacle eliminations; min-cost path with blocked cells, recharge cells and fuel K; large K needs a better state | P 2 / O 3 | 4 | US 4 | 2026-06-30 | high | yes | TT-021; TI 2026-05-27; TT-037/TI; TI 2026-01-31 |
| 33 | 12 | **Binary Tree Maximum Path Sum** | LC124 | 124 | print/reconstruct the path; path need not touch root or leaf | P 1 / O 2 | 5 | US 5 | 2026-07-18 | high | yes | TT-012; TT-050; TI 2026-01-26; TT-072; TT-073 |
| 34 | 116 | **3Sum** | LC15 | 15 | plain | P 1 / O 1 | 3 | US 1 / CN 2 | 2026-10 | high | yes | TT-052; NC 2930690; NC 2866278 |
| 35 | 120 | **Longest Increasing Subsequence** | LC300 | 300 | O(n log n); non-DP in 10 minutes | P 4 | 4 | US 1 / CN 3 | 2026-06 | high | yes | TT-063; NC 898590325818650624; NC 884557598727380992; NC 2838226 |
| 36 | - | **K-th node from the end of a list** |  | 19 | CN variants of LCOF 22 | P 1 / O 1 | 2 | CN 2 | 2026-10 | medium | yes | NC 2929706; NC 2926839 |
| 37 | 13 | **Tic-Tac-Toe GameOver / state check** |  | 348* | O(1) per move check (modified 348) | P 1 | 2 | US 2 | 2026-10-13 | medium | no | TI 2026-09-25 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 38 | 14 | **Circular queue / O(1) deque over a fixed array** | pushHead/popHead/pushTail/popTail/search O(1), rpush/lpush list, circular queue | 622* | fixed-size array with all five operations O(1) | P 1 / O 1 | 4 | US 4 | 2026-07-06 | high | no | TT-017; TT-043; TT-050; TI 2026-01-22 |
| 39 | - | **Transpose Matrix** | LC867, 矩阵转置 | 867* | CN only | O 1 | 2 | CN 2 | 2026-10 | medium | no | NC 940039518206414848; NC 2918654 |
| 40 | - | **Linked List Cycle / entry** |  | 141, 142 | fast-slow pointers | P 1 | 2 | CN 2 | 2026-10 | medium | yes | NC 2929568; NC 920033557844688896 |
| 41 | - | **First 10,000 / n-th prime** [custom] |  | - | sieve (related: LC204) | P 1 / O 1 | 2 | CN 2 | 2026-09 | medium | - | NC 927660076272291840; NC 2922272 |
| 42 | 76 | **Remove Nth Node From End** | kth from the end | 19 | ACM mode in CN | P 2 | 3 | US 2 / CN 1 | 2026-10 | high | yes | TI 2026-02-11; TT-055; NC 2929450 |
| 43 | 17 | **Delete k consecutive elements to balance even/odd index sums** [custom] |  | - | smallest start index such that sums at even and odd indexes of the remainder are equal (related: LC1664) | P 1 | 2 | US 2 | 2026-09-11 | medium | - | 1P3A 1189186 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 44 | 18 | **In-memory KV store with snapshot / restore** [custom] | KV store serialize/deserialize, 内存KV快照 | - | put/get plus snapshot() and restore(); the hard part is the serializer/deserializer | HM 1 | 2 | US 2 | 2026-10-15 | medium | - | 1P3A 1193703; TT-012 |
| 45 | 20 | **Find Median from Data Stream** | LC295 | 295 | bundled with min/max stack | P 2 / O 2 | 3 | US 3 | 2026-10-15 | high | yes | 1P3A 1193703; TI 2026-01-30; TI 2026-01-04 |
| 46 | - | **Ring of 10 points, ways to return to 0 in n steps** [custom] |  | - | step clockwise or counter-clockwise; count walks | O 1 | 2 | CN 2 | 2026-09 | medium | - | NC 2910016; NC 922663186854092800 |
| 47 | 21 | **OA: cyclic rotation pairs** [OA] | count/distinct cyclic number pairs | - | OA only | OA 2 | 2 | US 2 | 2026-09-10 | medium | - | TI 2026-09-10; TI 2026-08-12 |
| 48 | 22 | **In-memory file system** | design file system, ls/mkdir/addContent | 588 | plain; sometimes the second half only | P 1 / O 3 | 3 | US 3 | 2026-08-31 | high | yes | TI 2026-08-31; LCDiscuss; TT-085 |
| 49 | 23 | **Regular Expression / Wildcard Matching** | LC10/44 | 10, 44 | implement regex matching | P 1 / O 2 | 3 | US 2 / SG 1 | 2026-09-04 | high | yes | Reddit 1w6uktk; TT-050; TI 2025-12-16 |
| 50 | 96 | **Word Ladder with shortest path output** | word ladder II, 单词接龙 | 127, 126* | print the shortest transformation path | P 1 | 2 | US 1 / CN 1 | 2026-10 | medium | partial | TT-036; NC 2922504 |
| 51 | 102 | **Trapping Rain Water** | LC42 | 42 | plain | P 2 | 2 | US 1 / CN 1 | 2026-10 | medium | yes | TI 2026-04-01; NC 2925994 |
| 52 | 24 | **Word Search II (trie)** | search words in a character grid | 212 | senior hours ask it with a trie | P 2 / O 1 | 3 | US 3 | 2026-05-20 | high | yes | 1P3A 1177394; TI 2026-04-15; TI 2026-02-19 |
| 53 | 25 | **Sliding Window Maximum** | LC239 | 239 | plain | P 1 / O 1 | 2 | US 2 | 2026-07-24 | medium | yes | TT-009; TI 2026-06-16 |
| 54 | 26 | **Remove Duplicate Letters** | LC316 | 316 | plain; used as 30-minute second half of a screen | P 1 | 2 | US 2 | 2026-07-14 | medium | yes | TT-014; TT-024/TI |
| 55 | 27 | **Longest Substring with At Most K Distinct Characters** | LC340 | 340 | plain, opener of a two-problem hour | P 1 | 2 | US 2 | 2026-09-04 | medium | yes | TT-037/TI (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 56 | 28 | **Reverse Words in a String (preserve spaces, in place)** | LC151 | 151 | keep space counts; in place; more tests | P 1 / O 1 | 3 | US 3 | 2026-04-14 | high | yes | TT-035; TI 2026-03-10; TT-049 |
| 57 | 30 | **Validate Binary Search Tree** |  | 98 | write and run own tests | P 2 | 2 | US 2 | 2026-07-03 | medium | yes | TT-019; TI 2026-06-16 |
| 58 | 56 | **Queue using two stacks** |  | 232 | plain | P 1 | 2 | SG 1 / CN 1 | 2026-09-04 | medium | yes | Reddit 1w6uktk; NC 2814882 |
| 59 | 31 | **Make Costs of Paths Equal in a Binary Tree** | equalize root-to-leaf sums, N-ary +1 variant | 2673* | N-ary variant with only +1 operations | P 1 | 2 | US 2 | 2026-07-15 | medium | no | TT-013; TT-030 |
| 60 | 32 | **Implement a binary min-heap on an array** [custom] | hand-written heap, order courses with prerequisites | - | array heap with push/pop swaps; then use it to order courses by prerequisites | ? | 2 | US 2 | 2026-10-04 | medium | - | PracHub; TT-083 |
| 61 | 33 | **Group Anagrams** | LC49 | 49 | plain | OA 2 | 3 | US 3 | 2026-02-26 | high | yes | TT-047; TI 2026-02-11; TI 2026-02-11 |
| 62 | - | **Palindrome Partitioning** | LC131 | 131* | backtracking | P 2 | 2 | CN 2 | 2026-07 | medium | no | NC 2871942; NC 2823443 |
| 63 | 35 | **Subarray Sum Equals K** | LC560 | 560 | plain | P 2 | 2 | US 2 | 2026-07-29 | medium | yes | TT-008; TI 2026-01-29 |
| 64 | 38 | **Longest subarray of consecutive 1s (+2D)** | LC1004-like | 1004 | follow-up on a 2D array | P 1 / O 1 | 2 | US 2 | 2026-05-16 | medium | yes | TT-028; TI 2026-04-20 |
| 65 | 39 | **Contiguous / aligned memory allocator** | alloc/erase, first-fit, split/coalesce | 2502 | first-fit with split/coalesce, errors for zero/negative/over-capacity/double free; follow-ups: alignment of 8, live-allocation tracking, realloc, thread safety | OA 1 / P 1 | 2 | US 2 | 2026-06-11 | medium | yes | TI 2026-06-11; TI 2026-03-17 |
| 66 | 40 | **Accounts Merge** | merge accounts by shared email | 721 | union-find | P 1 | 2 | US 2 | 2026-07-25 | medium | yes | HelloInterview; TT-068/TI |
| 67 | 41 | **Valid Parenthesis String with * (+ print all)** | LC678 | 678 | DFS to output all valid strings; write own tests | P 3 / O 1 | 3 | US 3 | 2026-02-18 | high | yes | TT-050; TI 2026-01-30; TT-103 |
| 68 | - | **Distinct Subsequences** | LC115 | 115 | plain | ? | 1 | CN 1 | 2026-10 | low | yes | NC 2925463 |
| 69 | - | **Find the Duplicate Number** | LC287 | 287 | plain | P 1 | 1 | CN 1 | 2026-10 | low | yes | NC 2929220 |
| 70 | - | **Flip String to Monotone Increasing** | LC926 | 926* | plain | P 1 | 1 | CN 1 | 2026-10 | low | no | NC 2930609 |
| 71 | - | **Hyper-operation (超运算) hand-written** [custom] |  | - | CN only; statement not given | P 1 | 1 | CN 1 | 2026-10 | low | - | NC 2916924 |
| 72 | - | **Longest Valid Parentheses** | LC32 | 32 | plain | ? | 1 | CN 1 | 2026-10 | low | yes | NC 939524387030437888 |
| 73 | - | **Maximum Product Subarray** | LC152 | 152 | plain | P 1 | 1 | CN 1 | 2026-10 | low | yes | NC 2925500 |
| 74 | - | **Tool-call log: per-tool success rate and worst tool** [custom] |  | - | agent role; low cost aggregation | O 1 | 1 | CN 1 | 2026-10 | low | - | NC 938174888861253632 |
| 75 | 42 | **Possible Bipartition** | split people into two groups with dislike pairs | 886 | BFS/DFS two-colouring; interviewer pushes "optimise" on an already O(n+m) solution | P 1 | 1 | US 1 | 2026-10-14 | medium | yes | 1P3A 1193669 |
| 76 | 43 | **Maximize fish from decaying ponds** [custom] |  | - | research-scientist screen | ? | 1 | US 1 | 2026-10-09 | medium | - |  (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 77 | 44 | **Median / Kth of two sorted arrays** | LC4 | 4 | kth largest in two sorted arrays | P 1 / O 1 | 2 | US 2 | 2026-06-16 | medium | yes | TI 2026-06-16; TT-063 |
| 78 | 45 | **Koko Eating Bananas / minimum constant speed** | LC875 | 875 | brute force first, then optimise; analyse each line | P 1 / O 1 | 2 | US 2 | 2026-06-04 | medium | yes | TT-026; TI 2026-01-26 |
| 79 | 46 | **N-Queens** | LC51 | 51 | two test cases then complexity | P 1 / O 1 | 2 | US 2 | 2026-05-13 | medium | yes | TT-029; TI 2026-02-16 |
| 80 | 47 | **Spiral Matrix with follow-up constraints** |  | 54 | O(1) extra space, do not modify the input, single row/column edge cases | P 1 | 1 | US 1 | 2026-09-28 | medium | yes | TI 2026-09-28 |
| 81 | 107 | **Square root with precision** | LC69, Newton iteration | 69 | Newton iteration / precision | O 2 | 2 | US 1 / CN 1 | 2026-04 | medium | yes | TI 2026-03-10; NC 2825446 |
| 82 | 49 | **Add Two Numbers II** | LC445 | 445 | San Jose live coding | ? | 1 | US 1 | 2026-09-15 | low | yes | Glassdoor |
| 83 | - | **Concurrency-limited async task scheduler (JS)** [custom] | Scheduler with max 2 running | - | frontend/full-stack role | P 1 | 1 | CN 1 | 2026-09 | low | - | NC 2914598 |
| 84 | - | **Binary Search** | LC704 | 704 | plain | P 1 | 1 | CN 1 | 2026-09 | low | yes | NC 932058602422956032 |
| 85 | - | **Generate Parentheses** | LC22 | 22 | plain | P 1 | 1 | CN 1 | 2026-09 | low | yes | NC 2929192 |
| 86 | - | **Minimum Path Sum** | LC64 | 64 | plain | ? | 1 | CN 1 | 2026-09 | low | yes | NC 935858952644939776 |
| 87 | - | **Permutations** | LC46 | 46 | plain | ? | 1 | CN 1 | 2026-09 | low | yes | NC 2901760 |
| 88 | - | **Shortest Unsorted Continuous Subarray** | LC581 | 581 | plain | ? | 1 | CN 1 | 2026-09 | low | yes | NC 937314680270311424 |
| 89 | - | **Surrounded Regions** |  | 130* | plain | P 1 | 1 | CN 1 | 2026-09 | low | no | NC 934865450729472000 |
| 90 | - | **Target Sum** | LC494 | 494* | plain | P 1 | 1 | CN 1 | 2026-09 | low | no | NC 2917490 |
| 91 | 50 | **Word Break I / II** | LC139/140 | 139, 140 | plain | P 1 / O 1 | 2 | US 2 | 2026-06-16 | medium | yes | TI 2026-06-16; TT-085 |
| 92 | 51 | **CodeSignal OA set (drone relay, newspaper layout, zigzag subarrays)** [OA] |  | - | OA only | OA 1 | 2 | US 2 | 2026-03-17 | medium | - | TI 2026-03-17 (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 93 | 52 | **OA: repeated digit-group summation** [OA] |  | - | OA only | ? | 1 | US 1 | 2026-09-10 | medium | - |  (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 94 | 53 | **OA: identifier naming conversion in docstrings** [OA] | snake_case to camelCase inside backticks | - | OA only | OA 1 | 1 | US 1 | 2026-09-10 | low | - | TI 2026-09-10 |
| 95 | 57 | **Non-overlapping Intervals** | LC435 | 435* | HM round, greedy by end | HM 1 | 1 | US 1 | 2026-09-02 | medium | no | 1P3A 1188260 |
| 96 | 58 | **Seller Task Scheduler** [custom] | round-robin task scheduler, VIP seller | - | receive_task / process_next_task; rotate across sellers, VIP sellers get 2 tasks per turn, priority then FIFO | P 1 | 1 | US 1 | 2026-09-02 | medium | - | 1P3A 1188260/TI 2026-09-02 |
| 97 | 59 | **Design HashMap (+ concurrency)** | implement hash table, collision handling | 706 | built step by step from simple to hard with concurrency questions interleaved | P 2 / O 1 | 2 | US 2 | 2026-05-27 | medium | yes | TI 2026-05-27; TT-099 |
| 98 | 60 | **Enumerate all simple directed paths / cycles** [custom] |  | - | backtracking; cycles are the hard version | P 1 | 1 | US 1 | 2026-08-23 | low | - | TI 2026-08-23 |
| 99 | 61 | **Currency conversion queries** [custom] | exchange rate pairs, maximize amount after conversions | 399, 3387* | pairs with rates, queries return the rate or -1 (e.g. USD-JPY 108.0, JPY-USD 1/108.0, USD-GBP -1.0) | P 1 / O 1 | 3 | US 3 | 2026-01-05 | high | partial | 1P3A 1160243; TT-094; TT-106 |
| 100 | 62 | **Removable timestamp-ordered task scheduler** [custom] | addTask/removeTask/popTask(num), Task Manager | - | earliest-timestamp pop with removal and deterministic tie-break; popTask must remove the task | P 1 | 1 | US 1 | 2026-08-20 | medium | - | 1P3A 1186877/TI 2026-08-20 |
| 101 | 64 | **Water and Jug (+ shortest operation chain)** | LC365 | 365 | also output the shortest operation sequence; harder version | ? | 2 | US 2 | 2026-05-08 | medium | yes | TT-033; TT-088 |
| 102 | 65 | **Create Binary Tree from Descriptions** |  | 2196* | plain | O 1 | 1 | US 1 | 2026-08-17 | low | no | TI 2026-08-17 |

### 1.3 Below the cut line (ranks 103 to 186)

| # | US rank | Family | Aliases | LC | How TikTok changed it | Stages (events touching) | #refs | Region | Last seen | Conf | In decks | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 103 | 66 | **Pythagorean triple in an integer array** [custom] |  | - | a^2+b^2=c^2 with abs/squares, zero and duplicates; O(n^2) | O 1 | 1 | US 1 | 2026-08-17 | medium | - | 1P3A 1186440/TI 2026-08-17 |
| 104 | 67 | **Stickers to Spell Word** | LC691 | 691* | bitmask DP; prune by first uncovered character | O 1 | 1 | US 1 | 2026-08-17 | medium | no | 1P3A 1186440/TI 2026-08-17 |
| 105 | - | **Letter Combinations of a Phone Number** | LC17 | 17 | plain | ? | 1 | CN 1 | 2026-08 | low | yes | NC 922663816993705984 |
| 106 | 68 | **Symmetric Tree** |  | 101 | plain | ? | 1 | US 1 | 2026-08-15 | low | yes | HelloInterview |
| 107 | 69 | **Nested comment tree from flat records** [custom] | flatten/build comment tree | - | flat (id, parent_id) records to a nested tree | P 1 | 1 | US 1 | 2026-08-13 | low | - | TI 2026-08-13 |
| 108 | 70 | **Add two signed numeric strings** [custom] | 含正负号字符串相加 | 415 | plain add strings plus sign handling | ? | 1 | US 1 | 2026-08-11 | medium | yes | TT-002 |
| 109 | 71 | **Idempotent versioned database update** [custom] |  | - | locked on PracHub; statement not recoverable | ? | 1 | US 1 | 2026-08-09 | low | - | PracHub |
| 110 | 72 | **Largest Rectangle in Histogram** | LC84 | 84 | plain; complexity analysis | P 2 / O 1 | 2 | US 2 | 2026-02-18 | medium | yes | TI 2026-02-18; TT-056/TI |
| 111 | 73 | **AI-assisted OrderValidator (rule DAG)** [custom] |  | - | rules form a DAG; remove a rule and reconnect predecessors to successors; own AI IDE; tests are graded | P 1 | 1 | US 1 | 2026-08-06 | low | - | TI 2026-08-06 |
| 112 | 75 | **Delete a node from a tree and reconnect** |  | 450 | non-BST version: replace by deepest-rightmost | P 1 | 2 | US 2 | 2026-02-11 | medium | yes | TI 2026-02-11; TT-055 |
| 113 | - | **Next Permutation** | LC31 | 31 | CN only | ? | 1 | CN 1 | 2026-08 | low | yes |  (+1 counted from 1P3A bank / CN table (no per-report id)) |
| 114 | - | **Longest Common Subsequence / Substring** | LC1143 | 1143 | output the sequence; substring with DP | ? | 2 | CN 2 | 2026-04 | medium | yes | NC 2830536; NC 2713354 |
| 115 | 147 | **Unique Paths (+ must pass through a cell)** | LC62 | 62 | multiply two calls for the via-point version | O 1 | 2 | US 1 / CN 1 | 2026-04 | medium | yes | TT-104; NC 2840893 |
| 116 | 78 | **Longest Repeating Character Replacement** | LC424 | 424 | plain | O 1 | 1 | US 1 | 2026-07-24 | medium | yes | TT-009 |
| 117 | 79 | **Flatten a multilevel list, skip empty nested nodes** |  | 430* | nested node with empty value is excluded | O 1 | 1 | US 1 | 2026-07-18 | medium | no | TT-012 |
| 118 | 80 | **Most frequent element, ties -> smaller** [custom] |  | - | warm-up easy | P 1 | 1 | US 1 | 2026-07-15 | medium | - | TT-013 |
| 119 | 81 | **Longest Common Suffix Queries (trie)** | LC3093 | 3093* | most common suffix via trie | P 1 | 1 | US 1 | 2026-07-02 | medium | no | TT-020 |
| 120 | 82 | **Minimum Window Substring** | LC76 | 76 | plain | P 1 | 1 | US 1 | 2026-06-29 | low | yes | TI 2026-06-29 |
| 121 | 83 | **Maximum unique-character subset** | LC1239 | 1239* | bitmask/backtracking | O 1 | 1 | US 1 | 2026-06-28 | low | no | TI 2026-06-28 |
| 122 | 84 | **Sorted array: values appearing more than n/3** [custom] |  | - | sub-linear time using the sorted order | P 1 | 1 | US 1 | 2026-06-27 | medium | - | TT-022/TI |
| 123 | 85 | **Count Number of Nice Subarrays** | LC1248 | 1248 | brute force accepted first | ? | 1 | US 1 | 2026-06-26 | medium | yes | TT-023 |
| 124 | 86 | **Search Insert Position / binary search ladder** | LC35 | 35* | ladder 35 -> 153 -> 154 | P 1 / O 1 | 2 | US 2 | 2026-02-18 | medium | no | TT-050; TT-095 |
| 125 | 87 | **Count of Interesting Subarrays** | LC2845 variant | 2845* | variant of the original | ? | 1 | US 1 | 2026-06-18 | medium | no | 1P3A 1180698 |
| 126 | 88 | **Longest zigzag path in a grid** [custom] |  | - | DFS/DP on grid | P 1 | 1 | US 1 | 2026-06-17 | low | - | TI 2026-06-17 |
| 127 | - | **Dynamic-batching request queue (pseudo-code)** [custom] |  | - | AI-platform social-hire post, low confidence | ? | 1 | CN 1 | 2026-06 | low | - | NC 924248590447280128 |
| 128 | - | **Product of Array Except Self** | LC238 | 238* | plain | P 1 | 1 | CN 1 | 2026-06 | low | no | NC ai-2860170 |
| 129 | 89 | **Serialize and Deserialize Binary Tree** |  | 297 | space-optimise the null markers | P 1 | 2 | US 2 | 2026-02-04 | medium | yes | TI 2026-02-04; TT-092 |
| 130 | 90 | **OA: house segments after deletions** [OA] |  | - | OA only | OA 1 | 1 | US 1 | 2026-05-31 | low | - | TI 2026-05-31 |
| 131 | 91 | **BFS maze / map shortest path with path output** [custom] |  | - | BFS + backtrace | P 2 | 2 | US 2 | 2026-01-03 | medium | - | TT-064; TT-103 |
| 132 | 92 | **First and last position in a sorted array** | LC34, rightmost occurrence | 34 | O(log n) rightmost occurrence | P 1 | 2 | US 2 | 2025-12-12 | medium | yes | TT-069; TI 2025-10-19 |
| 133 | 93 | **Fruit Into Baskets (candy line variant)** | LC904 | 904 | pick consecutive candies, only two kinds, stop at a third | ? | 1 | US 1 | 2026-05-12 | medium | yes | TT-031 |
| 134 | 94 | **OA: sort concentric matrix borders clockwise** [OA] |  | - | OA only | OA 1 | 1 | US 1 | 2026-04-20 | low | - | TI 2026-04-20 |
| 135 | 95 | **Minimum parentheses additions** | LC921 | 921* | plain | P 1 | 1 | US 1 | 2026-04-19 | low | no | TI 2026-04-19 |
| 136 | - | **Beautiful Arrangement II** | LC667 | 667* | plain | P 1 | 1 | CN 1 | 2026-04 | low | no | NC 2833665 |
| 137 | - | **Expression tree (+ - * / power factorial)** [custom] |  | - | AI-research flavoured backend role | O 1 | 1 | CN 1 | 2026-04 | low | - | NC 2830757 |
| 138 | - | **Intersection of Two Linked Lists** |  | 160 | plain | ? | 1 | CN 1 | 2026-04 | low | yes | NC 2830536 |
| 139 | - | **Set Matrix Zeroes** |  | 73* | plain | P 1 | 1 | CN 1 | 2026-04 | low | no | NC 2829767 |
| 140 | - | **Permutation in String** | LC567 | 567* | plain | P 1 | 1 | CN 1 | 2026-04 | low | no | NC 2833873 |
| 141 | - | **Permutation Sequence** | LC60 | 60* | plain | P 1 | 1 | CN 1 | 2026-04 | low | no | NC 2826851 |
| 142 | 97 | **Most Frequent Subtree Sum** | LC508 | 508* | return all values on ties; prep-service post | ? | 1 | US 1 | 2026-04-11 | low | no | LCDiscuss |
| 143 | 98 | **Probability one fair die beats another** [custom] |  | - | two dice with given faces; sort + two pointers | P 1 | 1 | US 1 | 2026-04-04 | low | - | TI 2026-04-04 |
| 144 | 99 | **Missing Ranges / Summary Ranges with bounds** | LC163/228 | 163*, 228* | [3,5,10] -> [[0,2],[4],[6,9]] with lower and upper bounds | ? | 1 | US 1 | 2026-04-02 | medium | no | TT-038 |
| 145 | 100 | **Tree diameter / longest path** |  | 543 | plain | P 1 / O 1 | 1 | US 1 | 2026-04-02 | low | yes | TI 2026-04-02 |
| 146 | 101 | **Swim in Rising Water / min time grid path** |  | 778* | priority queue or binary search on T | ? | 1 | US 1 | 2026-04-01 | medium | no | TT-039 |
| 147 | 103 | **Combinations** | LC77 | 77 | choose k of 1..n | P 1 | 1 | US 1 | 2026-03-27 | medium | yes | TT-040 |
| 148 | 104 | **Time Based Key-Value Store** | timestamped KV, 981 | 981* | plain original, once combined with sliding windows and LRU | O 1 | 1 | US 1 | 2026-03-20 | low | no | TI 2026-03-20 |
| 149 | 105 | **Two Sum variants (in-flight movie pair)** | LC1 | 1 | plain | O 1 | 1 | US 1 | 2026-03-17 | low | yes | TI 2026-03-17 |
| 150 | - | **Expand bracket-number string then recompress** [custom] | LC394 variant | 394 | non-LeetCode compression format | O 1 | 1 | CN 1 | 2026-03 | low | yes | NC 2823289 |
| 151 | 106 | **Photo groups via transitive similarity** [custom] | friend circles variant | 323* | isSimilar matrix; count groups after transitive closure | P 1 | 1 | US 1 | 2026-03-10 | medium | no | TT-044/TI |
| 152 | 109 | **OA: case-insensitive adjacent differences** [OA] |  | - | OA only | OA 1 | 1 | US 1 | 2026-03-05 | low | - | TI 2026-03-05 |
| 153 | 110 | **Parse a nested list string** | LC339/385 | 385*, 339* | parse "[...]" into nested lists with a stack | ? | 1 | US 1 | 2026-02-27 | medium | no | TT-046 |
| 154 | 111 | **Per-user per-day login counts from a log stream** [custom] |  | - | sorted by user; also validate bad dates/times | P 1 | 1 | US 1 | 2026-02-24 | medium | - | TT-051 |
| 155 | 112 | **Find All Anagrams in a String** | LC438 | 438 | plain | P 1 / O 1 | 1 | US 1 | 2026-02-21 | low | yes | TI 2026-02-21 |
| 156 | 113 | **Number of Days Between Two Dates** | LC1360 | 1360* | plain | O 1 | 1 | US 1 | 2026-02-21 | medium | no | TT-049 |
| 157 | 114 | **Subsets I / II** | LC78/90 | 78, 90* | plain | O 1 | 1 | US 1 | 2026-02-21 | medium | partial | TT-049 |
| 158 | 115 | **Coin Change II (combination counts)** | LC518 | 518 | plain | O 1 | 1 | US 1 | 2026-02-17 | low | yes | TI 2026-02-17 |
| 159 | 117 | **Amount of Time for Binary Tree to Be Infected** |  | 2385* | optimal solution required | ? | 1 | US 1 | 2026-01-29 | medium | no | TT-054 |
| 160 | 118 | **Min Cost Climbing Stairs** | LC746 | 746* | plain | ? | 1 | US 1 | 2026-01-28 | medium | no | TT-056 |
| 161 | 119 | **Kth Smallest Subarray Sum** | LC1918 | 1918* | named only by number | ? | 1 | US 1 | 2026-01-08 | medium | no | TT-062 |
| 162 | 121 | **Populating Next Right Pointers** |  | 116* | plain | O 1 | 1 | US 1 | 2026-01-06 | medium | no | TT-063 |
| 163 | 122 | **OA: local maximum on a 1-D stream** [OA] |  | - | OA only | OA 1 | 1 | US 1 | 2026-01-04 | low | - | TI 2026-01-04 |
| 164 | 124 | **Longest String Chain** | LC1048 | 1048* | write test cases | ? | 1 | US 1 | 2025-12-13 | medium | no | TT-067 |
| 165 | 125 | **Successful Pairs of Spells and Potions** | LC2300 | 2300* | plain | P 1 | 1 | US 1 | 2025-12-13 | medium | no | TT-068/TI |
| 166 | 126 | **Minimum Size Subarray Sum** | LC209 | 209 | plain | ? | 1 | US 1 | 2025-12-10 | medium | yes | TT-071 |
| 167 | 127 | **Cells that can flow to the border** | Pacific Atlantic | 417 | high-to-low flow to the boundary | P 1 | 1 | US 1 | 2025-12-10 | medium | yes | TT-070 |
| 168 | 128 | **Kth smallest in a sorted matrix** | LC378 | 378 | plain | P 1 | 1 | US 1 | 2025-12-08 | low | yes | TI 2025-12-08 |
| 169 | 129 | **Contiguous subarray with the largest min+max** [custom] |  | - | [5,12,9,6,4] -> 12+9 = 21, length >= 2; brute force then linear | P 1 | 1 | US 1 | 2025-11-26 | medium | - | TT-074/TI |
| 170 | 130 | **Minimum Swaps to Make Strings Equal** | LC1247 | 1247* | plain | P 1 | 1 | US 1 | 2025-11-20 | medium | no | TT-077 |
| 171 | 131 | **24 Game** | LC679 | 679 | plain | ? | 1 | US 1 | 2025-11-15 | medium | yes | TT-080 |
| 172 | 132 | **De-duplicate singly and doubly linked lists** [custom] |  | 83 | new-grad round with business discussion | ? | 1 | US 1 | 2025-11-01 | low | yes | job-compass |
| 173 | 133 | **Inorder iterator over a string-valued tree** [custom] |  | - | each node holds a string; next() returns one character in inorder | O 1 | 1 | US 1 | 2025-10-31 | medium | - | TT-085 |
| 174 | 134 | **Jump Game I / II** | LC55/45 | 55, 45 | plain (NG) | ? | 1 | US 1 | 2025-10-30 | medium | yes | TT-086 |
| 175 | 135 | **get_chat_messages window merge** [custom] | merge chat message windows | - | API returns 5 messages above and below an ID inclusive; merge several responses, dedupe, ordered | ? | 1 | US 1 | 2025-10-21 | medium | - | TT-090 |
| 176 | 136 | **PercentileFinder (addNums / findPercentile)** [custom] | running percentile, bisect | - | maintain a number set, return the p-th percentile; asked for a better structure than bisect | ? | 1 | US 1 | 2025-10-21 | medium | - | TT-089 |
| 177 | 137 | **Binary tree column (vertical) traversal with sorting** |  | 987* | plain | ? | 1 | US 1 | 2025-10-20 | medium | no | TT-091 |
| 178 | 138 | **Combination Sum** | LC39 | 39 | plain (NG) | P 1 | 1 | US 1 | 2025-10-17 | medium | yes | TT-093 |
| 179 | 139 | **Count inverse pairs** | LCOF 51 | LCOF | merge sort | ? | 1 | US 1 | 2025-10-17 | low | yes | job-compass |
| 180 | 140 | **Weighted random sampler** | random pick with weight | 528 | follow-up: dynamic weight updates (Fenwick / segment tree / balanced tree) | P 1 | 1 | US 1 | 2025-10-16 | medium | yes | TT-094 |
| 181 | 141 | **IP range to the shortest CIDR list** | IP to CIDR | 751* | 127.0.0.7-127.0.0.16 -> [127.0.0.7/32, 127.0.0.8/29, 127.0.0.16/32]; list must be shortest | ? | 1 | US 1 | 2025-10-14 | medium | no | TT-096 |
| 182 | 142 | **Remove All Adjacent Duplicates in String II** | LC1209 | 1209 | plain; asked with hash-table and DNS 八股 | ? | 1 | US 1 | 2025-10-12 | medium | yes | TT-097 |
| 183 | 143 | **24-bit color to nearest pure color** [custom] |  | - | new-grad round; statement truncated in source | P 1 | 1 | US 1 | 2025-10-09 | medium | - | TT-101 |
| 184 | 144 | **Paged API: best-rated food in a city** [custom] |  | - | new-grad round; loop over pages | P 1 | 1 | US 1 | 2025-10-09 | medium | - | TT-101 |
| 185 | 145 | **Binary Tree Cameras** |  | 968* | tree DP; second hard tree problem as spoken follow-up | P 1 | 1 | US 1 | 2025-10-09 | medium | no | TT-102 |
| 186 | 146 | **Text Justification** | LC68 | 68 | plain | O 1 | 1 | US 1 | 2025-10-05 | medium | yes | TT-103 |

## 2. System design (ranked by US + SG refs x recency; CN shown separately)

Counts are prompts, not 1P3A "hot topic" tallies. Overlaps are removed where the sources overlap visibly (TrueInterview and 1P3A bank carry the same events). Hello Interview user counts are not added where overlap with the bank is unknown. CN designs are listed as reported; the "dozens" of Agent-platform prompts are counted as 30 (approximate).

| # | Prompt | #refs | Region | Last seen | Stages | What interviewers pushed on | Conf | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | **Payment system (checkout, charge, confirmation, ledger)** (支付系统（收银台、扣款、确认、账本）) | 5 | SG 2 / US 3 | 2026-10-13 | onsite, HM | 每一个可重试的步骤都要幂等（idempotency key）；用户不能被重复扣款，订单不能在没收到钱时被标记已付 ; 支付状态机 + append-only ledger（整数最小货币单位）；与 PSP 对账（reconciliation）；丢失或重复的 webhook；步骤之间崩溃 ; 追问一：卖家打款（payout）后 ledger 怎么变；追问二：两家 PSP 之间路由，一家变差时 failover；追问三：支付挂起 1 小时，如何解决、用户看到什么；追问四：全额与部分退款不破坏对账 ; 安全：不碰卡数据（PSP tokenization）；HM 轮只有约 30 分钟，一名候选人因没讲 Stripe UI 如何嵌入供应商页面、时间用完而失分 | high | TI 2025-12-10; Reddit 1qqb5n6; PracHub design-a-payment-system; 1P3A bank; Glassdoor SG |
| 2 | **Agent / AI platform designs (tool use, QA pipeline, memory, harness)** (Agent / AI 平台设计（工具调用、QA 流水线、记忆、harness）) | 35 | CN 30 / US 5 | 2026-09-16 | phone, onsite | memory、context 压缩、harness、sub-agent 深度限制、评测；工具调用参数错误 / 超时 / 重试；幂等 key 为什么不让模型自己生成 ; CN 岗位里数量最大的设计类，但与美国 senior 后端关系较弱 | low | TI; 1P3A 1189821; Nowcoder (dozens) |
| 3 | **Top-K / leaderboard / trending (top songs by country, recent likes)** (Top-K / 排行榜 / 热榜（各国热歌、近期点赞）) | 9 | CN 5 / US 4 | 2026-09-24 | onsite, senior | 先估算：约 5 万 listens/s 写、5 万 reads/s、每国 top-10 约每 10 分钟刷新；GET /songs/top?region=US、POST /songs/{id}/listen ; 要精确还是近似：没问清楚 top-K 是否必须精确是一次被拒的原因；count-min sketch 误差界、heavy hitters ; 滑动窗口与滚动窗口、迟到和乱序事件；Kafka 分区与爆款内容造成的热 key；结果走缓存；availability over consistency、读延迟 < 1 s ; 全局榜与分地区榜 | medium | TI 2026-08-30 / 2026-06-11; 1P3A 1187870; TT-028; PracHub guide; CN table |
| 4 | **Monitoring / alerting / metrics aggregator** (监控告警 / 指标聚合) | 4 | CN 1 / US 3 | 2026-10 | phone | 客户端库上报计数；按时间桶 rollup；热 key；重试和重复上报下的正确性；基数（cardinality）控制 ; 告警规则评估与用户可配置告警（2025-09 的一次 2-1 面试：design monitoring system that can send alerts users configure）；延迟预算 | medium | TI 2026-09-15; Hello Interview metrics-aggregator; 1P3A bank; LC Discuss 7150750 (pre-window) |
| 5 | **Content / video moderation (ML scores + rules + human review + appeals)** (内容 / 视频审核系统（ML 打分 + 规则 + 人审 + 申诉）) | 6 | CN 1 / US 5 | 2026-08-12 | onsite, senior/manager | 近实时 SLA 下带重 ML 的链路；规则引擎要能在几分钟内更新、不重新发版 ; 幂等执行（idempotent enforcement）与完整审计线索：模型版本、分数、命中规则、动作 ; 全球规模与数据驻留；人审队列与申诉流程；突发流量与背压（backpressure） | high | 1P3A bank content-moderation-system-design; TI 2026-04-17; Hello Interview video-moderation (4 users, last 2026-04, not added: overlap unknown) |
| 6 | **Short-video recommendation / feed / recommendation engine** (短视频推荐 / 信息流 / 推荐引擎) | 5 | CN 1 / US 4 | 2026-10 | onsite, Growth R2 | 冷启动、特征泄漏（feature leakage）、多目标权重 ; 候选生成与排序分层、retrieval 阶段的 K、serving 延迟 ; A/B 测试（Innovative Growth 岗位相关，推断） | medium | TT-021; TI 2026-08-17 / 2026-01-28; 1P3A bank short-video-recommendation-system |
| 7 | **Flash sale / ticket booking under surge traffic** (秒杀 / 抢票（突发流量）) | 18 | CN 16 / US 2 | 2026-10-05 | onsite | 突发流量先扛住：负载均衡、排队 / waiting room、限流，别让突发直接打到后端服务和数据库 ; 库存预扣：Redis + Lua 保证一人一单、不超卖；下单失败后回补库存；MQ 削峰与积压处理 ; 10 个库存、1 万 QPS 怎么保证服务稳定；热点 key；10 万人抢 1000 个座位且长途乘客优先（CN） ; 第二个核心问题文本被付费墙截断（可能是库存 / 超卖，未核实） | medium | TI 2026-10-05; PracHub guide; CN table |
| 8 | **Consistency / cache design (cache stampede, hot key)** (一致性 / 缓存设计（缓存击穿、热 key）) | 2 | US 2 | 2026-10-13 | onsite | 请求合并（coalescing）、锁、提前刷新、TTL 加抖动 ; 失败场景比架构图更重要；该候选人给出了"tiktok 在线上真正用的方案" | medium | Blind; 1P3A 1192940; TI |
| 9 | **Job scheduler / task system** (任务调度系统 / Task System) | 3 | US 3 | 2026-09-15 | phone, onsite | 每个 (job_id, fire_time) 只有一个持久化槽位；多台调度机同时看到到期任务：lease / fencing、at-most-once 提交 ; 停机后的 backfill；worker 执行中崩溃；部分系统宕机时失败通知仍要发出；重试 / 退避如何与 at-most-once 共存 ; 约 1 万 starts/s、整分钟边界 5 到 10 倍突发；调度延迟与死信的可观测性。评分的是这些失败场景的追问 ; TT-091 版本：PM 定义任务（QPS 低）、按 profile 选 creator、creator 在 TikTok App 看任务（约 1 万 QPS）、完成任务领奖（约 1 千 QPS） | medium | TI job-scheduler-design (free text in kevin-2023-code mirror); TT-091 |
| 10 | **Real-time auction bidding** (实时拍卖出价系统) | 2 | US 2 | 2026-09-24 | onsite | 每个参与者要以最小延迟看到当前最高价；原子更新出价、竞态条件 ; 一份被引用的答案：REST 入口 -> Kafka（按 auction_id 分区，保证同一场拍卖的出价有序）-> Bid Worker（校验 + UPDATE MySQL + PUBLISH Redis）-> SSE 服务（Redis Pub/Sub 推给客户端） ; MySQL 存全部出价 + 状态机，不只存最高价；exactly-once 出价处理；断线重连、WebSocket 与 SSE 取舍 | medium | 1P3A 1177394; TI 2026-05-20; PracHub guide |
| 11 | **Distributed KV / cache / file store** (分布式 KV / 缓存 / 文件存储) | 6 | CN 4 / SG 1 / US 1 | 2026-10 | phone, onsite | 单点故障、负载均衡、高可用低延迟；哈希路由 + 主从异步备份在极端故障下的数据风险 ; 严格递增的版本号（versions） | low | 1P3A 1161499; PracHub guide; Nowcoder |
| 12 | **Video-keyword association review system (team spec)** (视频-关键词关联审核系统（团队真实模块）) | 2 | US 2 | 2026-07-06 | onsite | 广告创意计划很多，每次提交 50+ 视频 × 1000+ 关键词，计算视频与关键词的关系 ; 版本化更新、可续传上传、任务系统；答案要以笔记 / 伪代码写进 codepad（不是通用系统设计） | medium | 1P3A 1182289; TI 2026-06-01 |
| 13 | **Live room comment / like / barrage (danmaku) system** (直播间评论 / 点赞 / 弹幕系统) | 14 | CN 12 / US 2 | 2026-10 | phone, onsite | fan-out、顺序、与视频时间线同步和重放、断线重连 ; 弹幕每秒百万级推送的高可用；点赞计数与 Top100 排行（Redis ZSET）、写放大、热点 ; 评论分页用游标而不是 LIMIT offset；热度排序 hot_score = log10(2*likes + replies) + 时间衰减（CN 单篇押题文，低可信） | medium | TI 2026-04-28; TT-011; Nowcoder 2929684 / 2925500 / 2926839; CN table |
| 14 | **Currency exchange-rate system** (汇率系统) | 1 | US 1 | 2026-10-15 | onsite | 汇率数据的存取、查询与多跳换算（与编码题 currency_conv 同一主题） | low | 1P3A 1193703 |
| 15 | **Distributed rate limiter (design)** (分布式限流器（设计）) | 3 | CN 2 / US 1 | 2026-09-24 | phone, onsite | 令牌桶与滑动窗口；Redis + Lua；分布式场景的 key 设计（手写版见编码表 rate_limiter） | low | PracHub guide; Nowcoder |
| 16 | **TikTok LIVE coin tracking and settlement** (TikTok LIVE 打赏金币追踪与结算) | 1 | US 1 | 2026-09-05 | senior onsite | 全球分布式、高精度的金币跟踪与结算；全球用户实时虚拟礼物，保证幂等（idempotency） ; 每场直播创作者的精确收益；每周可靠结算。账本、对账、跨区一致性是推断的深挖点（原文只有一句题面） | low | Hello Interview tiktok-live-coin-tracking |
| 17 | **Demand-side ad platform data model (campaigns, targeting, edit history) / ad de-duplication** (广告平台数据模型（计划、定向、修改历史）/ 广告去重) | 3 | CN 2 / US 1 | 2026-09 | onsite | 建模：campaign / targeting / edit history 与版本；广告召回的数据结构（not in / in 条件，属性成百上千万量级）；已看广告去重的省内存结构（Bloom filter 类） | low | TI 2026-04-23; Nowcoder |
| 18 | **Short URL / TinyURL** (短链接服务) | 5 | CN 4 / US 1 | 2026-08 | phone | 标准题：ID 生成、重定向、缓存；追问多落在故障模式而非多地域 | medium | TI 2026-02-28; CN table |
| 19 | **Chat / IM / group-message notification** (聊天 / IM / 群消息通知) | 4 | CN 3 / US 1 | 2026-10 | onsite | 消息不丢、重连后去重下发；最近 30 到 40 条快速加载；群聊 fan-out 与存储模型 | low | TT-084; Nowcoder |
| 20 | **Long tail, one report each** (长尾（各 1 例）) | 8 | US 8 | 2026-08-28 | phone, onsite | 各例仅有标题，无追问记录 | low | TI |

Cross-cutting themes (from the rows above): idempotency and exactly-once effects (payment, coins, bids, moderation enforcement, job slots); money correctness (ledger, reconciliation, integer minor units, async settlement); windowed aggregation under skew (exact vs approximate, hot keys, late events); failure behaviour over architecture drawing (crash mid-step, duplicate or lost callbacks, backpressure); operational shape (SLA, lag, audit trail, rules without redeploy). Formats: 45-60 min, sometimes 15 min inside a mixed hour or 3 h in Singapore; prompts are often a module of the team's real product and may be typed into a code pad with no drawing tool.

## 3. Scenario and oral fundamentals (八股, 场景题)

Hand tallies, approximate where the note says so. US = PDF / TrueInterview / 1P3A / PracHub; CN = Nowcoder and mirror. These come as the first 20-30 min of a technical hour (resume drill then 八股) or as a separate fundamentals hour.

| # | Topic | US | CN | Last seen | Stages | Notes |
|---|---|---|---|---|---|---|
| 1 | Backend fundamentals oral hour (CAP, indexes, concurrency, logging, distributed systems) | 6 | 0 | 2026-09-28 | phone, onsite | 1P3A bank backend-fundamentals-oral-cluster n=6 (2026-03-13..2026-09-28); also TT-003, TT-024, TT-068, TT-018, TT-009 R3 (45 min), TI blog 2026-09-06 |
| 2 | Redis: distributed lock (SET NX + Lua, watchdog, RedLock, failover), data structures, persistence | 3 | 35 | 2026-10 | phone, onsite | CN 35 mentions (forums_cn.md sec 2); US TT-024, TT-025, PracHub guide (sorted sets, persistence) |
| 3 | MySQL: indexes, B+ tree, isolation / MVCC / gap lock, slow query, deep paging | 5 | 12 | 2026-10 | phone, onsite | US TT-003, TT-024, TT-068, TT-087, TI 2026-04-12; CN approximate (deep paging 3 + about 9 enumerated) |
| 4 | Cache problems: penetration / breakdown / avalanche, cache-aside consistency, hot key, big key | 2 | 6 | 2026-10 | phone, onsite | US TI guide and PracHub guide (not per-report); CN hot-key/big-key 4 + 2 enumerated |
| 5 | Message queues: Kafka partitions / rebalance / ordering, RabbitMQ no-loss, dead letter, backlog | 3 | 6 | 2026-10 | phone, onsite | US TT-024 (2026-06-25), TT-025 / 1P3A rag-agent-kafka drill (2026-06-03), TT-060 (2026-01-16); CN approximate |
| 6 | Idempotency and distributed transactions (TCC, SAGA, outbox, empty rollback) | 2 | 6 | 2026-10 | phone, onsite | CN table 6; US PracHub payment follow-ups, Glassdoor SG; also a Redis-key / idempotency-key probe in Agent roles |
| 7 | Java / Go / Python runtime and concurrency (ConcurrentHashMap, LinkedHashMap, thread pool, GC, GMP, GIL) | 5 | 10 | 2026-10 | phone, onsite | US TT-050 R3, TT-073, TT-099, TT-025, TI 2025-11-16; CN approximate |
| 8 | Networking and OS: TCP handshake / TIME_WAIT, TLS, DNS, URL-to-page flow, virtual memory | 8 | 6 | 2026-09-03 | phone, onsite | US TT-097, TT-101, TT-087, TI 2026-08-23 (x2), TI 2026-09-05; CN browser-URL flow 3 and TIME_WAIT 3 (approximate) |
| 9 | SRE: Linux / networking troubleshooting, shell script, disk full, Docker / K8s | 10 | 0 | 2026-09-03 | phone, onsite | 1P3A bank sre-linux-networking-troubleshoot n=10 (2025-12-08..2026-09-03); TT-018, TT-040 |
| 10 | Service protection: rate limit, degrade, circuit breaker, retry with backoff, QPS spike 10x | 0 | 8 | 2026-10 | phone, onsite | CN only: Sentinel, 10k->100k QPS, "why not infinite retry", general fuse / degrade strategy |
| 11 | Search / storage internals: Elasticsearch mapping and inverted index, vector index (HNSW / IVF), Milvus 100B | 1 | 4 | 2026-09-25 | phone, onsite | US PracHub 2026-09-25; CN approximate |
| 12 | Agent / RAG / LLM-application oral (MCP, memory, eval, ReAct, context compression) | 3 | 30 | 2026-10 | phone, onsite | CN dozens (approximate); US TT-025, TT-009, 1P3A rag-agent-kafka drill |
| 13 | ML knowledge oral cluster (attention, DPO, PPO, normalization) -- MLE / RS roles | 13 | 3 | 2026-10-15 | phone, onsite | 1P3A bank ml-knowledge-oral-cluster n=13; not backend |
| 14 | Frontend / language trivia (JS rest parameter, Spring bean lifecycle, @Autowired, Vue reactivity) | 2 | 3 | 2026-09 | phone, onsite | TT-057, TT-084; CN fullstack posts |

## 4. Behavioural and hiring-manager questions

| # | Question family | #refs | Last seen | Stage | Notes / sources |
|---|---|---|---|---|---|
| 1 | Project deep dive / resume drill (every technical round; 10-45 min) | 56 | 2026-10-13 | phone, onsite, HM | 1P3A bank project-deep-dive-round n=56 (2025-11-19..2026-10-13); typical probes: why this tech, mature infra considered, metrics, bottleneck, org-level design reasons |
| 2 | HM / final round behavioural (+ occasional pseudo-code or coding) | 11 | 2026-08-17 | HM | 1P3A bank hm-behavioral-final-round n=9 (2026-01-29..2026-08-17) + TT-098 (2025-10-11), TT-079 (2025-11-15) |
| 3 | Hardest project / technical challenge / proudest project | 15 | 2026-08-12 | phone, HM | TT-001, 010, 013, 023, 027, 034, 041, 049, 056, 060 + TI 2026-04-17, 2026-04-12, 2026-01-23, 2026-01-02 |
| 4 | Conflict, disagreement with manager or teammate, communication difficulty | 5 | 2026-08-25 | phone, HM | TT-051, TT-056, TT-091, TI 2026-01-01, TI 2026-08-25 (1P3A bank motivation-ambiguity-collaboration n=3) |
| 5 | Ambiguity, failure, prioritisation (STAR) | 2 | 2026-02-12 | HM | TT-056 list; TI 2026-02-12 |
| 6 | Why TikTok / career plan / teamwork approach | 5 | 2026-05-11 | phone, HM | TT-032, TT-035, TT-068, TI 2025-12-08, TI 2026-02-12 |
| 7 | Stability, incidents and production troubleshooting | 5 | 2026-09-05 | phone | TI 2026-09-05 (x2), TI 2026-01-27, TT-026, 1P3A 1179052; PracHub guide HM list |
| 8 | AI usage in work and projects | 2 | 2026-03-01 | phone | TT-046, TI 2026-03-01; AI-assisted coding rounds are in the coding table (order_validator) |
| 9 | Impact: UX wins, over-engineering, promotion story | 3 | 2026-04-02 | phone | TI 2026-02-01, TI 2026-02-28, TT-038 |
| 10 | Fit probes: Chinese language, workload intensity, location | 3 | 2026-06-24 | HM | Reddit 1t5pu24 (2026-05-06), Blind 2026-06-24, TI/G1 "high-intensity workload" (undated) |
| 11 | Reverse BQ / questions for the interviewer (last 5-15 min) | 5 | 2026-07-07 | phone | TT-016, TT-029, TT-049, TT-070, TT-077 |

Official value list (ByteStyle, six values) and how the HM round is run are in `behavioral.md` and `loop.md`; no first-hand report cites a value by name as a rubric.

## 5. What the decks are missing (summary of `additions.json`)

- **LeetCode originals to add: 50** (reported at least once in the window and not in `index.json`; the 3387 entry has no sighting date). Most-reported: Transpose Matrix (867, 2), Design Tic-Tac-Toe (348, 2), Palindrome Partitioning (131, 2), Make Costs of Paths Equal in a Binary Tree (2673, 2), Design Circular Queue (622, 2), Search Insert Position (35, 2), Reverse Nodes in Even Length Groups (2074, 2), Flip String to Monotone Increasing (926, 1).
- **TikTok variants to add: 34** (statements reconstructed in Chinese; every statement lists inferred parts in `note`). Top by refs x recency: lru-cache-ttl (12), rate-limiter-implementation (10), islands-follow-ups (8), largest-number-below-n-from-digits (5), reverse-k-group-variants (5), deep-merge-nested-json (4), basic-calculator-ladder (6), course-schedule-output-path (3).
- **System-design prompts ranked: 20** rows.

LeetCode additions (id, slug, refs, last seen):

| LC | Slug | Title | Refs | Last seen | Why |
|---|---|---|---|---|---|
| 867 | `transpose-matrix` | Transpose Matrix | 2 | 2026-10 | Transpose Matrix: 2 report(s) (CN 2); CN only. e.g. 940039518206414848, 2918654 |
| 348 | `design-tic-tac-toe` | Design Tic-Tac-Toe (premium) | 2 | 2026-10-13 | Tic-Tac-Toe GameOver / state check: 2 report(s) (US 2); premium; "GameOver in O(1)" is the modified LC348 asked of new graduates; 1P3A bank tic-tac-toe-game-state-check n=2. e.g. ti4.tic_tac_toe |
| 131 | `palindrome-partitioning` | Palindrome Partitioning | 2 | 2026-07 | Palindrome Partitioning: 2 report(s) (CN 2); backtracking. e.g. 2871942, 2823443 |
| 2673 | `make-costs-of-paths-equal-in-a-binary-tree` | Make Costs of Paths Equal in a Binary Tree | 2 | 2026-07-15 | Make Costs of Paths Equal in a Binary Tree: 2 report(s) (US 2); N-ary variant with only +1 operations. e.g. TT-013, TT-030 |
| 622 | `design-circular-queue` | Design Circular Queue | 2 | 2026-07-06 | Circular queue / O(1) deque over a fixed array: 2 report(s) (US 2); circular queue; asked twice (PDF TT-017 and TrueInterview 2026-01-22). e.g. TT-017, ti97.deque_circular |
| 35 | `search-insert-position` | Search Insert Position | 2 | 2026-02-18 | Search Insert Position / binary search ladder: 2 report(s) (US 2); binary-search ladder 35 -> 153 -> 154 (new-grad) and a 26NG round 2 problem. e.g. TT-050, TT-095 |
| 2074 | `reverse-nodes-in-even-length-groups` | Reverse Nodes in Even Length Groups | 2 | 2025-12-23 | Reverse Nodes in k-Group (+ variants): 2 report(s) (US 2); reverse the incomplete tail too; from the tail; O(1) space; even-length group variant; first write a plain reversal. e.g. TT-066, ti105.k_group |
| 926 | `flip-string-to-monotone-increasing` | Flip String to Monotone Increasing | 1 | 2026-10 | Flip String to Monotone Increasing: 1 report(s) (CN 1). e.g. 2930609 |
| 130 | `surrounded-regions` | Surrounded Regions | 1 | 2026-09 | Surrounded Regions: 1 report(s) (CN 1). e.g. 934865450729472000 |
| 188 | `best-time-to-buy-and-sell-stock-iv` | Best Time to Buy and Sell Stock IV | 1 | 2026-09 | Best Time to Buy and Sell Stock family: 1 report(s) (CN 1); third part of a Chinese Agent-role screen (once, twice, n times). e.g. 2913828 |
| 494 | `target-sum` | Target Sum | 1 | 2026-09 | Target Sum: 1 report(s) (CN 1). e.g. 2917490 |
| 435 | `non-overlapping-intervals` | Non-overlapping Intervals | 1 | 2026-09-02 | Non-overlapping Intervals: 1 report(s) (US 1); HM round, greedy by end. e.g. P3A-1188260 |
| 691 | `stickers-to-spell-word` | Stickers to Spell Word | 1 | 2026-08-17 | Stickers to Spell Word: 1 report(s) (US 1); bitmask DP; prune by first uncovered character. e.g. P3A-1186440 |
| 2196 | `create-binary-tree-from-descriptions` | Create Binary Tree From Descriptions | 1 | 2026-08-17 | Create Binary Tree from Descriptions: 1 report(s) (US 1). e.g. ti14.create_tree_desc |
| 430 | `flatten-a-multilevel-doubly-linked-list` | Flatten a Multilevel Doubly Linked List | 1 | 2026-07-18 | Flatten a multilevel list, skip empty nested nodes: 1 report(s) (US 1); nested node with empty value is excluded. e.g. TT-012 |
| 3093 | `longest-common-suffix-queries` | Longest Common Suffix Queries | 1 | 2026-07-02 | Longest Common Suffix Queries (trie): 1 report(s) (US 1); most common suffix via trie. e.g. TT-020 |
| 1239 | `maximum-length-of-a-concatenated-string-with-unique-characters` | Maximum Length of a Concatenated String with Unique Characters | 1 | 2026-06-28 | Maximum unique-character subset: 1 report(s) (US 1); inferred from the TrueInterview title "Maximum Unique Character Subset" (hard, onsite, bitmask/backtracking); the report gives no LC number. e.g. ti24.max_unique_subset |
| 2845 | `count-of-interesting-subarrays` | Count of Interesting Subarrays | 1 | 2026-06-18 | Count of Interesting Subarrays: 1 report(s) (US 1); reported as "a variant of LC 2845 (Count of Interesting Subarrays)"; the original is the base to study. e.g. P3A-1180698 |
| 238 | `product-of-array-except-self` | Product of Array Except Self | 1 | 2026-06 | Product of Array Except Self: 1 report(s) (CN 1). e.g. ai-2860170 |
| 2050 | `parallel-courses-iii` | Parallel Courses III | 1 | 2026-06-15 | Course Schedule / topological sort family: 1 report(s) (US 1); TrueInterview "Parallel Courses III" (phone + onsite, 2026-06-15); family also asked as lexicographically-smallest order with a min-heap. e.g. ti36.course_schedule |
| 921 | `minimum-add-to-make-parentheses-valid` | Minimum Add to Make Parentheses Valid | 1 | 2026-04-19 | Minimum parentheses additions: 1 report(s) (US 1). e.g. ti51.min_parens_add |
| 60 | `permutation-sequence` | Permutation Sequence | 1 | 2026-04 | Permutation Sequence: 1 report(s) (CN 1). e.g. 2826851 |
| 73 | `set-matrix-zeroes` | Set Matrix Zeroes | 1 | 2026-04 | Set Matrix Zeroes: 1 report(s) (CN 1). e.g. 2829767 |
| 567 | `permutation-in-string` | Permutation in String | 1 | 2026-04 | Permutation in String: 1 report(s) (CN 1). e.g. 2833873 |
| 667 | `beautiful-arrangement-ii` | Beautiful Arrangement II | 1 | 2026-04 | Beautiful Arrangement II: 1 report(s) (CN 1). e.g. 2833665 |
| 126 | `word-ladder-ii` | Word Ladder II | 1 | 2026-04-12 | Word Ladder with shortest path output: 1 report(s) (US 1); second problem of a phone screen: Word-Ladder-like with the shortest path printed (ladder II); LC127 is already in the decks. e.g. TT-036 |
| 508 | `most-frequent-subtree-sum` | Most Frequent Subtree Sum | 1 | 2026-04-11 | Most Frequent Subtree Sum: 1 report(s) (US 1); single prep-service post (LC Discuss 7875303, low); return all values on ties. e.g. EN-lc2 |
| 163 | `missing-ranges` | Missing Ranges (premium) | 1 | 2026-04-02 | Missing Ranges / Summary Ranges with bounds: 1 report(s) (US 1); premium; the report is LC228-style ("a variant of LC 228") but its example [3,5,10] -> [[0,2],[4],[6,9]] with a lower and upper bound is Missing Ranges. e.g. TT-038 |
| 228 | `summary-ranges` | Summary Ranges | 1 | 2026-04-02 | Missing Ranges / Summary Ranges with bounds: 1 report(s) (US 1); cited by number in the report; the actual task has lower/upper bounds, which is LC163 (both listed). e.g. TT-038 |
| 778 | `swim-in-rising-water` | Swim in Rising Water | 1 | 2026-04-01 | Swim in Rising Water / min time grid path: 1 report(s) (US 1); priority queue or binary search on T. e.g. TT-039 |
| 981 | `time-based-key-value-store` | Time Based Key-Value Store | 1 | 2026-03-20 | Time Based Key-Value Store: 1 report(s) (US 1); TrueInterview onsite 2026-03-20; bank time-based-key-value-store n=1. e.g. ti61.time_kv |
| 323 | `number-of-connected-components-in-an-undirected-graph` | Number of Connected Components in an Undirected Graph (premium) | 1 | 2026-03-10 | Photo groups via transitive similarity: 1 report(s) (US 1); isSimilar matrix; count groups after transitive closure. e.g. TT-044 |
| 339 | `nested-list-weight-sum` | Nested List Weight Sum (premium) | 1 | 2026-02-27 | Parse a nested list string: 1 report(s) (US 1); cited by number in the report ("similar to LC339"); the nested-list parsing task is closest to LC385 (both listed); premium. e.g. TT-046 |
| 385 | `mini-parser` | Mini Parser | 1 | 2026-02-27 | Parse a nested list string: 1 report(s) (US 1); closest actual match for the report that cited LC339 (parse a nested-list string with a stack). e.g. TT-046 |
| 90 | `subsets-ii` | Subsets II | 1 | 2026-02-21 | Subsets I / II: 1 report(s) (US 1). e.g. TT-049 |
| 1360 | `number-of-days-between-two-dates` | Number of Days Between Two Dates | 1 | 2026-02-21 | Number of Days Between Two Dates: 1 report(s) (US 1). e.g. TT-049 |
| 2385 | `amount-of-time-for-binary-tree-to-be-infected` | Amount of Time for Binary Tree to Be Infected | 1 | 2026-01-29 | Amount of Time for Binary Tree to Be Infected: 1 report(s) (US 1); optimal solution required. e.g. TT-054 |
| 746 | `min-cost-climbing-stairs` | Min Cost Climbing Stairs | 1 | 2026-01-28 | Min Cost Climbing Stairs: 1 report(s) (US 1). e.g. TT-056 |
| 1918 | `kth-smallest-subarray-sum` | Kth Smallest Subarray Sum (premium) | 1 | 2026-01-08 | Kth Smallest Subarray Sum: 1 report(s) (US 1); named only by number in the report (PDF TT-062 "未具名题目 [LC1918]"); premium problem; low confidence on the exact problem. e.g. TT-062 |
| 116 | `populating-next-right-pointers-in-each-node` | Populating Next Right Pointers in Each Node | 1 | 2026-01-06 | Populating Next Right Pointers: 1 report(s) (US 1). e.g. TT-063 |
| 337 | `house-robber-iii` | House Robber III | 1 | 2026-01-03 | House Robber (incl. III on a tree): 1 report(s) (US 1); tree DP version. e.g. TT-064 |
| 1048 | `longest-string-chain` | Longest String Chain | 1 | 2025-12-13 | Longest String Chain: 1 report(s) (US 1); write test cases. e.g. TT-067 |
| 2300 | `successful-pairs-of-spells-and-potions` | Successful Pairs of Spells and Potions | 1 | 2025-12-13 | Successful Pairs of Spells and Potions: 1 report(s) (US 1). e.g. TT-068 |
| 1247 | `minimum-swaps-to-make-strings-equal` | Minimum Swaps to Make Strings Equal | 1 | 2025-11-20 | Minimum Swaps to Make Strings Equal: 1 report(s) (US 1). e.g. TT-077 |
| 711 | `number-of-distinct-islands-ii` | Number of Distinct Islands II (premium) | 1 | 2025-11-19 | Number of Islands family: 1 report(s) (US 1); follow-up of Number of Distinct Islands: rotations and flips count as the same shape. e.g. TT-078 |
| 987 | `vertical-order-traversal-of-a-binary-tree` | Vertical Order Traversal of a Binary Tree | 1 | 2025-10-20 | Binary tree column (vertical) traversal with sorting: 1 report(s) (US 1). e.g. TT-091 |
| 154 | `find-minimum-in-rotated-sorted-array-ii` | Find Minimum in Rotated Sorted Array II | 1 | 2025-10-15 | Search in Rotated Sorted Array / find min: 1 report(s) (US 1); third rung of the binary-search ladder (with duplicates). e.g. TT-095 |
| 751 | `ip-to-cidr` | IP to CIDR (premium) | 1 | 2025-10-14 | IP range to the shortest CIDR list: 1 report(s) (US 1); premium; the report uses an inclusive start/end IP range rather than LeetCode 751's (ip, n) input. e.g. TT-096 |
| 968 | `binary-tree-cameras` | Binary Tree Cameras | 1 | 2025-10-09 | Binary Tree Cameras: 1 report(s) (US 1); tree DP; second hard tree problem as spoken follow-up. e.g. TT-102 |
| 3387 | `maximize-amount-after-two-days-of-conversions` | Maximize Amount After Two Days of Conversions | 1 | undated | Maximize Amount After Two Days of Conversions: named in the ombharatiya FAANG-Coding-Interview-Questions list (commit 2026-10-09, derivative of TrueInterview data) as TikTok "currency exchange"; the sighting has no date, so it is not strictly inside the window; low confidence |

Variants (see `additions.json` for the full Chinese statements):

| Key | Title | Refs | Last seen | Region |
|---|---|---|---|---|
| `lru-cache-ttl` | LRU cache with TTL (+ LFU, weighted, thread-safe follow-ups) | 12 | 2026-10 | CN 3, US 4 |
| `rate-limiter-implementation` | Hand-written rate limiter | 10 | 2026-08 | CN 2 |
| `islands-follow-ups` | Number of Islands and its follow-ups | 8 | 2026-07-08 | US 8 |
| `largest-number-below-n-from-digits` | Largest number below N from an allowed digit set | 5 | 2026-10-15 | CN 4, US 1 |
| `reverse-k-group-variants` | Reverse nodes in k-group variants | 5 | 2026-09-15 | CN 2, US 3 |
| `deep-merge-nested-json` | Deep merge of two nested JSON objects | 4 | 2026-10-15 | CN 4 |
| `basic-calculator-ladder` | Basic calculator ladder (validate, then evaluate) | 6 | 2026-06-24 | CN 1, US 4 |
| `course-schedule-output-path` | Course Schedule with the learning path (and Word Ladder path) output | 3 | 2026-08-15 | CN 1, US 2 |
| `currency-conversion-queries` | Currency conversion queries | 2 | 2026-10-15 | US 1 |
| `kv-store-snapshot-restore` | In-memory KV store with snapshot and restore | 2 | 2026-10-15 | US 2 |
| `ring-walk-count` | Walks on a 10-point ring returning to 0 | 2 | 2026-09-15 | CN 2 |
| `delete-window-balance-even-odd` | Delete a k-window so even-index and odd-index sums match | 2 | 2026-09-11 | US 1 |
| `contiguous-memory-allocator` | Contiguous memory allocator | 2 | 2026-06-11 | US 2 |
| `path-sum-n-ary-prefix-sum` | Count downward paths with target sum in an N-ary tree | 2 | 2026-05-30 | US 2 |
| `water-jug-shortest-operations` | Water and Jug with the shortest operation sequence | 2 | 2026-05-08 | US 2 |
| `grid-min-cost-fuel-recharge` | Grid minimum-cost path with blocked cells, recharge cells and fuel K | 2 | 2026-04-09 | US 2 |
| `spiral-matrix-constant-space` | Spiral matrix with O(1) extra space and no mutation | 1 | 2026-09-28 | US 1 |
| `fixed-array-deque-o1` | Fixed-size array deque / list with O(1) operations | 2 | 2026-03-25 | US 2 |
| `seller-task-scheduler` | Seller task scheduler (round-robin, VIP, priority) | 1 | 2026-09-02 | US 1 |
| `removable-timestamp-task-scheduler` | Removable timestamp-ordered task scheduler | 1 | 2026-08-20 | US 1 |
| `max-path-sum-with-path` | Binary tree maximum path sum with path reconstruction | 2 | 2026-02-18 | US 2 |
| `pythagorean-triple-in-array` | Pythagorean triple in an integer array | 1 | 2026-08-17 | US 1 |
| `valid-parenthesis-string-print-all` | Valid parenthesis string with * and print all valid strings | 2 | 2026-02-18 | US 2 |
| `nested-comment-tree` | Build a nested comment tree from flat records | 1 | 2026-08-13 | US 1 |
| `ai-assisted-order-validator` | AI-assisted OrderValidator (rule DAG) | 1 | 2026-08-06 | US 1 |
| `flatten-multilevel-list-skip-empty` | Flatten a multilevel list, excluding empty nested nodes | 1 | 2026-07-18 | US 1 |
| `sorted-array-more-than-n-over-3` | Values appearing more than n/3 times in a sorted array | 1 | 2026-06-27 | US 1 |
| `login-count-per-user-per-day` | Per-user per-day login counts from a log stream | 1 | 2026-02-24 | US 1 |
| `subarray-max-min-plus-max` | Subarray (length >= 2) maximising min + max | 1 | 2025-11-26 | US 1 |
| `inorder-string-iterator` | In-order character iterator over a string-valued tree | 1 | 2025-10-31 | US 1 |
| `chat-message-window-merge` | Chat message window merge (get_chat_messages) | 1 | 2025-10-21 | US 1 |
| `percentile-finder` | PercentileFinder (addNums / findPercentile) | 1 | 2025-10-21 | US 1 |
| `weighted-sampler-dynamic-update` | Weighted sampler with dynamic weight updates | 1 | 2025-10-16 | US 1 |
| `ip-range-to-cidr` | IP range to the shortest CIDR list | 1 | 2025-10-14 | US 1 |

## 6. Known weaknesses of these numbers

- Aggregators overlap in ways the sources do not state: TrueInterview dates match 1P3A bank dates on many records, so the 7-day merge is a heuristic; counts are a lower bound for US families and an unknown mix for CN families.
- 1P3A thread bodies are behind a points wall, so the bank gives names and counts only; PDF items carry the compilation's own dates (not verified interview dates).
- Chinese counts mix intern, campus and social hires, and several Nowcoder posts are AI-rewritten templates (marked low); the 面经-NN columns re-list other posts, so some CN counts may still be a little high.
- Stage data is sparse: most PDF and CN records do not name the round.
- Problem identification from short titles can be wrong (examples: "Maximum Unique Character Subset" read as LC1239; "LC1247" and "LC4293" named by a PDF record with garbled numbers).
