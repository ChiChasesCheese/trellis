# Snowflake OOD / Class-Design / Concurrency — 2023–2026 sweep

Compiled 2026-09-13. These are coding questions whose deliverable is a **class with a stateful
API** (multiple methods sharing internal state across calls) rather than a single pure function —
the shape the brief calls out: task scheduler `addTask/executeTask`, deque→queue service,
transactional in-memory KV store, rate limiter, cron scheduler, LRU/TTL caches. Sourcing and
confidence key are identical to `coding_oa.md`; several entries here are cross-referenced from
`coding_phone_onsite.md` with the full class spec expanded.

## Format facts specific to OOD/design rounds

- Design questions at Snowflake skew toward **Snowflake's own product surface**: RBAC/role
  inheritance (Snowflake has first-class ROLE objects and grants), an audit/query-log system
  ("*Think of this as pg_stat in postgres*" — direct quote from a Snowflake interviewer, see item 6),
  a distributed cron/task scheduler (Snowflake TASK objects run on cron schedules — see
  https://docs.snowflake.com/en/user-guide/tasks-intro, which the interview questions plainly
  mirror), and warehouse-cache eviction (LRU, because "frequently-accessed micro-partitions stay
  hot in SSD; cold ones get evicted by exactly this policy" — paraphrased framing repeated across
  multiple prep sites, LOW individually but thematically load-bearing).
- Concurrency is an explicit, named axis: "implement thread-safe data structures such as a
  concurrent LRU cache or a key-value store with transactional semantics, requiring understanding
  of locking, race conditions, and concurrent data access patterns" (LOW-MED, generic prep-guide
  framing, but corroborated by the KV-store problem's own explicit "Follow-up 2: Concurrency"
  section, item 2 below, which is a real problem-bank entry, not a generic guide claim).
- At least one design question has been observed **embedded inside a timed OA** rather than a
  live round — see item 7 (Student Enrollment System, OOP) — suggesting Snowflake doesn't
  strictly separate "OOD" into its own round; it can show up anywhere.

---

## 1. Task Scheduler — `addTask(id, priority, ts)` / `executeTask()` (matches brief's example exactly)
**Confidence: MED-HIGH**
Sources: https://www.fastprep.io/problems/snowflake-priority-task-manager and
https://www.fastprep.io/problems/snowflake-priority-task-execution-duplicate-ids, both tagged
**Snowflake, Full-time Onsite Interview, Medium** (full statements reproduced in
`coding_phone_onsite.md` #22–23). Also matched by an earlier WebSearch synthesis describing "a
priority-based task scheduler interview problem asked at Snowflake... `addTask(taskId, priority,
timestamp)`... `executeTask()` choosing by priority while skipping IDs that already executed" —
i.e. the search engine's own summary of these two FastPrep pages independently reconstructs the
exact API shape named in this dossier's brief.

**Class API (base version, item 22):**
```
class TaskManager:
    def add(self, task_id: int, priority: int, timestamp: int) -> None: ...
    def execute(self) -> int:  # returns task_id of highest-priority pending task, or -1 if empty
        ...
```
Tie-break order: higher priority wins; ties broken by earlier timestamp; further ties by smaller
task_id. Constraints: ≤1e5 operations, unique positive task ids.

**Follow-up (duplicate-ID variant, item 23):**
```
class TaskManager:
    def add(self, task_id: str, priority: int, timestamp: int) -> None: ...
    def execute(self) -> str:  # "" if nothing eligible
        ...
```
Rule change: task_id is now a string and **may repeat**; once *any* occurrence of an id has been
executed, all other queued/future occurrences of that same id become permanently ineligible (a
"completion suppresses duplicates" semantic, not a plain priority queue). Up to 200,000 ops.

**Design-round framing**: a natural interviewer follow-up sequence is (a) plain priority queue with
tie-breaks, (b) add duplicate-ID suppression, (c) concurrency — make `add`/`execute` safe under
concurrent callers, (d) persistence/crash-recovery (this last step overlaps with item 5, the cron
scheduler, in spirit).

## 2. Transactional in-memory key–value store (nested transactions + concurrency)
**Confidence: HIGH-MED**
Source: https://prachub.com/coding-questions/design-transactional-in-memory-key-value-store,
Hard, Technical Screen, company explicitly tagged Snowflake.
**Caveat**: a same-shaped "Transactional Key-Value Store" problem also exists in 1point3acres's
generic problem bank tagged to a *different* company (xAI) at
https://www.1point3acres.com/interview/problems/post/7100152 (login-gated, only step outline
visible: "Step 1: Simple Transactions, Step 2: Nested Transactions, Step 3: Real-World Issues") —
this is a common enough interview archetype that it plausibly recurs across multiple companies
independently; it does not invalidate the Snowflake-tagged PracHub report, but don't assume
uniqueness to Snowflake when building a problem set.

