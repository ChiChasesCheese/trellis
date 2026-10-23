---
id: hl-j14-takewhile
node: java21.j14-stream-api
type: qa
step: 7
---
## Q
在 `[1, 2, 3, 10, 2, 1]` 上，`takeWhile(x -> x < 5)`、`dropWhile(x -> x < 5)`、`filter(x -> x < 5)` 各得到什么？有什么前提？

## A
- `takeWhile` → `[1, 2, 3]`：遇到第一个不满足的就停。
- `dropWhile` → `[10, 2, 1]`：丢到第一个不满足的，剩下全留。
- `filter` → `[1, 2, 3, 2, 1]`：对每个元素都判断。

同理在 `[1, 2, 5, 1]` 上 `takeWhile(x<3)` 是 `[1, 2]`，`filter(x<3)` 是 `[1, 2, 1]`。

`takeWhile/dropWhile` 是**短路**操作，对无限流有用，且**只对有序流有可预期结果**，对 `HashSet.stream()` 之类的无序流没有意义。
