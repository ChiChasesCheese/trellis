# Snowflake Phone-Screen / Onsite Coding — 2023–2026 sweep (with older HIGH-confidence anchors)

Compiled 2026-09-13. Same source/confidence methodology as `coding_oa.md`. Note: Snowflake's
English-language first-hand footprint for phone/onsite rounds is thin — the two best verbatim posts
are from 2019 and 2024, so several format facts below lean on those older HIGH sources plus more
recent MED aggregators (FastPrep, tagged by company+round+date) to describe the current (2025–2026)
loop shape.

## Format facts

- **Recruiter screen (25 min)** → **2 back-to-back technical phone screens (60 min each)** → **virtual
  onsite (4–5 rounds × 60 min)**. Confirmed structure, HIGH: 2019 post
  https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/
  (Data Platform team) and independently by 1point3acres search-snippet summary: "a recruiter
  screen, two back-to-back coding phone screens, then a virtual onsite that mixes coding, system
  design, and behavioral" (https://www.1point3acres.com/interview/problems/company/snowflake,
  page itself Cloudflare-403 but indexed snippet reachable via WebSearch, 2026).
- **Phone-screen time split ≈ 10 min intro / 40–50 min coding / 10 min candidate-Q&A**, confirmed
  verbatim (HIGH) in the 2019 post above ("10 mins General Introduction... 40 mins Coding... 10 mins
  Any questions"; second screen: "50 mins - Coding... 10 mins").
  A single senior-level phone screen instead pairs **1 LeetCode-style coding problem + a
  design/discussion segment** in one 60-min slot (HIGH, 2024-02-14,
  https://leetcode.com/discuss/interview-question/4727339/Snowflake-Senior-Software-Engineer-Phone-Screen/:
  "Coding: [Word Search II]... Design: Design an audit event/log system... I'm not sure if the
  interviewer was looking for two problems").
- **Difficulty is reported as inconsistent by design** — Blind: "coding wasn't LC style but
  something random" (Square employee, 2022-12-08,
  https://www.teamblind.com/post/snowflake-tech-screen-interview-hktkef7g) vs. "They gave me
  leetcode hard on the screens" (Amazon employee, 2022-10-15,
  https://www.teamblind.com/post/snowflake-coding-interview-difficulty-l8hbkbsq) vs. "got asked
  leetcode question with increasing difficulty and constraints. Started with LC medium" (Meta
  employee, 2022-10-14, same thread). A 2023 report: "generic computer science questions... For
  coding, it was implement existing Data structure" (LinkedIn employee, 2023-12-11,
  https://www.teamblind.com/post/what-kind-of-questions-snowflake-asks-in-initial-coding-and-system-design-round-p1qfuxwl).
- **"Medium + hard escalating within one problem" pattern**: confirmed HIGH in the 2019 post (Q2
  = LC "Binary Tree Inorder Traversal" with a **live follow-up** for O(1)-space Morris traversal:
  "He told me I would get a bonus point if I could do it in constant space").
- **Interviewer behaviour varies sharply**: silent/unhelpful ("talking to the system design
  interviewer was like talking to a wall... did not utter a single word", 2024 senior post above) vs.
  actively helpful with optimization follow-ups (2019 post: "interviewers were super nice and helped
  me when I got stuck... many follow ups on code optimization").
- **Senior/staff candidates get an added 30-min Tech Talk** (project presentation) round in the
  onsite loop (LOW-MED, https://www.tryexponent.com/guides/snowflake-software-engineer-interview
  and https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/, 2026-03-16).
- **OA problems are recycled into phone screens**: at least one problem (Minimum Clicks Between
  Wiki Pages) is independently tagged by FastPrep as appearing in *both* the OA and Phone Screen
  pools as of 2026-09 — see `coding_oa.md` #29.
- FastPrep's structured pool sizes as of 2026-09: **17 phone-screen-tagged** + **4 onsite-tagged**
  Snowflake coding problems (https://www.fastprep.io/snowflake-interview).

---

## 1. Word Search II (LC 212) + audit/event log design — senior phone screen
**Confidence: HIGH** (verbatim)
Source: https://leetcode.com/discuss/interview-question/4727339/Snowflake-Senior-Software-Engineer-Phone-Screen/, posted 2024-02-14, role: Senior Software Engineer, outcome: Reject.
- Coding: https://leetcode.com/problems/word-search-ii/description/ (LC 212), unmodified. Candidate solved it.
- Design half of the same 60-min slot: "Design an audit event/log system. The system should store queries made to snowflake system. User should be able to find columns, tables accessed in a time period. This system should also tell users what columns, tables have not been accessed in some time 't'. No constraint on storage. HA/reliable etc. *Think of this as a pg_stat in postgres*." (cross-referenced in `ood.md`.)

## 2. Array-difference removal + Binary Tree Inorder Traversal (Morris follow-up) + Patching Array
**Confidence: HIGH** (verbatim)
Source: https://leetcode.com/discuss/interview-question/424385/snowflake-phone-screen-patching-array/, posted 2019-11-09, team: Data Platform.
- Screen 1, Q1: "Remove all the elements of B which are present in A (A and B are arrays). Both arrays can consist of duplicates and are not sorted."
- Screen 1, Q2: LC 94 Binary Tree Inorder Traversal, with a live O(1)-space (Morris traversal) bonus follow-up.
- Screen 2, Q1: LC 484 "Patching Array", unmodified, "many follow ups on code optimization."
- Notably this candidate says the onsite that follows is "3 rounds including Coding, System Design, Lunch and Behavioral" (2019-era loop shape, thinner than the 2025–26 4–5-round virtual loop described above).

## 3. Course-prerequisite ordering (topological sort) — phone/code screen
**Confidence: HIGH** (verbatim)
Source: https://leetcode.com/discuss/interview-question/1965084/snowflake-software-engineer-phonecode-screen/, posted 2022-04-19, team: Data Application Foundations. Verbatim: "there [are] a total of n courses a student can take... p[i] = [a,b] indicates the student must take course b first... Return ordering of courses... If it is impossible to finish all courses return an empty array." Example given: n=5, p=[[0,1],[2,3],[0,2]] → [1,3,2,0,4] or [3,2,1,0,4]. Candidate could not finish; explicitly LC 210 "Course Schedule II" in disguise (also reused verbatim/unmodified in the OA index, see `coding_oa.md` #16).

## 4. Closest Bathroom / Desk on a Grid (multi-source BFS)
**Confidence: MED-HIGH** (corroborated across 2 independent structured sources)
Sources:
- https://www.1point3acres.com/interview/problems/94f2a5c6-db25-4269-9359-a47bcc61d8b8 (public-preview problem, company tag Snowflake): "Given a 2D grid with bathrooms ('B'), desks ('D')... determine the shortest Manhattan distance from each desk to its nearest bathroom using 4-directional movement... multi-source BFS." Constraints: 1≤m,n≤1000. Example: bathroom at (0,2), desks (1,1)/(2,3) → distances 2/3; no bathrooms → all -1.
- https://www.fastprep.io/problems/snowflake-closest-bathroom-desk-grid — "Closest Bathroom / Desk on a Grid (Snowflake Phone Screen)", tagged "High Frequency", tags BFS/grid/two-pointer/heap, ~60-min slot.
Also independently listed as a "High Frequency" featured problem on 1point3acres's own company-listing snippet.

## 5. Web Crawler Shortest Path Reconstruction
**Confidence: MED**
Sources: https://www.fastprep.io/problems/snowflake-web-crawler-shortest-path (Phone Screen, Graph/BFS, last reported 2026-09) and independently named "Web Crawler (BFS-based)" as a phone-screen coding example in https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ (2026-03-16, LOW individually) — combined MED. Statement (from title + tags): BFS over a crawled-page graph, then reconstruct the shortest path (not just distance) between two pages.

## 6. Character Frequencies Across Strings / Across Nested String Lists
**Confidence: MED** (structured source, easy/introductory phone-screen filler questions)
Sources: https://www.fastprep.io/problems/snowflake-character-frequency-across-strings and https://www.fastprep.io/problems/snowflake-character-frequency-across-nested-lists, both Easy, Array/Hash-Table, Phone Screen, last reported 2026-06. Likely a warm-up question before the main problem, consistent with the 2-question-per-screen format noted above.

## 7. Top Two Users by Total Purchase Amount
**Confidence: MED** — https://www.fastprep.io/problems/snowflake-top-two-users-by-total-purchase, Easy, Array/Hash-Table, Phone Screen, last reported 2026-06.

## 8. Effective Access Control (RBAC / DAG permission inheritance) — RBAC cluster, item 1
**Confidence: MED-HIGH** (5-way corroborated cluster; see also `ood.md` for the class-design framing)
Source: https://www.fastprep.io/problems/snowflake-effective-access-control, Medium, Phone Screen. Statement: "nodes inherit permissions from parent nodes in a DAG. Each node has local allow and deny lists, and inherits from all reachable ancestors. A permission is effective only when it appears in the combined allow set and does not appear in any deny set (deny overrides allow)." `getEffectiveAccess(allowLists, denyLists, edges) -> String[][]`. Nodes ≤500, edges ≤5000, permissions ≤2000.
This is one of a five-member RBAC/DAG-inheritance family recurring at Snowflake (makes domain sense: Snowflake's own product has RBAC roles and object-graph ACLs) — see items 9–11 below and `coding_oa.md`. Family confidence raised to MED-HIGH because the underlying "resolve inherited allow/deny over a DAG with deny-wins tie-break" mechanic repeats almost identically across FastPrep and PracHub, from different scrapers.

## 9. Effective Role Privileges (RBAC cluster, item 2)
**Confidence: MED-HIGH**
Source: https://www.fastprep.io/problems/snowflake-effective-role-privileges, Medium, Phone Screen, last reported 2026-05. "A role's effective privileges are all privileges from its ancestors plus its own direct privileges." `getEffectivePrivileges(privileges, grants) -> String[][]`, DAG, n≤2e5. Example: privileges=[["A"],["B"],["C"]], grants=[[0,1],[1,2]] → [["A"],["A","B"],["A","B","C"]]. Near-duplicate mechanic to item 8, just phrased as "roles/privileges" instead of "nodes/permissions" — almost certainly the same underlying interview problem reworded by two different scrape/paraphrase passes, OR two closely related real Snowflake questions (RBAC is core Snowflake domain knowledge, so both are plausible).

## 10. ACL Inheritance with Local-Only Deny Rules (RBAC cluster, item 3)
**Confidence: MED** — https://www.fastprep.io/problems/snowflake-acl-with-local-deny, Medium, Phone Screen, last reported 2026-09 (this month). Variant where deny rules apply only locally (not inherited), forcing a different DP/traversal than items 8–9.

## 11. Resolve Inherited Allow and Deny Permissions in a DAG (RBAC cluster, item 4)
**Confidence: MED**
Source: https://prachub.com/coding-questions/resolve-inherited-allow-and-deny-permissions-in-a-dag, Medium, Technical Screen, "Last Updated" 2026-08-29 (see caveat in `coding_oa.md` about PracHub dates being re-index dates, not sighting dates). Statement: "permissions flow from parents to children... 1) If the node or any ancestor is in the deny list, the final permission is denied. 2) Otherwise, if the node or any ancestor is in the allow list, allowed. 3) Otherwise denied by default." `resolveInheritedPermission(nodes, edges, allow, deny)`, nodes ≤200,000. Example: nodes=[root,teamA,teamB,service], edges chain root→teamA/teamB→service, allow=[root], deny=[teamB] → [true,true,false,false].

## 12. Compute Effective Letter Permissions in a DAG (RBAC cluster, item 5)
**Confidence: MED** — https://prachub.com/coding-questions/compute-effective-letter-permissions-in-a-dag, Medium, "Last Updated" 2026-09-03. Title-only corroboration of the same RBAC/DAG family; full body not independently re-fetched (would require a second PracHub call — treated as MED on family-consistency grounds alone).

## 13. Recent Event Stream Queries / "Query Unique and Most-Frequent Keys in a Recent Event Window"
**Confidence: MED** (2-source corroboration, same underlying spec)
Sources: https://www.fastprep.io/problems/snowflake-recent-event-stream-queries (Phone Screen, Medium, Hash-Table/Queue, last reported 2026-08): sliding window of `m` most-recent events; ops `record ts key`, `count ts` (distinct keys strictly before ts), `top` (most frequent key, lex tie-break). `processRecentEvents(operations, m) -> String[]`. Example: m=3, ops→["2","a","2","a"]. Independently listed on PracHub as "Query Unique and Most-Frequent Keys in a Recent Event Window" (Medium, Technical Screen, "Last Updated" 2026-08-29, https://prachub.com/coding-questions/query-unique-and-most-frequent-keys-in-a-recent-event-window) with matching description ("Process a timestamp-ordered event stream while retaining only its most recent m arrivals... most frequent qualifying key, lexicographic tie-breaking").

## 14. Distributed Tree Counting State Machine
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-distributed-tree-counting-state-machine, Medium, Phone Screen, last reported 2026-07. Statement: simulate a nonblocking count protocol over a rooted tree; root broadcasts `GET_COUNT` to children in increasing id order (FIFO, exactly-once delivery); leaves report 1; internal nodes wait for all children then report `1 + sum(children)`; root emits final total. `simulateTreeCount(parent[]) -> String[]` logging each `from->to:MESSAGE` plus a final `ROOT_COUNT:value`. Example: parent=[-1,0,0,1,1] → 9-line trace ending `ROOT_COUNT:5`. This is a genuine distributed-systems-flavored coding question (message ordering / async aggregation), fitting Snowflake's platform-engineering emphasis — cross-referenced in `ood.md` as a concurrency/simulation design problem.

## 15. Minimum N-ary Tree Depth Deletions — tree-height-reduction cluster, item 1 (phone screen)
**Confidence: MED-HIGH** (3-source family, spanning phone-screen and OA)
Source: https://www.fastprep.io/problems/snowflake-minimum-nary-tree-deletions, Medium, Phone Screen. "Given a rooted n-ary tree... via a parent array, find the minimum set of nodes to delete so the tree's maximum depth doesn't exceed k. Only non-root leaf nodes can be deleted... return node IDs in ascending order." `minimumDepthDeletions(parent[], k) -> int[]`. Examples: parent=[1,1,2,2,3,4],k=3 → [7]; parent=[1,2,3,4],k=2 → [3,4,5]. See `coding_oa.md` #41 (Minimum Height, the re-rooting variant of the same family) and item 16 below (Prune a Multiway Tree, the count-only variant).

## 16. Prune a Multiway Tree to a Maximum Depth — tree-height-reduction cluster, item 2
**Confidence: MED**
Source: https://prachub.com/coding-questions/prune-a-multiway-tree-to-a-maximum-depth, Medium, Technical Screen, "Last Updated" 2026-08-29. "Given a rooted multiway tree as a parent array, return the minimum explicit subtree deletions needed to keep every remaining node within a maximum depth while preserving the root." `minimumSubtreeDeletionsForDepth(parent, k) -> int`. Example: parent=[-1,0,0,1,1,3], k=2 → 1. Count-only sibling of item 15's ID-listing version — same underlying "cut subtrees to bound depth" idea reported by two different scrapers with different output requirements, consistent with genuinely being asked both ways across different candidates/cycles.

## 17. Design an In-Memory File System — phone-screen coding (see `ood.md` for full class-design writeup)
**Confidence: HIGH-MED**
Sources: https://www.fastprep.io/problems/snowflake-design-in-memory-file-system (Hard, Phone Screen, https://www.fastprep.io/snowflake-interview lists it under Phone Screen pool); GitHub https://raw.githubusercontent.com/harry-the-nerd/interview-notes-questions/main/snowflake/design-in-memory-file-system.md (sourced from darkinterview.com per repo README, states: "This is similar to LeetCode 588 - Design In-Memory File System... and is a common Snowflake interview question around data structures and API design"); also appears as a PracHub System-Design-tagged entry (https://prachub.com/interview-questions/design-an-in-memory-file-system, 2026-08-24) and is listed among "low-level design questions" on techprep.app (https://www.techprep.app/companies/snowflake). Four independent aggregator hits + a maps-to-LC-588 anchor = the strongest-corroborated design/coding-hybrid question in this sweep. Full spec in `ood.md`.

## 18. Simulate a Queued Multi-Rule Rate Limiter — phone screen
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-queued-multi-rule-rate-limiter, Medium, Phone Screen. "Implement a serialized, thread-safe rate limiter processing a finite FIFO request stream. Each request `[arrivalTime, successFlag]`... Rules `[limit, window]`, permitting at most `limit` successful executions in `(time-window, time]`... Failed handlers wait for capacity but consume no slots." `simulateRateLimiter(requests, rules) -> long[]`. Example: requests=[[0,1],[1,1],[2,1],[3,1],[4,1]], rules=[[2,5]] → [0,1,5,6,10].
Corroborated at the theme level by multiple generic mentions of "distributed rate limiter" design at Snowflake (tryexponent, algo.monster) — see `ood.md` for the onsite sliding-window variant (item 20 below) and full class-design treatment.

## 19. Parentheses Matching (stack)
**Confidence: LOW** — named as a phone-screen coding example ("Parentheses Matching (Stack approach)") in https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ (2026-03-16). No further detail, no corroboration; likely LC 20 "Valid Parentheses" or a stack-based variant.

## 20. Service Startup / Dependency Ordering (Kahn's algorithm)
**Confidence: LOW-MED** — same linkjob 2026-03-16 recap, phone-screen example: topological sort of service startup dependencies via Kahn's algorithm. Thematically consistent with the confirmed Course Schedule II reuse (item 3 above and `coding_oa.md` #16), so treated as LOW-MED rather than pure LOW.

## 21. Illustrative-only LC examples (do NOT treat as confirmed reports)
The following are repeatedly cited by prep-guide sites (algo.monster, techprep.app, tryexponent.com,
educative.io, staffengprep.com, interviewchamp.ai) as "the kind of difficulty" Snowflake asks, but
none of these sources claims a first-hand sighting with a date — **LOW, illustrative only**:
Merge k Sorted Lists, Maximum Profit in Job Scheduling, Design Hit Counter, Design LRU Cache
(though LRU Cache is separately given a full design write-up in `ood.md` because Snowflake's own
storage-caching domain makes it a very plausible recurring question, and it's the one item in this
list independently repeated by 3+ prep sites with the specific "warehouse micro-partition cache"
framing rather than generic LC boilerplate).

---

## Onsite rounds

## 22. Execute Tasks by Priority — task scheduler, onsite (see `ood.md` for full class API)
**Confidence: MED-HIGH**
Source: https://www.fastprep.io/problems/snowflake-priority-task-manager, Medium, **Full-time Onsite Interview**. "Implement a task manager that processes `add` and `execute` operations. When adding, store a task with its identifier, priority, and timestamp. When executing, remove and return the pending task with highest priority." Tie-break: higher priority → earliest timestamp → smallest id; empty queue → -1. `executeTasks(operations[], taskIds[], priorities[], timestamps[]) -> int[]`. Examples given (ids 101/102, priorities 2/5 → executes 102 then 101 then -1). Directly matches the brief's example `addTask(id, priority, ts)/executeTask()` task-scheduler OOD problem.

## 23. Priority Task Execution with Duplicate IDs — task scheduler, onsite variant
**Confidence: MED-HIGH**
Source: https://www.fastprep.io/problems/snowflake-priority-task-execution-duplicate-ids, Medium, Full-time Onsite Interview. Adds: duplicate task IDs allowed; "once any occurrence of an ID executes, all other occurrences (queued or future) become ineligible." `executeTasksWithDuplicateIds(operations[], taskIds[](string), priorities[], timestamps[]) -> String[]`, returns "" when nothing eligible. Constraints up to 200,000 ops. This and item 22 are almost certainly the two halves of one multi-part onsite problem (base version, then a "handle duplicate IDs" follow-up) rather than two independent sightings — see `ood.md` and `TALLY.md` for how they're counted.

## 24. Sliding-Window Rate Limiter — onsite
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-sliding-window-rate-limiter, Medium, Fulltime Onsite Interview. "Process request timestamps sequentially. Allow each request only when fewer than `limit` previously accepted requests fall within `(t-windowSeconds, t]`." `acceptRequests(requestTimes[], limit, windowSeconds) -> boolean[]`. Examples: [1,2,3,4,7], limit=3, window=5 → [T,T,T,F,T]. Companion to the phone-screen multi-rule/queued rate limiter (item 18) — Snowflake appears to ask a simpler single-rule version onsite and a harder multi-rule/queueing version at phone screen, or vice versa depending on cycle.

## 25. Parallel Courses III (LC 2050) — onsite
**Confidence: MED-HIGH** (unmodified LC-numbered problem, explicit onsite tag)
Source: https://www.fastprep.io/problems/snowflake-parallel-courses-iii, Hard, Snowflake Fulltime Onsite Interview, Graph. Statement and examples match LC 2050 exactly (n courses, prerequisite pairs, per-course duration, minimize months to finish all courses via critical-path DP over a DAG). Example: n=5, relations=[[1,5],[2,5],[3,5],[3,4],[4,5]], time=[1,2,3,4,5] → 12.

## 26. Design a Reliable/Distributed Job Scheduler — onsite/VO system-design-with-coding-elements
**Confidence: LOW-MED**
Sources: https://prachub.com/interview-questions/design-a-reliable-job-scheduler-2 (Hard, "Last Updated" 2026-06-09) and https://prachub.com/interview-questions/design-a-cron-job-scheduler (Medium, Technical Screen, "Last Updated" 2026-06-17). Statement: "Design a distributed cron job scheduler that triggers user-defined jobs on recurring schedules... support cron-style expressions (e.g. `0 */6 * * *`), along with `pause(job_id)` and `resume(job_id)`... (a) Public API (b) Data model (c) Core scheduler loop (d) pause/resume race conditions (e) multi-instance safety without double-firing (f) crash recovery." Scale: ~1e6 job definitions, tens of thousands due in the busiest minute, minute-granularity cron, at-least-once delivery, HA across replicas. This is system-design-flavored but has a concrete class/API surface (`schedule`, `pause`, `resume`) that overlaps the brief's "cron scheduler" OOD ask — cross-referenced in `ood.md`. Two PracHub pages with matching content but "Last Updated" dates 8 days apart (both within the suspicious re-index cluster noted in `coding_oa.md`), so treated as one problem, LOW-MED given single-aggregator sourcing.

## 27. Meeting-room scheduling (min rooms for overlapping requests) — 2026 intern VO
**Confidence: LOW** (page login-gated; only a one-line snippet recovered)
Source: https://www.1point3acres.com/interview/post/7546739, "Snowflake 2026 Software Engineer Intern VO Interview Experience" — WebFetch summary recovered: "a meeting room scheduling problem to find the minimum rooms required for overlapping requests" as the "Technical interview for Snowflake 2026 internship." Full body behind login (unfetched: login wall). Maps to: LC 253 "Meeting Rooms II" family.

## 28. Frontend/fullstack track: React + "GFE" coding tasks
**Confidence: LOW** (login-gated snippets only)
Sources: https://www.1point3acres.com/interview/thread/1170738 ("Snowflake Fulltime Software Engineer Frontend Tech Phone Screen... React questions and GFE coding tasks", unfetched beyond snippet) and https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/'s mention of "Build an Arrow-Controlled Kanban Board in React" (PracHub, 2026-08-03) — out of scope for a backend GenSWE kit but flagged in case the frontend/fullstack track is relevant to leveling context.
