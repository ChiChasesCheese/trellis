# 模型答案：REST API 的 RPC 抽象层

## 0. 复述 + 不变量

**复述**：几十个 REST 服务，各自的鉴权、分页、错误、限流都不同；给 Java / Python / Go 调用方提供像本地函数一样的 typed 调用，统一处理横切关注点；后端持续加接口、偶尔不兼容改版；写操作不能因重试执行两次。

**先问的问题**：要的是客户端库、中心网关，还是都要？延迟预算多少？调用方能否接受代码生成？

**不变量**：写操作至多执行一次；调用方看不到 HTTP 细节；老版本 stub 在弃用期内继续可用；每次调用可追踪（`request_id`）。**不做**：业务校验、服务网格级流量治理。

## 1. 接口描述（真相源）

```yaml
service: billing
version: v2
auth: oauth_client_credentials
methods:
  getInvoice:
    http: GET /v2/invoices/{id}
    idempotent: true
    returns: Invoice
    errors: {404: NOT_FOUND, 409: CONFLICT}
  listInvoices:
    http: GET /v2/invoices
    pagination: {style: cursor, request: page_token, response: next_page_token}
    returns: stream<Invoice>
  chargeCustomer:
    http: POST /v2/charges
    idempotent: false            # 只有带 Idempotency-Key 才允许重试
    idempotency_header: Idempotency-Key
```

构建期从这份描述生成三种语言的 typed stub；stub 只做参数绑定，逻辑都在共享运行时。

## 2. 运行时：middleware 链

```
stub 调用
 → auth（按服务选策略；token 缓存 + 过期前刷新 + singleflight）
 → deadline（整体 deadline 向下游传播为 header）
 → retry（只重试可重试错误；指数退避 + 抖动；重试预算 ≤ 请求量的 10%）
 → circuit breaker（按目标服务 + 方法）
 → metrics / tracing（延迟直方图、错误码、重试次数、request_id）
 → transport（连接池、HTTP/2、TLS）
```

统一错误模型：`ApiError{code, retryable, http_status, message, request_id}`，每服务适配器把各自错误体映射进来。

## 3. 关键流程

**读**：stub → 链 → 失败且 `retryable` 且预算够 → 退避重试；429 读 `Retry-After`。
**写**：调用方不传幂等键时，SDK 自动生成 UUID 并在本次调用的所有重试中复用；后端（或网关）按 `(service, key)` 存结果 24 小时，重复请求直接返回首次结果。后端不支持幂等键的写接口，SDK **不重试**，把"结果未知"作为独立错误码抛给调用方。
**分页**：适配器把 offset / cursor / link-header 统一成迭代器；迭代器记住最后成功的游标，失败后可续传。

## 4. 失败模式

| 问题 | 处理 |
|---|---|
| 重试风暴放大故障 | 重试预算 + 熔断 + 抖动 |
| 写操作超时但实际成功 | 幂等键去重；无幂等键则不重试、报 `UNKNOWN_OUTCOME` |
| token 同时过期、并发刷新 | singleflight，过期前 10% 提前刷新 |
| 后端不兼容改版 | IDL 版本化；旧 stub 打旧端点；CI 做 IDL diff 拦截破坏性变更 |
| 三种语言行为不一致 | 契约测试：同一套用例跑三种 SDK 对同一个 mock server |
| 深分页中途失败 | 迭代器从最后成功游标续传 |

## 5. 库 vs 网关

- **只做 SDK**：延迟最低，但策略更新要所有调用方升级。
- **只做网关**：策略集中、跨语言一致，但多一跳、网关本身要高可用。
- **推荐组合**：SDK 负责本地关注点（超时、重试、熔断、分页、类型）；网关负责要集中管的策略（限流配额、审计、幂等存储）。

## 6. 发布与验证

契约测试进 CI；IDL diff 检查破坏性变更；SDK 语义化版本；新重试策略按服务灰度开关；仪表盘看每方法错误率、重试率、熔断打开次数。

## 7. Snowflake 参照

Snowflake 的 JDBC / ODBC / Python / Go 驱动是"同一协议、多语言客户端"：共享 REST 协议、统一错误码、会话 token 刷新、结果分块拉取。把 SDK 的"分页迭代器"类比成驱动的"结果集分块下载"，面试时是自然的桥接。

## 8. 45 分钟时间表

| 分钟 | 内容 |
|---|---|
| 0–5 | 形态澄清（SDK / 网关）+ 不变量 |
| 5–15 | IDL 与代码生成、统一错误模型、分页迭代器 |
| 15–28 | middleware 链：鉴权、deadline、重试预算、熔断 |
| 28–36 | 写操作幂等、版本演进 |
| 36–42 | 库 vs 网关取舍 |
| 42–45 | 测试与监控、反问 |
