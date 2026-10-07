# REPORT · cb06_filevault

> 由编排者代存（子代理被拒写 REPORT.md）；数字已由编排者重跑：验收 41 passed（约 1.5 s）· `IMPL=starter -m core` 25 failed / 16 deselected · starter 95 passed · solution 133 passed · 朴素去重（`tmp/cb06_naive/run.sh naive-t1`）2 个并发 core 测试红 · 朴素配额 1 红。

## Summary

`filevault`：多用户文件存储服务（`X-User-Id` → 用户；JSON/base64 上传 → `FileService` → sqlite 元数据 + `BlobStore` 字节），照 Abnormal 真实 take-home "File Vault"（`../../../catalog/raw/ai_round_sweep_2026-10-07.md`：去重 + 搜索过滤 + 配额/统计 + metrics + GenAI 录屏）的形态原创，用标准库重造并把**并发正确性**做成可验收的难点。t1 去重（含上传/删除并发）· t2 搜索与过滤 · t3 配额 + 统计 + 限流。`walkthrough.md` 末尾有 5 分钟"讲你怎么用 AI"的录屏提纲。

## 代码库地图（`starter/`）

| 模块 | 一句话 |
|---|---|
| `filevault/cli.py`, `__main__.py` | `serve` / `upload` / `ls` / `fsck`（`--data-dir` 全局） |
| `filevault/app.py` | 组合根：`create_app(data_dir, settings=, store=, clock=, env=)` |
| `filevault/config.py`, `config/default.toml` | `Settings`、tomllib + `FILEVAULT_<KEY>` 覆盖、严格校验；`quota_bytes_per_user` / `rate_limit_per_sec` / `admin_users` 已在配置里但无人读取 |
| `filevault/service.py` | `FileService`：upload / get / read / list_files / delete；API 与 CLI 共用 |
| `filevault/models.py`, `errors.py`, `validation.py`, `timeutil.py` | `FileRecord`；领域错误（`InvalidInput(field, …)`）；校验；UTC ISO 时间与可注入 `Clock` |
| `filevault/storage/` | `BlobStore` 接口；`LocalDiskStore`（原子替换）、`InMemoryStore` |
| `filevault/store/` | `Database`（每线程连接、迁移、**无人使用的** `transaction()`）、`FileRepository`、`Where`（参数化条件）、`paginate`（keyset 游标） |
| `filevault/api/` | `framework.py`、`app.py`（`X-User-Id` 认证、`translate` 领域错误 → HTTP）、`testing.py`、`routes/files.py`、`routes/health.py` |
| `filevault/metrics.py`, `ratelimit.py` | 计数器（已有 `uploads_total`）；`TokenBucket`（**未挂到任何端点**） |
| `filevault/maintenance.py` | `fsck`（数据库 vs blob 存储） |
| `filevault/legacy/hash_index.py` | deprecated 的 md5 内存索引，半成品 |
| `fixtures/uploads.json` | 9 条样本（含注入文件名 `x' OR '1'='1.pdf`、含 `%`/`_` 的文件名、多用户） |
| `README.md` | **一处过时**：声称 `legacy/hash_index.py` 用于去重 |

## 规模（实测）

| 项 | starter | solution |
|---|---|---|
| Python 文件 / 行数 | 44 / 2,067（包 1,355 + 测试 712） | 46 / 2,716（包 1,631 + 测试 1,085） |
| 全部文件 | 50 | — |
| 自带测试 | 95 passed，0.22 s | 133 passed，0.36 s |
| 验收 | `IMPL=starter -m core`：25 failed，16 deselected；`-m regression`：8 passed | 41 passed，约 1.6 s |

## 埋点清单

