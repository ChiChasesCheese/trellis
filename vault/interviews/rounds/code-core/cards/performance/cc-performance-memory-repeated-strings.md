---
id: cc-performance-memory-repeated-strings
node: performance.memory
type: qa
---
## Q
10^6 rows each carry a merchant id drawn from a pool of 5 000 distinct values. Your per-row records hold one `str` per row and memory is tight. What cheap change buys the most?

## A
**Intern the repeated strings so 10^6 references point at 5 000 objects.** The parser allocates a fresh `str` per line, so identical ids are not shared by default.

```python
pool = {}
mid = pool.setdefault(mid, mid)     # or sys.intern(mid)
```

- Better still: map each id to a small `int` index once at parse time, store the int, and recover the string only when rendering output.
- Same trick for repeated status codes, currency codes and dates.
- It costs three lines and typically saves 30–50 % on id-heavy inputs — no algorithmic change.

## Q zh
10^6 行，每行带一个商户 id，取自 5 000 个不同值的池子。你的每行记录各存一个 `str`，内存吃紧。哪个便宜的改动收益最大？

## A zh
**把重复字符串驻留（intern），让 10^6 个引用指向 5 000 个对象。** 解析器每行都新分配一个 `str`，所以相同的 id 默认并不共享。

```python
pool = {}
mid = pool.setdefault(mid, mid)     # 或 sys.intern(mid)
```

- 更好：解析时一次性把每个 id 映射成一个小 `int` 下标，存这个 int，只在渲染输出时还原字符串。
- 同样适用于重复的状态码、币种代码和日期。
- 代价三行代码，在 id 密集的输入上通常省下 30–50% —— 算法一字未改。
