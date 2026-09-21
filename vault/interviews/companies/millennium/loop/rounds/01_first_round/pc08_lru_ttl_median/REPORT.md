# pc08 LRU Cache + TTL + Median From Stream — report

## Summary
QuantVault 的 Millennium 面试题单把 LRU Cache 与 Median from a Data Stream 各自独立列出（未标具体轮次）；两题都是这套题库里"经典设计题 + 追问"第一轮编码题的典型形态。3-part：Part 1 LRU Cache（一手，两种实现——`OrderedDict` 与手写双链表——互相验证）→ Part 2 加 TTL **(reconstructed)** → Part 3 Median From a Data Stream（一手，双堆）。

## Sources & confidence
MED：QuantVault Millennium 面试题单，LRU Cache、Median from a Data Stream 分别列出，未标注轮次；两题都是 Stripe/Snowflake 题库里的高频同族题。Part 2（TTL 扩展）未见一手报道，标 (reconstructed)：是 LRU Cache 面试最常见的标准追问方向。

## Approach by part
1. `LRUCache` 用 `OrderedDict.move_to_end` + `popitem(last=False)`；`LRUCacheLinked` 手写双向链表（MRU 在尾、LRU 在头）+ `dict[key -> node]`，两者在同一组随机操作序列上做行为对照（20 组场景 × 200 次操作）。
2. `LRUCacheTTL` 注入 `clock` 可调用对象；`put` 时把到期时刻记成 `clock() + ttl`（绝对时刻，不因 `get` 而刷新）；`get` 惰性检查过期，过期即视为未命中并顺带清除；容量淘汰是完全独立的第二套机制，只看 LRU 顺序不看 TTL。
3. `MedianStream` 用大顶堆（`lower`，存负数模拟）+ 小顶堆（`upper`），每次 `add` 后重新平衡到两堆大小差 ≤ 1；中位数是较大堆堆顶，或两堆堆顶平均值。

## Pitfalls hidden tests target
- `get` 未命中返回 `-1`，不抛异常；更新已存在的 key 不占用额外容量（`capacity=2` 时更新 + 再插入一个新 key 只淘汰一个）
- 两种 LRU 实现必须在随机操作序列上完全一致（用来防止"手写链表版本"漏掉某个指针更新导致淘汰顺序错误）
- TTL 是绝对到期，不是滑动窗口：`get` 命中一次不会推迟过期时间——专门用例在到期前一步 `get` 成功、到期那一步再 `get` 验证仍然按原始到期时刻过期
- 容量淘汰与 TTL 过期互相独立：TTL 还早的条目一样会被挤出（worked example 直接验证这条）
- `ttl<=0`、`capacity<=0`、`key`/`value` 非 `int`、`bool` 伪装成 `int` → 全部 `ValueError`
- `MedianStream.add` 拒绝 `bool`（`bool` 是 `int` 子类，不能悄悄当数字接受）；空流 `median()` → `ValueError`
- 中位数与暴力排序法在 20 组随机流（长度 1–40）上逐步比对，0 处不一致
- io 测试覆盖三个 part 的完整命令流；Part 3 额外挂 `fmt`（验证整数值中位数不带小数点的格式规则）

## Complexity & measured cost
Part 1：`get`/`put` 均摊 O(1)（两种实现）。Part 2：同 Part 1，惰性过期检查是 O(1)。Part 3：`add` O(log n)，`median` O(1)。perf：10 万个 `ADD`（随机整数范围 ±1,000,000）+ 一次 `MEDIAN`，`solution.py` 作为脚本端到端 < 2 s（编排者验证）。

## Test inventory
24 tests — part1 9（含 1 io）· part2 7（含 1 io）· part3 8（含 1 io/fmt、1 perf）；edge 16 · fmt 1 · perf 1 · io 3。`grep -c "def test" test_pc08.py` = 24。空 `starter.py`（`starter_template.py` 的拷贝）跑同一套测试：24 个里 22 个失败，全部三个 part 都大面积红。

## Skills exercised
O(1) 缓存的两种等价实现路径（库容器 vs 手写双向链表）及其交叉验证方法 · 依赖注入时钟把"和时间相关"的逻辑变成确定性可测试代码 · 把"过期"和"淘汰"设计成两套独立机制并在文档里把边界写死，而不是含糊地混在一起 · 双堆维护流式中位数，插入 O(log n) 与查询 O(1) 的权衡。
