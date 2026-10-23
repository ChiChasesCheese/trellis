---
id: hl-j09-reversed-details
node: java21.j09-sequenced-collections
type: qa
step: 10
---
## Q
`reversed()` 还有哪些性质：连调两次、返回类型、遍历时修改原集合？需要独立副本怎么办？

## A
- `list.reversed().reversed()` 就是原来的 `list`（`==` 为 `true`）；
- **返回类型协变**：`List.reversed()` 返回 `List`，`Deque` 返回 `Deque`，`LinkedHashSet` 返回 `SequencedSet`，`SortedSet` 返回 `SortedSet`；
- 遍历视图时修改原集合触发 **`ConcurrentModificationException`**，同普通 `Iterator`；
- 需要独立副本：`new ArrayList<>(list.reversed())` 或 `List.copyOf(list.reversed())`。
