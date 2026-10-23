---
id: hl-j08-forbidden-2
node: java21.j08-var
type: qa
step: 6
---
## Q
这四种 `var` 写法的错误是什么：`var m = String::length;`、`var x = 1, y = 2;`、`var z[] = new int[1];`、`var self = self + 1;`？

## A
- `var m = String::length;`：`method reference needs an explicit target-type`（方法引用要靠目标类型）。
- `var x = 1, y = 2;`：`'var' is not allowed in a compound declaration`（不允许复合声明）。
- `var z[] = new int[1];`：`'var' is not allowed as an element type of an array`。
- `var self = self + 1;`：`cannot use 'var' on self-referencing variable`（不能自引用）。
