# 评分 rubric（五维，1–4 分/维，满分 20）

## 1. Problem framing

- **1 分**：直接开始画"一个数据库存 schema"，不主动澄清"需求模糊"在哪，不提兼容性校验、并发
  注册、多版本 pin、外部协议互操作。
- **4 分**：**主动列出并自己回答**几个模糊点（这是这题的题眼）：schema 版本粒度是每次变更一个
  版本还是按发布批次；目录是否也管访问控制（明确回答"不管，那是 sd13 的职责，目录只存元数据"）；
  多区域下谁是写权威。说出不变量：**schema 演进必须先过兼容性校验才能被接受**；**同名数据集
  的注册必须强一致，不能两个并发请求都成功**；**每一个历史 schema / manifest 版本一旦写入永不
  修改**，消费者可以 pin 住旧版本；**读路径（schema + 物理位置查找）是全公司查询规划的热路径**，
  不能被写路径的问题拖慢或拖挂。

## 2. API & data model

- **1 分**：一张 `tables(name, schema_json, location)` 表，原地更新，没有版本、没有兼容性模式、
  没有对外协议。
- **4 分**：API：`POST /datasets`（强一致创建，名字冲突即拒绝）、`POST /datasets/{id}/schema`
  （带 `compatibility_mode`，校验失败返回具体冲突字段）、`POST /datasets/{id}/commit`（提交新
  文件清单，**乐观并发**，带 `base_version`）、`GET /datasets/{id}?schema_version=`（可 pin 老
  版本）、外部协议适配层（Iceberg REST catalog 风格的 `GET/POST /v1/namespaces/.../tables/...`）。
  数据模型三层——**注册层** `datasets(id, name, namespace, current_schema_version,
  current_manifest_version)` 名字唯一约束；**schema 层** `schema_versions(dataset_id, version,
  definition, compatibility_mode)` 只增不改；**清单层** `manifest_versions(dataset_id, version,
  file_list_pointer, parent_version)` 不可变快照 + 原子指针切换。

## 3. Failure modes & scale

- **1 分**：schema 变更直接原地覆盖，不校验兼容性；两个并发的文件清单提交谁后写谁赢，没有意识
  到会丢更新；没提读路径怎么扛高 QPS。
- **4 分**：**并发注册同名数据集**——强一致存储上的唯一约束/CAS 拒绝第二个；**并发提交文件清单**
  ——**乐观并发控制**：提交必须带 `base_version`，与当前版本不一致就拒绝、调用方重新读最新版本
  再重试（同 Iceberg/Delta 的原子提交协议）；**读路径 staleness 是安全的，因为一切都不可变且带
  版本号**——读到稍旧的指针只是读到一个仍然有效的旧快照，不是脏读，这是允许读走有界延迟副本而
  不牺牲正确性的关键洞察；**兼容性校验本身可能有 bug**——用消费者真实 pin 住的 schema 版本做
  影子回放校验，不能只信结构化规则；**规模**：schema/manifest 查找走带失效推送的边缘缓存或订阅
  变更流，不是每次查询规划都打元数据存储。

## 4. Separation of concerns

- **1 分**：注册、兼容性校验、文件清单提交、对外协议适配全部糅在一个服务里。
- **4 分**：**注册 / schema 演进 API**（校验 + 写入）→ **元数据存储**（强一致 source of truth：
  注册表、schema 版本、manifest 版本）→ **变更流**（新版本产生后广播，供下游订阅而非轮询）→
  **读副本 / 边缘缓存**（服务高 QPS 的 schema+位置查找，带有界 staleness）→ **外部协议适配层**
  （把 Iceberg REST catalog 协议的调用翻译成内部的 commit/read，不污染内部数据模型）。血缘图
  存边但**明确不做**复杂图查询（那是独立服务的职责，本题只负责存储）。

## 5. Delivery beyond the diagram

- **1 分**：画完就停。
- **4 分**：灰度——新的兼容性校验先以"只记录不拒绝"的影子模式跑一段时间，统计会拦掉多少真实
  变更再切换成强制；外部协议适配层先接入一个外部引擎做金丝雀；核心指标：提交冲突率（乐观并发
  重试次数）、读副本相对写权威的 staleness、兼容性校验误拒率、pin 在旧版本超过阈值时间的消费者
  数（迁移卡住的信号）；故障演练：并发提交风暴、元数据存储只读降级时读路径是否还能工作。能类比
  Snowflake：FoundationDB 里的不可变快照 + 原子指针切换就是 Time Travel 的实现方式，Iceberg /
  Apache Polaris 就是本题"标准协议对外互操作"要求的产品化版本。
