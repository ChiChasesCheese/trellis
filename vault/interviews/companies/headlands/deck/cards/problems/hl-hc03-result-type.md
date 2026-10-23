---
id: hl-hc03-result-type
node: problems.hc03-recursive-sum
type: qa
step: 4
---
## Q
递归求和为什么返回 sealed 的 `SumResult`（`Ok` / `Overflow`），而不是抛异常、返回 -1 或静默回绕？

## A
```java
public sealed interface SumResult permits Ok, Overflow {}
public record Ok(long value) implements SumResult {}
public record Overflow(BigInteger exact) implements SumResult {}
```
- 静默回绕是最坏的 bug。
- 抛异常：调用方可能忘了 `catch`，而且「n 太大」是**可预期的业务结果**。
- 返回魔法数 `-1`：区间求和里负数是合法的和。
- sealed 结果类型：调用方用 `switch` 处理，**编译器强制处理 `Overflow`**，`Overflow` 还带数学精确值方便降级。

实现里仍用异常：`ArithmeticException` 只在实现内部，在**公共入口**转成值——「内部抛异常，边界转成值」：
```java
try { return new Ok(addUp(n, w)); }
catch (ArithmeticException e) { return new Overflow(exactTo(n)); }
```
`StackOverflowError` **不捕获**，直接传给调用方；吞掉会把「栈不够」误报成别的东西。`n < 0` 抛 `IllegalArgumentException`。

`Width.add`：先在 `long` 里相加（两个 `int` 范围内的数在 `long` 里绝不溢出），`INT` 时再 `Math.toIntExact(s)` 检查，`LONG` 时 `Math.addExact`：
```java
long s = Math.addExact(a, b);
return switch (this) { case INT -> Math.toIntExact(s); case LONG -> s; };
```
直接 `int` 相加要自己判回绕（`((a ^ s) & (b ^ s)) < 0`），易写错。
