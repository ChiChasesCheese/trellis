---
id: hl-j14-filtering-empty-group
node: java21.j14-stream-api
type: qa
step: 13
---
## Q
`groupingBy(symbol, filtering(t -> t.qty() >= 200, ...))` 与「先 `filter` 再 `groupingBy`」有什么区别？什么时候用前者？

## A
5 笔成交，`AAPL` 有三笔（其中一笔 300），`MSFT` 两笔（都 <200）：

- `filtering` 版本：`{AAPL=[300], MSFT=[]}`，**仍保留空组 `MSFT=[]`**。
- 先 `filter` 再分组：`{AAPL=[300]}`，`MSFT` 整个组消失。

需要「每个分组都出现，即使为空」的报表，用 `Collectors.filtering`（组内过滤）。
