# cb06 · 逐场脚本
> FileVault：多用户文件存储（标准库 WSGI + sqlite + `BlobStore`），对应 Abnormal 真实 take-home "File Vault" 的同形代码库 · t1 去重（含并发）· t2 搜索与过滤 · t3 配额、统计、限流 · 练：`python3 loop/ai_screen.py start cb06 <t>` · 面试官视角：`interviewer.md`

## 0. 探索（0–10 min，三个 ticket 通用）
- 先打开：
  - `CONTRIBUTING.md`：面试官写给你的约定（owner 隔离、字节走 `BlobStore`、SQL 只在 repository、原子写用 `Database.transaction()`）；T6 的规矩接在它后面。
  - `filevault/service.py:FileService.upload`：现在是 `store.put(file_id, data)` 再 `files.add(record)`，每文件一个 blob；三张 ticket 都改这里。
  - `filevault/store/db.py:Database.transaction`：`BEGIN IMMEDIATE` 的写事务，**没人调用**。
  - `filevault/store/query.py:Where` + `filevault/store/pagination.py:paginate`：参数化条件与 keyset 游标，`GET /files` 已在用。
  - `filevault/ratelimit.py:TokenBucket` 与 `config/default.toml`：限流器写好了、配置里 `quota_bytes_per_user` / `rate_limit_per_sec` / `admin_users` 都有，但没有任何代码读它们。
  - `filevault/legacy/hash_index.py`：md5 内存索引，冻结；README 说"用它去重"是过时的。
- T1 结果应包含：入口 `python -m filevault serve | upload | ls | fsck`（`cli.py:main` → `app.py:create_app`）与 `X-User-Id` 头的 HTTP API（`api/app.py:ApiApp.handle` → `api/framework.py:resolve` → `api/routes/files.py`）；数据流 handler → `FileService` → `FileRepository`（sqlite，`files` 表）+ `BlobStore`（`LocalDiskStore` 写 `data/blobs/`）；扩展点 `@route`、`BlobStore`、`Where`、`paginate`、`store/migrations/NNNN_*.sql`、`api/app.py:translate`、`config.py:Settings`；测试 `cd starter && python -m pytest -q`（95 passed，约 0.2 s）、单文件 `python -m pytest tests/test_api.py -q`。
- 心智模型（60 s，英文原句）："FileVault is a small multi-user file service. A request comes in with an `X-User-Id`, the route calls `FileService`, which writes bytes through the `BlobStore` interface and metadata through `FileRepository` into sqlite. Everything is scoped by owner. The extension points are the `@route` registry, `BlobStore`, the `Where` query builder with keyset pagination, migrations, and typed config. Two things stand out: `Database.transaction()` exists but nobody uses it, and the rate limiter and the quota settings exist but nothing reads them. `legacy/hash_index.py` is frozen, and the README is wrong that it deduplicates. Tests run in about a fifth of a second."

## t1 · dedup（VLT-212）
### 题
同样的附件被反复上传，存储费翻倍：每个唯一内容只存一份，用户看到的一切不变；用 `dedup_hits_total` 与 `bytes_saved` 报告效果。

### 参考答案
- 设计：缝是 `FileService.upload`/`delete` 里"写 blob + 写记录"那一对。内容寻址：`blobs(sha256 PK, blob_path, size, ref_count)` + `files.sha256`；upload 在**一个 `db.transaction()`** 里 `INSERT … ON CONFLICT(sha256) DO UPDATE SET ref_count = ref_count + 1 RETURNING ref_count`，`ref_count == 1` 才 `store.put`；delete 在事务里先删记录，再 `ref_count - 1`，归零才 `store.delete`。两个方案：A 事务 + 唯一约束（选），B Python 锁（多 worker 下无效，CONTRIBUTING 明确不要）。每用户仍各有 `FileRecord`，对外 API 不变。
- 改动：
  - `filevault/store/migrations/0002_blobs.sql`：`blobs` 表、`files.sha256` 列（旧行为 NULL）与索引。
  - `filevault/store/blobs.py:BlobRepository.acquire/release`：引用计数；`acquire` 返回"是否新建"。
  - `filevault/service.py:FileService.upload`：算 SHA-256，blob 路径 `<sha[:2]>/<sha>`，事务内 acquire → 条件 put → `files.add`；事务后 `metrics.incr("dedup_hits_total")`、`metrics.incr("bytes_saved", size)`。
  - `filevault/service.py:FileService.delete`：事务内 `files.delete`（失败即 `FileNotFound`）→ release → 归零才 `store.delete`；`sha256 IS NULL` 的旧行删自己的私有 blob。
  - `filevault/models.py:FileRecord.sha256`、`store/files.py`（列）、`store/__init__.py`、`app.py:create_app`（装配 `BlobRepository`）。
