---
id: errors-cleanup-consume-last
node: errors.cleanup
type: qa
step: 6
---
## Q
创建工单的接口给每个新工单分配自增 id。校验失败的请求也让计数器加了一，会出什么问题？计数器、时间戳、版本号这类状态该在哪一步动？

## A
**失败的调用不消耗任何东西，状态最后才动**

- **编号出现缺口**：失败的请求烧掉一个 id，第一张成功的工单拿到 2 而不是 1，测试和对账都会对不上；
- **规则**：先做所有可能抛错的事（校验、查重、调用依赖），最后才改计数器、写入记录；
- **“最后一个会抛错的语句之后”才消耗**：如果写入本身能失败，要连同计数器放进事务，或者写成功再加；
- **同理**：失败的 feed 不推进时间戳，被拒的请求不占限流名额，不通过的编辑不加版本号；
- **一条断言就能守住**：失败以后调用方可观察的一切（计数、快照、版本）都和调用前一致。

```python
class Ids:
    n = 0
    def bad(self, title: str) -> None:
        self.n += 1                           # 先消耗
        if not title: raise ValueError("title")   # 再校验：号白烧了
    def good(self, title: str) -> None:
        if not title: raise ValueError("title")   # 先校验
        self.n += 1                           # 最后才消耗

a, b = Ids(), Ids()
for t in ("", "x"):
    for f in (a.bad, b.good):
        try: f(t)
        except ValueError: pass
print(a.n, b.n)                               # 2 1：bad 把第一个号烧掉了
```

**知识点：**所有路径上的清理（Cleanup on Every Path）
