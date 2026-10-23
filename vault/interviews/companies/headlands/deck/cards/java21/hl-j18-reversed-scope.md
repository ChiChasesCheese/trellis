---
id: hl-j18-reversed-scope
node: java21.j18-comparators-interfaces
type: qa
step: 7
---
## Q
`Comparator.comparing(A::x).thenComparing(A::y).reversed()` 与 `Comparator.comparing(A::x).reversed().thenComparing(A::y)` 的区别？

## A
`reversed()` 作用于**它前面整条链**：

```java
comparing(Person::city).thenComparing(Person::name).reversed()   // city、name 都反了
comparing(Person::city).reversed().thenComparing(Person::name)   // 只有 city 降序，name 仍升序
```
前者：x 降序、y 也降序；后者：x 降序、y 升序。实验：后者得 `[alice, Bob, Carol, Eve, dave]`（正确），前者得 `[alice, Eve, Carol, Bob, dave]`（两个键都反了）。
