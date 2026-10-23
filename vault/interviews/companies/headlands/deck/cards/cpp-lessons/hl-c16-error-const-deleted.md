---
id: hl-c16-error-const-deleted
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 10
---
## Q
编译器报 `'this' argument to member function 'inc' has type 'const Counter', but function is not marked const` 和 `call to implicitly-deleted copy constructor of 'std::unique_ptr<int>'` 各是什么问题？怎么修？

## A
- 前者：对 `const` 引用调用了**非 `const` 成员函数**。修法：若 `inc` 确实要修改就别用 `const` 引用；若是只读函数，在成员函数后加 `const`。
- 后者：**拷贝了 `unique_ptr`**，拷贝构造被删除（因为它只能移动）。修法：转移所有权用 `std::move`：`auto b = std::move(a);`。