**Class API:**
```
class TransactionalKVStore:
    def get(self, key: str) -> int | None: ...
    def put(self, key: str, value: int) -> None: ...
    def delete(self, key: str) -> None: ...
    def begin(self) -> None: ...       # start a new (possibly nested) transaction scope
    def commit(self) -> bool: ...      # False if no active transaction
    def rollback(self) -> bool: ...    # False if no active transaction
```
Semantics: writes inside a transaction are immediately visible to later ops in the *same*
transaction; `rollback()` undoes only changes since the matching `begin()`; nested `commit()`
merges into the parent scope (only the outermost commit touches global state).
Constraints: ≤200,000 ops, nesting depth ≤ op count, keys 1–100 chars, values are ints.
Example: `[put(a,1), begin, put(a,2), get(a), begin, delete(a), get(a), rollback, get(a), commit,
get(a)]` → `[2, None, True, 2, True, 2]`.

**Follow-up 2 (concurrency, explicit in the source)**: "Extend to multi-threaded access with
linearizable semantics. Threads have independent transaction stacks; each thread sees only its own
uncommitted changes until the outermost transaction commits." Recommended approach per source:
one shared dict + per-thread stack of undo-logs; first-touch snapshotting per key so rollback only
undoes that transaction's own changes; reads scan the calling thread's stack newest-first before
falling back to the global store.

