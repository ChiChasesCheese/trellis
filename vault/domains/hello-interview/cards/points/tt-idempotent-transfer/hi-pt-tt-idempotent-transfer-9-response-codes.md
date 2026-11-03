---
id: hi-pt-tt-idempotent-transfer-9-response-codes
node: tt.lld.tt-idempotent-transfer.points
type: qa
step: 7
---
## Q
**幂等转账服务 · 返回码与响应丢失**｜追问 · 出自：幂等转账服务 › 取舍与追问

追问：转账已成功但响应丢了怎么办？各种情况返回什么状态码？

## A
**响应丢失。** 客户端重试得到保存的结果，看到成功，这正是设计目标。
**状态码。** 新建成功 201，重放返回同样的码和内容；`StillRunning` 用 409 加 `Retry-After`；`KeyReuse` 用 422。
