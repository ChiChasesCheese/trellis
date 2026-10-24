# GitHub survey — TikTok / ByteDance interviews (English half)

Collected 2026-10-24 with `gh api search/repositories`, `search/code` and `git clone --depth 1` (clones in `/tmp/tiktok_research_en/gh/`, not kept).
Queries run: "tiktok interview", "tiktok interview questions", "bytedance interview", "字节 面经", "字节跳动 面经", "tiktok oa", "tiktok system design interview",
"company wise leetcode questions", "tiktok leetcode", "bytedance leetcode"; code search: "tiktok phone screen interview", "tiktok system design interview",
"字节跳动 面经 后端", "tiktok interview experience", "bytedance onsite interview" (the "tiktok onsite backend interview" code query returned HTTP 503).
Result: the old 2019-2023 Chinese 面经 repos (aylei/interview, rhwayfun/interview, resumejob/interview-questions, 0voice/*) are stale and campus-oriented; ignore for the 2025-10 to 2026-10 window.
Four sources are worth keeping; all others are listed at the bottom with the reason they were dropped.

Confidence labels: high = first-hand post with the problem text; medium = summary that names the problem; low = fragment, SEO, or derived list.

---

## 1. kevin-2023-code/Tech-Interview-Questions and Tech-OA-Questions  (TrueInterview mirror) — best GitHub source

- URLs: https://github.com/kevin-2023-code/Tech-Interview-Questions (commit ae8c9b0, 2026-10-24) and https://github.com/kevin-2023-code/Tech-OA-Questions (commit 2026-10-24).
- What it is: a CC BY 4.0 hourly sync of the TrueInterview (trueinterview.io) catalog. The ByteDance page counts **345 questions** (OA 37 / phone 249 / onsite 94), 204 carrying a sighting date, most recent 2026-10-05, **44 sightings in the last 90 days**. TikTok questions are filed under "ByteDance".
- Files used:
  - `companies/bytedance.md` (statistics + every question with round, level tags, date)
  - `companies/bytedance/interview-process.md`, `interview-process-software-engineer.md`, `interview-process-infrastructure-engineer.md` (process guides, "based on 111 / 92 candidate-reported experiences, mostly 2025 Q4 to 2026 Q3")
  - `data/questions.jsonl` (machine-readable: title, format, difficulty, rounds, topics, `reported` date) — filtered list saved in my scratch as `ti_bytedance_list.txt`.
- Confidence: **medium**. It is an aggregator, so individual reports are not independently checkable; the free question pages mirror the text, the paid ones show only a title. The "Level" tags (New grad / Mid / Senior / Staff+) are the aggregator's own and several questions carry 3 tags at once, so they are weak evidence of the level of one loop. Process claims in the guide are synthesis across reports, not one report.
- Process facts it gives (all under "ByteDance Software Engineer", 92 reports):
  - Gates: rounds booked one at a time; each is pass/fail; the recruiter's label for the next round is often wrong (a "system design" round turned out to be pure coding or fundamentals).
  - 2 to 4 sequential video calls of 45-60 min, then a hiring-manager (HM) round; no single onsite day; reported span ~2 weeks to several weeks, silences common; decisions same day to ~8 business days.
  - Almost every technical hour opens with a **resume drill of 10-45 min**, then 1-2 problems in a shared editor, "usually the Lark codepad"; many interviewers want code that compiles and passes **tests you write**; some forbid moving the cursor outside the pad.
  - Backend fundamentals hour (oral): composite/covering indexes, CAP, locking, cache breakdown/avalanche, cache-aside consistency, Kafka partitions/rebalancing, Redis persistence, WebSocket vs SSE, Java LinkedHashMap vs ConcurrentHashMap; one candidate had 50 min of questions and 10 min to reverse a linked list.
  - Design rounds: "mid-level and senior loops include one or two design hours of ~60 min; senior screens have squeezed design into 15 minutes of a mixed hour".
  - HM round: project defense + behavioral + often a coding problem; "frequently held in Mandarin"; at senior bands "the defense turns adversarial".
  - Level: assessed mostly from the resume drill and design rounds, then matched to headcount ("passed all rounds at 2-1, told only 2-2 headcount remained"); rematching to another team restarts part of the loop.
  - Table of levels and approximate US TC from the guide: 1-2 ~$195K, 2-1 ~$275K, 2-2 ~$450K, 3-1 ~$620K (aggregator estimate, medium-low).
  - Application cap for new-grad postings: 2 positions across TikTok and affiliates; feedback shared across loops.
  - 2026 joint-venture note in the guide: "Since January 2026, TikTok's US operations sit in a joint venture majority-owned by American investors, with ByteDance retaining 19.9%" (consistent with Blind posts about "USDS JV").
- Per-question list with dates: see `coding.md` and `system_design.md` (which cite this file as source T1). The full filtered list (all sightings 2025-10 onward) is in the section "TrueInterview filtered list" at the end of `forums_en.md`.

## 2. ombharatiya/FAANG-Coding-Interview-Questions

- URL: https://github.com/ombharatiya/FAANG-Coding-Interview-Questions (commit 8d5d120, 2026-10-09), files `README.md` §ByteDance/TikTok and `FAANG-Recent-Questions.md` §ByteDance/TikTok.
- Gives: 41 LeetCode problems tagged ByteDance/TikTok (Easy/Medium/Hard), 14 "custom" problems, 10 system-design prompts, and a trends paragraph. Claims: "2-3 problems per round", "interviewers write their own problems and progressively mutate them", OA moved from HackerRank to **CodeSignal**, MCQ removed, **4 coding problems in 70-90 minutes** (down from ~120 in 2025), proctored (camera, screen share), "AI tools explicitly banned", HM round can contain an LC-Hard DP "under a strict clock" (one candidate: "two LeetCode hard DP questions in one hour").
- System design list it reports (dates in the file): For You page (two-phase candidate generation + ranking); real-time live streaming at billion scale; content moderation pipeline; social graph service; ad serving platform / RTB; **near-real-time top-ten songs by country** (Aug 2026); **asynchronous video moderation pipeline: ML risk scores feeding a rules engine, async review queue** (Sep 2026); **cache stampede on a hot key** (request coalescing, locks, early refresh, jittered TTLs; Aug 2026); **payment system, time-boxed HLD: checkout, charge, confirmation, idempotency and failure handling** (Sep 2026); **monitoring dashboard with explicit latency goals** (Sep 2026).
- Custom problems: GPU resource management (job queue, scheduler, monitor, fairness, bin-packing); Server Investment; Round Robin Load Balancer (new 2026 OA); removable timestamp-ordered task scheduler (Aug 2026); lexicographically smallest course order via min-heap topological sort (Sep 2026); video chunk scheduler; hashtag trend detector; comment tree flattening; content moderation priority queue; video dedup via hashing; live viewer count at billion scale.
- Confidence: **low-medium**. No per-report source, no URLs; it matches TrueInterview closely (many identical items and the same Aug-Sep 2026 items), so treat it as a derivative of the same data, not an independent confirmation.

## 3. liquidslr/leetcode-company-wise-problems (LeetCode-premium tag lists as CSV)

- URL: https://github.com/liquidslr/leetcode-company-wise-problems (commit 2b71796, 2026-10-20), folders `TikTok/` and `ByteDance/`, five windows each: Thirty Days, Three Months, Six Months, More Than Six Months, All.
- TikTok rows: 4 (30 days), 18 (3 months), 36 (6 months), 276 (more than 6 months), 317 (all). ByteDance: 0 / 1 / 3 / 49 / 59 — ByteDance tag is effectively dead since TikTok replaced it.
- Top TikTok, 30 days: LRU Cache (100), Cheapest Flights Within K Stops (82), Making A Large Island (82), All Nodes Distance K in Binary Tree (82).
- Top TikTok, 3 months: Number of Islands (100), LRU Cache (100), Making A Large Island (95), Meeting Rooms II (95), Block Placement Queries (88.9), Spiral Matrix / Two Sum / Decode String / Merge Intervals (80.9), then (69.8) Number of Distinct Islands, Find Median from Data Stream, Longest Substring with At Most K Distinct Characters, Rotate Array, Single-Threaded CPU, Basic Calculator II, Remove Duplicate Letters, Cheapest Flights Within K Stops, All Nodes Distance K in Binary Tree.
- Top TikTok, 6 months: LRU Cache (100), Number of Islands (94.7), Meeting Rooms II (78.4), Decode String / All O`one Data Structure / Making A Large Island (74.1), Merge Intervals / Course Schedule / Cheapest Flights / Number of Distinct Islands / Reverse Nodes in k-Group / Block Placement Queries (68.9), Spiral Matrix / Find First and Last Position / Path Sum III / Find Median from Data Stream / Two Sum (62.1); at 52.7: Longest Mountain, Rotate Array, Possible Bipartition, Serialize and Deserialize N-ary Tree, Gas Station, Count Number of Nice Subarrays, Partition Array for Maximum Sum, Subarray Sums Divisible by K, Search in Rotated Sorted Array, Longest Substring with At Most K Distinct, Reverse Linked List, Single-Threaded CPU, Basic Calculator II, Binary Tree Right Side View, Minimum Size Subarray Sum, Binary Tree Maximum Path Sum, Remove Duplicate Letters, Intersection of Two Linked Lists, All Nodes Distance K in Binary Tree.
- Top TikTok, all time: LRU Cache (100), Number of Islands (95.9), Meeting Rooms II (85.7), Longest Increasing Subsequence (85.7), Number of Distinct Islands (85), Longest Substring Without Repeating Characters (84.3), Course Schedule (82.7), Merge Intervals (81.9), Text Justification (81), Trapping Rain Water (79.1), N-Queens (74.9), Making A Large Island (74.9), Search in Rotated Sorted Array / Spiral Matrix / Minimum Window Substring / Decode String (72.5), Course Schedule II / Subarray Sum Equals K (71.1).
- Confidence: **medium** for "what LeetCode users tagged", **low** as evidence of what is asked at senior backend loops (the tag is crowd-sourced and skews to new-grad OAs; the frequency is a relative score, not a count).

## 4. atomeocean/job-compass (Chinese mirror of 1point3acres interview metadata)

- URL: https://github.com/atomeocean/job-compass, `docs/assets/json/interview-experience/{tiktok,bytedance}/` (4 ByteDance and 6 TikTok JSON files).
- Gives only metadata (level, date, result, round types), no problem text. Nearest to our target: `bytedance/v2na3e.json`, a 2026-05 *site reliability engineer*, level "senior", HR reached out on LinkedIn, two virtual-onsite rounds rated 4 and 2, rejected; source link https://www.1point3acres.com/bbs/thread-1177932-1-1.html. Others are new-grad/intern.
- Confidence: **low** (no content).

## Checked and dropped

| Repo | Why dropped |
|---|---|
| lmiztbrv/tiktok-interview-patterns | single-README SEO blog ("the patterns that actually show up ... 5-week prep plan"), no sources; it summarizes recurring problems and says "several 2026 candidate write-ups contradict each other"; low. Its claims (CodeSignal/HackerRank OA with 3-4 problems in 70-120 min; 2-3 technical rounds of 45-60 min; project deep dive; light system design: TinyURL, rate limiter, notification fan-out) agree with other sources but add nothing independent. |
| AlexiosNine/tiktok-algorithm-prep | derivative study site (24 problems, Go examples); its `sources.json` only points to older LeetCode Discuss/Reddit posts (2021-2025 Singapore, Android/iOS, SRE) which I checked directly. |
| wearzdk/interview-experience | Chinese 牛客/脉麦 scraper site (3,592 files), campus-heavy; belongs to the Chinese-platform half. |
| resumejob/interview-questions, 0voice/*, aylei/interview, rhwayfun/interview, lwlpyl/ByteDance, chenfan0/bytedance | 2019-2023 Chinese 面经, outside the window. |
| snehasishroy/leetcode-companywise-interview-questions, krishnadey30/LeetCode-Questions-CompanyWise, hxu296/*, MysteryVaibhav/* | same data family as (3) or older. |
| ayush-that/codejeet | blog-style company pages; `bytedance-medium-interview-questions-guide.md` is SEO. |
| kx-Huang/LeetCode-TikTok, zhs1397/leetcode, nandinijariwala/Tiktok-LeetCode-Q-A | personal solution repos with no interview-process content. |
