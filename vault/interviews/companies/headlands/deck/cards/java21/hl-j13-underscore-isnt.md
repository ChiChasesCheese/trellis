---
id: hl-j13-underscore-isnt
node: java21.j13-unnamed-variables
type: qa
step: 9
---
## Q
`_` 不是什么？`int x = _ + 1;`、`void f(int _)`、字段 `int _;` 能编译吗？

## A
- **不是变量**：不能读、不能赋值。`int x = _ + 1;` 报错 `the underscore keyword '_' is only allowed to declare unnamed patterns, local variables, exception parameters or lambda parameters`。
- **不是「忽略编译检查」**：`sealed` 穷尽性照常。
- **不能用于方法参数、字段**：`void f(int _)` 不合法，只有声明位置表里的地方可用。
- 局部变量 `var _` 必须有初始化。
