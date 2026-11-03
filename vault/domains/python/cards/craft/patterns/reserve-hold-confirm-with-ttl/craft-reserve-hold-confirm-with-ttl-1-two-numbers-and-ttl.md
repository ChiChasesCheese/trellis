---
id: craft-reserve-hold-confirm-with-ttl-1-two-numbers-and-ttl
node: craft.patterns.reserve-hold-confirm-with-ttl
type: qa
step: 1
---
## Q
**预留—确认—过期 · 为什么库存要记 on_hand 和 reserved 两个数，预留还要有 TTL**｜写法

下单流程是：用户加入购物车，几分钟内付款。如果加入购物车就直接把库存减 1，用户放弃后库存怎么还回来？如果不减，两个人同时买最后一件会怎样？

## A
**要点。** 把库存拆成两个数：在架（on_hand，仓库里真实有多少）和预留（reserved，已经被人占住但还没发货）。可售 = 在架 − 预留。预留一件只加 `reserved`；确认发货时在架和预留一起减；取消或过期只减 `reserved`。预留必须带过期时间（TTL），否则被放弃的购物车会永久吃掉库存。

```python
def available(self):
    self.expire_due()
    return self.on_hand - self.reserved        # 可售 = 在架 - 预留

def expire_due(self):
    for rid, (n, exp) in list(self.holds.items()):
        if exp is not None and exp <= Clock.t:
            del self.holds[rid]
            self.reserved -= n                 # 过期：只放回预留，不动在架

def confirm(self, rid):
    n, _ = self.holds.pop(rid)
    self.on_hand -= n                          # 确认发货：在架和预留一起减
    self.reserved -= n
```

在架 3 件，用户占满后离开，一小时后的可售量：

```
无 TTL -> 一小时后可售 0 （在架 3 预留 3 ）
有 TTL -> 一小时后可售 3 （在架 3 预留 0 ）
```

**为什么。** 两个数各自回答一个问题：仓库里有多少（盘点要对得上），还能卖多少（对用户说）。合成一个数就没法区分「占着的」和「走了的」。

**易错。** 没有「占」和「过期」成对设计的预留，是库存系统里最常见的泄漏。
