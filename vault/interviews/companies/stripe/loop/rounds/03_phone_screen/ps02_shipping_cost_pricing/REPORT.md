# ps02 Shipping Cost Pricing — 报告

## 概述
在费率表 + 订单列表上的三个解锁式关卡：单位统一定价 -> 数量分档（单一命中档位定价）->
每个档位显式标注 `incremental`（累进式，类似个税阶梯）或 `fixed`（整个数量按命中档位定价）
的混合计费。这与 Stripe Billing 自身的 `graduated` vs `tiered`（volume）定价区分如出一辙，
两个独立来源（中文 + 英文）都证实了完全相同的三步结构，以及 Part 3 中精确一致的
`incremental`/`fixed` 术语。

## 来源与可信度
高 —— learncswithus.com（2025-10-20，主要来源，逐级详细记录，包括评分说明"没有自动化测试用例，
按逻辑 + 结构评分，边界情况不强制要求"）与 1point3acres.com/interview/post/7100079 的目录
（`Simple Fixed Price -> Volume Discounts -> Mixed Pricing Types`，逐字相同的递进结构）交叉印证，
并独立地由 `en_forums.md` 第 151 行（linkjob.ai P9，英文侧，明确点名 Part 3 的
`incremental`/`fixed-pricing`）再次证实。两个来源都没有给出具体数字示例，也没有敲定区间的
开闭性或精确的错误信息格式 —— 这些是重构的决定，在 problem.md 的规则部分明确标注（闭区间
`[min_qty,max_qty]`；三条固定错误字符串），而非来自原始来源的事实。

## 各部分思路
1. **Part 1**：`dict[(country,product)] -> unit_cost_cents`，每笔订单 `O(1)` 查找。
2. **Part 2**：`dict[(country,product)] -> [bands]`，解析时一次性按 `min_qty` 对档位排序
   （费率表的行顺序被明确视为不可信 —— 演示样例故意把顶档放在最前面，且有测试专门验证这点）。
   每笔订单：线性扫描找到包含该数量的档位（实际中每个产品的档位数很少；`bisect` 作为后续
   优化点写进文档，未提前实现 —— 避免对一张约 3 档/产品的表做过度设计）。
3. **Part 3**：原样复用 Part 2 的档位匹配查找；只有命中档位的 `type` 会分叉定价逻辑：
   `fixed` 调用和 Part 2 完全相同的 `qty * cost`，`incremental` 从 `min_qty=1` 开始遍历
   每一档直到命中档位，累加每一档内落在其中的数量乘以该档自身费率，并显式检查连续性
   （`incremental gap` 错误），只有当订单数量真正需要穿过缺口时才触发 —— 用一个专门的
   演示样例验证，展示*同一张*费率表既能给出正常价格（qty=5，从未触及缺口）也能报错
   （qty=20，必须穿过缺口）。

## 隐藏测试针对的坑点
- 费率表行在文件中乱序（必须先按 `min_qty` 排序再查找，不能假设文件本身有序）。
- 档位边界：`min_qty` 和 `max_qty` 都是闭区间，需在*同一*档位的两端都测试（`1-10`/`11-20`
  分界处的 `qty=10` 和 `qty=11` 必须给出不同且正确的答案）。
- 三种独立且需逐字匹配的错误字符串 —— `unknown product`、`no tier`、`incremental gap` ——
  刻意设计为不同的失败模式，不能混淆（例如命中档位查找本身出现缺口是 `no tier`，不是
  `incremental gap`；后者只在已经找到命中档位，但走向它的路径中遇到缺口时才触发）。
- 相同数量下 `fixed` 与 `incremental` 必须给出不同结果（同一形状的阶梯下 qty=15 分别是
  $67.50 和 $72.50）—— 这是最可能抓到"实现了 incremental 但悄悄忽略每档 type 字段（即始终
  累加）"这类候选人的测试。
- 货币解析：`"5"`、`"5.5"`、`"5.50"` 必须都表示相同的 5.50 —— 常见 bug 是把裸 `.5` 当成
  5 分而不是 50 分（小数部分应该右补齐，不是左补齐）。
- `quantity = 0` 必须直接定价为 `$0.00`，完全不触碰档位查找，但仍要求产品存在（未知产品的
  零数量订单仍然报错）。
- 输出保持**输入顺序**，不按 `order_id` 排序（不同于 ps01/q03 的按用户分组）——每个订单
  是独立查询，不是聚合键。

