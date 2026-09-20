---
id: problems-amazon-locker-three-failures-differ
node: problems.machines.amazon-locker
type: qa
step: 4
tags: [grown]
---
## Q
在快递柜（Amazon Locker）的取件口上，码不存在、码过期、码用错了门，这三种失败哪些算可疑、哪些要作废那个码？

## A
只有**码不存在**算可疑，也只有它累计失败计数、可能触发柜机冷却——码表里根本没有它，唯一的解释就是有人在猜。

**码过期**：码是真的，只是本人来晚了。不计入失败计数，否则迟到三天的顾客会被当成攻击者锁在门外。但要就地把状态收干净：柜格回池、包裹标记退回寄件人、码从码表删除，然后才抛 `ExpiredCodeError`——只抛异常不回收，柜格会一直挂在已占用上直到下一次扫描。

**码用错了门**（拿投件码按了取件口）：不计失败，**而且绝不能作废这个码**——否则顾客按错一次，退货就只能打客服。

还有一条同源的纪律：**作废要推迟到动作真的成功之后**。校验一步、烧码另一步——否则「退货塞不进预留的柜格」这种失败会白白烧掉顾客手里的投件码。

```python
def _validate(self, code, purpose, now, events):
    ...                   # 三条失败分支
    self._failures = 0    # 出示了真码就不算可疑
    return grant

def _burn(self, grant):
    del self._grants[grant.code]
```
