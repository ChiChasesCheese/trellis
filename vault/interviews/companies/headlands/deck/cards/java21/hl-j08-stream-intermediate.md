---
id: hl-j08-stream-intermediate
node: java21.j08-var
type: qa
step: 17
---
## Q
流水线的复杂中间结果，如 `groupingBy(Fill::symbol, TreeMap::new, summingLong(Fill::qty))`，用 `var` 接有什么好处？嵌套分组结果的类型是什么？

## A
```java
var qtyBySymbol = fills.stream().collect(
        Collectors.groupingBy(Fill::symbol, TreeMap::new, Collectors.summingLong(Fill::qty)));
// 类型是 TreeMap<String, Long>；不用在左边写
```
嵌套 `groupingBy(Fill::symbol, ..., groupingBy(Fill::side, ...))` 的结果类型是 `TreeMap<String, TreeMap<Side, Long>>`，手写很长，用 `var` 接，再 `for (var e : nested.entrySet())` 遍历。

`var` 最适合：类型很长且没有信息量的嵌套泛型。
