---
id: correctness-idempotency-key-design
node: correctness.idempotency
type: qa
---
## Q
Design the idempotency-key flow for a `POST /payments` endpoint (Stripe-style). Who generates the key, what does the server store, and what does a retry get back?

## A
- **Client generates** the key (UUID) *per operation intent* — one key per "charge this cart once", reused across all retries of that intent, never per HTTP attempt.
- Server, in the **same transaction** as the side effect, inserts the key into a keyed store (unique constraint) along with request hash and, on completion, the **serialized response**.
- A retry with the same key returns the **stored original response** (same status code and body) — it does not re-execute.
- If the retry's request body differs from the stored hash, reject with 422: same key + different params is a client bug, not a retry.

## Q zh
为 `POST /payments` 端点（Stripe 风格）设计幂等性 key 流程。谁生成 key，服务器存什么，重试获得什么？

## A zh
- **客户端生成** key（UUID），*每个操作意图* — 一个 key 对应一次"扣这个购物车"，在该意图的所有重试间复用，绝不是每个 HTTP 尝试一个。
- 服务器在与副作用**同一事务**内，将 key 插入 keyed store（unique 约束），记录请求哈希，完成时记录**序列化响应**。
- 用同一 key 重试返回**存储的原始响应**（相同状态码和响应体）— 不重新执行。
- 如果重试的请求体与存储的哈希不同，拒绝返回 422：相同 key + 不同参数是客户端 bug，不是重试。
