---
id: pl-cpp-stl-ranges-best-practice
node: cpp.stl-ranges
type: qa
step: 9
---
## Q
资深 C++ 工程师怎样使用标准容器、算法和视图？有哪些固定的习惯？

## A
**容器选择**：
1. **默认 `std::vector`**；知道大小就先 `reserve(n)`，避免反复扩容和失效；
2. 键值查找默认 `std::unordered_map`；需要有序遍历用 `std::map`；读多写少且数据量不大时试 `std::flat_map`（C++23），连续内存缓存更友好；
3. 小而定长的数据用 `std::array`；
4. 避免 `std::list`、`std::deque` 除非有明确理由并测过；
5. 热路径上考虑第三方容器（abseil 的 `flat_hash_map`、folly），它们在哈希表上常常比标准库快得多。

**算法与循环**：
1. 能用标准算法表达的，用算法（`std::ranges::find_if`、`transform`、`accumulate`）而不是手写 for：名字说明意图，也少出越界；
2. 但**简单的范围 for** `for (const auto& x : v)` 比三行 lambda 的算法更清楚，不要为用算法而用；
3. 删除用 `std::erase_if(v, pred)`（C++20）而不是手写循环；
4. 新代码用 ranges 版本的算法，报错更短。

**视图**：
1. 视图用来**表达变换**，用 `ranges::to` 在需要时物化；
2. **不要把视图存进长寿对象或返回**，除非底层数据的生命周期明确更长；
3. 谓词和变换函数**不带副作用**，因为视图的求值次数和顺序不保证与直觉一致。

**字符串与连续数据**：
1. 函数参数：只读字符串用 `std::string_view`，只读数组用 `std::span<const T>`；
2. 需要存储时存 `std::string`、`std::vector`，不存视图；
3. 不要把 `string_view` 传给要求 `\0` 结尾的 C 接口：它不保证结尾有 `\0`。

**迭代器失效**：
1. 修改容器后，假设所有迭代器、指针、引用都作废，除非文档明确说明稳定；
2. 需要稳定引用时存**索引**或用 `std::deque`、节点容器；
3. 删除时用 `it = v.erase(it)` 的形式。

**工具**：
- libc++ 加固模式 / `-D_GLIBCXX_ASSERTIONS`：`operator[]` 越界终止；
- ASan：抓失效后的使用；
- `clang-tidy` 的 `bugprone-use-after-move`、`modernize-loop-convert`、`performance-*`。

**为什么**：这些习惯的共同目标是让"容器的内存布局"和"数据的生命周期"在代码里看得见，因为这两件事是 C++ 性能与安全的真正来源。
