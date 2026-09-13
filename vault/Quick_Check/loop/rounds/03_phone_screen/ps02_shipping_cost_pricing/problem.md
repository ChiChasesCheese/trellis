# ps02 · Shipping Cost Pricing — 统一定价 → 数量分档 → incremental/fixed 混合计费

**类型：** 电面 / 实习技术电面（解锁式，HackerRank） · **阶段：** 技术电面（约 1 小时，"时间紧张"） · **最近一次出现：** 2025-10-20（learncswithus.com） · **出现频率：** 2 篇独立记录（learncswithus.com 的详细三级拆解；1point3acres.com/interview/post/7100079 的"Shipping Cost Calculator"目录，逐步骤完全一致）+ linkjob.ai P9"会计/分档定价"实习技术电面（`en_forums.md` 第 151 行，2025，"Part 1 订单+运费总额 → Part 2 分档定价，单价随数量增加而降低 → Part 3 两种计费模型：incremental vs fixed-pricing"），从英文侧独立证实了同一个三级结构 · **可信度：** 高（两个中文来源目录几乎一致 + 一个英文来源证实同样的三部分递进结构，且关键的是 Part 3 精确一致的 `incremental` / `fixed` 术语）

## 背景
一个基于 Stripe 的电商平台需要在结账时对运费定价：一张国家/产品费率表 + 一份订单列表。
Level 1 是简单的单位定价查找（dict）。Level 2 把费率变成数量**分档**（volume bands）——
真实候选人反馈这是"最难的一级，因为没有明确的类型标记来区分它和 Level 1，必须自己发现
区间逻辑"。Level 3 给每个档位加上一个 `type`（`incremental` vs `fixed`），这正是
累进计费 vs 单一统一费率档位的区别 —— 与 Stripe Billing 自身在 `graduated` 和
`tiered`（`volume`）定价之间的区分完全一致。

## 输入（stdin）
```
PART n
RATES
<费率行>
<费率行>
...
ORDERS
<订单行>
<订单行>
...
```
* `PART n` —— `n` ∈ {1,2,3}。`RATES` 和 `ORDERS` 字面标记行是必须的且大小写敏感；
  两者之间的都是费率行，之后的都是订单行。
* **订单行**（所有 part 通用）：`order_id,country,product,quantity` —— `quantity`
  是非负整数。输出是**每个订单一行，按输入顺序**（订单是独立查询，不聚合/分组/排序 ——
  不同于 ps01/q03 的按用户分组）。
* **费率行**，schema 取决于 `PART n`：
  - Part 1（统一定价）：`country,product,unit_cost`
  - Part 2（分档）：`country,product,min_qty,max_qty,cost` —— `cost` 是该档位的
    **单位**费率。
  - Part 3（混合）：`country,product,min_qty,max_qty,cost,type` —— `type` ∈
    `{incremental, fixed}`。
* 所有货币字段（`unit_cost`、`cost`）都是**0-2 位小数**的普通十进制字符串，没有货币符号，
  没有千位分隔符（`5`、`5.0`、`5.00`、`12.50` 都合法；`12.5000` 是格式错误）。解析为整数分 ——
  **绝不使用浮点数**。
* `min_qty`/`max_qty` 都是整数；`max_qty` 可以是**字面 token `inf`**（小写，精确匹配），
  表示无上限。区间是**两端都闭合**：`[min_qty, max_qty]`（恰好等于某一边界的数量属于该档）。
* 同一个 `(country, product)` 的各档位**不会重叠**，但在费率表中**可能以任意顺序出现**
  （使用前按 `min_qty` 排序 —— 不要假设文件已排序）。
* 最多约 200 条费率行，10^5 条订单行。

## 输出
每个订单一行，按输入顺序：`order_id: $x.xx`（两位小数，`$` 符号，`: ` 分隔符，与 OA 惯例
一致），或对被拒订单输出 `order_id: ERROR <message>` —— 见下方三种错误信息格式（精确固定，
隐藏测试逐字匹配）。

