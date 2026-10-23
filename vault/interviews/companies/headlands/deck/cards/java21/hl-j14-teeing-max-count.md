---
id: hl-j14-teeing-max-count
node: java21.j14-stream-api
type: qa
step: 22
---
## Q
用 `teeing` 写出：对 `List<Long> qtys` 同时求最大值和个数，返回形如 `"max=300 n=5"` 的 `String`。

## A
```java
qtys.stream().collect(Collectors.teeing(
    Collectors.maxBy(Comparator.<Long>naturalOrder()),
    Collectors.counting(),
    (mx, n) -> "max=" + mx.orElseThrow() + " n=" + n));
```
- `maxBy` 返回 `Optional<Long>`，所以合并函数里用 `orElseThrow()`。
- `Comparator.<Long>naturalOrder()` 的显式类型参数用来避免类型推断失败。
- 一次遍历同时得到两个结果，不需要可变累加器。
