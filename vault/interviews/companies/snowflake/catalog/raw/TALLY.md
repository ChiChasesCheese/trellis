# Snowflake Coding-Question Tally — 2023–2026 sweep

Compiled 2026-09-13. One row per distinct problem/cluster (candidates cross-posting the same event
counted once; aggregator copies of the same underlying report counted once). "#refs" = number of
*independent* sources (different site/post, not different pages of the same recap) that report the
problem, per `coding_oa.md` / `coding_phone_onsite.md` / `ood.md`. Where a problem is really a
"base + follow-up" pair reported as two separate aggregator pages (e.g. the task-scheduler
duplicate-ID variant), they're listed as one row with the variant noted, since they are one
interview problem with a follow-up, not two independent sightings. File§ points to the section in
this directory with full detail. Sorted by #refs desc, then by most-recent "last seen" desc.

| Problem | Round(s) | #refs | First seen | Last seen | Confidence | File§ |
|---|---|---|---|---|---|---|
| Task Scheduling — paid vs. free server (0/1-knapsack scheduling) | OA | 3 | 2022-09-08 | 2026-03-16 | HIGH | coding_oa.md #1 |
| Vowel-run-length DP family (consecutive-vowel count / vowel-only substrings / "String Patterns") | OA | 4 | 2022-09-08 | 2026-06 | MED-HIGH | coding_oa.md #2,#3,#14,#18 |
| RBAC / DAG permission-inheritance family (Effective Access Control, Effective Role Privileges, ACL Local-Deny, Resolve Inherited Allow/Deny, Compute Effective Letter Permissions) | Phone Screen | 5 | 2026-05 | 2026-09 | MED-HIGH | coding_phone_onsite.md #8–12 |
| Tree-depth/height-reduction family (Minimum N-ary Tree Deletions / Prune Multiway Tree / Minimum Height re-rooting) | OA + Phone Screen | 3 | 2025-03 | 2026-08-29 | MED-HIGH | coding_oa.md #41; coding_phone_onsite.md #15–16 |
| Design an In-Memory File System (LC 588-style) | Phone Screen | 4 | (undated, recurring) | 2026-08-24 | HIGH-MED | ood.md #3; coding_phone_onsite.md #17 |
| Task Scheduler `addTask(id,priority,ts)` / `executeTask()` (± duplicate-ID follow-up) | Onsite | 2 | 2026-08 | 2026-08 | MED-HIGH | ood.md #1; coding_phone_onsite.md #22–23 |
| Closest Bathroom / Desk on a Grid (multi-source BFS) | Phone Screen | 2 | — | 2026-09 | MED-HIGH | coding_phone_onsite.md #4 |
| Recent Event Stream Queries / Query Unique & Most-Frequent Keys in a window | Phone Screen | 2 | 2026-08 | 2026-08-29 | MED | coding_phone_onsite.md #13 |
| Design Distributed Cron / Reliable Job Scheduler (`schedule/pause/resume`) | Technical Screen / System-Design-with-API | 2 | 2026-06-09 | 2026-06-17 | LOW-MED | ood.md #5; coding_phone_onsite.md #26 |
| Word Search II (LC 212) + Audit/Query-Event Log system design ("pg_stat for Snowflake") | Phone Screen (senior) | 1 (verbatim, 2-part) | 2024-02-14 | 2024-02-14 | HIGH | coding_phone_onsite.md #1; ood.md #6 |
| Array-diff removal + Binary Tree Inorder Traversal (Morris follow-up) + Patching Array | Phone Screen (2 rounds) | 1 (verbatim, 3-part) | 2019-11-09 | 2019-11-09 | HIGH | coding_phone_onsite.md #2 |
| Patching Array (LC 484) | OA + Phone Screen | 2 | 2019-11-09 | 2023-02-10 | HIGH | coding_oa.md #9; coding_phone_onsite.md #2 |
| Binary Tree Inorder Traversal (LC 94, ± Morris follow-up) | OA + Phone Screen | 2 | 2019-11-09 | 2023-02-10 | MED-HIGH | coding_oa.md #22; coding_phone_onsite.md #2 |
| Course Schedule II / prerequisite topological sort (LC 210) | OA + Phone/Code Screen | 2 | 2022-04-19 | 2023-02-10 | MED-HIGH | coding_oa.md #16; coding_phone_onsite.md #3 |
| Server Selection (grid/2D DP, target O(m·n)) | OA | 2 (image-only posts) | 2022-09-08 | 2023-02-10 | MED | coding_oa.md #5 |
| Maximum Order Volume / "phone calls" (weighted interval scheduling) | OA | 3 | 2021-01-25 | 2025-03 | MED | coding_oa.md #4 |
| Paint the Ceiling (generated side-lengths, binary-search pair count) | OA | 2 | 2025-03 | 2026-03-16 | MED | coding_oa.md #23 |
| Vowel Substring, LC-exact (LC 2062) | OA | 2 | 2023-02-10 | 2026-06 | MED | coding_oa.md #14 |
| Minimum Clicks Between Wiki Pages | OA + Phone Screen | 1 source, 2 pools | 2026-09 | 2026-09 | MED | coding_oa.md #29 |
| Web Crawler Shortest Path Reconstruction | Phone Screen | 2 | 2026-03-16 | 2026-09 | MED | coding_phone_onsite.md #5 |
| Transactional in-memory key–value store (nested tx + concurrency follow-up) | Technical Screen | 1 (+1 same-shape at a different company) | — | — | HIGH-MED | ood.md #2 |
| Rate limiter — sliding-window (onsite) + queued multi-rule (phone screen) | Onsite + Phone Screen | 2 | — | — | MED | ood.md #4; coding_phone_onsite.md #18,#24 |
| Parallel Courses III (LC 2050, unmodified) | Onsite | 1 | 2026-08 | 2026-08 | MED-HIGH | coding_phone_onsite.md #25 |
| Distributed Tree Counting State Machine (async message-passing aggregation) | Phone Screen | 1 | 2026-07 | 2026-07 | MED | ood.md #7; coding_phone_onsite.md #14 |
| Throne Inheritance without an initial king (LC 1600 variant) | Phone Screen | 1 | — | — | MED | ood.md #8 |
| LRU Cache (Snowflake warehouse-cache framing) | Onsite (SDE-II, claimed recurring) | 3 (thematic, undated) | — | — | LOW-MED | ood.md #9 |
| Merge Intervals (LC 56, unmodified) | OA | 1 | 2023-02-10 | 2023-02-10 | MED | coding_oa.md #19 |
| Minimum Interval to Include Each Query (LC 1851) | OA | 1 | 2023-02-10 | 2023-02-10 | MED | coding_oa.md #21 |
| Palindromic Subsequences (LC 2002) | OA | 1 | 2023-02-10 | 2023-02-10 | MED | coding_oa.md #12 |
| Graph Valid Tree (LC 261) | OA | 1 | 2023-02-10 | 2023-02-10 | MED | coding_oa.md #17 |
| String Formation via dictionary (LC 1639) | OA | 1 | 2023-02-10 | 2023-02-10 | MED | coding_oa.md #15 |
| Remove Stones to Minimize the Total (LC 1962) | OA | 1 | 2024-12 | 2024-12 | MED | coding_oa.md #39 |
| Character Frequencies (Across Strings / Nested Lists) | Phone Screen | 1 | 2026-06 | 2026-06 | MED | coding_phone_onsite.md #6 |
| Top Two Users by Total Purchase Amount | Phone Screen | 1 | 2026-06 | 2026-06 | MED | coding_phone_onsite.md #7 |
| Generating Login Codes | OA (New Grad) | 1 | 2026-09 | 2026-09 | MED | coding_oa.md #27 |
| Service Startup / Dependency Ordering (Kahn's algorithm) | Phone Screen | 1 | 2026-03-16 | 2026-03-16 | LOW-MED | coding_phone_onsite.md #20 |
| Min-Height-Trees Graph Variant (LC 310 + twist) | OA | 1 | 2026 | 2026 | LOW-MED | coding_oa.md #45 |
| Drawing Edge | OA | 1 | 2026-06 | 2026-06 | LOW-MED | coding_oa.md #28 |
| Horizontal Pod Autoscaler ("pod count") | OA | 1 | 2026-07 | 2026-07 | LOW-MED | coding_oa.md #30 |
| Efficient Deployments ("get maximum sum") | OA | 1 | 2026-06 | 2026-06 | LOW-MED | coding_oa.md #31 |
| Minimum Total Weight ("find min weight") | OA | 1 | 2025-03 | 2025-03 | LOW-MED | coding_oa.md #32 |
| Unequal Elements ("find max length") | OA | 1 | 2025-03 | 2025-03 | LOW-MED | coding_oa.md #33 |
| Minimum Index Distance: Person and Cake | OA | 1 | 2026-05 | 2026-05 | LOW-MED | coding_oa.md #34 |
| Simple Array Rotation Game | OA | 1 | 2026-04 | 2026-04 | LOW-MED | coding_oa.md #35 |
| Grid Traversal ("get min jumps") | OA | 1 | 2025-05 | 2025-05 | LOW-MED | coding_oa.md #37 |
| Find the Maximum Length of a Good Subsequence I | OA | 1 | 2024-12 | 2024-12 | LOW-MED | coding_oa.md #38 |
| Meeting-room scheduling (min rooms, LC 253 family) | Onsite (2026 intern VO) | 1 | 2026 | 2026 | LOW | coding_phone_onsite.md #27 |
| Parentheses Matching (stack) | Phone Screen | 1 | 2026-03-16 | 2026-03-16 | LOW | coding_phone_onsite.md #19 |
| Student Enrollment System (OOP base/subclass, in-OA) | OA | 1 | 2026 | 2026 | LOW | ood.md #10; coding_oa.md #46 |
| Maximize OR-Sum (bit manipulation, doubling) | OA | 1 | 2026 | 2026 | LOW | coding_oa.md #44 |
| Text Scoring / "super bit strings" variant | OA | 1 | 2026 | 2026 | LOW | coding_oa.md #42 |
| String Transformation (suffix rotations) | OA | 1 | 2026 | 2026 | LOW | coding_oa.md #43 |
| Non-Overlapping Intervals variant | OA | 1 | 2023-02-10 | 2023-02-10 | LOW | coding_oa.md #6 |
| Lexicographically Largest Array (MEX-based) | OA | 1 | 2023-02-10 | 2023-02-10 | LOW | coding_oa.md #8 |
| Minimize / Maximum Array Value | OA | 1 | 2023-02-10 | 2023-02-10 | LOW | coding_oa.md #10–11 |
| Largest Sub Grid | OA | 1 | 2023-02-10 | 2023-02-10 | LOW | coding_oa.md #13 |
| "Same Bit Pair" | OA | 1 | 2022-11-19 | 2022-11-19 | LOW | coding_oa.md #20 |
| Prime String / Work Schedule (Infra Intern OA) | OA (intern) | 1 | 2025 | 2025 | LOW | coding_oa.md #25–26 |
| Solve Matrix Equations ("find a") | OA | 1 | 2024-10 | 2024-10 | LOW | coding_oa.md #40 |
| Max Element Indexes After Rotations | OA | 1 | 2026-03 | 2026-03 | LOW | coding_oa.md #36 |
| Frontend React + "GFE" coding tasks (out of scope for backend GenSWE) | Phone Screen (frontend track) | 2 | 2026 | 2026-08-03 | LOW | coding_phone_onsite.md #28 |
| "Grid Land" / Kth Smallest Instructions — **flagged as mislabeled (actually a Lucid OA)** | OA (caution) | 1 | 2020-03-03 | 2023-02-10 | LOW / CAUTION | coding_oa.md #7 |

## Notes on methodology
- Rows with identical "First seen"/"Last seen" of 2023-02-10 mostly derive from the single 2023
  Canada-internship candidate's own index post
  (https://leetcode.com/discuss/interview-question/3169843/), which links to 20 separate
  screenshot-only sibling posts. Each linked title is counted as a real, distinct OA problem
  (the index-poster clearly saw them), but most of those 20 have **no independently recoverable
  problem statement** beyond the LC-exact ones (which link straight to a canonical LC problem
  page) — see `coding_oa.md` for which are "(unfetched: image-only post)".
- PracHub "Last Updated" timestamps cluster on a small number of days (2026-04-05, 04-12, 06-12,
  06-15, 06-17, 08-15, 08-23, 08-24, 08-29, 09-03) across many unrelated problems — this is almost
  certainly a site re-index/republish date, not an independent sighting date, so PracHub dates are
  used only as a recency floor, not as evidence of a specific report date.
- interviewfox.ai and linkjob.ai each published a "here are the 3 OA questions I got in 2026"
  recap, and the two recaps name **completely different** problem sets for what both claim is the
  current-cycle Snowflake OA. This is treated as a strong signal that at least one (possibly both)
  of these "first-hand" recaps is templated/SEO-generated rather than a real candidate report;
  individual problems from these two sites are therefore capped at LOW unless independently
  corroborated by FastPrep, PracHub, LeetCode Discuss, or 1point3acres.
- Total distinct problems/clusters catalogued: **59** (across `coding_oa.md`, `coding_phone_onsite.md`,
  and `ood.md`), within the requested 40–80 range without padding — every row above traces to at
  least one dated or explicitly Snowflake-tagged source; no generic "commonly asked at big tech"
  LeetCode list items were added merely to hit a count.
