---
id: foundations-availability-vs-consistency-axis
node: foundations.tradeoffs
type: qa
---
## Q
For each, pick availability-first or consistency-first and justify in one line: (a) shopping-cart adds, (b) inventory decrement at checkout, (c) social-feed reads.

## A
- **(a) Cart adds — availability**: losing a sale to an error page costs more than merging a cart later (conflicts resolvable).
- **(b) Inventory at checkout — consistency**: overselling stock creates real-world cost; better to fail the request.
- **(c) Feed reads — availability**: a slightly stale feed is invisible to users; freshness is not a contract.

Pattern: choose per **operation**, not per system — the same product mixes both.


## Q zh
分别选择可用性优先还是一致性优先，并用一句话说明理由：(a) 购物车添加，(b) 结账时库存扣减，(c) 社交推送流阅读。

## A zh
- **(a) 购物车 — 可用性**：错误页面损失的销售比后来合并购物车的成本更大（冲突可解决）。
- **(b) 结账时库存 — 一致性**：超卖会产生真实的成本；最好是拒绝请求。
- **(c) 推送流阅读 — 可用性**：用户察觉不到稍微陈旧的推送流；新鲜度不是承诺的一部分。

模式：按**操作**选择，不是按**系统** — 同一个产品会混合使用两者。
