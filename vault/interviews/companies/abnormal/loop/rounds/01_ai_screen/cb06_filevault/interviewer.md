# interviewer.md · cb06_filevault（面试官视角）

> 本文件包含答案：只在做完某张 ticket 之后再看那一节（`python3 loop/ai_screen.py reveal cb06 tN`）。
> 题型依据：Abnormal 的真实 take-home（"File Vault"：去重 + 搜索过滤 + 配额/统计 + metrics，要求录屏讲 Gen-AI 用法；`catalog/raw/ai_round_sweep_2026-10-07.md` S-1）。原题是 Django/DRF，这里用标准库重造同形代码库，并把"并发正确性"做成可验收的难点。
> 面试官开场原话（英文）："This is FileVault, our file-storage service. Pick up this ticket. You can use Claude Code. I'll answer questions, but I won't tell you how to build it."
> 评分原话（官方）：Judgment — "evaluate approaches, scope work into milestones, and decide what fits the existing system"；Agency — "make decisions, state assumptions, test your own work, keep momentum"。

通用的"契合本系统"清单（三张 ticket 都适用）：

| 约定（`CONTRIBUTING.md`） | 对应落点 |
|---|---|
| 一切按用户隔离 | repository 方法都带 `owner`；handler 只用 `request.user`（`X-User-Id`），别人的文件是 404 不是 403 |
| 字节只走 `BlobStore` | `storage/base.py:BlobStore`；业务代码不直接 `open()` blob 路径 |
| SQL 只在 repository 里；用 `Where` 拼条件，值永远是绑定参数 | `store/query.py:Where`、`store/files.py:FileRepository` |
| 原子写用 `Database.transaction()`，不要用 Python 锁 | `store/db.py:Database.transaction`（`BEGIN IMMEDIATE`；starter 里**没人用它**） |
| 改 schema = 新 migration | `store/migrations/NNNN_*.sql`，不改 `0001_init.sql` |
| 配置优于常量 | `config/default.toml` + `config.py:Settings/_validate`，`FILEVAULT_<KEY>` 环境覆盖 |
| 错误：service 抛领域错误，`api/app.py:translate` 映射成 HTTP | `errors.py`、`api/framework.py:ApiError` 家族；handler 不手写错误 body |
| 跳过/吞掉的要计数 | `metrics.incr(...)` |
| 不碰 `filevault/legacy/` | `hash_index.py` 是冻结的 md5 原型；README 里"legacy/hash_index.py 用于去重"是**过时**的说法 |

---

## t1 · dedup（VLT-212）

### ① 好的 v1 长什么样
候选人在探索阶段读到 `FileService.upload`：现在是"先 `store.put(file_id, data)`，再 `files.add(record)`"，每个文件一个 blob。他注意到 `Database.transaction()` 存在却没人用、`legacy/hash_index.py` 是 md5 的半成品（不要扩展），README 的"用 hash_index 去重"是错的。好的 v1：用 SHA-256 做内容寻址——新 migration `0002_*` 建 `blobs(sha256 PK, blob_path, size, ref_count)` 并给 `files` 加 `sha256` 列；upload 在**一个 `db.transaction()`** 里 `INSERT … ON CONFLICT(sha256) DO UPDATE SET ref_count = ref_count + 1`，由"是否新建了这一行"决定要不要 `store.put`；delete 同样在事务里先删 `FileRecord`、再 `ref_count - 1`，归零才 `store.delete`。每个用户仍有自己的 `FileRecord`（文件名、时间各自保留，对外 API 不变）。并发靠**唯一约束 + 写事务**，不是 Python 锁。`dedup_hits_total` 和 `bytes_saved` 用现有 `metrics.incr`。35 分钟内 M1 = 顺序场景下去重（两次上传一个 blob、删一个另一个还在），M2 = 事务化与竞态测试，M3 = metrics。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 跨用户去重吗？ | "Yes, across users — that's where most of the duplicates are. But nothing a user can see should change." （默认：跨用户；要求候选人说出侧信道风险：A 能否从上传耗时推断 B 有这个文件。接受"per-user 去重"的答案，只要有理由） |
| 已有的文件要回填吗？ | "Not today. New uploads only." （旧行 `sha256` 为 NULL，各自保留私有 blob；delete 要照顾到这类行） |
| 用什么哈希？ | "Something collision-safe." （SHA-256；`legacy/hash_index.py` 的 md5 不行） |
| 删除时怎么办？ | "A file must never disappear because someone else deleted theirs." |
| 两个人同时上传同一个文件？ | "That has to work. We have a lot of workers." （→ 唯一约束 + 事务；追问是否多进程） |
| 文件名/创建时间还保留吗？ | "Each user keeps their own record, name and timestamp." |
| 要不要在读取时验证哈希？ | "Not for v1." |
| 指标要什么？ | "Counters, the way we already do them." |
| 上传大文件内存怎么办？ | "Files are capped at 10 MB today. Don't solve streaming." |

