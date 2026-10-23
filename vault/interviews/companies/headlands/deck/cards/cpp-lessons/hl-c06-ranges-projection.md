---
id: hl-c06-ranges-projection
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 16
---
## Q
ranges 的投影（projection）是什么？写出按成员 `qty` 排序、按成员 `sym` 查找、取最大 `qty` 的代码。

## A
投影：算法的最后一个参数，先把元素映射为某个成员再比较，不用手写比较器。第二个参数 `{}` 表示默认比较器（`std::ranges::less`）。

```cpp
namespace rg = std::ranges;
rg::sort(fills, {}, &Fill::qty);                  // 按 qty 升序
auto it = rg::find(fills, "AAPL", &Fill::sym);    // 按 sym 查找
auto mx = rg::max_element(fills, {}, &Fill::qty); // qty 最大的
```
- 例：`{MSFT 50, AAPL 100, NVDA 10}` 按 qty 排序得 `NVDA MSFT AAPL`，AAPL 下标 2，最大 qty 是 AAPL。
- 对应 Java 的 `Comparator.comparing(Fill::qty)`。
