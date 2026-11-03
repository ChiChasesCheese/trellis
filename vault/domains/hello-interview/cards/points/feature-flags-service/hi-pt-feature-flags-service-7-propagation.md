---
id: hi-pt-feature-flags-service-7-propagation
node: qb.sd.feature-flags-service.points
type: qa
step: 4
---
## Q
**功能开关服务 · 配置传播与快照**｜必会 · 出自：功能开关服务 › 深入 2

改了开关多快生效？SDK 怎么拿到并更新规则？为什么快照要有版本号、做成不可变对象？

## A
**传播。** 快照（JSON 加版本号）发布到对象存储挂 CDN；SDK 启动拉取，之后每 10～30 秒带 `ETag` 轮询（无变化回 304），可选 SSE/发布订阅推送把延迟缩到秒级；紧急熔断走推送。
**版本。** SDK 只接受更高版本，不被迟到的旧快照覆盖；快照不可变、整体替换，一个请求内取一次引用，天然线程安全。
