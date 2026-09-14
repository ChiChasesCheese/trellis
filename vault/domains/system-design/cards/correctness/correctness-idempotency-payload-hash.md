---
id: correctness-idempotency-payload-hash
node: correctness.idempotency
type: cloze
---
An idempotency-key record must also store a {{c1::hash of the request payload (and the endpoint/params)}}; a request reusing the key with a **different** body must be {{c2::rejected with an error (Stripe: 422), never replayed or re-executed}} — otherwise a client bug that reuses keys across distinct operations gets the *first* operation's stored response and silently believes the second one succeeded.

## zh
幂等性 key 记录还必须存储 {{c1::请求载荷的哈希值（和端点/参数）}}；用同一 key 但**不同**请求体的请求必须 {{c2::拒绝返回错误（Stripe: 422），绝不重放或重新执行}} — 否则客户端 bug 跨不同操作复用 key，得到*第一个*操作的存储响应，错误地相信第二个成功了。