### t1 去重
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `store/db.py:Database.transaction`（已有、无人使用） | upload/delete 各在一个写事务里做"引用计数 + 写/删字节"，唯一约束 `ON CONFLICT` 决定谁写字节 | `threading.Lock`；先 `SELECT` 再 `INSERT` |
| 必须复用 | `storage/base.py:BlobStore` | 内容哈希作为 blob 路径，仍走 `put/get/delete` | 直接 `open()` 写磁盘 |
| 必须复用 | `store/migrations/` + `Database.migrate`、`metrics.incr` | 新 `0002_*.sql`；`dedup_hits_total`、`bytes_saved` | 改 `0001`；全局变量 |
| 看起来像但不该改 | `legacy/hash_index.py` 与 README 的说法 | 不碰 | 扩展 md5 索引 |
| 模糊点 | 跨用户去重？回填？侧信道？ | 问；默认跨用户、不回填、说出耗时侧信道 | 合并成一条共享记录，丢掉各自的文件名/时间 |
| 隐蔽时序 | delete 与同内容 upload 交错 | 删字节也在同一事务里 | 事务外删文件，删掉刚被引用的 blob |

### t2 搜索
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `store/query.py:Where`（列名/运算符白名单） | 新增条件方法，值全是绑定参数 | f-string 拼 SQL（夹具里的注入文件名当场暴露） |
| 必须复用 | `store/pagination.py:paginate` + `FileRepository.list_for_owner` | 过滤并进同一个 `Where`，保持 keyset 游标 | `OFFSET` 分页；另写 `/search`；全取回再过滤 |
| 必须复用 | `errors.py:InvalidInput` + `api/app.py:translate`、`timeutil.parse_iso` | 校验抛 `InvalidInput` → 400 + `details.field` | 手写 400 body |
| 看起来像但不该改 | `GET /files` 的响应形状 | 保持 `items` / `next_cursor` | 换新格式，破坏现有客户端 |
| 模糊点 | `type` 是 MIME 还是扩展名？边界？无时区日期？`%`/`_` 通配符？ | 默认 MIME 精确、含边界、无偏移视作 UTC、通配符转义 | `q=100%` 误匹配一切 |

### t3 配额 + 统计 + 限流
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `ratelimit.py:TokenBucket` | 按用户建桶挂到 `POST /files`，`Retry-After` 来自 `seconds_until` | 重写令牌桶；`time.sleep` |
| 必须复用 | `config.py:Settings`（三个键已存在） | 直接读取 | 常量 `10 * 1024 * 1024` |
| 必须复用 | `Database.transaction`、`translate` + `ApiError.headers` | 配额检查与插入同一写事务；413 / 429 + `Retry-After` | 事务外检查，并发超卖 |
| 看起来像但不该改 | `max_upload_bytes`（同为 413） | 区分"单文件过大"与"超配额" | 拿它充当配额 |
| 模糊点 | 逻辑还是物理占用？谁是 admin？限流范围？多 worker？ | 默认逻辑占用、读 `admin_users`、只限 `POST /files`、内存桶（说出多 worker 缺口） | 按物理占用 |

## 验收测试清单

| ticket | core | stretch | regression | 合计 |
|---|---|---|---|---|
| t1 | 7 | 2 | 3 | 12 |
| t2 | 10 | 3 | 2 | 15 |
| t3 | 8 | 3 | 3 | 14 |

只用已有入口：`create_app(data_dir, clock=, env=, store=)`、`TestClient`（`X-User-Id`，JSON/base64）、`filevault.metrics`、`data_dir/blobs`；新名字只有 ticket 点名的。并发验收（t1 两个、t3 一个）用线程 + `threading.Barrier`，各重复 8 轮，并通过 `create_app(store=...)` 注入一个每次 `put`/`exists`/`delete` 睡 50 ms 的 `LocalDiskStore` 子类（`cb06_support.slow_local_store`）放大 check-then-act 窗口。实测：SELECT 再 INSERT 且不用 `transaction()` 的朴素去重，t1 两个并发 core 测试 5/5 次全红；配额检查挪到事务外的朴素实现，t3 并发超卖测试 5/5 次红；solution 全套 5/5 绿。

## solution 改动行数（`diff -ruN -x __pycache__`，按 starter → t1 → t2 → t3 逐步快照）

| ticket | 总行数 | 其中测试 |
|---|---|---|
| t1 | 178 | 82 |
| t2 | 247 | 149 |
| t3 | 285 | 142 |
| 合计（含 README 14 行） | 724 | 373 |

## 最弱处

- t2 `type` 只按 MIME 精确匹配；t3 限流测试依赖两次上传落在同一秒内；"重复内容计入配额"是 stretch（逻辑 vs 物理是设计选择）。
