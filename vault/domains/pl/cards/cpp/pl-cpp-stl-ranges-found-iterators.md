---
id: pl-cpp-stl-ranges-found-iterators
node: cpp.stl-ranges
type: qa
step: 3
---
## Q
迭代器（iterator）到底是什么？它的五种类别怎样决定哪些算法能用在哪些容器上？

## A
**迭代器**是"像指针一样用的对象"：`*it` 取当前元素，`++it` 移到下一个，`it == end` 判断结束。指针本身就是迭代器的一种。一个序列用**半开区间** `[begin, end)` 表示：`begin()` 指向第一个元素，`end()` 指向最后一个元素之后的位置（不能解引用）。

**为什么要这层抽象**：算法不关心数据存在哪里，只要求迭代器会做哪几件事。`std::find(first, last, x)` 只需要"前进"和"读取"，因此对数组、`vector`、`list`、文件流都适用。

**五种类别**（能力逐级增强）：

| 类别 | 额外能力 | 例子 |
|---|---|---|
| 输入（input） | 单遍读取 | 读流 |
| 前向（forward） | 可多遍 | `forward_list` |
| 双向（bidirectional） | 可 `--it` | `list`、`map` |
| 随机访问（random access） | 可 `it + n`、`it1 - it2` 常数时间 | `deque`、`vector` |
| 连续（contiguous，C++20） | 元素在内存里连续 | `vector`、`array` |

**算法按所需类别选择**：`std::sort` 需要随机访问（要跳到任意位置交换），所以不能用于 `std::list`。`std::list` 自己带成员函数 `list.sort()`。如果硬写 `std::sort(l.begin(), l.end())`，C++17 之前的写法会在标准库深处爆出一屏模板错误（本机实测一次错误展开 126 行，核心是 `invalid operands to binary expression ('std::__list_iterator<int, void *>'...)`），C++20 的 `std::ranges::sort(l)` 则报：`'std::list<int> &' does not satisfy 'random_access_range'`。

**标准库如何利用类别**：`std::advance(it, n)` 在随机访问迭代器上是 O(1)（`it += n`），在双向迭代器上是 O(n)（循环 `++it`）。同一个函数名，根据类别选择最优实现，这是静态多态的典型用法。

**与其他语言对比**：Java 的 `Iterator` 只有 `hasNext/next`，Python 的迭代器只有 `__next__`，Rust 的 `Iterator` trait 是单遍，加上 `DoubleEndedIterator`、`ExactSizeIterator` 等 trait 表达能力。C++ 的特点是**类别层次直接决定算法可用性与复杂度**。

**要记住的一点**：C++ 里问"这个算法能不能用在这个容器上"，答案取决于迭代器类别；容器的选择会限制你能用的算法。
