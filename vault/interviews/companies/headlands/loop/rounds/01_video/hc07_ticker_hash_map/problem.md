# hc07 · 股票代码哈希表

行情系统每秒要按股票代码（ticker）查几百万次表，最直接的写法是 `unordered_map<string, long>`。面试官让你把它优化一下。突破口在 key 上：ticker 最多 8 个大写字母，正好能塞进一个 64 位整数，key 就从「堆上的字符串」变成「寄存器里的一个数」。Part 1 先把 ticker 打包成整数，Part 2 再写一个以这个整数为 key 的小哈希表。其余的优化（删除、完美哈希、缓存行）都是口头追问。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "We look up stock tickers in an unordered_map millions of times a second. How would you optimize it?"
> 接着会问："Why is a string key slow?" "How would you pack a ticker into an integer?" "Now write the hash table yourself." "How do you delete?" "What if the ticker set is known in advance?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：ticker 是不是只有 A–Z、最长几个字符？value 是什么类型？需不需要删除？ |
| 3–13 分钟 | **Part 1**：ticker 打包成 64 位整数，`encode` / `decode` |
| 13–30 分钟 | **Part 2**：开放寻址哈希表，`put` / `get` |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 把 ticker 打包进一个 64 位整数（约 10 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long encode(String ticker)` · `static String decode(long key)` |
| C++ | `std::uint64_t encode(const std::string&)` · `std::string decode(std::uint64_t)` |

- 每个字符占一个字节，第一个字符在最高位。`"AAPL"` 打包成 `0x4141504C`（十进制 1094799436），`"A"` 是 65。
- `encode`：长度不是 1..8，或含 A–Z 以外的字符，Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- `decode` 是 `encode` 的逆运算。不是合法打包值的（0、负数、含非 A–Z 的字节、字节中间有 0）同样抛异常。
- 不同的 ticker 打包结果不同：`"A"` 和 `"AA"` 不会撞，因为 `A` 的字节不是 0。合法的 key 一定 `> 0`，所以 0 可以留作「空格」标记。

## Part 2 · 开放寻址哈希表（约 17 分钟）

| 语言 | 签名 |
|---|---|
| Java | `void put(long key, long value)` · `OptionalLong get(long key)` · `int size()` · `int capacity()` |
| C++ | `void put(std::uint64_t, std::int64_t)` · `std::optional<std::int64_t> get(std::uint64_t) const` · `size()` · `capacity()` |

- 不许用 `HashMap` / `unordered_map`。两个数组（key、value）加开放寻址、线性探测（linear probing）：冲突就看下一格。
- 容量是 2 的幂，初始 16。放入新 key 之前，如果放完会超过 3/4 的装载因子（load factor），先把容量翻倍并重新插入所有 key。任何时刻 `size * 4 <= capacity * 3`。
- `put` 写入或覆盖，key 必须 `> 0`，否则抛 `IllegalArgumentException` / `std::invalid_argument`。`get` 找不到返回 `empty` / `nullopt`；value 为 0 也算存在。
- 哈希函数不能写成 `key & (capacity - 1)`：打包后低位几乎全相同，会全部挤到少数几格。测试里 3000 个低 32 位全为 0 的 key 检查这一点。
- 没有删除。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么整数 key 比字符串 key 快？
2. 要支持删除怎么办？为什么不能直接把格子清空？
3. 为什么装载因子取 3/4，不让表装满？
4. 开盘前就知道全部 ticker，还能怎么优化？
5. 缓存行（cache line）对这张表的布局有什么影响？
6. `std::hash<uint64_t>` 在常见实现里是恒等函数，这意味着什么？

## 边界

- ticker：1 个字符、8 个字符、9 个字符、空串、小写、含空格或点。
- key：0、负数、`ZZZZZZZZ`（最大的合法 key）。
- 表：value 为 0 和负数、覆盖同一个 key、增长到 20000 个 key、低位全相同的 key。

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc07_ticker_hash_map       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc07_ticker_hash_map --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc07_ticker_hash_map       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc07_ticker_hash_map --tag part1
```
