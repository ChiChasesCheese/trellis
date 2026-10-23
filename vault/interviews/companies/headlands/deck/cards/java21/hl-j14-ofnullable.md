---
id: hl-j14-ofnullable
node: java21.j14-stream-api
type: qa
step: 8
---
## Q
`Stream.ofNullable(x)` 做什么？典型用法是什么？

## A
`null` → 空流，否则单元素流（Java 9）。

用于「查不到就跳过」：

```java
keys.stream()
    .flatMap(k -> Stream.ofNullable(map.get(k)))
    .toList();
```
不用再写 `x == null ? Stream.empty() : Stream.of(x)`。`Stream.ofNullable(null).count()` 是 0。
