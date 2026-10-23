---
id: hl-j09-empty-exception
node: java21.j09-sequenced-collections
type: qa
step: 7
---
## Q
在空的 `ArrayList`、`ArrayDeque`、`LinkedHashSet`、`TreeSet` 上调 `getFirst()` / `removeFirst()` 会怎样？

## A
抛 **`NoSuchElementException`**——不返回 `null`，也不是 `IndexOutOfBoundsException`。`getLast()` / `removeLast()` 同理。

对比旧写法 `list.get(list.size() - 1)`：空列表时抛含糊的 `IndexOutOfBoundsException: Index -1`。
