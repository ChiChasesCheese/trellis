---
id: hl-j18-default-misuse
node: java21.j18-comparators-interfaces
type: qa
step: 21
---
## Q
什么时候该用接口的 `default` 方法，什么时候不该？

## A
只用于两种情况：
1. **接口演进**：向已发布接口添加方法而不破坏实现者；
2. **可组合的小帮助方法**（如 `and`、`negate`）。

能改全部实现者的内部接口，用抽象方法更清楚。注意 `default` 不是多继承状态：接口不能有实例字段，`default` 只能调抽象方法与其他 `default` 方法；菱形冲突是编译错误，必须覆盖并 `X.super.m()` 指名。