- 关键测试：`tests/test_service.py::test_same_content_is_stored_once`（两次上传 `store.paths()` 长度 1）· `::test_blob_survives_until_the_last_reference_is_deleted` · `tests/test_store.py::test_blob_refcounting` · `acceptance/test_t1.py::test_delete_racing_with_upload_never_loses_the_content`（删除与同内容上传用 barrier 交错 15 轮，内容不丢、blob 数为 1）。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 用户视角复述；T4 定词 "unique file" = 内容相同；T2 后挑 3 问 | "I read this as: same bytes, one copy on disk, every user keeps their own record. Three questions: does dedup cross users, what happens to existing files, and what must survive a concurrent delete?" | T2：`Given this ticket and this codebase: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Facts you can look up in the code, look up — don't ask me. No code.` 面试官多半答：跨用户去重但对外不变；只管新上传（旧行 `sha256` NULL）；删除不能让别人的文件消失。默认假设：跨用户，SHA-256，不回填。 |
| 13–16 方案 | T3；T5；定 M1–M3；T6 立规矩 | "The seam is upload and delete in `FileService`. A transaction plus a unique constraint, or a Python lock — the lock breaks with several workers, so I'll go with the transaction. M1 is dedup in the sequential case, demoable in 15 minutes." | T3：`Here's my list: SHA-256 content address; blobs table with ref_count; one write transaction per upload/delete; keep a FileRecord per user; two counters. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.` T5：`I think the seam is FileService.upload/delete (existing pieces: Database.transaction, BlobStore, FileRepository). Compare "transaction + unique constraint" vs "threading.Lock" in 5 lines each: fit with existing code, behaviour with several workers, failure isolation. Recommend one. Don't edit anything.` 选事务：理由落在 `CONTRIBUTING` 与 `Database.transaction` 上。T6：见 `claude_playbook.md` T6，再加 `Bytes only through BlobStore; SQL only in store/; use Database.transaction() for atomic writes.` |
| 16–30 M1 | plan mode → 审计划三问 → T7 红 → 绿 → 真实入口演示 | "First failing test: upload the same bytes twice, expect one blob. Red first." | T7 红：`Write ONE failing test for "same bytes uploaded twice are stored once" through app.service.upload, in tests/test_service.py, matching the existing style. Assert len(app.store.paths()) == 1 and that both records read back the same bytes. Run it and show me it fails. Don't fix anything.` 失败信息应是 `assert 2 == 1`，不是 import 错。T7 绿：`Minimal change to make that test pass: migration 0002 with a blobs table and files.sha256, a BlobRepository in store/, and FileService.upload using Database.transaction(). Reuse BlobStore. Nothing else. Run tests/test_service.py.` 最小改动：upload 路径，约 60 行。 |
| 30–40 M2 | 删除的引用计数；并发测试；metrics | "M2 is delete with reference counting, then a threaded test for the race, then the two counters." | T7：`Write ONE failing test: two users upload the same bytes, one deletes, the other still downloads, and after both delete the store is empty.` 然后 T7：`Write ONE test with two threads and a threading.Barrier uploading the same new content, repeated 15 times; each round must leave exactly one blob and two records.` 有东西变红走 T8：`Reproduce this with one command or one failing test that shows the exact symptom. Then give 3 ranked hypotheses, each with the prediction that would confirm it. Don't fix yet.` 最后 `bytes_saved` 与 `dedup_hits_total` 用 `metrics.incr`。 |
| ~40 审查 | T10 一轮；收一条拒一条 | "One adversarial pass now: I'll keep what's real and say why I reject the rest." | T10：`Adversarial review of the current diff against the ticket. Assume the author is overconfident. Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under bad input. Do NOT validate or summarize. Max 5 issues, ranked.` 典型 v1 会被抓到：① delete 里 `store.delete` 若放在事务外，会和同内容上传交错而删掉刚被引用的 blob → **收下**，挪进事务；② "给 `bytes_saved` 加缓存/全局 dict 记录每个哈希" → **拒绝**，`blobs` 表已是事实来源，过度设计。 |
| 42–45 收尾 | T11 证据；T12 写 NOTES.md | "Fresh run: everything green. Here is dedup through the real CLI." | T11：`cd starter && python -m pytest -q`；`python -m filevault --data-dir /tmp/fv upload report.txt --user alice` 连跑两次，再 `find /tmp/fv/blobs -type f \| wc -l` → 输出 `1`（starter 同样操作输出 `2`）；`python -m filevault --data-dir /tmp/fv fsck` → `ok`。T12：`List every item we named today (ticket, assumptions, review findings). Mark each done / out of scope. Write NOTES.md: assumptions + known gaps + v2.` known gaps："no backfill of old files, no hash check on read, cross-user dedup timing side channel, orphan blob if the process dies mid-upload (fsck finds it)". |
| 45+ 讲解 | 做了什么 · 为什么契合 · 假设 · 测了什么 · gaps | "I used the transaction helper that was already there, so concurrent uploads of the same content can't both create it, and a delete can't remove a blob an upload is about to reference." | X5：用 seam / locality 说明"改动集中在 upload/delete 与一个新 repository"。 |

