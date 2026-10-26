# hc15 · 流式中位数

成交价一笔一笔到达，面试官要你随时回答「到现在为止的中位数是多少」。经典做法是两个堆；接着问「只看最近 k 笔呢」，这时堆删不掉旧数据，要换一种结构。价格用整数最小价位（tick，`long`）存。分数在两处：偶数个数时中位数怎么定义，以及滑动窗口里重复的价格怎么删。

## 面试官会怎么说

> "Prices arrive one by one. Support `add(price)` and `median()`."
> 接着会问："What do you return for an even count?" "Now only the last k prices count." "What if I want the 95th percentile?" "What if prices are bounded?" "A million operations?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：偶数个时取哪个？价格是整数吗？没有数据时怎么办？ |
| 3–16 分钟 | **Part 1**：两个堆 |
| 16–32 分钟 | **Part 2**：最近 k 笔的滑动窗口中位数 |
| 32–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 两个堆（约 13 分钟）

| 语言 | 签名 |
|---|---|
| Java | `class StreamingMedian` · `void add(long price)` · `long median()` |
| C++ | `class StreamingMedian` · `void add(long long)` · `long long median() const` |

- `median()` 返回**下中位数**（lower median）：把已有的数排序，取第 `⌈n/2⌉` 小的那个，即下标 `(n - 1) / 2`。奇数个就是正中间；偶数个取中间两个里较小的，结果一定是真实出现过的整数价格。
- 没有数据：Java 抛 `NoSuchElementException`，C++ 抛 `std::out_of_range`。
- 例子：加入 `5, 1, 9` → 5。加入 `10, 20` → 10；再加 `30, 40` → 20。`{7,7,7,-3}` → 7；再加两个 `-3` 变成 `{-3,-3,-3,7,7,7}` → -3。

## Part 2 · 最近 k 笔的中位数（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `WindowMedian(int k)` · `void add(long price)` · `long median()` |
| C++ | `WindowMedian(int k)` · `void add(long long)` · `long long median() const` |

- 只有最近 k 笔参与：加入第 k+1 笔时，最老的一笔离开窗口。窗口没满时和 Part 1 一样。
- 规则同 Part 1（下中位数、没数据抛异常）；`k < 1` 抛 `IllegalArgumentException`（C++：`std::invalid_argument`）。
- 结构：用一个队列记住到达顺序，用「较小的一半」和「较大的一半」两个有序容器存价格。C++ 用两个 `std::multiset`；Java 用两个 `TreeMap<Long, Integer>`（价格 → 出现次数）。堆不能删任意元素，所以这里换成有序容器。
- 离开的那笔要从它所在的那一半里**只删一个**，再重新平衡两半的个数（较小的一半个数 = 较大的一半个数，或多一个）。
- 例子：`k = 3`，依次加 `1, 2, 3` → 2；加 `100`，窗口 `{2,3,100}` → 3；加 `200`，窗口 `{3,100,200}` → 100。
- 例子：`k = 4`，窗口 `{5,5,5,9}` → 5；再加两个 `9`，窗口 `{5,9,9,9}` → 9。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么中位数能用「一个大顶堆 + 一个小顶堆」？
2. 滑动窗口为什么不继续用堆？惰性删除（lazy deletion）是什么？
3. 任意百分位（比如 P95）怎么做？
4. 价格在一个已知的小范围里时，有没有更简单的做法？
5. 一百万次操作要多久？
6. 偶数个时想要真正的平均数怎么办？会不会溢出？

## 边界

- 没有数据时取中位数
- 偶数个、奇数个
- 重复价格，包括窗口里全是同一个价格
- `k = 1`
- 负数价格

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc15_streaming_median       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc15_streaming_median --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc15_streaming_median       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc15_streaming_median --tag part1
```
