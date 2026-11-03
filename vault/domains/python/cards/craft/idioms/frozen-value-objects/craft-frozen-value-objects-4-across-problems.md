---
id: craft-frozen-value-objects-4-across-problems
node: craft.idioms.frozen-value-objects
type: qa
step: 4
---
## Q
**不可变值对象 · 转账、账本、额度里同一个 `!=`**｜写法

幂等转账、复式账本、额度系统在判断「重复提交」时，代码里都出现了一个 `!=`。它们比较的是什么？这个比较为什么是一行就够？

## A
**要点。** 三者都先按业务 ID 找到旧记录，再用冻结对象的 `!=` 判断「内容有没有变」：没变就当成功地什么都不做，变了就抛冲突。冻结对象让「同内容」有了一行的定义，不用逐字段手写比较，加一个字段也不会漏比。

```python
# idempotent-transfer：指纹是个只有四个字段的冻结类
fingerprint = _Request(src, dst, amount, currency)
...
if rec.fingerprint != fingerprint:
    raise KeyReuse("同一个键不能用于不同的请求")

# double-entry-ledger：整条分录就是值，postings 是 tuple[Posting, ...]
if (seq := self._by_id.get(entry.id)) is not None:
    if self._journal[seq - 1] != entry:
        raise ConflictError(f"分录 {entry.id} 被复用但内容不同")
    return seq

# credit-token-balance：新建一个 Grant，再和旧的比
new = Grant(grant_id, amount, at, expires_at)
old = self._grants.get(grant_id)
if old is not None:
    if old != new:
        raise ConflictError(...)
    return
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

不变的是：先建新值、再和旧值 `!=`。变的是比较的对象：一个只含请求字段的专用指纹、整条记录本身、一个刚构造好的新值。分录里的 `postings` 必须是 tuple，否则 `Entry` 就既不可哈希也不是真的值。

**见于。** idempotent-transfer、double-entry-ledger、credit-token-balance、pub-sub（消息冻结，同时交给多个订阅者不用加锁）、image-transform-pipeline（图像可哈希，当缓存键）。

**信号。** 对象要被比较「内容是否一样」、当字典或集合的键、或同时交给多个线程读。方法收到调用方传来的对象，而你要把它存起来。
