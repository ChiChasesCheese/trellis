---
id: pl-cpp-value-categories-found-copy-elision
node: cpp.value-categories
type: qa
step: 5
---
## Q
C++17 的“强制拷贝省略”（guaranteed copy elision）是什么？它与 NRVO、`return std::move(x)` 各是什么关系？

## A
**拷贝省略**：函数返回一个对象时，编译器不先在函数里构造、再拷贝或移动到调用处，而是**直接在调用者的目标位置构造**。

**C++17 以前**：编译器可以省略，但要求拷贝/移动构造函数必须可访问，是优化而非保证。
**C++17 起**：当返回的是**纯右值**（`return T{...};`）时，省略是**语言规则**：根本不存在临时对象，初始化直接作用于目标。所以不可拷贝、不可移动的类型也能按值返回。

**实测**（每个构造/拷贝/移动都打印一行）：

```cpp
Noisy make()       { return Noisy{}; }          // 打印: ctor
Noisy make_named() { Noisy n; return n; }       // NRVO，实测: ctor
Noisy make_bad()   { Noisy n; return std::move(n); } // ctor, move, dtor
Pinned make_p()    { return Pinned{}; }  // Pinned 的拷贝和移动都 = delete，仍可编译
```

**三种情形**：
1. **返回纯右值**（`return T{}`）：C++17 保证省略，零次拷贝或移动。
2. **返回具名局部变量**（`return n;`）：叫 NRVO（具名返回值优化），标准**允许但不强制**；主流编译器基本都做，但类型仍须可移动。不能做时，编译器会先尝试把 `n` 当右值**移动**。
3. **`return std::move(n);`**：把 `n` 变成将亡值，不再是“返回局部变量名”的形态，**反而阻止 NRVO**，多出一次移动。clang 给出警告：`moving a local object in a return statement prevents copy elision [-Wpessimizing-move]`。

**对比**：这与 Rust 的返回值移动类似，但 Rust 的移动一定是按位复制，由优化器去掉；C++ 的省略是语言层面的规则，连构造函数都可以不调用。

**要记住的一点**：按值返回局部对象，**什么都不要加**；`std::move` 在这里是画蛇添足。
