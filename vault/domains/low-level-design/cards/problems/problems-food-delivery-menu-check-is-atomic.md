---
id: problems-food-delivery-menu-check-is-atomic
node: problems.marketplaces.food-delivery
type: qa
step: 7
tags: [grown]
---
## Q
外卖的菜品可售状态由后厨随时改动，可能正好发生在顾客点「提交」的那一刻。校验应该放在哪一步？某道菜售罄时，少送一道还是整单失败？

## A
校验、开店判断和**抄下价格**必须在餐厅自己的锁里**一次做完**，拆成两步就留下一条缝：

```python
def quote(self, wanted: Mapping[str, int]) -> tuple[OrderLine, ...]:
    with self._lock:
        if not self._open:
            raise RestaurantClosedError(...)
        missing = [i for i in wanted if i not in self._items or i in self._sold_out]
        if missing:
            raise ItemUnavailableError(...)
        return tuple(OrderLine(...) for i, n in wanted.items() if n > 0)
```

但它**不消灭**餐厅的拒单权：最终裁决权永远在餐厅手上，所以 REJECTED 这条边必须存在。校验只是把绝大多数缺货挡在两百毫秒内，而不是让顾客等两分钟——典型的「乐观校验 + 权威兜底」。

**缺货一律整单失败，不做部分履约。** 少送一道菜，配送成本一分不少，顾客满意度却断崖式下跌；而且「哪几道可以不送」系统根本判断不了。真要支持，那是一个需要顾客当场确认的新流程（「米饭没了，是否继续？」），不是这里加一个 `if`。

价格必须抄进订单行：餐厅晚上改一次价，不能让白天的历史订单金额跟着变。
