---
id: cc-model-idem-same-key-different-payload
node: model.idempotency
type: qa
---
## Q
A payment is submitted twice with the same id: once with the same amount, once with a different one. What are the two answers?

## A
**Same id + same parameters → silent success, recorded once. Same id + different parameters → rejected, and the original stands unchanged.**

```python
if pid in payments:
    return payments[pid].amount == amount     # True = replay, False = conflict
```

This is exactly what an idempotency key does in a real API, and statements mirror it. Two traps: the replay must return *success* (a client retrying after a timeout must not see an error), and it must not overwrite the stored amount or timestamp — the second request's timestamp is discarded, which matters when a later query filters by time.

## Q zh
同一个 id 的付款提交了两次：一次金额相同，一次金额不同。两种答案分别是什么？

## A zh
**同 id + 同参数 → 静默成功，只记录一次。同 id + 不同参数 → 拒绝，原记录原封不动。**

```python
if pid in payments:
    return payments[pid].amount == amount     # True = replay, False = conflict
```

这正是真实 API 里 idempotency key 的行为，题面也照搬。两个坑：重放必须返回**成功**（超时后重试的客户端不该看到错误）；以及不得覆盖已存的金额或时间戳 —— 第二次请求的时间戳被丢弃，这在后续按时间过滤的查询里很重要。