## 规则

### Part 1 — 统一单位定价
`unit_cost × quantity`。如果 `(country, product)` 完全没有费率行：
`ERROR unknown product <country>/<product>`。`quantity = 0` 始终定价为 `$0.00`
（仍要求产品存在于费率表中 —— 未知产品的零数量订单仍然报错）。

### Part 2 — 数量分档，单一命中档位定价
找到 `[min_qty, max_qty]` 包含订单 `quantity` 的档位（闭区间，`max_qty = inf` 表示无上限）。
**整个**订单数量都按该档位的费率计费：`cost × quantity`（不是累加式 —— 15 单位的订单落在
"11–20"档，就按 `15 × band_11_20.cost` 计价，仅此而已；这就是下方 Part 3 所称的
`fixed` 计费类型）。
错误（按此顺序检查）：
1. `(country, product)` 完全没有费率行 → `ERROR unknown product <country>/<product>`
2. 有费率行但没有任何档位的区间包含 `quantity`（覆盖范围中的**缺口**，或 `quantity`
   低于第一档的 `min_qty`）→ `ERROR no tier for <country>/<product> at qty=<quantity>`
`quantity = 0` 不做档位查找直接定价为 `$0.00`（与 Part 1 相同的产品必须存在规则）。

### Part 3 — incremental/fixed 混合计费
与 Part 2 相同的档位查找（找到包含 `quantity` 的档位；同样的两种错误情形和相同的信息）。
**命中档位的 type**（不是任何其他档位的）决定整笔订单如何定价：
* **`fixed`**：与 Part 2 相同 —— `matched_band.cost × quantity`。
* **`incremental`**：累进/阶梯式计费（类似个税阶梯）。从 `min_qty = 1` 开始，按 `min_qty`
  升序遍历每一档直到命中档位；每一档贡献"落在该档内的数量" × "该档自身费率"，其中"落在
  该档内"对最后（命中）档位以 `quantity` 为上限截断。所遍历的档位**必须从 1 开始连续**
  （`band[i].min_qty == band[i-1].max_qty + 1`，第一档的 `min_qty == 1`）—— 命中档位
  **及之前**的链条出现断裂是一种独立的错误：`ERROR incremental gap for <country>/<product>
  at qty=<quantity>`（只有当订单数量真的需要穿过缺口时才触发 —— 一个完全落在缺口**之前**
  某档内的数量永远不会遇到它，见下方演示样例）。
* 缺口检查是按订单进行的，不是费率表的静态校验 —— 一张费率表可能存在缺口但从未被任何订单
  查询到，这不算错误。

## 演示样例
```
# Part 1
RATES
US,widget,5.00
CA,widget,7.25
ORDERS
o1,US,widget,3
o2,CA,widget,2
o3,US,gadget,1
-->
o1: $15.00
o2: $14.50
o3: ERROR unknown product US/gadget

# Part 2（费率表中的档位故意乱序 —— 使用前必须按 min_qty 排序）
RATES
US,widget,21,inf,4.00
US,widget,1,10,5.00
US,widget,11,20,4.50
ORDERS
o1,US,widget,5
o2,US,widget,15
o3,US,widget,50
-->
o1: $25.00     (5 单位，全按 1-10 档的 5.00 -> 5 * 5.00)
o2: $67.50     (15 单位，全按 11-20 档的 4.50 -> 15 * 4.50，不是累加式)
o3: $200.00    (50 单位，全按 21-inf 档的 4.00 -> 50 * 4.00)

# Part 3（同样的 1-10/11-20/21-inf 美国阶梯，现在是 'incremental'；另一条独立的加拿大阶梯，'fixed'）
RATES
US,widget,1,10,5.00,incremental
US,widget,11,20,4.50,incremental
US,widget,21,inf,4.00,incremental
CA,widget,1,10,5.00,fixed
CA,widget,11,20,4.50,fixed
ORDERS
o1,US,widget,15
o2,CA,widget,15
-->
o1: $72.50     (incremental: 10 单位 @ 5.00 = 50.00，+ 5 单位 @ 4.50 = 22.50 -> 72.50)
o2: $67.50     (fixed: 命中档位是 11-20 @ 4.50 -> 15 * 4.50，与 Part 2 的 o2 数字相同)

# Part 3 — incremental 缺口，取决于具体订单（这是最微妙的一个，务必手算验证）
RATES
US,widget,1,10,5.00,incremental
US,widget,15,inf,3.00,incremental
ORDERS
o1,US,widget,5
o2,US,widget,20
-->
o1: $25.00                                          (5 单位，完全落在 1-10 内，从未触及
                                                       11-14 的缺口 -> 不报错)
o2: ERROR incremental gap for US/widget at qty=20    (命中档位是 15-inf，但从 1 开始遍历
                                                       链条时先撞上 11-14 的空缺)
```

