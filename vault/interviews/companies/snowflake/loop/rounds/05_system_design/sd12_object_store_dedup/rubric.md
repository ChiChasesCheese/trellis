# 评分 rubric（五维，1–4 分/维，满分 20）

## 1. Problem framing

- **1 分**：直接说"算个 hash，一样就不存"，没有提删除、覆盖、并发、跨租户。
- **4 分**：复述后说出不变量：**任何可见的 key 永远能读到它写入时的内容**（删除/覆盖别的 key 不影响它）；**物理块在仍有引用时绝不回收**；**去重对用户不可见且不泄露跨租户信息**；明确"不做"：不保证回收实时、不做强一致的全局 list。确认规模、对象大小分布、读写比。

## 2. API & data model

- **1 分**：只有 `objects(key, hash)` 一张表；没有分块；没有引用计数或可达性。
- **4 分**：API：`PUT`（小对象一次，大对象 `InitiateMultipart / UploadPart / Complete`）、`GET`（支持 range）、`DELETE`、`LIST prefix`；数据模型分三层——**命名层** `objects(bucket, key, version, manifest_id, created_at, deleted)`（覆盖 = 新版本）、**清单层** `manifests(manifest_id, [chunk_hash...], size)`、**块层** `chunks(tenant_scope, chunk_hash, location, size, refcount 或 last_seen_epoch)`；内容寻址键 = `hash(content)`，去重域 = 租户（或显式共享域）。

## 3. Failure modes & scale

- **1 分**：引用计数加减不考虑崩溃；删除就立刻删块；没意识到"查到块存在后、写引用前，块被回收"的竞态。
- **4 分**：讲清**上传与回收的竞态**：新引用必须在"块存在性检查"与"回收"之间原子化——用 **mark-and-sweep + 宽限期**（回收只删"最近 N 小时没有被任何清单引用、且早于宽限期"的块）或在同一事务里 `refcount+1`；引用计数漂移靠周期性全量可达性扫描校正；**大对象分块**（固定 4–8 MB 或内容定义分块 CDC 抗插入偏移）+ 分块续传；hash 碰撞用 SHA-256 并在写入时校验长度；**跨租户侧信道**：去重域限定在租户内，或全局去重但上传路径永远真实传输字节（不做"秒传"）；热点块副本放大；元数据按 bucket/key 哈希分片。

## 4. Separation of concerns

- **1 分**：一个服务同时管命名、存块、算引用。
- **4 分**：**前端/API 层**（无状态，鉴权、分块、算 hash）→ **元数据服务**（命名层 + 清单层，强一致、分片）→ **块存储**（不可变内容寻址 blob，只增不改）→ **回收器**（离线 mark-and-sweep，独立于写路径）。块一旦写入永不修改，所有可变状态集中在元数据。

## 5. Delivery beyond the diagram

- **1 分**：画完就停。
- **4 分**：去重率、回收积压、引用计数与可达性扫描的差异数作为核心指标；灰度：先"只算 hash 不去重"影子运行统计去重率与碰撞，再开启；回收先 dry-run 只标记不删除；故障演练：回收器与上传并发、元数据分片迁移中上传。能类比 Snowflake：clone 共享 micro-partition、删除要等 Time Travel 与 Fail-safe 窗口过去。