### 追问与答
- "Two workers upload the same new file at the same moment. Walk me through what each one does." → 两个都 `BEGIN IMMEDIATE`，sqlite 让一个先拿写锁；先到者的 `ON CONFLICT` 插入新行（`ref_count` 1）并写字节，后到者命中冲突把计数加到 2、不写字节。靠唯一约束 + 写事务，不是 Python 锁。
- "A delete and an upload of the same content interleave. What is the worst thing that could happen?" → delete 把计数减到 0、事务外才删文件，而同一时刻上传已看到旧行并引用了它，结果记录指向不存在的字节。所以删除字节必须在同一个写事务里。
- "Is dedup across users a privacy problem?" → 是：A 可能通过"上传秒回"推断 B 有同一文件。v1 接受并写进 known gaps；缓解是对外耗时一致，或把去重限定在同一用户/租户内。
- "How would you roll this out and backfill?" → 新上传先行；旧行 `sha256 IS NULL` 就是待办清单，后台任务逐个算哈希并合并；每步用 `fsck` 校验。
- "What's missing?" → 读取时校验哈希、流式哈希、回填、孤儿 blob 的 GC。

### 翻车点
- AI 加一个 `threading.Lock` 包住"查哈希 → 写"：单进程能过测试，多 worker 失效，也违反 CONTRIBUTING；该用已有的 `Database.transaction()`。
- AI 直接 `pathlib.Path.write_bytes` 写磁盘或扩展 `legacy/hash_index.py`：绕过 `BlobStore` 接口 / 碰了冻结模块。
- 先查后插（`SELECT` 再 `INSERT`）：顺序测试全绿，两个线程同时上传就出两个 blob 或唯一约束冲突。
- 把 `FileRecord` 合并成一条共享记录：用户的文件名、时间丢失，对外行为变了（"without changing what users see"）。

## t2 · search（VLT-231）
### 题
用户文件太多找不到：在 `GET /files` 上加 `q`、`type`、`min_size`、`max_size`、`from`、`to`，非法值要说清是哪个参数。

