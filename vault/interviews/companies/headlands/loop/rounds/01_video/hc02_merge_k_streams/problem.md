# hc02 · 合并 K 个有序序列

面试官给你 k 个各自升序的序列，要你合并成一个升序序列。核心是最小堆（min-heap）：每个序列当前最小的那个元素放进堆，堆顶就是下一个输出。写完之后面试官会追问「数据是流，不能一次装进内存怎么办」，这就是惰性迭代器。多线程、非阻塞这类更深的追问放在口头部分。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Merge k sorted lists into one sorted list."
> 接着会问："What's the complexity?" "Now the inputs are streams — give me an iterator that merges them lazily." "What if each stream is slow and blocks? What if one stream never produces anything?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：k 可以是 0 吗？序列可以为空吗？元素类型是什么？有重复吗？ |
| 3–15 分钟 | **Part 1**：最小堆合并 |
| 15–30 分钟 | **Part 2**：惰性迭代器 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 最小堆合并（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<Integer> merge(List<List<Integer>> lists)` |
| C++ | `std::vector<long long> merge(const std::vector<std::vector<long long>>&)` |

- 每个输入序列升序（允许相等）。输出是所有元素的升序序列，输入不被修改。
- k = 0、全部为空、中间夹着空序列，都返回对应的结果（可能是空列表），不抛异常。
- 比较不能写 `a - b`，两个极端值相减会溢出。
- 例子：`[[1,4,7],[2,5,8],[3,6,9]]` 得到 `[1,2,3,4,5,6,7,8,9]`；`[[1,4,5],[1,3,4],[2,6]]` 得到 `[1,1,2,3,4,4,5,6]`。

## Part 2 · 惰性迭代器（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static Iterator<Integer> mergeIterators(List<Iterator<Integer>> sources)` |
| C++ | `class MergeIterator`：构造函数收 `std::vector<std::vector<long long>>`，成员 `bool has_next()` · `long long next()` |

- 构造时不读任何 source。第一次 `hasNext` / `next` 才从每个 source 各取一个队首。
- 输出一个元素后，它所在 source 的下一个元素推迟到下一次调用才取。所以消费 n 个元素最多从 source 取 k + n − 1 个。
- 要能对两个无限序列取前 10 个：偶数序列和奇数序列合并，前 10 个是 `0..9`。
- 耗尽后 Java `next()` 抛 `NoSuchElementException`，C++ 抛 `std::out_of_range`。`hasNext` 可以反复调用，不消耗元素。
- C++ 版为了简单，source 就是 vector，惰性体现在「按需从堆里弹出并补下一个」。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 复杂度是多少？k 很大、每个序列很短时和 k 很小、序列很长时有区别吗？
2. 为什么不能先拼成一个数组再排序？
3. 怎么保证相等元素的顺序稳定（序号小的序列在前）？
4. 每个 source 是会阻塞的网络连接，怎么办？
5. 「非阻塞」的接口应该长什么样？某个 source 暂时没数据时合并器能输出什么？
6. 有界缓冲区和背压（backpressure）是什么，为什么需要？

## 边界

- k = 0、全空、单个序列、空序列夹在中间
- 大量相等元素
- `Integer.MIN_VALUE` / `Integer.MAX_VALUE`（C++ 是 `LLONG_MIN` / `LLONG_MAX`）
- 迭代器耗尽之后再调 `next`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc02_merge_k_streams       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc02_merge_k_streams --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc02_merge_k_streams       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc02_merge_k_streams --tag part1
```
