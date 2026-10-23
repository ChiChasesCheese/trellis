---
id: hl-j09-add-semantics
node: java21.j09-sequenced-collections
type: qa
step: 8
---
## Q
`addFirst` / `addLast` 在 `List`、`LinkedHashSet`、`TreeSet` / `TreeMap`、不可变的 `List.of(...)` 上分别怎么表现？

## A
- `List`：`addFirst` 会把所有元素往后挪。
- `LinkedHashSet`：元素**已存在**时，**把它移到头 / 尾**（不是忽略）。
- `TreeSet` / `TreeMap` 等由比较器决定位置的：**抛 `UnsupportedOperationException`**。
- 不可变的 `List.of(...)`：读两端 OK（如 `getLast()`），改动抛 `UnsupportedOperationException`。
