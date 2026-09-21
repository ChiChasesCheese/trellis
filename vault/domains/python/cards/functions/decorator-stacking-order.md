---
id: decorator-stacking-order
node: functions.decorators
type: qa
source: python-docs
---
## Q
叠放多个装饰器 `@g` `@f` `def foo(): ...`（`g` 写在 `f` 上面）展开后等价于 `foo = g(f(foo))` 还是 `foo = f(g(foo))`？离 `def` 最近的装饰器先被应用吗？

## A
等价于 `foo = g(f(foo))`：离 `def` 最近的 `f` 先包一层，离得最远的 `g` 包在最外层，应用顺序自底向上（bottom to top）——这和数学里函数复合 `(g∘f)(x) = g(f(x))` 的顺序一致。调用 `foo()` 时的执行顺序则相反：先进入最外层 `g` 的包装逻辑，再进入 `f` 的包装逻辑。
