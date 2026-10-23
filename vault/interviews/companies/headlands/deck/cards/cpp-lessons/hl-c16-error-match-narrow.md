---
id: hl-c16-error-match-narrow
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 11
---
## Q
编译器报 `no matching function for call to 'add'`、`non-constant-expression cannot be narrowed from type 'long' to 'int' in initializer list`、以及对 `std::list` 调用 `std::sort` 的一长串错误，分别是什么原因？

## A
- `no matching function for call to 'add'`：参数类型不匹配；看下面 `note: candidate function not viable: no known conversion from 'std::vector<int>' to 'int' for 1st argument`，就是传了 `vector<int>` 给 `int` 参数。
- `cannot be narrowed ... in initializer list`：**花括号初始化禁止窄化转换**，如 `int x{big};` 里 `big` 是 `long`；修法是显式转换（`static_cast<int>`）或改用圆括号/换类型。
- `std::sort(l.begin(), l.end())` 对 `std::list`：报错出自标准库内部（`__last - __first`），因为 `list` 迭代器不支持随机访问；用成员函数 **`l.sort()`**。
