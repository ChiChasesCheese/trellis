---
id: hl-j14-other-collectors
node: java21.j14-stream-api
type: qa
step: 12
---
## Q
`Collectors.filtering`、`flatMapping`、`summarizingLong` 各做什么？

## A
- `Collectors.filtering(pred, downstream)`（Java 9）：**在分组的每一组内部**过滤。
- `Collectors.flatMapping(fn, downstream)`（Java 9）：在每组内部展开。
- `Collectors.summarizingLong/Int/Double`：一次得到 count、sum、min、max、average，类型是 `LongSummaryStatistics`，例如 `{count=5, sum=610, min=10, average=122.0, max=300}`。

它们都是下游收集器，配合 `groupingBy` 使用。
