---
id: hl-hc09-integer-tick
node: problems.hc09-top-trades-by-notional
type: qa
step: 6
---
## Q
为什么价格用整数 tick 而不用 `double`？结合律对并行聚合为什么关键？平行数组（SoA）有什么好处和代价？

## A
tick 是最小报价单位（美股常见 1 tick = 0.01 美元，`180.00` 存成 `18000`）。`double` 表示不了 0.1 这类小数，累加有误差，且**加的顺序不同结果不同**：`(0.1+0.2)+0.3 = 0.6000000000000001`，`0.1+(0.2+0.3) = 0.6`。

后果：
- 浮点误差会把两个「应相等」的 notional 变成「谁大谁小」，**tie-break 失效**；
- Part 4 分块并行累加再合并，合并顺序取决于线程调度，浮点结果每次可能不同。

整数加法满足**结合律**（`(a+b)+c == a+(b+c)`）和**交换律**，怎么分块、什么顺序合并都一样——这是并行聚合正确的根本原因。金融惯例：钱用整数最小单位，或 `BigDecimal`；浮点价格要先转整数 tick 或定点数；notional 用 `BigDecimal`。

**平行数组**（parallel arrays / SoA，每字段一个数组）：`prices`、`volumes` 是 `long[]`，内存连续，CPU 缓存能一口气预取很多个——局部性好；对比 AoS（每条记录一个对象）`List<Trade>` 对象散落堆各处要追指针。例外：`String[] tickers` 是指针数组，按 ticker 聚合时仍要追指针。代价：数组间「对齐」靠约定，长度不等编译也过，所以先检查等长，不等抛 `IllegalArgumentException`。

变体：VWAP（成交量加权均价）= Σ(price×volume)/Σvolume，小心整除与分母 0；每个 ticker 内部的前 k 笔最大成交：`groupingBy` + 每组一个堆。
