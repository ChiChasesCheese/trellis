---
id: hl-j02-fix-square
node: java21.j02-sealed
type: qa
step: 22
---
## Q
下面的代码为什么编译不过？怎么改？

```java
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
class Square implements Shape {}
```

## A
`Square` 是普通 `class`，没有 `final` / `sealed` / `non-sealed`，编译错误 `sealed, non-sealed or final modifiers expected`。

改成 `final class Square implements Shape {}`，或者改成 `record`（`record` 隐式 `final`）。
