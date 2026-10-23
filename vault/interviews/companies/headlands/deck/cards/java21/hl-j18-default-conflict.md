---
id: hl-j18-default-conflict
node: java21.j18-comparators-interfaces
type: qa
step: 10
---
## Q
类实现多个接口、又继承父类，同名 `default` 方法怎么选？三条规则是什么？怎么指名调用某个接口的版本？

## A
按顺序：
1. **类优先**：父类（或本类）里的方法永远胜过接口的 `default`。例：`Derived extends Base implements Maker`，`describe()` 是 `base`。
2. **更具体的接口优先**：`B extends A` 且都有 `m()` 的 default，则 `B` 的赢。
3. **否则必须自己覆盖**，否则**编译错误**（菱形冲突）；用 `X.super.m()` 指名调用某接口的版本，如 `Maker.super.describe() + "+" + Taker.super.describe()` 得 `maker+taker`。

测试：`C extends B implements I`，`B`、`I` 都有 `m()`，`new C().m()` 调 `B.m()`；若 `C implements I, J` 两者都有 default `m()`，`C` 必须覆盖，可写 `I.super.m()`。
