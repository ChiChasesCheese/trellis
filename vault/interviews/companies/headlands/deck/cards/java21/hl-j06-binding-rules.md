---
id: hl-j06-binding-rules
node: java21.j06-instanceof-pattern
type: qa
step: 8
---
## Q
`instanceof` 模式的绑定变量有哪些其他规则：命名冲突、`final`、类型是否可能成立？

## A
- **名字不能与已有局部变量 / 参数冲突**（`variable s is already defined`）；同一条件里重复绑定同名也不行。
- 绑定变量**默认不是 `final`**，可重新赋值；想禁止写 `o instanceof final String s`。
- **类型必须可能成立**：`Integer x; x instanceof String s` 编译错误，`Integer` 永不可能是 `String`。
- `if / else if` 链里多个 `instanceof String s` 各自独立，可同名；但 `a instanceof X s && b instanceof Y s` 同条件内同名会报错。