### 参考答案
- 设计：缝是 `GET /files` → `FileService.list_files` → `FileRepository.list_for_owner` 这条已有的分页链路。扩展而不是另开 `/search`；全部条件走 `Where`（绑定参数、列名白名单），游标与排序不变（`(created_at, id)` keyset，所以同一时间戳也不重不漏）；校验放 `validation.py` 并抛已有的 `InvalidInput(field, …)`，`api/app.py:translate` 已把它映射成 400 + `details.field`。两个方案：A 在 SQL 里过滤（选）；B 取回全部再在 Python 里 `filter()`（破坏分页、规模差）。
- 改动：
  - `filevault/store/query.py:Where.contains`：`LOWER(col) LIKE ? ESCAPE '\'`，`%` `_` `\` 作字面量。
  - `filevault/models.py:FileFilters`：六个可选条件。
  - `filevault/store/files.py:FileRepository.list_for_owner`：多一个 `filters` 参数，逐项加进同一个 `Where`。
  - `filevault/validation.py:parse_filters`：数字非负、日期 `parse_iso`、区间不倒置，错误带字段名。
  - `filevault/service.py:FileService.list_files` 透传；`filevault/api/routes/files.py:list_files` 取六个参数。
- 关键测试：`tests/test_api.py::test_injection_filename_is_just_a_string`（`q=' OR '1'='1` 只命中 `x' OR '1'='1.pdf`）· `::test_filters_paginate_without_gaps` · `tests/test_validation.py::test_parse_filters_names_the_bad_parameter` · `tests/test_query.py::test_contains_is_case_insensitive_and_escapes_wildcards` · `acceptance/test_t2.py::test_filtered_pagination_with_identical_timestamps_loses_nothing`。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | T4 定词 "type"；T2 后挑 3 问 | "I'll extend `GET /files` rather than add a search endpoint. Questions: is `type` the MIME type or the extension, are the bounds inclusive, and what should a bad value return?" | T2（同 t1 的 prompt）。面试官多半答：`type` 是 content type 精确匹配；边界含；非法值 400 且说出参数名。默认假设：`q` 对文件名做不区分大小写的子串；日期无时区按 UTC；全部条件 AND。 |
| 13–16 方案 | T3；T5；M1–M3 | "The seam is the existing list path: `list_for_owner` with `Where` and keyset pagination. I'd rather add filters there than build a second query path. M1 is `q` and `type`." | T3：`Here's my list: q substring case-insensitive, type exact, size range inclusive, date range inclusive UTC, 400 naming the parameter, injection-safe, stays paginated. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.` T5：`I think the seam is FileRepository.list_for_owner (existing pieces: Where, paginate, InvalidInput). Compare "filters in SQL via Where" vs "fetch all, filter in Python" in 5 lines each. Recommend one. Don't edit anything.` 选 SQL：分页和规模。 |
| 16–30 M1 | T7 红绿；真实入口演示 | "First test: `q=REPORT` returns both report files, case-insensitively." | T7 红：`Write ONE failing test for "q matches filenames case-insensitively" through GET /files in tests/test_api.py, matching the existing style. Seed q3-report.pdf, Q3-Report-final.PDF and notes.txt; expect exactly the first two. Run it and show me it fails.` 红的原因是返回 3 项（过滤被忽略）。绿：`Minimal change: add Where.contains (parameterised LIKE with ESCAPE), thread a filters object through list_files into list_for_owner, read q and type in the route. Nothing else.` |
| 30–40 M2 | 大小/日期/校验；注入与分页测试 | "M2 is size and date ranges, validation, and the nasty cases: the fixture has a filename that looks like SQL injection." | T7：`Write ONE failing test: q="' OR '1'='1" returns only the file literally named "x' OR '1'='1.pdf".` 再 `Write ONE failing test: min_size=abc returns 400 and the error details name min_size.` 红了走 T8（例如分页丢条目）：`Reproduce this with one command or one failing test ... Then give 3 ranked hypotheses ... Don't fix yet.` |
| ~40 审查 | T10 | "One adversarial pass: I want to know what breaks with odd input." | T10（同 t1）。典型发现：① `LIKE` 的 `%`/`_` 未转义，`q=100%` 误匹配 → **收下**；② "给 filename 加索引/FTS5" → **拒绝**，`LIKE '%x%'` 吃不到普通索引，规模问题写进 known gaps，不在 35 分钟里做。 |
| 42–45 收尾 | T11；T12 | "Fresh run: green. Now through the real server." | T11：`cd starter && python -m pytest -q`；启动 `python -m filevault --data-dir /tmp/fv serve --port 8000`，`curl -s "localhost:8000/files?q=report" -H "X-User-Id: alice"` → 只返回 `Q3-Report.pdf` 一项；`curl -s "localhost:8000/files?min_size=abc" -H "X-User-Id: alice"` → `{"error": {"code": "bad_request", "details": {"field": "min_size"}, "message": "min_size must be a whole number of bytes"}}`。T12 同前；known gaps："`LIKE '%x%'` does not use an index, `type` is exact match, ASCII-only case folding"。 |
| 45+ 讲解 | 同 t1 | "Filters are all bound parameters, so the injection-looking filename is just a string, and pagination is untouched." | X5。 |

