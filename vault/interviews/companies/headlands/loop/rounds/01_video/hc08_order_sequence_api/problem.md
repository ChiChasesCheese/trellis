# hc08 · 订单序列的前缀查询

交易系统里有一串活跃订单，按到达的先后排好。你要维护这串订单：往末尾放一张、删掉（或减少）一张，并回答「排在订单 X 前面的有几张、总数量是多少」。第一版用 `LinkedHashMap` 或列表，查询从头数一遍就行；面试官接着会问「订单有几百万张，查询能不能不扫全表」，答案是树状数组（Fenwick tree）。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Maintain a sequence of active orders in insertion order. `put(id, qty)` appends an order, `delete(id, qty)` removes that quantity from it, and `countBefore(id)` / `quantityBefore(id)` return how many orders, and how much total quantity, sit strictly before `id`."
> 接着会问："Can the queries be sublinear?" "What if the memory must stay bounded as orders come and go?" "What if several threads call this?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：删除是整单还是可以只减一部分？删光后再 `put` 同一个 id 排在哪里？ |
| 3–15 分钟 | **Part 1**：`LinkedHashMap` 版，查询线性扫描 |
| 15–30 分钟 | **Part 2**：树状数组版，查询 O(log n) |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 朴素版（约 12 分钟）

| 语言 | 类与方法 |
|---|---|
| Java | `OrderSequence`：`void put(long id, long qty)` · `long delete(long id, long qty)` · `int countBefore(long id)` · `long quantityBefore(long id)` |
| C++ | `ordseq::OrderSequence`：`put` · `del` · `count_before` · `quantity_before`（`del` 因为 `delete` 是关键字） |

- `put`：订单放到序列末尾。`qty <= 0` 或 id 已经活跃：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- `delete`：减少 `qty` 个单位，返回剩余数量；剩余为 0 时订单离开序列；没删光的订单位置不变。未知 id：`NoSuchElementException` / `std::out_of_range`。`qty <= 0` 或超过剩余：`IllegalArgumentException` / `std::invalid_argument`，状态不变。
- `countBefore(id)`、`quantityBefore(id)`：排在 `id` 前面（不含它自己）的订单数、剩余数量之和。未知 id 同样抛 `NoSuchElementException` / `std::out_of_range`。
- 例子：依次 `put(10,5)`、`put(20,3)`、`put(30,7)`，则 `countBefore(30) = 2`，`quantityBefore(30) = 8`，`quantityBefore(10) = 0`。
- `delete(10,2)` 返回 3，订单 10 仍排第一；`delete(20,3)` 返回 0，20 离开序列，这时 `countBefore(30) = 1`，`quantityBefore(30) = 3`。
- 删光之后再 `put(20,4)`，20 排到最后：`countBefore(20) = 2`，`quantityBefore(20) = 10`。

## Part 2 · 树状数组（约 15 分钟）

| 语言 | 类与方法 |
|---|---|
| Java | `FastOrderSequence(int capacity)`，方法同上 |
| C++ | `ordseq::FastOrderSequence(int capacity)`，方法同上 |

- 接口和错误规则与 Part 1 完全一样，只是 `countBefore` / `quantityBefore` 要 O(log n)。
- 构造时给定 `capacity`：整个生命周期里 `put` 的总次数上限（删除不回收位置）。位置用完后再 `put`：Java 抛 `IllegalStateException`，C++ 抛 `std::logic_error`。
- 每次 `put` 拿到下一个位置 1, 2, 3, …；用两棵树状数组分别存「订单数」和「数量」。删光订单时把它位置上的订单数减 1、数量减去剩余量，位置不再使用。
- 测试里 20 万次 `put` 加 10 万次 `countBefore` 和 10 万次 `quantityBefore` 要在几秒内跑完；对同一串随机操作，结果必须和 Part 1 一致。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 删除只留洞、位置只增不减，内存怎么控制？压缩（compaction）的摊还代价是多少？
2. 为什么用树状数组而不用线段树，或者 `TreeMap`？
3. 总数量加起来可能超过 `long` 的范围，怎么处理？
4. 多个线程同时 `put` 和查询，怎么办？
5. 自己写哈希表时，为什么要先用 splitmix 之类的函数把 id 搅一遍？
6. 如果还要「第 k 张订单是谁」，树状数组能做吗？

## 边界

- 空序列上的查询：未知 id。
- 只有一张订单：`countBefore` 和 `quantityBefore` 都是 0。
- 删光再 `put` 同一个 id：排到最后。
- 位置用完的那一次 `put`（容量等于已用位置数）。
- id 为 0、负数、`Long.MIN_VALUE` 都是合法 id。

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc08_order_sequence_api       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc08_order_sequence_api --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc08_order_sequence_api       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc08_order_sequence_api --tag part1
```
