---
id: hl-j14-java8-gaps
node: java21.j14-stream-api
type: qa
step: 3
---
## Q
Java 8 的 Stream 有哪四个不足，分别对应后来哪个新 API？

## A
1. **一次遍历同时算两个量**（如 VWAP = 总名义金额 / 总数量），只能手写可变累加器 → `Collectors.teeing`（12）。
2. **最后一步啰嗦**：`collect(Collectors.toList())`，且返回的 `List` 具体类型规范不保证 → `Stream.toList()`（16）。
3. **`iterate` 是无限的**，要配 `limit`，「到某个条件就停」没法直接写 → 三参数 `Stream.iterate`、`takeWhile`（9）。
4. **一个元素产出 0..n 个结果**只能 `flatMap`，每个元素都要建一个小 `Stream`（如 `Stream.of(x)` / `Stream.empty()`）→ `mapMulti`（16）。
