---
id: hl-j02-generic-enum
node: java21.j02-sealed
type: qa
step: 8
---
## Q
`sealed interface` 能不能带类型参数？`enum` 能不能出现在 `permits` 里？各写一个例子。

## A
可以。
```java
sealed interface Either<L, R> permits Left, Right {}
record Left<L, R>(L value) implements Either<L, R> {}

sealed interface Signal permits Tick, Bar {}
enum Tick implements Signal { UP, DOWN }
```
`enum` **隐式 `final`**，所以可以直接出现在 `permits` 里，不需要再写修饰符。