## 复杂度与实测开销
Part 1 为 `O(n)`；Part 2-3 为 `O(n * b)`，`b` 为该订单 `(country, product)` 对应的档位数
（很小，受费率表规模约束，题面规模下总计约 200 行）。性能测试：10 万订单跑 Part 1（15 行
费率表，5 国家 x 3 产品），开发阶段临时计时约 0.07s，远低于 2s / 256MB 预算（测试时通过
`run_script` fixture 实测）。

## 测试清单
21 个测试 —— part1: 8 · part2: 6 · part3: 7；edge: 9 · fmt: 1 · io: 3 · perf: 1。

## 涉及技能
S02 解析（定宽 vs 变宽 CSV 行，`RATES`/`ORDERS` 分节标记）· S06 整数货币（分为单位，
十进制字符串解析，绝不用浮点）· S07 分档/计量定价数学（闭区间档位查找，累进 vs 统一计费）·
S09 精确格式化（货币 + 逐字错误字符串）· S10 明确的错误处理（三种独立、固定的错误信息格式）·
S19 增量式设计（Part 2 的查找原样复用为 Part 3 的 `fixed` 分支）

## 电面话术：边写边说什么
1. **读题时**：先复述协议再动手——"RATES 到 ORDERS 之间是费率行,ORDERS 之后每行是一个独立订单,
   输出按订单出现的顺序,不做分组/排序"——避免默认套用 ps01/q03 那种"按 key 排序输出"的肌肉记忆。
2. **写 Part 1 前**：说明货币解析策略——"金额一律解析成整数分,`5`、`5.5`、`5.50` 都当 5.50 处理,
   全程不出现浮点数"。
3. **写 Part 2 前**：主动提出区间开闭问题——"题面没直接给,我按闭区间 `[min_qty,max_qty]` 实现,
   也就是边界值精确落在某一档就算那一档;如果你们的定义不同,这里只需要改一个比较符号"。
4. **写 Part 2 时**：提醒自己费率表可能乱序——"我先把每个 (country,product) 的档位按 min_qty
   排序,再做查找,不假设输入文件本身有序"——这是原始面经里明确提到的"最容易踩的坑"。
5. **写 Part 3 前**：讲清楚"哪个 type 说了算"——"我只看命中的那一档的 type,而不是要求整条费率
   链条的 type 都一致;如果面试官问'如果不同档 type 不一样怎么办',这个设计天然就是良定义的"。
6. **写 incremental 分支时**：现场画一下"缺口"场景——"如果链条从 1 开始不连续,只有订单数量真的
   需要穿过那个缺口时才报错;数量在缺口前面就命中的订单不受影响"——用 worked example 里 qty=5 vs
   qty=20 的对比现场证明。
7. **收尾**：主动提"如果一个订单要买多个 product,现在的单行 order protocol 怎么扩展"——展示对
   协议可扩展性的思考,呼应面经里"没有自动测例,面试官看代码结构"的评分导向。

## 复盘（Fable 5.1，2026-09-01）
**改了什么**
- `solution.py` 重构为范本（`part1/2/3` 与 `main` 签名不变）：`Band` 由 4 元组改为 NamedTuple 并带 `contains(qty)`
  （闭区间只写一次）；定价函数改为"返回整数分，算不出就 `raise PricingError`"，取代原来贯穿各层的 `(cost, err)`
  tuple；三种错误文案只在 `_price_orders` 的 `try/except` 一处变成 `ERROR ...` 字符串。`_price_tiered` 30 行拆为
  "找档位 + fixed"与 `_price_incremental`；`_split_sections` 的 `assert` 改为 `ValueError`；`parse_money_to_cents`
  去掉题面未定义的负数分支并用 `partition` 简化；`TIER_TYPES` 常量。
- `test_ps02.py` 新增 2 个：`part1 edge` 零数量 + 未知商品仍报错（题面明文，原未测）；`part3 edge` incremental 走到
  `inf` 顶档（`$215.00`，原来 `inf` 分支只在报错路径被触及）。现在 23 tests：part1 9 · part2 6 · part3 8；
  edge 11 · fmt 1 · io 3 · perf 1。`IMPL=starter` 22 failed / 1 passed。
- black 格式化（4 文件），`loop/lint.sh` 通过。
**为什么**：无 F 级 bug；全部是 S 级可读性/复用/错误处理约定。4 组 worked examples 已用 `python3 solution.py` 逐字核对。
**遗留**：无。`bisect` 版档位查找仍作为追问讨论不实现。
