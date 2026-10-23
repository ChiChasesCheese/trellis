---
id: hl-j01-compact-ctor-rules
node: java21.j01-record
type: qa
step: 11
---
## Q
`record` 紧凑构造器的四条规则是什么？为什么在里面写 `this.qty = qty;` 会编译失败？

## A
1. 组件名在函数体里是**参数**（不是字段），可读，也可重新赋值（如 `symbol = ...`）。
2. **不能**写 `this.symbol = ...`，报 `cannot assign a value to final variable symbol`。
3. **不能 `return`**：末尾的赋值必须执行。
4. **可以抛异常**：这是做校验的主要手段。

原因：末尾的"参数赋给字段"是**编译器加的**，你再写一次就是给 `final` 字段赋两次。要改写入的值，改的是**参数**，例如 `qty = Math.max(qty, 1);`。
