# Snowflake OA / HackerRank Problems — 2023–2026 sweep

Compiled 2026-09-13 for GenSWE (Software Engineer – Backend, Menlo Park/Bellevue, IC1–IC2) prep.
Sources: LeetCode Discuss (fetched verbatim via LeetCode GraphQL `topic(id)` query — many older
Snowflake OA posts are **image-only screenshots with no OCR'd text**, marked below), 1point3acres
(`bbs/thread-*` pages and the Cloudflare-gated `/interview/problems/company/snowflake` listing are
403/login-walled; only its public-preview problem pages and Telegram-mirrored thread titles were
reachable), FastPrep (structured, paraphrased problem bank explicitly tagged
company=Snowflake/round/date — problems are AI-paraphrased "Source Match" clones of the real
report, not verbatim, so treated as MED unless corroborated), PracHub (similar structured/paraphrased
bank; "Last Updated" dates cluster on a handful of days — Apr 5, Apr 12, Jun 12/15/17, Aug 15/23/24/29,
Sep 3 2026 — strongly suggesting these are page-generation/re-index dates, not independent sighting
dates, so PracHub dates are NOT used as "first/last seen" evidence, only as a weak recency floor),
Blind, Glassdoor (summaries only, pages 403), interviewfox.ai / linkjob.ai (AI/SEO-generated OA
recap articles — different pages claim different "author's own 2026 OA" question sets for the same
company/timeframe, which is the fingerprint of templated/fabricated recaps; used only as LOW
confidence, and only for facts corroborated elsewhere), GitHub (raw.githubusercontent.com fetchable;
one Snowflake file found, in `coding_phone_onsite.md`'s file-system entry cross-reference).

Confidence key: **HIGH** = first-hand candidate post (verbatim or near-verbatim) or an original
LeetCode-numbered problem confirmed as reused; **MED** = a single structured aggregator with
consistent, specific detail (FastPrep/PracHub/1p3a), or ≥2 independent sources agreeing on
specifics; **LOW** = single SEO/AI-recap source with no corroboration — flagged, not dropped, since
Snowflake's public English footprint is much thinner than Stripe's.

## Format facts (cross-source)

- **Platform: HackerRank.** Confirmed across all eras (2019 phone-screen post through 2026 recaps).
- **Question count has been stable at 2–3 per OA across 2020–2026**, but the time budget has crept
  up: 90 min / "1 LC Medium + 2 LC Hards" (Core Engineering Intern, reported 2021-01-25,
  https://leetcode.com/discuss/interview-question/1031552/ — HIGH, verbatim); 90 min / 3 problems,
  Java or C++ 11/14/20 only (Core/Data Engineering Intern, reported 2022-09-08,
  https://leetcode.com/discuss/interview-question/2550834/Snowflake-OA-(CoreData-Engineering-Intern) —
  HIGH, verbatim); 135 min / 3 problems — 2 DP + 1 backtracking (Infrastructure Automation Intern,
  Summer 2025, reported via 1point3acres thread-1120493, summarized in WebSearch snippet, MED —
  page itself 403); 120 min / 3 problems, medium–hard (2026 new-grad cycle, per
  https://www.linkjob.ai/interview-questions/snowflake-hackerrank-oa/ and
  https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/ — LOW individually,
  but corroborated by FastPrep's OA problem list below, which independently shows the same-named
  problems, so the 120 min/3-problem 2026 format is MED overall).
- **Language gating**: Python allowed only for Infra/AI-ML tracks; Core/Database/Core-Eng tracks
  require C++ or Java (LOW, interviewfox, uncorroborated) — but the 2022 Core/Data-Eng post above
  independently confirms "Only Java or C++ 11/14/20 allowed" for that track (HIGH), so the
  track-gating claim itself is plausible even if the specific 2026 wording is LOW.
- **Proctoring**: HackerRank Proctor Mode, periodic webcam/screenshot capture reported (LOW, single
  source, interviewfox).
- **Where in the funnel**: OA is the first technical gate, before recruiter/technical phone
  screens, across every era sampled (2020 intern through 2026 recaps).
- **Reported difficulty**: "8–10/10", "long descriptions, strict edge cases, high time pressure"
  (LOW, interviewfox) but consistent with HIGH-confidence posts describing 90-minute LC Hard-level
  content passed with 2 minutes to spare (2021 post above).
- The 2023 Summer-Internship-Canada megathread
  (https://leetcode.com/discuss/interview-question/3169843/, posted 2023-02-10, HIGH — this is a
  candidate's own index of 20 links, each individually a screenshot-only post) shows the OA
  question **pool** is much larger than any single sitting; candidates draw from a shared bank and
  a handful of problems recur across cycles (see clusters below).

---

## 1. Task Scheduling — paid vs. free server (0/1-knapsack-flavored scheduling)
**Confidence: HIGH**
Sources:
- https://leetcode.com/discuss/interview-question/2550834/Snowflake-OA-(CoreData-Engineering-Intern) — posted 2022-09-08, role: Core/Data Engineering Intern, 90 min OA, verbatim: "You are given two arrays, cost and time. You have a paid server, and a free server. You receive the tasks in order from left to right. For the ith task, if there is no task already running on the paid server, you must schedule the new task on the paid server. Otherwise, you can choose to schedule the task on the paid server or the free server. cost[i] represents the cost of performing the ith task on the paid server, and time[i] represents the time it takes to perform the ith task on the paid server. It costs nothing to schedule a task on the free server, and the free server processes the ith task in 1 unit of time, regardless of time[i]. Return the minimum cost to schedule all tasks."
- https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ (2026-03-16, LOW individually) independently names "Task Scheduling – 0/1 knapsack variation optimizing costs across paid and free servers" as one of 3 OA problems reported for the 2026 cycle — matches the 2022 statement closely enough to be the same recurring problem, raising this to MED-HIGH combined with the LC source.
- Also indexed (link only, unfetched — screenshot post) as item #1 "Task Scheduling" in the 2023 Canada intern list: https://leetcode.com/discuss/interview-question/2775415 (posted 2022-11-03; content is 3 images, no OCR text — "(unfetched: image-only post)").
Confidence rationale: verbatim HIGH source + independent 2026 recap naming the same mechanic = recurring OA problem across ≥3 cycles (2022, 2023-index, 2026).

## 2. Consecutive-vowel string counting (DP)
**Confidence: HIGH** (verbatim) — cluster with #12 (String Patterns)
Source: https://leetcode.com/discuss/interview-question/2550834/ (same post as #1), problem 1 of 3: "You are given two integers n and k. Return the number of strings of length n you can form where there are no more than k consecutive vowels in the string." 90 min, Core/Data Engineering Intern, 2022-09-08.
Maps to: no exact LC number; DP over (position, trailing-vowel-run-length).

## 3. Vowel-only substrings containing every vowel
**Confidence: HIGH** (verbatim)
Source: https://leetcode.com/discuss/interview-question/2550834/ (same post), problem 2 of 3: "You are given a string s. Return the number of substrings within s that contain at least one of each vowel, and do not contain any consonants." 2022-09-08.
Maps to: LC 1987 "Count Vowel Substrings of a String" (near-identical family) — also independently listed as item "Vowel Substring" in the 2023 Canada index (https://leetcode.com/discuss/interview-question/2550995, link only) and as "Vowel Substring" on FastPrep (Medium, String/Sliding Window, last reported 2026-06, https://www.fastprep.io/problems/snowflake-vowel-substring) — MED-HIGH combined.

## 4. Maximum Order Volume ("phone calls") — weighted interval scheduling
**Confidence: MED** (original LC post now returns "topic does not exist"; recovered via aggregator)
Sources:
- Referenced by title/URL in https://leetcode.com/discuss/interview-question/1033329/snowflake-oa-intern/ (2021-01-25, HIGH that the title existed) and in the 2023 Canada index item 3 (2023-02-10) — but the underlying post id 1028649 now 404s server-side ("That topic does not exist" — unfetched, likely deleted).
- Full statement recovered from https://www.fastprep.io/problems/phone-calls — "Maximum Order Volume (Snowflake Online Assessment)", Hard, DP: "A supermarket receives customer calls with known start times, durations, and order volumes... only one call can be in progress at any one time... select non-overlapping calls to maximize total order volume." `phoneCalls(start[], duration[], volume[]) -> int`, n ≤ 1e5, values ≤ 1e9/1e3. Example: start=[10,5,15,18,30], duration=[30,12,20,35,35], volume=[50,51,20,25,10] → 76 (calls 2,4).
Maps to: weighted job scheduling / "Maximum Profit in Job Scheduling" (LC 1235) pattern, binary-search + DP.

## 5. Server Selection
**Confidence: MED** (real, but statement is image-only in both known copies)
Sources: https://leetcode.com/discuss/interview-question/2594968/Snowflake-or-OA-or-Server-Selection (posted 2022-09-08, "(unfetched: image-only post)" — commenter could not solve); https://leetcode.com/discuss/interview-question/2794537 (posted 2022-11-08, title "Server Selection", also image-only, but text comment gives constraint: "2 <= m <= n <= 1000... there is an O(N^2) solution, but [asking] how to solve in O(m*n)"); indexed as item #2 in the 2023 Canada list (2023-02-10).
Statement: candidate reports it as a 2D DP over m servers / n items, target complexity O(m·n). No further detail recoverable without the images.

## 6. Non-Overlapping Intervals variant
**Confidence: LOW** (index-only, link points to a screenshot post never independently corroborated)
Source: item #4 of the 2023 Canada index, https://leetcode.com/discuss/interview-question/2115993 (unfetched). Maps to: likely LC 435 "Non-overlapping Intervals" family.

## 7. "Grid Land" / Kth-Smallest-Instructions — mislabeled cross-company item, flag only
**Confidence: LOW / CAUTION**
The 2021 Snowflake intern-OA post (https://leetcode.com/discuss/interview-question/1033329/, 2021-01-25) links https://leetcode.com/discuss/interview-question/527769/Lucid-or-OA-or-Gridland as merely "similar" to an easy Snowflake question — but that post's own title and verbatim body ("I have an online assessment for Lucid... problem is called gridworld... permutations of H's and V's") is explicitly a **Lucid** OA, dated 2020-03-03, not Snowflake. The 2023 Canada index nonetheless re-lists it as Snowflake item #5 "Grid Land / Kth Smallest Instructions." **Do not treat this as a confirmed Snowflake problem** — it looks like aggregator cross-contamination between two companies' similar grid-permutation OAs. Included here only as a caution for anyone building a problem set from the raw index.

## 8. Lexicographically largest array (MEX-based)
**Confidence: LOW** (index-only) — item #6 of 2023 Canada index, https://leetcode.com/discuss/interview-question/2550995 (unfetched, image-only per its "Vowel Substring" sibling post pattern).

## 9. Patching Array
**Confidence: HIGH** (real LC problem, confirmed reused verbatim in a Snowflake phone screen — see `coding_phone_onsite.md` #2) and independently indexed as OA item #7 in the 2023 Canada list (link is the canonical https://leetcode.com/problems/patching-array/, i.e., LC 484 asked as-is).
Maps to: LC 484 "Patching Array" — exact, unmodified.

## 10–11. Minimize Array Value / Maximum Array Value
**Confidence: LOW** (index-only) — items #8 (https://leetcode.com/discuss/interview-question/2146013) and #9 (https://leetcode.com/discuss/interview-question/2551033) of the 2023 Canada index; both unfetched (image posts). Likely LC 2439/2440-family "minimize the maximum of arrays after operations" variants given the naming.

## 12. Palindromic Subsequences
**Confidence: MED** — item #10 of the 2023 Canada index, links directly to LC 2002 "Maximum Product of the Length of Two Palindromic Subsequences" — i.e. this OA problem is the unmodified LeetCode problem.

## 13. Largest Sub Grid
**Confidence: LOW** (index-only) — item #11, https://leetcode.com/discuss/interview-question/850974 (unfetched, image post, originally dated ~2020 based on ID range so may predate Snowflake and be cross-indexed like #7).

## 14. Vowel Substring (LC-exact)
**Confidence: MED** — item #12 of the 2023 index links straight to LC 2062 "Count Vowel Substrings of a String" (exact reuse), separate from / overlapping problem #3's DP variant above — Snowflake appears to reuse this LC problem in both its exact and DP-generalized forms across different OA sittings.

## 15. String Formation via dictionary (LC-exact)
**Confidence: MED** — item #13 of 2023 index links to LC 1639 "Number of Ways to Form a Target String Given a Dictionary" (exact reuse).
**Naming collision warning**: a *different* "String Formation" is separately reported for the Summer-2025 Infrastructure-Automation-Intern OA (1point3acres thread-1120493, 135 min, 2 DP + 1 backtracking: "Prime String, Work Schedule, String Formation" — page itself 403, detail only from WebSearch snippet, so treat that specific 2025 "String Formation" as a distinct, LOW-confidence, unconfirmed-statement problem, not necessarily LC 1639.

## 16. Course Schedule II (LC-exact)
**Confidence: MED** — item #14 of 2023 index, https://leetcode.com/problems/course-schedule-ii/ (exact reuse). Companion to the phone-screen topological-sort question in `coding_phone_onsite.md`.

## 17. Graph Valid Tree (LC-exact)
**Confidence: MED** — item #15 of 2023 index, https://leetcode.com/problems/graph-valid-tree/ (exact reuse, LC 261).

## 18. "String Patterns" (image post, distinct instance)
**Confidence: LOW** (unfetched) but corroborates cluster #2 — item #16 of 2023 index, https://leetcode.com/discuss/interview-question/2825744, posted 2022-11-17, image-only (2 screenshots, no OCR). Separately, FastPrep lists a fully-specified **"String Patterns"** OA problem (Medium, DP, last reported 2024-10, https://www.fastprep.io/problems/calculate-ways): "Given a word length and maximum consecutive vowels allowed, calculate how many unique words can be generated... no more than `maxVowels` consecutive vowels." `calculateWays(wordLen, maxVowels) -> int mod 1e9+7`; wordLen ≤ 2500. Examples: (1,1)→26, (4,1)→412776, (4,2)→451101. This is the same family as OA problems #2/#3 above (consecutive-vowel DP), strongly suggesting Snowflake has run vowel-run-length DP variants repeatedly from 2022 through 2024. Also named "String Patterns" as OA problem #1 in the 2026 recap (linkjob, LOW individually): "Dynamic programming problem counting valid words with vowel constraints using dp[i][j] states" — consistent with the FastPrep spec. **Combined confidence: MED** for the vowel-DP family as a whole, recurring 2022→2026.

## 19. Merge Intervals (LC-exact)
**Confidence: MED** — item #17 of 2023 index, https://leetcode.com/problems/merge-intervals/ (LC 56, exact reuse).

## 20. "Same Bit Pair"
**Confidence: LOW** (unfetched, image post) — item #18, https://leetcode.com/discuss/interview-question/2835233, posted 2022-11-19.

## 21. Minimum Interval to Include Each Query (LC-exact)
**Confidence: MED** — item #19 of 2023 index, https://leetcode.com/problems/minimum-interval-to-include-each-query/ (LC 1851, exact reuse).

## 22. Binary Tree Inorder Traversal (LC-exact)
**Confidence: MED (as OA)** — item #20 of the 2023 index (LC 94, exact). Independently confirmed HIGH as a **phone-screen** question with a Morris-traversal follow-up (2019, see `coding_phone_onsite.md` #2), so this problem clearly recurs across rounds, not just within OA.

## 23. Paint the Ceiling — generated side-lengths, binary-search pair counting
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-paint-the-ceiling (Medium, OA, last reported 2025-03 per FastPrep's list metadata, though the fetched detail page didn't restate the date). Statement: recurrence `s_i = ((k*s_{i-1}+b) mod m) + 1 + s_{i-1}` generates n side lengths (n up to 6e6); count pairs whose product (area) ≤ a. `paintTheCeiling(s0, n, k, b, m, a) -> long`. Example: s0=2,n=3,k=3,b=3,m=2,a=15 → sides [2,4,6] → 5 valid pairs.
Independently named as OA problem #2 of the 2026 recap (linkjob, LOW individually): "Paint the Ceiling – Sequence generation with rectangle area optimization using two-pointer technique" — same title and mechanic, different years (2025 vs. reported-as-2026), so this is a recurring OA problem. **Combined: MED.**

## 24. Task Scheduling / paid-free-server, reprised (2026 naming)
Same underlying problem as #1 — see there. Linkjob's 2026 recap lists it as OA problem #3 alongside Paint the Ceiling and String Patterns, i.e. Snowflake appears to run a rotating 3-problem OA where these three recur together across sittings.

## 25. Prime String
**Confidence: LOW** (page 403; detail only via WebSearch snippet)
Source: 1point3acres thread-1120493 ("Snowflake [Summer 2025] Infrastructure Automation Intern OA"), summarized: "Prime String, Work Schedule, and String Formation," 2 DP + 1 backtracking, 135 minutes. Full statements unavailable (unfetched: 403 Cloudflare).

## 26. Work Schedule
**Confidence: LOW** (same source/limitation as #25).

## 27. Generating Login Codes
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-generating-login-codes — "Generating Login Codes (Snowflake Online Assessment)", Medium, Array/Two-Pointers, tagged "New Grad OA", last reported 2026-09 (i.e. this month). Full statement not independently re-fetched beyond the listing; title + tags only.

## 28. Drawing Edge
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-drawing-edge, Easy, Graph/Combinatorics, OA, last reported 2026-06.

## 29. Minimum Clicks Between Wiki Pages
**Confidence: MED** — https://www.fastprep.io/problems/snowflake-minimum-clicks-between-wiki-pages, Easy, Graph/BFS, reported for **both** OA and Phone Screen tracks as of 2026-09 (FastPrep lists it in both pools) — i.e. the same wiki-graph-BFS problem is recycled between OA and phone screen, consistent with Snowflake's general pattern of OA↔phone-screen problem reuse noted in the format facts.

## 30. Horizontal Pod Autoscaler ("Find Pod Count")
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-find-pod-count, Medium, Array/Segment Tree, OA, last reported 2026-07. Infra-flavored naming (k8s HPA) fits Snowflake's platform-team OAs.

## 31. Efficient Deployments ("Get Maximum Sum")
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-get-maximum-sum, Hard, DP/Array, OA, last reported 2026-06.

## 32. Minimum Total Weight ("Find Min Weight")
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-find-min-weight, Medium, Heap/Greedy, OA, last reported 2025-03.

## 33. Unequal Elements ("Find Max Length")
**Confidence: LOW-MED** — https://www.fastprep.io/problems/find-max-length, Hard, DP/Array, OA, last reported 2025-03.

## 34. Minimum Index Distance Between Person and Cake
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-minimum-index-distance-between-person-and-cake, Easy, Array/Two-Pointers, OA, last reported 2026-05.

## 35. Simple Array Rotation Game
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-simple-array-rotation-game, Easy, Array/Math, OA, last reported 2026-04.

## 36. Max Element Indexes After Rotations
**Confidence: LOW** (unrated on FastPrep) — https://www.fastprep.io/problems/snowflake-max-element-indexes-after-rotations, OA, last reported 2026-03.

## 37. Grid Traversal ("Get Min Jumps")
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-get-min-jumps, Hard, BFS/Matrix, OA, last reported 2025-05.

## 38. Find the Maximum Length of a Good Subsequence I
**Confidence: LOW-MED** — https://www.fastprep.io/problems/snowflake-find-the-maximum-length-of-a-good-subsequence-i, Medium, DP/Hash Table, OA, last reported 2024-12. (Maps closely to LC 2911/2903 "good subsequence" family.)

## 39. Remove Stones to Minimize the Total
**Confidence: MED** — LC-exact (LC 1962), reported via FastPrep OA pool, Easy, Heap/Greedy, last reported 2024-12.

## 40. Solve Matrix Equations ("Find A")
**Confidence: LOW** — https://www.fastprep.io/problems/snowflake-find-a, Easy, Math/Simulation, OA, last reported 2024-10.

## 41. Minimum Height (tree re-rooting operations)
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-minimum-height (Medium, Tree/Binary-Search, OA, last reported 2026-07). Statement: rooted tree (root=1); each operation detaches a child subtree and reattaches it directly under the root; up to `max_operations` ops; minimize resulting tree height. `getMinimumHeight(tree_nodes, tree_from, tree_to, max_operations) -> int`. Example: 4 nodes, edges (3→2),(1→3),(2→4), 1 op → detach (2,4), reattach 4 under root 1 → height 2.
Part of the recurring "tree depth/height reduction" family also seen in phone-screen and onsite rounds — see `coding_phone_onsite.md` items on N-ary tree deletions.

## 42. Text Scoring / "super bit strings" variant
**Confidence: LOW** — https://www.linkjob.ai/interview-questions/snowflake-hackerrank-oa/ (2026 recap), described as "string matching... prefix and suffix scores." No corroboration found; flagged as possibly a generic/fabricated recap entry (see Format-facts note on inconsistent "3-question" claims across interviewfox vs. linkjob for ostensibly the same 2026 cycle).

## 43. String Transformation (suffix rotations, target string in k steps)
**Confidence: LOW** — same linkjob 2026 recap as #42, no corroboration.

## 44. Maximize OR-Sum (bit manipulation, doubling elements)
**Confidence: LOW** — https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/ (2026 recap), "given an array and integer k, maximize bitwise OR by doubling elements up to k times." No corroboration; resembles but does not exactly match LC 2680 "Maximum OR". Flag as possibly fabricated/paraphrased-from-LC.

## 45. Min-Height-Trees Graph Variant
**Confidence: LOW-MED** — same interviewfox 2026 recap, "find root(s) minimizing tree height in a connected graph... non-standard height definition." Matches the shape of LC 310 "Minimum Height Trees" plus a custom twist; fits the recurring tree-height family (see #41) so treated as LOW-MED rather than pure LOW.

## 46. Student Enrollment System (OOP class-design, appearing inside an OA)
**Confidence: LOW** — same interviewfox 2026 recap: "Implement Student base class and Result subclass with grade tracking, percentage calculation, pass/fail logic (33.33% threshold), and recheck functionality." Notable because it's a class-design question embedded in the OA rather than the phone/onsite loop — cross-referenced in `ood.md`. Single source, no corroboration.

---

## Summary of OA problem-family clusters (see TALLY.md for ref counts)
1. **Vowel-run-length DP** (#2, #3, #14, #18, "String Patterns") — 2022→2026, ≥4 independent sightings.
2. **Weighted/interval scheduling** (#1 Task Scheduling paid/free server, #4 Maximum Order Volume, #6 Non-Overlapping Intervals) — recurring "pick non-overlapping items to optimize a value" shape.
3. **Tree height/depth reduction** (#41 Minimum Height, plus phone/onsite N-ary tree deletion family in `coding_phone_onsite.md`) — recurring across OA, phone, and onsite.
4. **Exact-LC reuse cluster** (#9 Patching Array, #12, #14, #15, #16, #17, #19, #21, #22) — the 2023 Canada index shows Snowflake OA draws directly from unmodified LeetCode problems roughly as often as from custom ones.
5. A long tail of FastPrep-only "medium-confidence" problems (#27–#40) that could not be independently corroborated but come from a source that explicitly tags company/round/date rather than writing generic SEO copy.
