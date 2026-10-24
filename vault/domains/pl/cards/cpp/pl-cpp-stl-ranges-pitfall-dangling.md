---
id: pl-cpp-stl-ranges-pitfall-dangling
node: cpp.stl-ranges
type: qa
step: 10
---
## Q
ranges 与视图最容易踩的陷阱是什么？对临时对象调用算法、range-for 遍历函数返回值的内部成员、`const` 视图，各会怎样？

## A
**陷阱一：对临时对象取迭代器**。`std::ranges` 的算法在传入**右值容器**时返回特殊类型 `std::ranges::dangling`，让你无法解引用：

```cpp
std::vector<int> make() { return {3, 1, 2}; }
auto it = std::ranges::find(make(), 2);   // 临时 vector 在语句结束后销毁
return *it;
```

真实编译错误：`indirection requires pointer operand ('borrowed_iterator_t<std::vector<int>>' (aka 'std::ranges::dangling') invalid)`。这是 ranges 的一个设计优点：把原本的悬垂迭代器变成**编译错误**。对应的老写法 `std::find(make().begin(), make().end(), 2)` 则编译通过，是 UB。

**陷阱二：range-for 遍历临时对象的成员**。

```cpp
struct S { std::vector<int> v{1,2,3}; const std::vector<int>& get() const { return v; } };
S make() { return S{}; }
for (int x : make().get()) sum += x;     // C++20：临时 S 在循环开始前就销毁了
```

本机实测：`-std=c++20` 下，ASan 报 `stack-use-after-scope`；`-std=c++23` 下输出正确的 `sum 6`。原因是 C++23（P2718）规定，range-for 的范围表达式里**所有临时对象的生命周期延长到整个循环结束**；之前只有最外层的临时对象被延长。这是一类用了二十年的隐性陷阱，在 C++23 修复，但要靠编译器和标准版本支持。**对策**：升到 C++23，或把 `make()` 先存进局部变量。

**陷阱三：`const` 视图不能遍历**。`filter` 视图为了让 `begin()` 均摊 O(1)，会缓存第一个满足条件的位置，所以 `begin()` 不是 `const` 的：

```cpp
const auto evens = nums | std::views::filter(is_even);
for (int x : evens) {}   // 报错：'this' argument to member function 'begin' has type 'const filter_view<...>', but function is not marked const
```

**对策**：不要把视图声明成 `const`，传给函数时用转发引用（`auto&&`）或 `std::ranges::range auto&&`。

**陷阱四：视图持有对底层容器的引用，容器修改后视图失效**。`push_back` 引起重新分配，视图里缓存的迭代器就悬空。

**陷阱五：谓词有副作用**。视图的求值次数不确定，例如 `filter` 后接 `take(2)` 的管道，取到第二个结果之后，`filter` 还会多算两个元素。

**共同的根因**：视图是"借用"，而 C++ 没有机制检查借期。ranges 通过 `dangling` 把最明显的一类变成了编译错误，其余仍然是你的责任。

**对策总结**：用 C++23；开 ASan；视图只做局部临时变换，不存储、不返回。