## 隐藏测试已知会针对的边界情况
- Part 1：未知的 `(country, product)` 组合；`quantity = 0`；0/1/2 位小数的金额字符串
  （`"5"`、`"5.5"`、`"5.50"` 都表示相同的 5.50）。
- Part 2：档位行在文件中乱序（必须排序）；数量恰好落在档位边界上（`min_qty` 和 `max_qty`
  都闭合 —— 同一档位的两端都要测试）；数量落在两档之间真正的缺口中；`max_qty = inf` 的
  开放顶档；`quantity = 0`。
- Part 3：**相同数量**下 `fixed` 和 `incremental` 必须给出不同但都正确的结果
  （上方演示样例，数量 15 时的 `$67.50` vs `$72.50`）；数量完全落在第一档内的订单永远
  不会遇到下游的缺口（不误报错误）；数量需要穿过缺口的订单**确实**报错，且报的是
  `incremental gap` 信息（不是 `no tier` 信息 —— 命中档位查找本身是成功的）。
- 格式：货币输出始终两位小数，始终带 `$` 符号；错误信息**逐字**匹配三种模板
  （`unknown product`、`no tier`、`incremental gap`）—— 隐藏测试做精确字符串比较，
  不是子串/前缀匹配。
- 性能：最多约 200 条费率行和 10^5 条订单行；一个 dict-of-lists 的费率表，每笔订单
  `O(log bands-per-product)` 的查找足以留有充足预算（实际每个产品的档位数很少 —— 在这个
  规模下每笔订单线性扫描也完全没问题，也是参考实现的做法；`bisect` 替代方案作为后续追问
  提及，不要提前过度设计）。

## 见过的变体
- learncswithus.com 明确报告"没有明确的类型标记来区分 [Level 2 与 Level 1]，必须自己
  发现区间逻辑"—— 也就是说在真实面试中，分档 schema 不会像本练习的五字段 CSV 这么干净地
  交给你；预计需要从自然语言描述或嵌套 dict 中推断出结构，并主动询问关于半开还是闭区间的
  澄清问题（本练习已经把这点敲定；真实面试可能没有）。
- linkjob.ai 的 P9 记录（`en_forums.md` 第 151 行）把 Part 1 描述为"订单 + 运费总额"，
  而非纯粹的单位查找 —— 即某些变体会把统一运费附加费折入 Part 1 的总额中。本题未实现
  （按中文来源的三级目录属于范围之外），但值得作为现场追问提起（"如果还有一笔固定的每单
  运费怎么办？"）。
- 来自主要来源的评分说明：真实面试中**没有自动化测试框架**（"你自己写测试用例并运行"），
  评分是"逻辑正确性 + 代码结构，不强制要求边界处理"—— 也就是说真实候选人在精确区间边界
  情况上的评分会比本练习的隐藏测试宽松得多。把这里的严格性视为面试*练习*，而非声称
  Stripe 真实评分标准如此苛刻。

