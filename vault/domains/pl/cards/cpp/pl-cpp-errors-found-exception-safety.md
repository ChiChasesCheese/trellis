---
id: pl-cpp-errors-found-exception-safety
node: cpp.errors
type: qa
step: 5
---
## Q
异常安全（exception safety）的几个保证级别是什么？怎样写出强保证的操作？

## A
**问题**：一个操作做到一半抛出异常，对象处于什么状态？调用者能否放心地继续使用？C++ 给出四个级别（David Abrahams 提出，标准库文档沿用）：

1. **无保证**：失败后对象可能损坏、资源泄漏。要避免。
2. **基本保证**（basic）：失败后没有资源泄漏，对象仍处于**有效但不确定**的状态，不变量保持成立。
3. **强保证**（strong）：失败后状态**恢复到操作之前**，要么完全成功要么什么都没发生（事务语义）。
4. **不抛保证**（nothrow）：操作一定成功，不会抛出（标 `noexcept`）。析构、`swap`、移动一般属于此级。

**RAII 自动给出基本保证**：只要资源都在对象里持有，栈展开就会释放它们，不泄漏。但"有效状态"需要你保证。

**实测对比**，往一个登记表里加名字，加之前先改了计数：

```cpp
void add_unsafe(const string& n, bool fail) { ++count; if (fail) throw X; names.push_back(n); }
void add_strong(const string& n, bool fail) {
  auto copy = names; copy.push_back(n);          // 先在副本上做可能失败的事
  if (fail) throw X;
  names.swap(copy); ++count;                      // 最后用不抛的操作提交
}
```

失败后：`add_unsafe` 得到 `count=1 names=0`（计数和数据不一致，不变量被破坏）；`add_strong` 得到 `count=0 names=0`（和调用前一模一样）。

**强保证的通用套路：拷贝并交换（copy-and-swap）**：
1. 在**副本**上完成所有可能失败的工作；
2. 用不会失败的操作（`swap`、指针赋值、`std::move`）一次性提交。

**取舍**：强保证有成本（多一次拷贝）。标准库的选择因容器而异：`vector::push_back` 在元素可移动不抛或可拷贝时提供强保证；`vector::insert` 在中间插入一般只提供基本保证。设计接口时，要在文档里写明提供哪个级别。

**为什么重要**：异常安全不是"抛出处写 try"，而是**每个修改状态的函数**都要想过：如果在第 k 行失败，对象是什么样。

**要记住的一点**：写会修改状态的函数时，先做会失败的事，最后做不会失败的提交；把"第一次修改状态"推迟到所有可能抛出的操作之后。