### 追问与答
- "What if a user has 5 million files?" → `(owner, created_at, id)` 索引只管分页；`LIKE '%x%'` 全扫该用户的行。要么做前缀搜索，要么 FTS5/trigram 索引；v1 把它写进 known gaps。
- "How do you know pagination is stable while files are being uploaded?" → keyset 游标按 `(created_at, id)` 往后走，新文件排在最前，不影响已翻过的页；`id` 兜住同一时间戳。
- "Why not an f-string? The filename is just a string." → 夹具里就有 `x' OR '1'='1.pdf`；`Where` 只放行白名单列名，值全是 `?`。
- "A user searches for `100%`." → 通配符必须转义，否则 `%` 会匹配一切。

### 翻车点
- AI 用 `OFFSET` 分页或另写 `/search`：绕开已有的 keyset `paginate`，翻页时重复/遗漏。
- AI 用 f-string 拼 `LIKE '%{q}%'`：夹具里的注入文件名当场暴露。
- 日期当字符串比较但不校验：`from=yesterday` 返回 200 而不是 400 + 字段名。
- 取回全部再在 Python 里过滤：分页游标失效，规模上不成立。

## t3 · quota + stats（VLT-247）
### 题
免费档每人 10 MB；财务要看 dedup 省了多少：超额 413、上传限流 429 + `Retry-After`，`GET /stats`（用户）与 `GET /admin/stats`（admin）。

### 参考答案
- 设计：三个"已有但没人用"的东西拼起来：配置键 `quota_bytes_per_user` / `rate_limit_per_sec` / `admin_users`、`TokenBucket`、`Database.transaction()`。配额按用户**逻辑占用**（他上传的文件大小之和，去重不减免），检查与插入在同一个写事务里，所以同一用户的并发上传不会一起通过；`QuotaExceeded` 由 `translate` 映射为 413（带 `used/quota/remaining`）；限流用 `TokenBucket` 按用户建桶，只挂 `POST /files`；两个 stats 端点是 `api/routes/stats.py` 新模块。两个方案：A 逻辑占用（选）；B 物理占用/按引用分摊（用户额度会因别人删文件而变）。
- 改动：
  - `filevault/errors.py:QuotaExceeded`；`filevault/api/app.py:translate` 映射；`filevault/api/framework.py:QuotaExceededError/TooManyRequests`、`ApiContext.limiter`。
  - `filevault/ratelimit.py:RateLimiter`：每用户一个 `TokenBucket`（容量 `max(1, rate)`），`check(user)` 返回 `None` 或等待秒数。
  - `filevault/service.py:FileService.upload`：事务内 `usage_for_owner` → 比较 → 才 acquire/put/add；`usage()`、`storage_stats()`。
  - `filevault/store/files.py:FileRepository.usage_for_owner/totals`、`store/blobs.py:BlobRepository.total_size`。
  - `filevault/api/routes/files.py:upload_file`：先 `ctx.limiter.check`，超限抛 `TooManyRequests(headers={"Retry-After": …})`；`api/routes/stats.py`：`/stats`、`/admin/stats`（非 admin 403）；`routes/__init__.py` 注册。
