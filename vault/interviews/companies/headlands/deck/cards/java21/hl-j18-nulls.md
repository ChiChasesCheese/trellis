---
id: hl-j18-nulls
node: java21.j18-comparators-interfaces
type: qa
step: 8
---
## Q
`Comparator.comparing(Person::age)` 遇到 `age == null` 会怎样？怎么容忍 null？`nullsLast` 再整体 `reversed()` 会怎样？

## A
遇到 null 键会 **NPE**。容忍 null：

```java
Comparator.comparing(Person::age, Comparator.nullsFirst(Comparator.naturalOrder()))
```
`reversed()` 反转的是**完整的比较结果，包括 null 的位置**：`nullsLast(...)` 再整体 `.reversed()`，null 排最后被反成最前（实验里 `dave` 年龄 null 排第一）。

想「降序且 null 仍在最后」，把 `nullsLast` 套在 `reverseOrder()` **外面**：`nullsLast(Comparator.reverseOrder())`。
