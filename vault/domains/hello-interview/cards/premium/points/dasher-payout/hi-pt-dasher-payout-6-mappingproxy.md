---
id: hi-pt-dasher-payout-6-mappingproxy
node: qb.lld.dasher-payout.points
type: qa
step: 6
---
## Q
**配送员报酬计算 · 不可变费率方案**｜追问 · 出自：配送员报酬计算 › 深入 5

`PayPlan` 的 `tiers` 是个字典，而方案对象是 `frozen=True` 的。调用方之后改了自己传进来的字典，会发生什么？怎么防？

## A
**问题。** 直接保存传入的字典，等于把可变状态交给了别人，已建好的方案被悄悄改掉。

**做法。** 在 `__post_init__` 里拷成只读视图。冻结的数据类要用 `object.__setattr__` 绕过冻结。

```python
object.__setattr__(self, "tiers", MappingProxyType(dict(self.tiers)))
```
**效果。** 方案成了不可变快照（不可变快照），可以放心共享。