- 关键测试：`tests/test_api.py::test_quota_boundary`（恰好等于配额可传，多 1 字节 413）· `::test_admin_stats_show_dedup_savings` · `::test_rate_limit_returns_429_with_retry_after` · `tests/test_service.py::test_quota_check_is_atomic_with_the_insert`（两线程各 60 字节、配额 100，恰一个成功）· `acceptance/test_t3.py::test_concurrent_uploads_cannot_overshoot_the_quota`。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | T4 定词 "usage"；T2 后挑 3 问 | "Before I build: does a duplicate count against the user's quota, who is an admin, and what should the 413 tell the user?" | T2（同前）。面试官多半答：按用户视角（逻辑），去重是公司的节省；admin 取配置 `admin_users`；413 要带剩余额度。默认假设：逻辑占用、恰好等于配额可传、限流只管 `POST /files`、内存桶（单进程）。 |
| 13–16 方案 | T3；T5；M1–M3 | "Three things already exist and nothing uses them: the config keys, the token bucket, and the write transaction. M1 is the quota with a 413, M2 the two stats endpoints, M3 the rate limit." | T3：`Here's my list: logical usage per user; check inside the write transaction; 413 with remaining; /stats and /admin/stats; token bucket per user on POST /files with Retry-After. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.` T5：`I think the seam is FileService.upload (existing pieces: Settings.quota_bytes_per_user, Database.transaction, TokenBucket, api/app.py:translate). Compare "check quota before the transaction" vs "check inside it" in 5 lines each: races, fit with CONTRIBUTING. Recommend one. Don't edit anything.` 选事务内。 |
| 16–30 M1 | T7 红绿 | "First test: exactly the quota is fine, one byte more is a 413." | T7 红：`Write ONE failing test through POST /files in tests/test_api.py: with quota_bytes_per_user=100 (FILEVAULT_QUOTA_BYTES_PER_USER), uploads of 60 then 40 bytes succeed and a third of 1 byte returns 413. Run it and show me it fails.` 红的原因是第三次返回 201。绿：`Minimal change: add QuotaExceeded in errors.py, check used + size against settings.quota_bytes_per_user inside the upload transaction, map it in api/app.py:translate with used/quota/remaining. Nothing else.` |
| 30–40 M2 | stats、限流 | "M2: two endpoints. M3 if time: the limiter, per user, uploads only." | T7：`Write ONE failing test: two identical uploads of 1000 bytes; GET /admin/stats as "admin" returns logical_bytes 2000, physical_bytes 1000, saved_bytes 1000; as a normal user it is 403.` 绿：新模块 `api/routes/stats.py` + 在 `routes/__init__.py` import。限流：`Write ONE failing test: with rate_limit_per_sec=1 the second immediate upload returns 429 with a Retry-After header, and a different user is unaffected.` 绿：`Reuse TokenBucket from ratelimit.py: one bucket per user in a small registry, applied only in the POST /files handler; raise a TooManyRequests ApiError with headers={"Retry-After": ...}. Do not write a new bucket.` |
| ~40 审查 | T10 | "One adversarial pass: I'm most worried about concurrency and the limiter." | T10（同前）。典型发现：① 配额检查在事务之外 → 同一用户两个并发上传一起通过、超卖 → **收下**；② "限流状态用 Redis" → **拒绝**，单进程内存桶按 ticket 够用，多 worker 的限制写进 known gaps。 |
| 42–45 收尾 | T11；T12 | "Fresh run: green. Real server, quota 100 bytes and 3 requests per second." | T11：`cd starter && python -m pytest -q`；用 `FILEVAULT_QUOTA_BYTES_PER_USER=100 FILEVAULT_RATE_LIMIT_PER_SEC=3 python -m filevault --data-dir /tmp/fv serve --port 8765`：先传 70 字节 → `201`；再传 34 字节 → `413`，响应 `{"error": {"code": "quota_exceeded", "details": {"quota": 100, "remaining": 30, "used": 70}, ...}}`；`curl -s localhost:8765/admin/stats -H "X-User-Id: admin"` → `{"file_count": 1, "logical_bytes": 70, "physical_bytes": 70, "saved_bytes": 0, "savings_ratio": 0.0}`，用 alice 调 → `403`；同一用户连发 4 次上传 → `201 201 201` 然后 `HTTP/1.0 429 Too Many Requests` 与 `Retry-After: 1`。T12 同前；known gaps："rate limiter is per process (N workers = N times the rate), bucket dict never evicts, no per-file-count limit, quota race protected only by sqlite's single writer"。 |
| 45+ 讲解 | 同前 | "Quota is logical on purpose: users are charged for what they uploaded, and finance's saved bytes are logical minus physical. The check shares the write transaction with the insert, so a user can't race past the limit." | X5。 |

