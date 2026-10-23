---
id: hl-c02-const-member-mutable
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 6
---
## Q
C++ 的 const 成员函数（`int get() const`）承诺了什么？`mutable` 成员有什么用？什么叫 const-correctness？

## A
- `int get() const` 承诺**不修改 `*this`**；`const` 对象或 `const T&` 只能调用 `const` 成员函数，调用非 const 的 `inc()` 会编译失败。
- **`mutable`** 成员是例外：const 成员函数里也可以改，用于**逻辑上不改变对象值**的内部状态，如懒计算缓存、读计数、`mutable std::mutex`。
- **const-correctness**：凡是不修改的参数、成员函数都写 `const`，让编译器帮你查错。这是 C++ 用类型表达"只读"的方式，Java 没有对应物。

```cpp
int get() const { ++reads_; return n_; }  // reads_ 是 mutable
```