### ③ 隐藏期望（文件:符号）
- `filevault/service.py:FileService.upload` / `delete`：去重与引用计数的落点；`FileRepository`/`BlobRepository` 里写 SQL，不在 service 里拼。
- `filevault/store/db.py:Database.transaction`：**已有但没被用的写事务**。正确做法是用它，而不是 `threading.Lock`（多 worker/多进程下锁无效）。
- `filevault/storage/base.py:BlobStore`：所有字节读写走接口（`put`/`get`/`delete`），blob 路径是内容哈希，`LocalDiskStore.put` 已是原子替换。
- `filevault/store/migrations/`：新 `0002_*.sql`（`blobs` 表 + `files.sha256`）；不改 `0001_init.sql`。
- `filevault/metrics.py:incr`：`dedup_hits_total`、`bytes_saved`（沿用 `uploads_total` 的做法）。
- `filevault/maintenance.py:fsck`：按 `files.blob_path` 判断 missing/orphaned——换成共享 blob 路径后仍成立（可以问候选人跑了 `fsck` 没有）。
- 不该碰：`filevault/legacy/hash_index.py`（md5，内存里，半成品）；README 里"hash_index 用于去重"。

### ④ 追问
1. "Two workers upload the same new file at the same moment. Walk me through what each one does."（→ `BEGIN IMMEDIATE` 串行化写；`ON CONFLICT` 决定谁写字节）
2. "A delete and an upload of the same content interleave. What is the worst thing that could happen, and why can't it?"（→ 删字节必须在同一写事务里，否则会删掉刚被新上传引用的 blob）
3. "Is dedup across users a privacy problem?"（→ 上传耗时侧信道；缓解：对外耗时一致/先收完 body 再判断/只在同租户内；v1 说明风险）
4. "How would you roll this out and backfill the existing files?"（→ 先只对新上传；后台任务逐个算哈希、合并 blob；`sha256 IS NULL` 的行就是待办清单）
5. "What if the process dies between writing the blob and committing?"（→ 孤儿 blob；`fsck` 能找出来；写在事务里所以提交失败会回滚行但字节可能残留）
6. "What's missing from your v1?"（→ 读时校验哈希、大文件流式哈希、GC/回填、多进程部署下的 busy 超时）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先问跨用户与回填；选 SHA-256 + 引用计数 + 事务；说出"为什么不用锁" | 做出来了，决策隐含 | 只做"查一下有没有同哈希再插入"（check-then-insert），没想到并发 |
| Agency | 10 分钟内定位 `upload`/`delete` 与 `transaction()`；先 M1 再并发再 metrics | 按顺序做完，没分里程碑 | 一头扎进流式哈希/分块存储，35 分钟没有端到端 |
| Fit-the-system | 新 migration、`BlobRepository` 放在 `store/`、走 `BlobStore`、用 `transaction()`、`metrics.incr` | 大部分到位，如把 SQL 写进 service | 直接 `open()` 写磁盘；用 `threading.Lock`；扩展 `legacy/hash_index.py`；改 `0001_init.sql` |
| Testing | 为 service 和 API 各加测试；有一个多线程测试（barrier）；跑 `fsck` | 只有顺序测试 | 没测试或只手测 |
| AI-supervision | 让 Claude 先读 `service.py`、`store/db.py`、`CONTRIBUTING.md`；审 diff 时抓到它"又加了 `threading.Lock`"或"又 `open()`" | 接受输出后再清理 | 整段粘贴 AI 的通用方案（pathlib 写磁盘 + 全局 dict 缓存哈希） |
| Communication | 一句话说清 ref_count 生命周期、侧信道风险与 known gaps | 讲了做了什么没讲没做什么 | 只念代码 |

---

## t2 · search（VLT-231）

