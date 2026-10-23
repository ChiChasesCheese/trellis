---
id: hl-j15-exact-intrinsic
node: java21.j15-math-string-utils
type: qa
step: 13
---
## Q
`Math.addExact` 这类方法在热路径上会慢吗？HotSpot 怎么实现它们？

## A
不慢，**别因怕慢而不用 Exact**。源码实现是「做加法，用符号位技巧判溢出，溢出就抛」，但 HotSpot C2 把它们当**内联函数**（intrinsic）：生成「加法指令 + 检查 CPU 溢出标志位 + 条件跳转到抛异常的冷路径」，无溢出时只比 `+` 多一条几乎不跳的分支。

而 `Math.clamp`、`HexFormat`、`StringBuilder.repeat` 是纯库方法，无 JIT 魔法，无新语法。

注意：异常本身（构造栈）成本大，所以 Exact 适合「溢出就是 bug / 非法输入」，不适合把异常当常规控制流。
