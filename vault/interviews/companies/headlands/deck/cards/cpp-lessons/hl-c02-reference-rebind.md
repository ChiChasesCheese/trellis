---
id: hl-c02-reference-rebind
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 7
---
## Q
```cpp
int a = 1, b = 2;
int& r = a;
r = b;
```
执行后 `a`、`b` 各是多少？`r` 指向谁？

## A
`a == 2`，`b == 2`，`r` 仍然是 `a` 的别名。
- `r = b` **不是换绑**，而是把 `b` 的值赋给 `r` 所绑定的对象 `a`。
- 引用必须在定义时初始化，永远绑定初始对象，没有"空引用"。
- 推论：含引用成员的类不可赋值（引用不能换绑）。
