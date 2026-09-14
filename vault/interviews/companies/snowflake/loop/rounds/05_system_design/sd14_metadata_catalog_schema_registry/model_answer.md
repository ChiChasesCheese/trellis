# 模型答案：Distributed Metadata Catalog and Schema Registry

> 取材：Iceberg / Delta Lake 的不可变快照 + 乐观并发提交协议；Confluent Schema Registry 的
> 兼容性模式（backward/forward/full）；Snowflake 元数据集中在 **FoundationDB**、**Iceberg /
> Apache Polaris** REST catalog（`../../../01-company-brief.md` §1）。本题来源为聚合站，按
> 覆盖面练；题面本身承认"需求模糊"，下面先把模糊点自己澄清掉。

## 0. 两句话复述 + 不变量 + 先澄清模糊点

**复述**：一个被查询规划器高频读、被多个团队并发写的元数据目录：存数据集的 schema（含历史
版本）与物理位置，schema 演进要过兼容性校验，还要通过标准协议对外互操作。

**先澄清三个模糊点（题面故意留白）**：
1. **目录不管访问控制** ——谁能读/写某个数据集是另一个系统的职责（对应 sd13 的 ACL 服务），
   本题的目录只存"是什么、在哪、长什么样"。
2. **schema 版本粒度 = 每次成功的兼容性校验产生一个新版本**（不是按发布批次合并），保证每个
   版本号都对应一个曾经真实生效过的、消费者可能已经在用的 schema。
3. **多区域下有一个唯一的写权威区域**（source of truth），其它区域只读、带有界 staleness——
   类比 Snowflake Execution Anchor"每个实体恰好一个当前写者"的思路。

**不变量**：
1. schema 演进必须先通过兼容性校验才能被接受。
2. 同名数据集注册强一致，不允许两个并发请求都成功。
3. 已写入的 schema / manifest 版本永不修改（不可变快照）。
4. 读路径（schema + 位置查找）是全公司查询规划的热路径，不因写路径问题被拖慢。

**不做**：不做复杂血缘图查询（只存边，查询是另一个服务的事）；不做跨多个数据集的原子 DDL 事务
（每个数据集自己的注册/提交是强一致的，跨数据集的原子操作是明确的未来扩展，不是 baseline）。

## 1. API 契约

```
POST /datasets                          {name, namespace, initial_schema} → {id, schema_version=1}
                                         （名字冲突 → 409，强一致拒绝）
POST /datasets/{id}/schema              {new_schema, compatibility_mode} → {schema_version}
                                         （校验失败 → 409 + 具体冲突字段）
POST /datasets/{id}/commit              {base_version, new_manifest} → {manifest_version}
                                         （base_version 落后于当前 → 409，乐观并发）
GET  /datasets/{id}?schema_version=     → {schema, manifest_location, ...}
GET  /datasets/{id}/schema/history

# 外部引擎互操作（Iceberg REST catalog 风格）
GET  /v1/namespaces/{ns}/tables/{table}
POST /v1/namespaces/{ns}/tables/{table} （同样走 base_version 乐观并发提交）
```

## 2. 数据模型

- `datasets(id, name, namespace, current_schema_version, current_manifest_version,
  created_at)` —— 注册层，`(namespace, name)` 唯一约束，强一致存储。
- `schema_versions(dataset_id, version, definition, compatibility_mode, created_at)` —— 只增
  不改；`version` 单调递增。
- `manifest_versions(dataset_id, version, file_list_pointer, parent_version, created_at)` ——
  不可变快照，`current_manifest_version` 的推进 = 原子指针切换（compare-and-swap）。
- `lineage_edges(from_dataset, to_dataset, transform_ref)` —— 只存边，不在本服务里做图遍历。

## 3. 核心流程

**注册新数据集**：在强一致元数据存储上做条件插入（`(namespace, name)` 唯一），冲突直接 409。

**schema 演进**：
1. 取当前 schema，与新 schema 做结构 diff。
2. 按 `compatibility_mode` 校验：`backward`（新 schema 能读旧数据 —— 只能加可空字段/带默认值
   字段，不能删必填字段或收窄类型）、`forward`（旧 reader 能读新数据）、`full`（两者都要满足）。
3. 校验不通过 → 拒绝并返回具体冲突字段；通过 → 追加新的不可变 `schema_versions` 行，`datasets.
   current_schema_version` 原子推进。

**提交新文件清单**（摄取任务写完新数据后）：
1. 调用方带着自己读到的 `base_version` 提交新 manifest。
2. 服务端比较 `base_version == current_manifest_version`：相等才接受，原子切换指针到新版本，
   旧版本保留（Time Travel 式历史）；不相等 → 409，调用方拉取最新版本、必要时合并后重试。
