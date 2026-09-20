---
id: problems-online-auction-proxy-bidding-three-rules
node: problems.marketplaces.online-auction
type: qa
step: 1
tags: [grown]
---
## Q
在线拍卖（online auction）系统里，出价者交给系统的是一个愿意付的**上限**（maximum），不是一口价，这叫代理出价（proxy bidding）。设在位领先者的上限是 `L`、当前价是 `P`、加价档（increment）是 `k`，新挑战者的上限是 `M`，当前价该怎么算？

## A
分三种情况，而且**价格只涨不跌**这一条必须单独兜底：

- `M > L`：换人。新价 = `min(M, L + k)`——挑战者只需要压过在位者一档，除非他的上限还不到那一档，那就按他的上限成交（险胜）。
- `M <= L`：不换人，但在位者被顶上去：新价 = `min(L, M + k)`。
- 无论哪一支，最后都执行 `P = max(P, 新价)`。

```python
if self._leader is None:
    self._leader, self._leader_max = bidder_id, maximum
elif maximum > self._leader_max:
    self._price = max(self._price, min(maximum, self._leader_max + self.increment))
    self._leader, self._leader_max = bidder_id, maximum
else:
    self._price = max(self._price, min(self._leader_max, maximum + self.increment))
```

漏掉 `max(P, 新价)` 是最常见的 bug：会出现「后来的小额出价把价格打下去」的荒唐结果。加上这一条之后，最终结果与出价到达顺序无关——最终价永远是 `min(最高上限, 次高上限 + 一档)`。