## 3. Design an In-Memory File System
**Confidence: HIGH-MED** (see `coding_phone_onsite.md` #17 for the 4-source corroboration chain:
FastPrep phone-screen tag, GitHub/darkinterview.com note explicitly calling it "a common Snowflake
interview question," PracHub, techprep.app)
**Class API** (FastPrep phrasing, functionally identical to LC 588):
```
class FileSystem:
    def ls(self, path: str) -> list[str]: ...                       # sorted; [name] if path is a file
    def mkdir(self, path: str) -> None: ...                          # create missing dirs recursively
    def addContentToFile(self, filePath: str, content: str) -> None: # create-or-append
    def readContentFromFile(self, filePath: str) -> str: ...
```
Constraints (GitHub spec): paths 1–100 chars, absolute, start with `/`; content 1–50 chars; ≤300
calls total. (FastPrep's phone-screen version scales this up: ops ≤2000, path components 1–30
lowercase letters, content ≤1000 chars, total operation-string length ≤200,000 — i.e. the same
question is asked at toy scale (GitHub/darkinterview trainer version) and at larger scale
(FastPrep's captured phone-screen version), consistent with real interviewers adjusting
constraints per candidate.)
Reference solution shape (from GitHub, Python): a trie/tree of `Node{children: dict, is_file: bool,
content: str}`; path traversal creates-on-demand for `mkdir`/`addContentToFile`, read-only
traversal (raise/error on missing path) for `ls`/`readContentFromFile`.
**Common interviewer follow-ups** (from the GitHub writeup, presented as the standard next
questions): add `rm`/`rmdir`; support very large files via chunked content storage; make it
thread-safe (per-node locks or reader-writer locks); make it durable (snapshot + write-ahead log).

## 4. Rate limiter — two variants (sliding-window single-rule onsite; queued multi-rule phone screen)
**Confidence: MED** (see `coding_phone_onsite.md` #18 and #24 for source detail)
**Variant A — stateless-ish sliding window (onsite)**:
```
def acceptRequests(requestTimes: list[int], limit: int, windowSeconds: int) -> list[bool]: ...
```
Half-open window `(t - windowSeconds, t]`; nondecreasing timestamps; ties process in input order;
rejected requests never occupy a slot. This can be implemented as a pure function replaying a
deque-based window, but is presented as "onsite" difficulty because interviewers push toward the
**class-based / streaming version**: `class RateLimiter: def allow(self, t: int) -> bool`, backed
by a deque of accepted timestamps, O(1) amortized per call — i.e. a live design exercise even
though the recorded problem statement is function-shaped.

**Variant B — queued, multi-rule, thread-safe (phone screen)**:
```
def simulateRateLimiter(requests: list[list[int]], rules: list[list[int]]) -> list[int]: ...
```
"Implement a **serialized, thread-safe** rate limiter processing a finite FIFO request stream...
Rules `[limit, window]` permit at most `limit` successful executions in `(time-window, time]`...
Handlers execute atomically in FIFO order. Failed handlers wait for capacity but consume no slots."
Up to 10 simultaneous rules must all be satisfied — this is functionally a **multi-window
token-bucket/sliding-window-log class** with an explicit concurrency/atomicity requirement, closer
to the brief's "rate limiter" OOD ask than Variant A. A natural class refactor:
```
class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int,int]]): ...
    def try_acquire(self, arrival_time: int) -> int:  # returns actual start time
        ...
```
with each rule maintaining its own deque of granted timestamps, and `try_acquire` needing to find
the earliest time at which *all* rules simultaneously have capacity — the interesting part of the
problem (example: requests all at t=0..4 with rule `[2,5]` → actual start times
`[0,1,5,6,10]`).
Generic corroboration that "distributed rate limiter" is a named Snowflake design topic: LOW-MED,
https://www.tryexponent.com/guides/snowflake-software-engineer-interview and algo.monster's guide.

## 5. Cron / distributed job scheduler — `schedule`, `pause(job_id)`, `resume(job_id)`
**Confidence: LOW-MED** (single aggregator, PracHub, but domain-anchored: Snowflake's own product
has a native TASK/cron scheduling primitive, https://docs.snowflake.com/en/user-guide/tasks-intro
and https://docs.snowflake.com/en/sql-reference/sql/create-task, which independently confirms this
is exactly the kind of system Snowflake engineers build and would plausibly interview on)
Source: https://prachub.com/interview-questions/design-a-cron-job-scheduler, Medium, Technical
Screen. Required design surface, quoted: "(a) Public API (b) Data model (c) Core scheduler loop for
finding and firing due jobs (d) Correct pause/resume semantics, including race conditions (e)
Multi-instance safety without double-firing (f) Crash recovery and reliability with no lost
triggers." Scale: ~1e6 job definitions, tens of thousands due in the busiest minute, minute-level
cron granularity, at-least-once delivery (jobs not assumed idempotent), multi-replica HA. A
skeleton API implied by the prompt:
```
class CronScheduler:
    def schedule(self, job_id: str, cron_expr: str, payload) -> None: ...
    def pause(self, job_id: str) -> None: ...
    def resume(self, job_id: str) -> None: ...
    def tick(self, now: int) -> list[str]:  # jobs due to fire, claimed exactly-once-ish
        ...
```
Evaluation focus per source: "clean layering (API → metadata store → scheduler → durable queue →
workers), concurrency tokens for safe claiming, idempotency keys for run dedup, multi-replica
coordination, explicit pause-vs-claim race handling" — i.e. the "OOD" part is really the claim/lease
API design (a single method whose correctness under concurrent schedulers is the whole point),
which is the same shape as a distributed-lock or leader-election mini-problem.

## 6. Audit / query-event log system ("think of this as pg_stat in postgres")
**Confidence: HIGH** (verbatim, paired with LC 212 in a real senior phone screen — see
`coding_phone_onsite.md` #1)
Source: https://leetcode.com/discuss/interview-question/4727339/, 2024-02-14. Verbatim requirements:
"The system should store queries made to snowflake system. User should be able to find columns,
tables accessed in a time period. This system should also tell users what columns, tables have not
been accessed in some time 't'. No constraint on storage. HA/reliable etc." This is presented as a
system-design prompt but has a clean, small, class-shaped core suitable for a live-coded skeleton:
```
class QueryAuditLog:
    def record_access(self, query_id: str, ts: int, tables: set[str], columns: set[str]) -> None: ...
    def accessed_in_range(self, table_or_column: str, t_start: int, t_end: int) -> list[str]: ...
    def unaccessed_since(self, t: int) -> set[str]:  # tables/columns with no access since t
        ...
```
Candidate's own account: "I proposed a design... asked about constraints, use case etc." but the
interviewer gave essentially no signal back ("did not utter a single word") — a reminder that this
prompt is deliberately open-ended and evaluated on the candidate's own structuring, not a fixed
expected API.

## 7. Distributed Tree Counting State Machine (message-passing / async aggregation)
**Confidence: MED** (see `coding_phone_onsite.md` #14 for full source)
Although delivered as a function `simulateTreeCount(parent) -> list[str]`, the natural class
refactor is a small actor/state-machine per node:
```
class TreeNode:
    def on_get_count(self, from_id: int) -> None: ...     # forward GET_COUNT to children, or reply 1 if leaf
    def on_report_count(self, from_id: int, value: int) -> None: ...  # aggregate; reply upward when all children in
```
with a FIFO message bus delivering `from->to:MESSAGE` exactly once, and the root printing
`ROOT_COUNT:value` on completion. This is effectively a miniature **distributed aggregation
protocol** (think: a toy version of a Snowflake metadata-service fan-out/fan-in count), which is
why it's grouped with the concurrency-flavored OOD problems rather than plain tree algorithms.

## 8. Throne Inheritance without an initial king (class-design, stateful genealogy)
**Confidence: MED**
Source: https://www.fastprep.io/problems/snowflake-throne-inheritance-without-initial-king, Medium,
Phone Screen, "Source Match: 86% (adapted from original problem)" — i.e. FastPrep's own metadata
flags this as a paraphrase of LC 1600 "Throne Inheritance," with a Snowflake-specific twist: the
family starts **empty** (no king at construction) rather than LC 1600's constructor-supplied king.
```
class ThroneInheritance:
    def birth(self, parent_name: str, child_name: str) -> None: ...  # first call establishes the founder
    def death(self, name: str) -> None: ...                          # idempotent
    def get_inheritance_order(self) -> list[str]: ...                # pre-order DFS skipping the dead
```
Key rules (verbatim-paraphrased): founder never changes even after death; siblings visited in
birth order (not alphabetical); dead branches remain structurally intact so their living
descendants still inherit position and can have their own children. Example: births
rhea→zoe, rhea→amy, zoe→leo; order → [rhea,zoe,leo,amy]; after death(zoe) → [rhea,leo,amy].
Constraints: ≤100 operations, ≤20 order queries, ≤100 distinct members.
This is a good "design a class around a fixed API contract with subtle edge cases" interview
question — the interesting part for an interviewer to probe is exactly the "no initial king" edge
case (what does `get_inheritance_order()` return before any `birth()`? Answer: `[]`).

## 9. LRU Cache (and the storage-engine framing)
**Confidence: LOW-MED for "recurring at Snowflake specifically" (repeated by 3+ prep guides with a
domain-specific framing, but no first-hand dated sighting was found in this sweep)**
Sources: https://staffengprep.com/companies/snowflake/, https://interviewchamp.ai/company-coding/snowflake/lru-cache,
https://www.techprep.app/companies/snowflake — all frame it the same specific way: "Snowflake asks
LRU cache constantly because it's the foundation of their warehouse cache — frequently-accessed
micro-partitions stay hot in SSD; cold ones get evicted by exactly this policy... appears recurring
at Snowflake SDE-II onsites." Standard `class LRUCache: def get(key); def put(key, value)` in O(1)
via hashmap + doubly-linked-list; the domain-specific follow-up prep guides suggest is "how would
you adapt this for a multi-tier cache (SSD + remote object storage)?" — plausible but unconfirmed
by any dated candidate report. Also occasionally requested with a **TTL** extension (generic LC
discuss posts on "LRU cache with TTL" exist, https://leetcode.com/discuss/interview-question/1105381/
and https://leetcode.com/discuss/interview-question/284925/, but neither is tagged Snowflake in its
own text — found via a keyword search, not a Snowflake-specific report, so excluded from confidence
scoring here beyond this note).

## 10. Student Enrollment System (OOP base/subclass, embedded in an OA)
**Confidence: LOW** (single source, see `coding_oa.md` #46)
Source: https://interviewfox.ai/interview-questions/snowflake-hackerrank-oa-guide/ (2026 recap).
"Implement Student base class and Result subclass with grade tracking, percentage calculation,
pass/fail logic (33.33% threshold), and recheck functionality." Notable primarily because it shows
Snowflake's OA can include a pure-OOP inheritance/encapsulation question, not just algorithms — but
with zero corroboration this should be treated as possibly fabricated recap content rather than
built into a problem set as-is.

---

## Cross-cutting concurrency notes (apply to items 1, 2, 4, 5, 7 above)
Every genuinely class-shaped Snowflake design problem found in this sweep has an explicit or
implied **concurrency follow-up**:
- Task Scheduler (item 1): implied — "make add/execute safe for concurrent callers" is the obvious
  next step given Snowflake's own multi-worker task-execution model.
- Transactional KV Store (item 2): **explicit** "Follow-up 2: Concurrency... linearizable
  semantics... per-thread transaction stacks."
- Rate Limiter (item 4): **explicit**, Variant B's own statement says "serialized, thread-safe...
  Handlers execute atomically."
- Cron Scheduler (item 5): **explicit**, "(e) Multi-instance safety without double-firing."
- Distributed Tree Counting (item 7): concurrency **is** the problem (message ordering, FIFO
  exactly-once delivery, async fan-out/fan-in).
This is a strong enough pattern (5/10 OOD items, independently sourced) that any Snowflake-focused
problem set should treat "add a thread-safety / distributed-correctness follow-up" as close to a
default expectation for design questions, not an occasional twist.
