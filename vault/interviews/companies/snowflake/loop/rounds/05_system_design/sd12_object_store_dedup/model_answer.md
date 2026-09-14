# 模型答案：带内容去重的对象存储

> 取材：内容寻址存储（CAS）通用做法；Git/restic/Dropbox 的分块去重；Snowflake clone 共享 micro-partition 与 Time Travel / Fail-safe 延迟回收（`../../../../01-company-brief.md` §2.2）。本题来源为聚合站，按覆盖面练。

## 0. 两句话复述 + 不变量

**复述**：一个按 `bucket/key` 读写的对象存储，底层按内容去重，让相同字节只存一份；删除、覆盖、续传、跨租户隔离都要对用户透明。

**不变量**：
1. **可读性**：一个未删除的 key 版本，永远能读到它写入时的完整内容。
2. **安全回收**：物理块只在确定无任何清单引用、且过了宽限期后才删除。
3. **不可变块**：块按内容哈希寻址，写入后永不修改。
4. **隔离**：去重不泄露其它租户是否存过某内容。

**不做**：不保证删除后立即释放空间；`LIST` 最终一致；不做跨区域强一致。

## 1. API 契约

```
PUT    /b/{bucket}/{key}                         小对象（< 8 MB）一次上传 → {version, etag}
POST   /b/{bucket}/{key}?uploads                 InitiateMultipart → upload_id
PUT    /b/{bucket}/{key}?upload_id=&part=n       UploadPart（可重试，幂等于 part 号）
POST   /b/{bucket}/{key}?upload_id=              Complete([part etags]) → {version}
GET    /b/{bucket}/{key}[?version=]  Range: …    读
DELETE /b/{bucket}/{key}                         写 tombstone 版本
GET    /b/{bucket}?prefix=&cursor=               列表（分页，最终一致）
```

## 2. 数据模型

- `objects(bucket, key, version) → {manifest_id | tombstone, size, created_at}` —— 命名层，按 `hash(bucket,key)` 分片，覆盖即写新版本。
- `manifests(manifest_id) → {chunk_hashes: [h1, h2, …], total_size}` —— 清单层，不可变。
- `chunks(scope, hash) → {location, size, created_at}` —— 块索引；`scope` = 租户 id（去重域）。
- 块本体：对象存储 / 分布式文件系统里的不可变 blob，路径由 `scope/hash` 决定。

## 3. 核心流程

**上传**：
1. 前端流式读入，**分块**：默认固定 8 MB；对备份类负载用内容定义分块（Rabin 滚动哈希，平均 4 MB，边界随内容移动，插入少量字节不会让后续所有块失配）。
2. 每块算 SHA-256；批量问块索引"`scope` 下哪些 hash 已存在"。
3. 不存在的块：写 blob（先写临时路径再原子重命名）→ 写块索引（条件插入，已存在则放弃自己的副本）。
4. 所有块就绪后写清单，再**在一个元数据事务里**写 `objects` 新版本指向该清单。只有这一步成功，对象才对用户可见。

**下载**：读 `objects` 最新非 tombstone 版本 → 清单 → 并行按 range 取块。

**删除 / 覆盖**：只写新版本（tombstone 或新清单），不碰块。

**回收（mark-and-sweep）**：
1. **mark**：周期性扫描所有存活版本的清单，把引用到的 `(scope, hash)` 标上本轮 epoch。
2. **sweep**：删除 `last_marked_epoch < current - 1` 且 `created_at` 早于宽限期（如 24 小时）的块。
3. 宽限期覆盖了"块刚写入、清单还没提交"的窗口，所以正在上传的块不会被扫走。

## 4. 失败模式与规模

| 问题 | 处理 |
|---|---|
| 上传查到块存在，之后回收器把它删了，清单指向空块 | 宽限期 + 回收只删"上一轮以前就未被标记"的块；写清单前再次确认块存在（或给块续一个 `last_referenced_at`） |
| 引用计数方案崩溃导致计数漂移 | 不依赖精确计数；用可达性扫描作为真相，计数只作快速路径的估计 |
| 分块上传中断 | part 按号幂等；`upload_id` 过期后未完成的块由回收器按宽限期处理 |
| hash 碰撞 | SHA-256；写入时校验长度，碰撞概率可忽略但记监控 |
| 跨租户"秒传"侧信道 | 去重域 = 租户；如需全局去重，上传路径永远真实传输字节，只在服务端后台合并 |
| 热门块读放大 | 热块多副本 / 缓存；清单并行读 |
| 元数据规模（数百亿对象） | 命名层按 bucket/key 哈希分片；清单与块索引按 hash 分片（天然均匀） |
| LIST 大前缀 | 二级索引 `(bucket, key 前缀)`，游标分页，最终一致 |

规模：每天 PB 级新增 ÷ 8 MB 块 ≈ 每天 1.25 亿块；块索引按 hash 均匀分片，写入吞吐线性扩展。

## 5. 分层与组件

```
API 前端（无状态）：鉴权 · 分块 · 算 hash · 流式上传/下载
元数据服务（强一致，分片）：objects 版本 · manifests · chunks 索引
块存储（不可变 blob）：只写一次，按 scope/hash 寻址
回收器（离线）：mark 可达块 · sweep 过期未标记块
```
唯一可变状态在元数据服务；块永不修改；回收与写路径解耦。

## 6. Rollout / 测试 / 监控

- **灰度**：先影子模式只算 hash 统计去重率、不改写路径；再对新写入启用；最后后台迁移存量。
- **回收**：先 dry-run 只标记、报告"将要删除"的量，人工核对后开启真实删除。
- **监控**：去重率；块索引大小；回收积压；可达性扫描与引用计数的差异；读到缺失块的次数（必须为 0，出现即 page）。
- **测试**：并发上传同一内容；上传与回收并发；删除一个 key 后另一个共享内容的 key 仍可读；覆盖后旧内容在宽限期后被回收。

## 7. 用 Snowflake 自己的原语作参照

Snowflake 的 **zero-copy clone** 就是"多个表共享同一批不可变 micro-partition"，删除一个表不影响 clone；真正释放存储要等 **Time Travel** 保留期和 **Fail-safe** 7 天都过去——这正是本题"引用消失后宽限期再回收"的产品级版本。元数据（哪个表版本引用哪些分区）集中在 **FoundationDB**，块（分区）本身不可变，和本题的分层完全同构。

## 8. 45 分钟口述时间表

| 分钟 | 内容 |
|---|---|
| 0–4 | 复述 + 四个不变量 + 不做什么 |
| 4–10 | API（含分块续传）+ 三层数据模型 |
| 10–20 | 上传 / 下载 / 删除覆盖流程；固定分块 vs 内容定义分块 |
| 20–30 | 回收：mark-and-sweep + 宽限期；与上传的竞态 |
| 30–37 | 跨租户侧信道、碰撞、热点、元数据分片 |
| 37–42 | 灰度、dry-run、监控 |
| 42–45 | Snowflake clone / Time Travel 类比 + 反问 |
