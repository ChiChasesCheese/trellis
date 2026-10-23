---
id: hl-j08-forbidden-1
node: java21.j08-var
type: qa
step: 5
---
## Q
这四种 `var` 写法为什么不能编译：`var u;`、`var n = null;`、`var arr = {1, 2, 3};`、`var f = () -> 1;`？

## A
- `var u;`：没有初始化器，`cannot use 'var' on variable without initializer`。
- `var n = null;`：`null` 没有类型，`variable initializer is 'null'`。
- `var arr = {1, 2, 3};`：`array initializer needs an explicit target-type`。
- `var f = () -> 1;`：`lambda expression needs an explicit target-type`。

规律：`var` 要求右边**自带足够的类型信息**；lambda、数组初始化器、`null` 都要靠左边的"目标类型"，而 `var` 没有左边的类型。
