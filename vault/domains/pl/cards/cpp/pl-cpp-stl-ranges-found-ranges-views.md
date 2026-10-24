---
id: pl-cpp-stl-ranges-found-ranges-views
node: cpp.stl-ranges
type: qa
step: 5
---
## Q
C++20 的 ranges 与 views 是什么？惰性管道怎样求值，与传统的迭代器对算法相比好在哪里？

## A
**range**（范围）：任何能给出 `begin()` 和 `end()` 的东西，如 `vector`、数组、视图。**view**（视图）：一个**轻量、不拥有数据**的范围，拷贝是 O(1)，它描述"如何看待"底层数据而不复制数据。常用视图：`filter`（过滤）、`transform`（映射）、`take`（取前 n 个）、`drop`、`reverse`、`zip`（C++23）。

**管道写法**（`|` 把视图串起来）：

```cpp
auto p = nums | views::filter(is_even) | views::transform(square) | views::take(2);
// 构建 p 时什么都没算；for 遍历时才逐个元素拉取
```

**惰性求值**：本机实测，给 filter 和 transform 的 lambda 加打印。构造管道时一行都没有输出；遍历时按元素**逐个流过整条管道**：

```
  filter 1
  filter 2
  transform 2
got 4
  filter 3
  filter 4
  transform 4
got 16
  filter 5
  filter 6
```

要点：元素 1 被过滤掉就不进 `transform`；每产出一个结果，管道才继续往后拉。**没有任何中间容器**，内存占用是 O(1)。

**注意最后的 `filter 5`、`filter 6`**：取到第二个结果 16 之后，迭代器自增时 `filter` 为了找下一个元素又多算了两次，哪怕 `take(2)` 之后不再需要。视图的求值次数不一定与直觉一致，带副作用的谓词会出意外。

**物化**：`std::ranges::to<std::vector>()`（C++23）把视图收集成容器；实测 `nums | transform(...) | to<vector>()` 得到 10 个元素。

**与传统写法对比**：

| | 迭代器对 | ranges |
|---|---|---|
| 调用 | `std::sort(v.begin(), v.end())` | `std::ranges::sort(v)` |
| 串联 | 每步存中间容器 | 管道，惰性 |
| 错误 | 模板深处，百行 | concepts，短 |
| 投影 | 写 lambda | `ranges::sort(v, {}, &T::field)` |

**对比其他语言**：Rust 的迭代器适配器（`.filter().map()`）、Java 的 `Stream`、Python 的生成器表达式，思路相同，都是惰性管道。差别在 C++ 的视图是**纯库实现、编译期展开**，在 `-O2` 下通常能优化到和手写循环相当；Java Stream 有运行时开销，且只能消费一次。

**要记住的一点**：视图不拥有数据，所以它的有效期受底层数据约束；用视图表达变换，用 `ranges::to` 在需要时物化。
