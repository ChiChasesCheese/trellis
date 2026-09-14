# 模型答案：ACL Authorization Checking Service

> 取材：通用集中式授权服务的公开设计模式（Google Zanzibar 论文的分层思路：关系型策略图 + 缓存
> 一致性 token）；Snowflake **Horizon** 治理统一层与 **AI Agent Identity**、RBAC/grant 在
> **FoundationDB** 里的表达（`../../../01-company-brief.md` §1、§5）。本题来源为聚合站，按覆盖
> 面练。

## 0. 两句话复述 + 不变量

**复述**：一个被几十个内部系统高频调用的集中授权服务，回答"主体能不能对分层资源执行某动作"，
支持角色继承、显式拒绝优先、吊销后有界时间内失效，并把"代表用户操作的 AI agent"当作一等主体。

**不变量**：
1. **deny 优先**：任意一条 deny（无论来自哪一层继承）永远覆盖所有 allow。
2. **有界吊销延迟**：一次吊销必须在约定的时间窗内（如 5 秒）对所有读路径生效，不存在"永久
   缓存出的已吊销权限"。
3. **可审计**：每次决策都记录主体、资源、动作、结果、依据的策略版本。
4. **委托而非快照**：agent 的权限 = agent 自身授权 ∩ 委托它的用户**此刻**的授权，随用户权限
   变化实时收窄，不是 agent 创建时的静态拷贝。

**不做**：不保证跨区域瞬时强一致；不是通用图数据库；批量"列出我能访问的资源"不保证与单次点查
一样的延迟 SLA（走单独的物化索引）。

## 1. API 契约

```
POST /authorize
  {principal, action, resource} → {decision: allow|deny, reason, policy_version}

POST /authorize/batch
  {principal, action, resources: [...]} → [{resource, decision}, ...]

PUT    /grants        {subject, permission, resource_pattern, effect, expiry?} → grant_id
DELETE /grants/{id}
PUT    /roles/{role}/assign  {principal, scope, expiry?}

GET /audit?principal=&resource=&since=&cursor=
```

## 2. 数据模型

- `principals(id, type: human|agent|service, delegated_by, delegation_expiry)` —— agent 的
  `delegated_by` 指向发起委托的用户；`delegation_expiry` 到期后该 agent 的一切授权自动失效。
- `resources(id, parent_id, type)` —— 层级：org → database → schema → table → column，天然
  有向无环；查询某资源的权限需要沿链向上找继承的 allow，但一旦任一层出现 deny 立即短路。
- `roles(id, name)` / `role_edges(parent_role, child_role)` —— 角色继承图，写入时做增量环检测，
  拒绝任何会形成环的边（同 S01 skill：RBAC/grant 就是一张 DAG，反向查询要走倒排索引）。
  `role_assignments(principal, role, scope, expiry?)`。
- `grants(subject, permission, resource_pattern, effect: allow|deny, policy_version,
  created_at)` —— `subject` 可以是 principal 或 role；`policy_version` 单调递增，每次写入
  产生新版本号，供缓存做一致性校验。
- 物化索引（异步刷新，不在写路径上）：`reachable_resources(principal) → resource id 集合`，
  服务批量"我能访问哪些资源"的场景，避免退化成 N 次点查。

## 3. 核心流程

**授权决策**：
1. 收到 `(principal, action, resource)`；先查本地/sidecar 缓存：命中且 `policy_version` 与
   最新已知版本一致 → 直接返回。
2. 未命中或版本落后：沿 `resource` 的父链 + `principal` 的角色继承链收集所有适用的 grant；
   任意一条 deny 短路返回 deny；否则若存在至少一条覆盖的 allow → allow；都没有 → 默认 deny。
3. 若 `principal` 是 agent：额外对 `delegated_by` 重新计算一遍决策，取两者的**交集**（agent
   决策 = agent 自身决策 AND 用户当前决策）。
4. 写审计（异步，见下）；把结果和当前 `policy_version` 写回本地缓存。

**授权变更 / 吊销**：
1. 写入新 `grant`（或删除旧 grant），策略存储原子递增 `policy_version`。
2. 向失效推送总线广播"哪些 `(principal 或 role, resource_pattern)` 受影响"；所有 sidecar 缓存
   订阅并主动删除对应条目。
3. 推送是**加速手段，不是正确性保证**——正确性来自每次决策都比对 `policy_version`；推送只是
   让大多数情况不必等 TTL 过期就失效，宽限期（如 5 秒 TTL 兜底）保证即使推送丢失，最坏情况的
   staleness 也有上界。

