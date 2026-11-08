---
id: hi-pt-recently-viewed-items-3-view-method
node: qb.lld.recently-viewed-items.points
type: qa
step: 3
---
## Q
**"最近浏览"记录 · view 的关键方法**｜必会 · 出自："最近浏览"记录 › 核心实现

"最近浏览"的 view(customer, item) 在客户自己的有序字典里怎么更新？用 limit=3 浏览 a、b、c、b、d 结果是什么？

## A
**关键代码。**
```python
if item in items: items.move_to_end(item)
else:
    items[item] = None
    if len(items) > self._limit: items.popitem(last=False)
```
**示例。** 浏览 b 时 b 提前成 a、c、b；浏览 d 超限丢 a，最新在前得 d、b、c。
**构造。** limit ≤ 0 在构造时拒绝。