### 追问与答
- "Two requests from one user arrive together, each just under the limit." → 检查和插入在同一个 `BEGIN IMMEDIATE` 事务里，第二个看到第一个已写入的用量，被 413；没有事务就会超卖。
- "You run 4 workers. What breaks in your rate limiter?" → 内存桶每个进程一份，实际速率是 4 倍；要么共享存储，要么在网关限流，要么 v1 明说只支持单进程。
- "Why is quota logical but the finance report physical?" → 两个读者两个问题：用户为自己上传的文件付费；财务关心磁盘上的实际字节，`saved = logical − physical`。
- "A user deletes a file another user also has." → 只有删除者的配额恢复；物理占用不变，因为引用计数还没归零。

### 翻车点
- AI 自己写一个令牌桶或 `time.sleep` 限流：`ratelimit.py:TokenBucket` 已经写好测好，且可注入时钟。
- 把配额写成常量 `10 * 1024 * 1024`：`quota_bytes_per_user` 早在 `config/default.toml` 里，测试靠 `FILEVAULT_*` 覆盖。
- 配额检查放事务外：顺序测试通过，并发超卖。
- 手写 413/429 响应 body：绕过 `translate` 与 `ApiError` 家族，错误形状与其他端点不一致。

## 录屏版：讲你怎么用 AI（5 分钟）

真实 take-home 只要一段屏幕录像，讲 Gen-AI 的用法，**不演示应用本身**。下面是一个 5 分钟提纲，素材取自你做 cb06 时的真实终端（任选 t1 或三张合并）。每一段先说结论，再亮出对应的提示词或 diff。

| 时间 | 讲什么 | 英文原句 |
|---|---|---|
| 0:00–0:30 | 开场：范围与做法 | "I'm going to show how I used Claude Code on this repo, not the app itself. I'll cover how I scoped the work, how I prompted, how I verified, and where I had to correct the AI." |
| 0:30–1:30 | 怎么 scope：读题、自己先列、再让 AI 补（T2、T3、X3） | "I didn't paste the ticket into the model. I read the code first, wrote my own list — SHA-256, a refcount table, one transaction per upload — and only then asked what I'd missed. The decisions are mine; the typing is Claude's." |
| 1:30–2:45 | 怎么 prompt：地图、接缝、规矩（T1、T5、T6） | "First prompt: map the repo and cite files, so it can't invent a structure. Second: here is the seam and the two options, compare them, don't edit. Then a short rules block: reuse existing abstractions, bytes only through `BlobStore`, atomic writes through `Database.transaction()`, tests next to the existing ones." |
| 2:45–3:45 | 怎么验证：红 → 绿、并发测试、真实入口（T7、T8、T11） | "Every change starts with a failing test I watched fail. For the race I wrote a two-thread test with a barrier, repeated fifteen times, because a sequential test would have passed the naive version. At the end I ran the real CLI: two uploads of the same file, one blob on disk, `fsck` says ok." |
| 3:45–4:30 | 怎么纠正 AI：点名它错在哪（T9、T10） | "Claude's first version wrapped the hash lookup in a `threading.Lock`. That passes a single-process test and breaks with several workers, and our CONTRIBUTING says to use the transaction helper, so I rejected it and pointed it at `Database.transaction()`. The adversarial review also flagged that the blob delete sat outside the transaction; I took that one. It suggested caching hashes in a dict; I dropped that — the table is already the source of truth." |
| 4:30–5:00 | 收口：没做的、下次怎么改（T12） | "Out of scope for v1, written in NOTES.md: backfill of old files, hash check on read, the cross-user timing side channel. Next time I'd write the concurrency test before the first prompt, because it's what the model got wrong." |

录屏前检查：终端 1 的 Claude 会话能看到你发的提示词；终端 2 有 `pytest` 与 CLI 的真实输出；不要打开应用页面演示功能；停在 5 分钟内。
