---
id: hl-c02-const-pointer-positions
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 5
---
## Q
面试问：`const int*`、`int* const`、`const int* const` 各是什么意思？怎么读？
Interview question: What do `const int*`, `int* const` and `const int* const` mean?

## A
**从右往左读声明**：
- `const int* p`：p 是指针，指向 `const int`。**不能**通过 p 改值（`*p = 5` 报错），p 本身**可以**改指向（`p = &y` 合法）。
- `int* const p`：p 是 `const` 指针，指向 `int`。p **不能**改指向，值**可以**改（`*p = 5` 合法）。
- `const int* const p`：两者都不能改。

```cpp
int x = 1, y = 2;
const int* p1 = &x;  p1 = &y;      // ok
int* const p2 = &x;  *p2 = 5;      // ok
```
