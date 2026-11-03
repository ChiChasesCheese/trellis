---
id: craft-idempotency-key-stores-result-2-store-rejection-and-fingerprint
node: craft.patterns.idempotency-key-stores-result
type: qa
step: 2
---
## Q
**幂等键存结果 · 业务拒绝也要存，同键不同内容要报错**｜写法

一次转账因为余额不足被拒绝，之后用户充了值，客户端用同一个键重试。服务端应该重新判断然后成功吗？如果客户端用同一个键却改了金额呢？

## A
**要点。** 都不应该重新执行。（1）业务拒绝是这个键的结果，也要存：同键重试永远拿到第一次的答案，否则同一个键的两次调用可能一次拒绝一次成功，调用方无法判断到底发生了什么。（2）同键不同内容是调用方的 bug，抛错（HTTP 里常用 422 或 409），不能悄悄返回旧结果，也不能当新请求执行。

```python
fp = (amount,)                              # 请求指纹：同键必须同内容
with self._mu:
    if key in self._recs:
        old_fp, result = self._recs[key]
        if old_fp != fp:
            raise KeyReuse("同一个键不能用于不同的请求")
        return result                       # 含「余额不足」
    result = "ok" if balance >= amount else "rejected:insufficient"
    self._recs[key] = (fp, result)          # 拒绝也存
    return result
```

先余额 10 付 50，再用同键余额 999 付 50，再用同键付 60，实际输出：

```
rejected:insufficient
rejected:insufficient
KeyReuse: 同一个键不能用于不同的请求
真正执行次数 1
```

**为什么。** 被拒绝是「值」，调用方 bug 才是「异常」：余额不足用返回值，键被复用才抛。

**代价。** 想要「余额变多后重试成功」，调用方就必须换一个新键，这是有意的设计：一个键对应一次意图。
