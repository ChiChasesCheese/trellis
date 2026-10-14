# hc11 · REPORT

## 概要

1p3a 2025-06 技术电面：「订单区间最大重叠 + 按买卖方处理撤单」。Part 1 是 LeetCode 253 的核心，考 tie 规则（同一时刻先结束后开始）；后面考你能不能把撤单翻译成「改区间」、在线维护，以及能否从零推出线段树和坐标压缩。讲义：`study/30-articles/hc11_order_interval_overlap.md`。

## 来源与置信度

见 problem.md §来源。置信度中：1p3a 1134455 一条，只有摘要一句话（QuantVault 标题同源，不计）。「最大重叠」「按买卖方撤单」的方向来自证据；半开区间约定、撤单 = 截短区间、Part 3 在线版、Part 4 坐标压缩全部 (reconstructed)；拿到原帖全文后以全文为准。

## 逐 Part 思路

1. **peak / maxOverlap**：start 数组与 end 数组各自排序，像归并一样扫描；处理第 i 个 start 时，`while ends[j] <= s` 则 `j++`（半开区间：同一时刻先结束；闭区间版改成 `<`）；`live = (i+1) - j`；严格 `>` 才更新，保留最早时刻。空区间跳过；只比较不做减法（坐标可以接近 `Long.MAX_VALUE`）。
2. **analyze**：先收集 Place（重复 id 报错）和 Cancel（`merge(id, time, Math::min)`，最早的撤单生效），再检查撤单 id 存在（与事件顺序无关）；有效区间是 `[start, min(end, cancel))`，`≤ start` 则跳过；按 BUY / SELL / ALL 三个 Lane 各扫一次（ALL 必须单独扫，因为买卖两边的峰值时刻可能错开）。switch 对 sealed `OrderEvent` 不写 default。
3. **OnlineOverlap**：每个车道（BUY / SELL / ALL）维护：`expiries`（TreeMap 结束时间 → 个数，即差分数组的未来部分）、`history`（TreeMap 变化点 → 活跃数，用 `floorEntry` 回答 `liveAt`）、`live`、`committedMax / Time`。`advance(to)` 先给 `lastTick` 封账，再 `pollFirstEntry` 折叠到期的订单；同一时间戳内先 place 后 cancel 不能污染最大值，所以最大值在时钟前进时才封账，查询当前值时临时比较（严格 `>` 保留最早时刻）。cancel 把订单的 end 改成撤单时间（替换 record），同时从 `expiries` 里撤掉原来的结束时间；已结束 / 已撤的订单返回 false；先校验再改状态。`t > now` 的预测查询不支持（抛 IAE）。
4. **IntervalIndex**：端点排序去重（二分查找定位）；基本段是 `[c[j], c[j+1])`，`[s, e)` 覆盖 `idx(s) .. idx(e)-1`；线段树用标记永久化：`mx[node] = add[node] + max(左右子)`，查询回溯时 `best + add[node]`；`maxIn` 用 floorIndex / lowerBound 定位段，伸出端点范围的部分按 0 计。

## 隐藏测试会打的坑

事件只按时间排序（同一时刻 +1 / -1 的顺序不定，`[1,3)` + `[3,5)` 会得出 2）；闭区间和半开区间混淆；以为 all = buy + sell；在线版每次 place 后就更新最大值；撤单时忘了撤掉 `expiries` 里原来的结束时间（之后到期又减一次）；`expiries` 计数减到 0 不删键；撤单时间 ≥ 计划结束仍算生效；先改状态后校验；`(lo+hi)/2` 溢出、`end-start` 溢出；线段树漏了 `+add[node]`；把 `[s, e)` 映射成 `idx(s)..idx(e)`；坐标不去重；对输入数组原地排序。

## 复杂度 + 实测时间

本机 12 核、JDK 21。

* Part 1 O(n log n)：1e6 个区间约 80 ms。
* Part 2 O(n log n)：50 万 Place + 25 万 Cancel 约 85–125 ms。
* Part 3 每个事件 O(log n)：60 万 place + 20 万 cancel 约 305–320 ms。
* Part 4 构造 O(m log m)、每次操作 O(log m)：30 万个 1e18 量级的区间建索引约 100 ms，10 万次 `maxIn` 约 27 ms；同样的数据扫描线只要 21 ms（只求全局最大时扫描线更好）。
* perf 预算 2 s。

## 测试清单

73 个：part1 19、part2 18、part3 17、part4 19；edge 27、perf 4、fmt 1、conc 0。part3 对随机事件流的每个前缀都用 Part 2 的 `analyze` 对拍。

## Java 21 特性

| id | 用在哪 |
|---|---|
| J01 record | `Peak` / `Place` / `Cancel` / `Report` / `Order`，紧凑构造器做校验 |
| J02 sealed | `OrderEvent` |
| J03 + J04 | `analyze` / `apply` 里的 switch 模式匹配 + record 模式 |
| J05 | switch 表达式 + `yield`（Lane 选择、apply） |
| J09 | TreeMap 的 `firstEntry` / `pollFirstEntry` / `floorEntry`（SequencedMap） |
| J08 | `var` |
| J07 | 文本块（测试脚本） |
| J13 | 未命名模式 `_`（测试，预览） |

## 面试官可能的追问

1. **为什么同一时刻先结束后开始？闭区间呢？** 半开区间用 `ends[j] <= s`，闭区间用 `<`；先问清楚约定。
2. **能用堆吗？** 可以（Meeting Rooms II）：按 start 排序 + 最小堆存结束时间。两数组做法不分配对象、tie 规则直观、容易扩展到方向和撤单。
3. **撤单比下单先到？** 批量版先收集再计算，与顺序无关；在线版事件已按时间排序，未知 id 抛异常。
4. **在线版同一时间戳先加后撤？** 最大值在时钟前进时才封账，查询当前值时临时比较。
5. **预测 `t > now` 时的活跃数？** live 减去 `expiries` 中键 ≤ t 的总和，TreeMap 遍历 O(k)；要 O(log n) 需要离线压缩 + Fenwick / 线段树，或带子树和的平衡树；而且不包含未来的撤单。
6. **什么时候用线段树而不是扫描线？** 只要全局最大，扫描线更快；增删交错、区间查询、在线反复查询时才上线段树，并且先做坐标压缩。
7. **懒标记为什么不下推？** 「区间加 + 区间最大」满足平移不改变相对大小，可以标记永久化；区间赋值 / 区间和就需要下推。
8. **坐标事先不知道？** 动态开点线段树（值域 [0, 2^60)，深度 60）或自己写平衡树。
