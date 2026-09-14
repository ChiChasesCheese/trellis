# 评分 rubric（五维，1–4 分/维）

## 1. Problem framing
- **1 分**：直接开始写一个 `HttpClient` 包装类，不区分库和网关，不谈写操作重试的风险。
- **4 分**：先澄清形态（客户端 SDK / sidecar / 中心网关 / 组合）；列出要统一的横切关注点：鉴权、超时、重试、限流、分页、错误模型、追踪；不变量：**写操作至多执行一次**（重试不重复扣费）、调用方不感知后端 REST 细节、后端改版不打断老调用方；非目标：不替后端做业务校验、不做服务发现以外的流量治理。

## 2. API & data model
- **1 分**：每种语言手写一套客户端，靠文档对齐。
- **4 分**：**单一接口描述为真相源**（OpenAPI 或内部 IDL：方法名 → HTTP 动词、路径模板、参数位置、响应 schema、分页方式、是否幂等、错误码映射）；代码生成三种语言的 typed stub；共享一个小的运行时核心（transport + middleware 链）；统一错误模型 `{code, retryable, message, details, request_id}`；分页抽象成迭代器 `for inv in billing.listInvoices(...)`，屏蔽 offset / cursor 差异；写操作带 `Idempotency-Key`。

## 3. Failure modes & scale
- **1 分**："失败就重试三次"，不分读写、不分错误类型。
- **4 分**：只重试**可重试错误**（连接失败、502/503/504、429）；429 尊重 `Retry-After`；指数退避 + 抖动 + **重试预算**（防止重试风暴放大故障）；写操作只在带幂等键时重试，后端按键去重；超时分层（连接 / 单次请求 / 整体 deadline，deadline 向下游传播）；熔断器按目标服务隔离；鉴权 token 过期时单飞刷新（singleflight）避免雷群；分页中途失败可以从上次 cursor 续传；后端不兼容改版：IDL 带版本，旧 stub 继续打旧版本端点，弃用期内双版本共存。

## 4. Separation of concerns
- **1 分**：一个巨大的客户端类里 if/else 处理所有服务的差异。
- **4 分**：分层清楚——IDL 与代码生成（构建期）→ 生成的 typed stub（每服务一份，薄）→ 运行时 middleware 链（auth → deadline → retry → circuit breaker → metrics/tracing → transport）→ 每服务的**适配器**只描述差异（分页风格、错误映射、鉴权方式），不写逻辑；可选中心网关承担跨语言一致的策略（限流、审计），SDK 承担低延迟的本地关注点。

## 5. Delivery beyond the diagram
- **1 分**：没提怎么发布、怎么验证。
- **4 分**：契约测试（IDL 生成 mock server，三种语言跑同一套用例）；兼容性检查进 CI（IDL diff 检测破坏性变更）；SDK 版本与后端版本矩阵；灰度：新 middleware（如新重试策略）按服务开关；指标：每方法延迟 / 错误率 / 重试次数 / 熔断打开次数，统一 `request_id` 串起调用链。