3. 这就是**乐观并发**，避免两个摄取任务并发写同一张表时后写的静默覆盖前写的更新。

**读 schema + 位置**：优先从读副本/边缘缓存取；缓存条目带版本号，变更流推送新版本失效旧缓存，
兜底短 TTL。因为一切不可变+带版本号，**读到稍旧的指针只是读到一个仍然合法的旧快照**，不是脏读
——这是"读路径可以走有界延迟副本"这个设计能成立的根本原因。

## 4. 失败模式与规模

| 问题 | 处理 |
|---|---|
| 两个团队并发注册同名数据集 | 强一致存储的唯一约束/CAS 插入，后到者收到 409 |
| 两个摄取任务并发提交新文件清单 | 乐观并发（`base_version` 比对），冲突方拉取最新版本重试，不会静默丢更新 |
| 兼容性校验规则本身有 bug，放过了破坏性变更 | 影子回放：用消费者真实 pin 住的历史 schema 版本重放校验，不能只信结构化规则本身 |
| 读副本落后于写权威 | 因为版本不可变，staleness 是安全的；给读路径一个明确的 staleness 上界（如几百毫秒）写进 SLA |
| 消费者永远 pin 在旧 schema 版本不迁移 | 监控"pin 在旧版本超过阈值时间"的消费者数，主动通知/报警，不是无限期免费兼容 |
| 外部引擎通过 Iceberg REST 协议写，和内部乐观并发写路径冲突 | 外部协议适配层复用**同一套** `base_version` 乐观并发提交语义，不搞两套互不感知的写路径 |
| 血缘图查询变复杂 | 明确不做：本服务只存边，复杂遍历交给独立的血缘查询服务 |
| 高 QPS 读（每次查询规划都要查） | 变更流 + 边缘缓存承担绝大多数读；元数据存储只服务缓存 miss 与写路径 |

## 5. 分层与组件

```
注册 / schema 演进 API（无状态）：兼容性校验 · 条件写入
        ↓
元数据存储（强一致 source of truth）：datasets · schema_versions · manifest_versions
        ↓ 异步
变更流（新版本产生 → 广播）           lineage_edges（只存边，不做图遍历）
        ↓
读副本 / 边缘缓存（服务高 QPS 查找，有界 staleness）
外部协议适配层（Iceberg REST catalog ↔ 内部 API，复用同一套乐观并发提交）
```

## 6. Rollout / 测试 / 监控

- **灰度**：新的兼容性校验规则先"只记录、不拒绝"跑一段时间，统计会拦掉多少真实变更，再切换成
  强制模式；外部协议适配层先接一个外部引擎做金丝雀，观察其提交模式是否符合乐观并发假设。
- **监控**：提交冲突率（乐观并发重试次数，异常升高说明热点表写竞争激烈）；读副本相对写权威的
  staleness；兼容性校验误拒率；pin 在旧 schema 版本超过阈值时间的消费者数。
- **测试**：并发注册同名数据集只有一个成功；并发提交文件清单不丢更新；backward/forward/full
  三种兼容性模式各自的边界用例（加必填字段应该被拒、加可空字段应该通过）；读副本降级/滞后时
  查询规划仍能拿到一个自洽的旧快照而不是半写状态。

## 7. 用 Snowflake 自己的原语作参照

Snowflake 的表元数据（版本、micro-partition 清单）集中存在 **FoundationDB**，用**不可变快照 +
原子指针切换**实现 **Time Travel**（`AT(TIMESTAMP)` 本质就是读某个历史 manifest 版本）——和本题
的 `manifest_versions` + `base_version` 乐观并发提交完全同构。**Iceberg** 表格式与 **Apache
Polaris**（2026-02 成为 Apache 顶级项目的开源 REST catalog）正是本题"标准协议对外互操作，让
外部引擎也能读目录"这个要求的真实产品化。

## 8. 45 分钟口述时间表

| 分钟 | 内容 |
|---|---|
| 0–6 | 主动澄清三个模糊点（ACL 归属、版本粒度、多区域写权威）+ 四个不变量 + 不做什么 |
| 6–13 | API + 注册/schema/manifest 三层数据模型 |
| 13–24 | schema 演进兼容性校验流程；manifest 乐观并发提交流程 |
| 24–32 | 并发注册竞态、提交冲突、staleness 为什么安全、兼容性校验自身的校验 |
| 32–38 | 分层组件图；外部 Iceberg REST 协议适配层怎么复用同一套提交语义 |
| 38–42 | 灰度、监控指标、测试用例 |
| 42–45 | FoundationDB / Iceberg / Polaris 类比 + 反问 |