## 4. 失败模式与规模

| 问题 | 处理 |
|---|---|
| 缓存返回"已吊销却仍允许"的决策 | 版本号比对 + 推送失效 + 短 TTL 兜底；**staleness 有明确上界，写进 SLA，不是"尽量快"** |
| 角色继承图出现环 | 写入时增量环检测（新边只需检查是否能从子角色反向到达父角色），拒绝写入；不在读路径上判环 |
| 中心授权服务不可用 | 按资源敏感度分级：高敏感（PII/财务）**fail-closed**；低敏感只读场景用断路器 + "上一次已知良好决策 + 短宽限期"降级，超过宽限期同样转 fail-closed；两档都要显式配置，不能全局 fail-open |
| 热点资源（共享表被几千个查询同时校验） | sidecar 本地缓存 + 推送失效，避免每次打中心服务；中心服务按 principal/resource 哈希分片扩展读吞吐 |
| Agent 委托链断裂（delegating 用户被删/离职） | `delegation_expiry` 到期或 `delegated_by` 失效 → 该 agent 所有决策退化为 deny，不是"继续用旧权限" |
| 审计写入失败 | 决策返回不等待审计落盘；审计走本地持久化队列异步 flush，失败重试 + 定期对账"决策数 == 审计条数"，差异报警 |
| 批量"列出可访问资源" | 不走 N 次点查；查预计算的 `reachable_resources` 物化索引，允许若干分钟的过期窗口 |
| 规模：几十亿次/天授权检查 | 读路径几乎全部命中 sidecar 缓存；中心服务只服务缓存 miss 与写路径；策略图按 principal/role 哈希分片 |

## 5. 分层与组件

```
客户端 SDK / sidecar 缓存（本地判定，订阅失效推送，兜底 TTL）
        ↓ 缓存 miss
授权 API（无状态）：收集 grant · deny 优先短路 · agent∩delegator 求交
        ↓
策略存储（强一致，版本化 source of truth）：principals · resources · roles · grants
        ↓ 异步
继承图环检测 + reachable_resources 物化索引（离线/近实时刷新）
失效推送总线（策略变更 → 广播给所有 sidecar）
审计服务（独立写路径，异步、可重放、对账）
```
唯一的强一致状态是策略存储；缓存与物化索引都是可重建的派生数据。

## 6. Rollout / 测试 / 监控

- **灰度**：新服务与旧权限判断逻辑并行跑（影子模式），逐条 diff 决策差异，尤其关注"新服务多
  放行了什么"——这是唯一不能容忍的方向；先上线只读校验路径，再切写路径。
- **监控**：吊销到全部读路径生效的 p99 延迟（核心 SLA 指标）；误放行次数（目标 0，出现即
  page）；审计完整率（决策数 vs 审计落盘数的差异）；角色继承图环检测拒绝次数；agent 决策里
  "因委托用户权限收窄而被拒绝"的次数（验证不变量 4 生效）。
- **测试**：并发"授权检查"与"吊销"竞态；delegated 用户权限收窄后 agent 立即失去对应权限；批量
  接口与单次点查结果一致；策略存储只读降级下高敏感资源的行为；故意构造环形角色继承确认写入
  被拒。

## 7. 用 Snowflake 自己的原语作参照

Snowflake 的 **Horizon** 就是这套设计在生产里的对应物：跨数据资产的统一治理层，RBAC/grant 图
存在 **FoundationDB**（强一致、版本化），2026 年 GA 的 **AI Agent Identity** 正是"agent 不是
静态快照权限，而是委托用户当前权限的受限子集"这条不变量的产品级实现——agent 的访问范围随委托
它的用户的权限变化而变化，而不是在 agent 创建时固定下来。

## 8. 45 分钟口述时间表

| 分钟 | 内容 |
|---|---|
| 0–5 | 复述 + 四个不变量（deny 优先、有界吊销延迟、可审计、委托非快照）+ 不做什么 |
| 5–12 | API + 身份/资源/策略三层数据模型 + agent 主体的 `delegated_by` |
| 12–22 | 授权决策流程；吊销与缓存竞态（版本号 + 推送 + TTL 兜底） |
| 22–30 | 环检测、fail-open vs fail-closed 分级降级、热点资源、审计写放大 |
| 30–37 | 分层组件图；批量查询走物化索引不是 N 次点查 |
| 37–42 | 灰度 diff、监控指标、测试用例 |
| 42–45 | Horizon / AI Agent Identity 类比 + 反问 |
