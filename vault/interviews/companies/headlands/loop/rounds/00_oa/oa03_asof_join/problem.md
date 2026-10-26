# oa03 · 时间点连接（as-of join）

给两张按时间戳升序排好的表：左表是成交（trades），右表是报价（quotes）。对左表的每一行，找出时间不晚于它的最新一条报价，把价格接上去。这是量化公司的日常操作，题目本身很短，难点在三处：「不晚于」包不包含相等、多个品种怎么同时维护、以及后面一连串关于乱序和流式的追问。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "You are given two timestamp-sorted tables, leftRows and rightRows. For each left row, attach the most recent right row at or before its timestamp."
> 接着会问："What if there are many symbols?" "What if you only accept a match within a time tolerance?" "What if the input isn't sorted?" "What if the data is streaming?" "How is this different from pandas merge_asof?"

题目的具体读法：左表每行是 `(ts, symbol)`，右表每行是 `(ts, symbol, price)`。对每个左行，返回「symbol 相同、且 `right.ts <= left.ts`」的最新右行的 price；没有这样的右行就返回「无匹配」（Java `OptionalLong.empty()`，C++ `std::nullopt`）。

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：相等的时间戳算不算匹配？同一时刻有多条右行取哪条？没有匹配返回什么？ |
| 3–15 分钟 | **Part 1**：单一品种，双指针 |
| 15–30 分钟 | **Part 2**：多个品种，哈希表 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 单一品种，双指针（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<OptionalLong> joinSingle(List<Left> left, List<Right> right)` |
| C++ | `std::vector<std::optional<long long>> join_single(const std::vector<Left>&, const std::vector<Right>&)` |

- Java 用嵌套 record：`AsOfJoin.Left(long ts, String symbol)`、`AsOfJoin.Right(long ts, String symbol, long price)`；C++ 在命名空间 `asof` 里有同样字段的 `Left`、`Right` 结构体。
- 忽略 symbol 列，两张表都按 ts 升序。结果和左表等长、同序。
- `right.ts == left.ts` 算匹配（「at or before」）。
- 例子：左 ts = 5, 12, 20；右 (ts, price) = (1, 100), (10, 110), (15, 115)，结果是 100, 110, 115。
- 左 ts = 1, 5；右只有 (3, 30)：结果是「无匹配」, 30。

## Part 2 · 多个品种（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<OptionalLong> join(List<Left> left, List<Right> right)` |
| C++ | `std::vector<std::optional<long long>> join(const std::vector<Left>&, const std::vector<Right>&)` |

- 只有 symbol 相同的右行才能匹配。一趟扫描：用哈希表 symbol → 目前见到的最新 price。
- 同一时刻 `right.ts == left.ts` 的右行算数；同一品种同一时刻有多条右行时，取表里靠后的那条。
- 例子：左 (5, A), (5, B), (9, B), (9, A)；右 (1, A, 10), (2, B, 20), (7, B, 21)，结果是 10, 20, 21, 10。
- 左 (5, A), (8, A)；右 (1, B, 1), (6, A, 60)：A 在 5 时还没有报价，结果是「无匹配」, 60。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 只接受时间差不超过 T 的匹配（`left.ts - right.ts <= T`），怎么改？
2. 输入没有排序怎么办？
3. 数据是流式的，右表可能乱序到达，怎么处理？
4. pandas 的 `merge_asof`、kdb 的 `aj` 和这题是什么关系？
5. 为什么不直接对每个左行扫一遍右表？

## 边界

- 任一张表为空
- 左行比所有右行都早（无匹配）
- `right.ts == left.ts`
- 同一品种同一时刻有多条右行
- 右表里有左表从没出现的品种

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/00_oa/oa03_asof_join       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/00_oa/oa03_asof_join --tag part1
python3 tools/cpptest.py start loop/rounds/00_oa/oa03_asof_join       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/00_oa/oa03_asof_join --tag part1
```
