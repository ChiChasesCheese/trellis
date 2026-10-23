---
id: hl-j09-ex-linkedhashset
node: java21.j09-sequenced-collections
type: qa
step: 21
---
## Q
`LinkedHashSet` 里已有 `a, b, c`，依次 `addFirst("c")`、`addLast("a")` 后的顺序是什么？`reversed()` 呢？这和 `Set.add` 对已存在元素的直觉有何不同？

## A
- 结果 `[c, b, a]`（`first=c`、`last=a`）：对已存在元素 `addFirst` / `addLast` 是**移动**；
- `.reversed()` → `[a, b, c]`。

`Set.add` 对已存在元素是"返回 `false` 什么都不做"，而 `LinkedHashSet.addFirst` / `addLast` **不是忽略，是移动**。
