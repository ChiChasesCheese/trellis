---
id: craft-lock-as-transaction-boundary-4-one-coarse-lock
node: craft.architecture.lock-as-transaction-boundary
type: qa
step: 4
---
## Q
**锁即事务边界 · 券商下单为什么能「全程一把锁」，撮合与结算还不会失败**｜架构

券商的 `place_order` 要校验、预留资金、撮合、逐笔结算、释放多余预留。把它全放进一把锁里，有人会觉得粗。粗锁什么时候是对的？撮合之后的结算为什么可以保证不再失败？

## A
**要点。** 两个条件让粗锁成立：（1）这些步骤共享同一组不变量（现金、持仓、挂单簿），拆成多把锁就要处理锁序；（2）失败点全部前移到「预留」这一步，预留成功后撮合、结算只是在花已冻结的资金，不会再失败，所以不需要中途回滚。粗锁不是错，错的是没想过它为什么够用。

```python
def place(cash, fills, reserve_first):
    need = sum(q * p for q, p in fills)
    if reserve_first:
        if need > cash:                  # 一次性预留：不够就整单拒绝
            return "rejected", 0, cash
        cash -= need                     # 之后的成交只是在花预留
        return "filled", sum(q for q, _ in fills), cash
    done = 0
    for q, p in fills:                   # 逐笔结算时才发现钱不够
        if q * p > cash:
            return "half-filled", done, cash
        cash -= q * p
        done += q
    return "filled", done, cash

print("不预留 :", place(80, [(10, 5), (10, 6)], False))
print("先预留 :", place(80, [(10, 5), (10, 6)], True))
```

现金 80，撮合出 `10@5`、`10@6`（共 110），两种写法的实际输出：

```
不预留 : ('half-filled', 10, 30)
先预留 : ('rejected', 0, 80)
```

**为什么。** 不预留的版本里，第一笔已经成交、钱已扣掉，第二笔才失败，留下半截状态，只能靠补偿修复；预留把这类失败变成一个可以直接拒绝的前置检查。

**代价。** 一把锁意味着所有账户的下单互相排队；规模上去后要按交易品种或账户分片，每片内部仍然保持「一片一把锁」。券商的行情推送放在锁外（`with` 块结束后才 `_publish`）。