### ① 好的 v1 长什么样
候选人在 `GET /files` 现有的 `paginate` + keyset 游标上扩展，而不是另写一个 `/search`。他注意到两个已有件：`store/query.py:Where`（参数化条件构造器）与 `store/pagination.py:paginate`（`(created_at, id)` 键集游标，排序稳定），并读了 `tests/test_query.py` 里"未知列被拒绝"的约定。好的 v1：新增 `Where.contains`（`LOWER(col) LIKE ? ESCAPE`，`%`/`_`/`\` 当字面量），`FileRepository.list_for_owner` 接受一个 filters 对象并全部走 `Where`；参数校验放在 `validation.py`（沿用 `InvalidInput(field, …)`，`api/app.py:translate` 已把它映射为 400 + `details.field`）；`from`/`to` 用 `timeutil.parse_iso`。注入文件名 `x' OR '1'='1.pdf` 作为普通字符串。分页游标不变，过滤后依然稳定（同一时间戳不重不漏，因为排序键包含 `id`）。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| `q` 匹配什么？ | "The filename. Case-insensitive, anywhere in the name." |
| `type` 是扩展名还是 MIME？ | "The content type, like `application/pdf`. Exact match is fine; `image/*` would be nice." |
| 大小/日期边界含不含？ | "Inclusive. Say so in the docs." |
| 日期格式、时区？ | "ISO-8601. If there's no offset, call it UTC." |
| 结果排序？ | "Newest first, like the list today." |
| 多个过滤条件？ | "All of them have to match." |
| 非法参数？ | "Tell the caller which one is wrong." （→ 400 + 字段名） |
| 文件名里有 `%` 或 `_` 呢？ | "It's a name, not a pattern." （LIKE 通配符转义） |
| 要不要全文搜索/内容搜索？ | "No. Names only." |
| 要不要加索引？ | "Think about it, but don't spend the time." |

### ③ 隐藏期望
- `filevault/store/query.py:Where`：新增方法、列名白名单（`COLUMNS`）与运算符白名单（`OPERATORS`）保持；**不拼 SQL 字符串**。
- `filevault/store/pagination.py:paginate/Page`、`FileRepository.list_for_owner`：keyset 分页保持，过滤条件并进同一个 `Where`。
- `filevault/errors.py:InvalidInput(field, message)` + `api/app.py:translate`：非法参数的统一出口；handler 不手写 400 body。
- `filevault/timeutil.py:parse_iso/to_iso`：日期解析与存储格式（定宽字符串，字符串序 = 时间序）。
- `filevault/api/routes/files.py:list_files`：在现有 handler 上加参数；`Request.arg`/`int_arg` 是已有的取参 helper。
- 不该碰：另起 `/search` 路由；在 Python 里 `filter()` 全表结果；`legacy/`。

### ④ 追问
1. "What if a user has 5 million files — what does this query do?"（→ `(owner, created_at, id)` 索引只覆盖分页；`LIKE '%x%'` 不能用索引；方案：前缀搜索 / FTS5 / trigram；v1 说明）
2. "How do you know pagination is stable while files are being uploaded?"（→ keyset 游标；新上传排在最前，不影响已翻过的页）
3. "Why not build the SQL with an f-string? The filename is just a string."（→ 注入；夹具里有 `x' OR '1'='1.pdf`；`Where` 只放行白名单列名）
4. "A user searches for `100%`. What happens?"（→ 通配符转义）
5. "Should `type=image` also match `image/png`?"（→ 产品决策；v1 精确匹配，`image/*` 是 stretch）
6. "What's missing from your v1?"

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 在 `GET /files` 上扩展，不另开 `/search`；先问 `type` 与边界语义，给默认并写进 docs | 做对了，语义没确认 | 先设计一套查询 DSL / 引入 FTS 依赖 |
| Agency | M1：`q` + `type`；M2：大小与日期 + 校验；M3：组合分页测试 | 一次写完所有过滤 | 把 35 分钟花在性能优化上 |
| Fit-the-system | 用 `Where`、`paginate`、`InvalidInput`、`parse_iso`；测试放进现有文件 | 用了 `Where` 但校验写在 handler 里 | f-string 拼 SQL；`OFFSET` 分页；自造错误 body |
| Testing | 覆盖注入文件名、`%`/`_`、边界包含、同时间戳分页、他人文件不可见 | 只测 happy path | 手测 |
| AI-supervision | 要求 Claude 复用 `Where`；审出它"顺手加了 `OFFSET`"或"在 Python 里过滤" | 接受后再修 | 接受了 f-string SQL |
| Communication | 说清边界语义与 `LIKE '%x%'` 的规模问题 | 提到性能但没给方向 | 没提 |

---

## t3 · quota + stats（VLT-247）

### ① 好的 v1 长什么样
候选人注意到配置里**早就有** `quota_bytes_per_user`、`rate_limit_per_sec`、`admin_users` 三个没人读的键，`ratelimit.py:TokenBucket` 写好测过却没挂上，`PayloadTooLarge`（413）已有。好的 v1：配额按用户"逻辑占用"（他上传的文件大小之和，去重不减免——产品上用户感知的是自己的文件）；检查放在 upload 的**同一个写事务**里（读 `SUM(size)` → 比较 → 插入），这样同一用户的并发上传不会一起通过；超额抛 `QuotaExceeded`，`translate` 映射为 413 并带 `used/quota/remaining`；`GET /stats`、`GET /admin/stats`（`admin_users` 之外 403）作为 `api/routes/` 下新模块注册；admin 的"物理占用"来自 `blobs`（共享部分）+ 无哈希的旧文件，"节省" = 逻辑 − 物理；`TokenBucket` 按用户建桶（一个很小的注册表），只挂 `POST /files`，超限 429 + `Retry-After`。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 配额算逻辑还是物理？去重要不要减免？ | "From the customer's point of view: the files they uploaded. Dedup is our saving, not theirs." （默认：逻辑占用；接受"按物理占用/按引用分摊"，但要说明代价：用户的额度会因别人删文件而变化） |
| 刚好等于配额可以传吗？ | "Yes, exactly 10 MB is fine." |
| 超额返回什么？ | "413, and tell them how much room they have left." |
| 限流的维度？ | "Per user. And only uploads for now." |
| 限流状态存哪？ | "In memory is fine — one process today. Tell me what changes with several." |
| 谁是 admin？ | "The `admin_users` in the config." |
| 节省比例怎么定义？ | "Saved bytes over logical bytes." |
| 删除后配额恢复吗？ | "Obviously." |
| 单个文件超过 `max_upload_bytes` 和超过配额有什么区别？ | "Both are 413; the message should say which." |
| `GET /stats` 要不要缓存？ | "No." |

### ③ 隐藏期望
- `filevault/config.py:Settings`（`quota_bytes_per_user`、`rate_limit_per_sec`、`admin_users`）：**已有的键**，直接读取，不要新造；测试里用 `FILEVAULT_*` 覆盖。
- `filevault/ratelimit.py:TokenBucket`（注入 clock，不 sleep）：复用，不重写一个。
- `filevault/store/db.py:Database.transaction`：配额检查与插入同一事务（并发正确性）。
- `filevault/errors.py` + `api/app.py:translate`、`api/framework.py:ApiError` 家族（加 429 同风格；`ApiError.headers` 已支持 `Retry-After`）。
- `filevault/api/routes/` 新模块 + `routes/__init__.py` 里 import；handler 用 `req.user`，admin 判断读 `ctx.settings.admin_users`。
- `filevault/service.py` / repositories：`SUM(size)` 之类的查询放进 repository，不在 service 里写 SQL。
- 不该碰：把配额塞进 `max_upload_bytes`；`legacy/`；在 handler 里 `time.sleep` 做"限流"。

### ④ 追问
1. "Two requests from one user arrive together, each just under the limit. What happens?"（→ 事务内检查；没有事务会超卖）
2. "You run 4 gunicorn workers. What breaks in your rate limiter?"（→ 内存桶各 worker 独立 → 实际速率 ×4；方案：共享存储/网关限流/粘性路由；v1 说明）
3. "Why is quota logical but the finance report physical?"（→ 两个读者，两个问题；`saved = logical − physical`）
4. "A user deletes a file another user also has. Whose quota changes?"（→ 只有删的人；物理占用不变，因为引用计数还在）
5. "What would you alert on?"（→ `quota_exceeded` / 429 的计数；`saved_bytes` 的趋势）
6. "What's missing from your v1?"（→ 限流 key 的清理（桶字典无限增长）、按文件数限额、admin 角色模型、`/stats` 的缓存）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先问逻辑 vs 物理；先发现三个"已有但没用"的东西（配置键、`TokenBucket`、`transaction()`）；说出多 worker 限流的局限 | 做出来了，没讨论语义 | 新造一套配额配置；自写限流算法 |
| Agency | M1：配额 + 413；M2：`/stats` + `/admin/stats`；M3：限流 | 一次全做，没有可演示的中间点 | 在限流算法上打磨，配额没完成 |
| Fit-the-system | 读已有配置键；用 `TokenBucket`、`translate`、`ApiError.headers`、`@route` | 复用了大部分，漏掉一两个（如没走 `translate`） | 常量写死 10 MB；自造限流；错误 body 手写 |
| Testing | 边界（恰好等于/多 1 字节）、删除后恢复、他人不受影响、429 + `Retry-After`、一个并发测试 | 只测 happy path | 手测 |
| AI-supervision | 让 Claude 先找"有没有现成的限流/配额配置"；审出它"又写了一个令牌桶" | 事后清理 | 接受 AI 引入的 Redis/第三方库 |
| Communication | 讲清"逻辑 vs 物理"口径与多 worker 的 known gap | 提了口径没提 gap | 没提 |
