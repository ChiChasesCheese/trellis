---
id: hl-j03-match-exception
node: java21.j03-pattern-switch
type: qa
step: 16
---
## Q
`sealed` 层级的 `switch` 没写 `default`，编译器仍生成的 default 目标是什么？什么情况下会真的走到？怎么复现？

## A
编译器生成一个 `default -> throw new MatchException(null, null)`。正常走不到；只有层级在**编译之后**被改过才会到。

复现：先编译 `sealed interface S permits X, Y` 和 `switch (s) { case X x -> 1; case Y y -> 2; }`；再把 `S` 改成 `permits X, Y, Z`，只编译 `S` 和 `Z`，不碰 `switch` 所在的类；运行 `f(new Z())` 得 `java.lang.MatchException`。

同理，`enum` 的 `switch` 表达式在编译后枚举多出新常量，运行时也是 `MatchException`。