## 来源
- https://learncswithus.com/2025/10/20/stripe-intern-screen/ (Stripe SDE Intern 面经｜Technical Screen, 2025-10-20) —— 主要来源：三级结构（统一 -> 分档 -> incremental/fixed 混合），HackerRank 平台，约 1 小时，"没有自动化测试用例"，"时间紧张"评分说明。
- https://www.1point3acres.com/interview/post/7100079 ("Shipping Cost Calculator" — Problem Summary -> Step 1 Simple Fixed Price -> Step 2 Volume Discounts -> Step 3 Mixed Pricing Types -> How to Solve It -> Bonus Discussion Topics) —— 从第二个独立中文来源交叉证实完全相同的三级递进。
- `loop/raw/en_forums.md` 第 151 行，P9"Accounting / tiered pricing"（linkjob.ai 实习技术电面记录，2025）—— 英文侧证实同样的三部分结构和 Part 3 的 `incremental` / `fixed` 术语。
- `loop/raw/cn_forums.md` 第 43–56 行（汇总中文摘要，与上述两个来源交叉引用）。

## 本题考察点
skills: S02 解析（定宽 vs 变宽 CSV 行，分节标记）· S06 整数货币（分为单位，绝不用浮点）·
S07 分档/计量定价数学（闭区间档位查找，累进 vs 统一计费）· S09 精确格式化（货币 + 逐字
错误字符串）· S10 明确的错误处理（三种独立、固定的错误信息）· S19 增量式设计（Part 2 的
单一查找原样复用为 Part 3 的 `fixed` 分支）

## 面试官会怎么追问
1. "如果同一个 `(country,product)` 在 Part 2 的费率表里出现了两条区间重叠的行,你的代码会怎么样?"
   — 题面保证"不重叠",但追问是在探你是否会做防御性校验,还是假设输入总是合法就直接崩。
2. "Part 3 的 `incremental` 类型,如果费率表从 `min_qty=1` 往上数不连续(有缺口),但订单数量恰好
   落在缺口*之前*的那个 band 里,你的代码会不会误报错?" — 直接对应 worked example 里 qty=5 vs
   qty=20 的区别,检验候选人是否真的理解"只在需要穿过缺口时才报错"这条设计。
3. "如果要求换成开区间 `(min_qty, max_qty]` 或半开区间,worked example 里 Part 2 的三个答案
   (25.00 / 67.50 / 200.00)哪些会变?" — 逼你现场证明"闭区间"是让边界值(qty=10、qty=21)有唯一
   归属的必要条件。
4. "现在货币是按美分存的整数,如果面试官要求支持 3 位小数的货币(比如某些中东货币),你的
   `parse_money_to_cents` 要怎么改?" — 考察是否把"两位小数"硬编码在了多处,还是只在一个地方。
5. "10 万条订单、200 条费率,如果要求把 `_find_band` 从线性扫描换成 `bisect` 二分,你会怎么改
   数据结构?" — 期望候选人指出"每个 (country,product) 的 band 数通常很小,线性扫描已经够快;
   只有 band 数很大时二分才有意义",而不是无脑上二分。
6. "如果一个订单里有多个 product(比如一次下单买 20 个 widget 和 5 个 gadget),现在的 CSV
   protocol 要怎么扩展?" — 检验候选人是否能在不推翻现有单行 order 设计的前提下,提出一个自然的
   扩展(比如允许同一个 `order_id` 出现多行,按 `order_id` 分组求和)。
7. "费率表本身没有校验步骤 —— 如果要在读入费率表时就检测出所有 `incremental` 链条的缺口(而不是
   等订单查询时才发现),你会怎么设计一个预处理校验函数?它的时间复杂度是多少?" — 把"运行时检测"
   升级成"静态校验",考察候选人对 O(bands log bands) 排序 + 一次线性扫描的复杂度分析能力。
