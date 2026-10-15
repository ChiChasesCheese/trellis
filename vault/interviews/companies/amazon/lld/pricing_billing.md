# LLD：价格 / 账单 / 费用计算（披萨、购物车折扣、AWS 账单、票价封顶、交易手续费）——教科书模式

> 题库里**没有**这一族题（`low-level-design/problems/` 45 题里 [lld:design-online-shopping](../../../../domains/low-level-design/drills/problems/design-online-shopping.md) 讲的是库存与订单状态机，不是定价规则）。
> 但它是 Amazon 新毕业生 LLD 轮**第二高频**的一族：`catalog/raw/forums.md` §4.4 记录 SDE I 8 条、SDE II+ 3 条（见 §1 的具体题面）。
> 代码：`code/pricing_billing.py`（`python3 -I code/pricing_billing.py` 打印 `OK pricing_billing`）。
> 官方评分口径（`../catalog/raw/official.md` §4.3）："Make code extendable and avoid single functions that do everything … seek more requirements to show how your solution evolves when requirements change."

## 1. 这道题在问什么：五个说法，一个骨架

`forums.md` 里报告过的原题（URL 与日期在该文件对应行）：

| 说法 | 来源（forums.md ID）| 级别 |
|---|---|---|
| "Design a **billing service for AWS** for a single user where the usage and rate of all the services used are given"（"best round, many follow-ups"，拿到 offer）| LC8520348，2026-08，US Seattle onsite | SDE I |
| "Design a **shopping cart price calculator API** … for a large scale service … Plan for being able to apply discounts"；追问：全场折扣、满额翻倍、买三送一、热门商品 | RD1wcfb9m，2026-09，EU | SDE I |
| train route G→U→H→K→I，`calculateFare(start, stop)`，**周末封顶**（"turned out to be an OOP/LLD question"）| LC8500377，2026-09 | SDE I |
| **Pizza** order：底、尺寸、配料的定制，算总价 | RD1mit913、KV1l7b54r、RD1mig65b，2025-06..08 | SDE I |
| **Cart-management** system "with proper design patterns, discount rules, full class code on a notepad" | LC8568929，2026-10 | SDE I |
| "Calculate **fees for stocks, bonds** etc. Each type has a given rate and some conditions … rules apply to all types … extendible" | LC8364677，2026-06 | — |

骨架都是：**输入（行项目 / 用量 / 行程）+ 一串有顺序的规则 → 一张可解释的账单**。面试官的追问全是"再加一种规则你要改几处"。

手算一个最小例子（购物车）：书 20.00×2、笔 5.00×4、笔记本 1000.00×1，原价 = 40 + 20 + 1000 = **1060.00**。
- 全场 10% 折扣：−106.00 → **954.00**。
- 再加 8% 税：先折扣后税，税基 954.00，税 76.32 → **1030.32**；先税后折扣则税基是 1060.00，税 84.80，折扣仍只按原价 −106.00 → **1038.80**。**同样两条规则，顺序不同金额不同**——所以顺序必须是显式的、可测试的。

## 2. 前置知识

### 2.1 钱为什么不能用浮点数
- **是什么**：`float` 是二进制小数，`0.1` 在二进制里是无限循环小数，只能近似存储。
- **为什么需要关心**：`0.1 + 0.2 == 0.30000000000000004`。账单加一百行，误差就会让"各行相加 ≠ 总额"，客户用计算器核对时发现不一致。
- **怎么工作**：用**整数分**存钱（`19.99 美元 = 1999`），加减乘整数都精确。需要乘比例（税率、折扣率）时用 `Decimal`（十进制定点数）计算，**最后舍入到分一次**。
- **Python**：`Money(cents: int)`；`Decimal("0.075")` 必须用**字符串**构造（`Decimal(0.075)` 会把浮点误差也带进来）。

### 2.2 舍入：何时舍、怎么舍
- 常见两种：**四舍五入（half-up）**与**银行家舍入（half-even，0.5 向偶数舍）**。金融场景有的法规要求后者；面试里**选一种并说出理由**即可（我们选 half-up，对客户直观）。
- 负数：`ROUND_HALF_UP` 在 `Decimal` 里是"远离零"，所以 `-2.5 → -3`，与 `2.5 → 3` 对称（测试里有断言）。
- **舍入位置**：中间步骤不舍，在"账单上客户看得见的那一行"舍一次（AWS 用量行：每行舍一次，总额 = 各行之和）。否则 N 行各舍一次的误差累积和"总额一次性舍入"不同，要在需求里说清是哪种。
- **分摊**：整单折扣 10.00 要摊到 3 个行项目（退货时按行退款），`10.00/3` 除不尽。用**最大余数法**（`allocate`）：先向下取整，剩余零头分给小数部分最大的几份，保证"份额之和恰好等于总额"。

### 2.3 策略模式（Strategy）
- **是什么**：把"一种算法"做成一个对象，统一接口 `apply(...)`，可以互换。
- **为什么**：折扣种类会不断增加（百分比、买三送一、满减、优惠券…）；用 `if rule_type == ...` 的大函数每加一种就改一次，且难测。
- **怎么工作**：`PriceRule.apply(ctx) -> list[Adjustment]` 是**纯函数**（不改 ctx），`PricingEngine` 按顺序执行并"记账"。纯函数让每条规则可单独测试，也让 `BestOf`（"试算几条、取最优"）成为可能。

### 2.4 装饰器（Decorator）与"数据驱动"：披萨怎么建模
- 教科书答案是 Decorator：`Pizza` ← `PepperoniDecorator(Pizza)` ← `ThickCrustDecorator(...)`，`cost()` 层层相加。
- **缺点**：配料价格依赖尺寸（大号更贵）时，每个装饰器都要知道尺寸；每个新配料一个新类；非法组合要到运行时才发现。
- **我们的选择**：**菜单是数据**（`topping_price[name][size]`），`PizzaBuilder` 分步收集选择、`build()` 时一次性校验并生成行项目，再交给同一个引擎算税和折扣。新增配料 = 加一行数据，零新类。
- **面试里怎么说**："Decorator 适合行为叠加（比如日志、压缩流），这里变化的是数据而不是行为，所以我选数据驱动 + Builder；如果面试官更想看 Decorator，我也可以用它做同一件事，代价是……"（说出代价就是满分回答）。
- 但在本引擎里，`ThresholdBoost`（"满额则折扣翻倍"）**确实**是 Decorator：它包装另一条规则并改变其输出——这才是 Decorator 的正确用法。

### 2.5 阶梯计价（Tiered pricing）：边际而不是整体
- **是什么**：用量越大单价越低，例如（**示例费率，不是 AWS 现价**）：前 51,200 GB 每 GB 0.023，接下来 460,800 GB 每 GB 0.022，之后 0.021。
- **关键**：每一档**只对落在这一档内的那部分**用量收这一档的价（和个人所得税的边际税率同理），不是"总用量落在哪一档就整体按哪一档"。
- 例：102,400 GB = 51,200×0.023 + 51,200×0.022 = 1177.60 + 1126.40 = **2304.00**。
- **先聚合再分档**：一个月里有很多条用量记录。分档应对**月度总量**生效；逐条分档会让每条都当成"第一档（最贵）"。例：两条 30,000 GB，各自分档 = 2×690 = 1380.00；聚合成 60,000 后 = 1177.60 + 193.60 = **1371.20**（测试里有断言）。费率随用量递减时，逐条分档**会向客户多收钱**。
- **免费额度**：每月前 N 个单位免费，同样扣在聚合后的总量上（`FreeTierThen`）。

### 2.6 幂等：用量记录是"至少一次"投递
计量系统通常用消息队列上报用量，**可能重复投递**。每条记录带 `usage_id`，账单生成时去重；否则客户被多收钱。这与 `../sd/problems/cdc_replication_pipeline.md` 里"至少一次 + 幂等"同一个道理。

### 2.7 Builder 与校验时机
`PizzaBuilder` 允许链式调用逐步设置；**校验放在 `build()`**，因为只有这时才知道选择是否完整（必须选尺寸；配料必须在菜单里）。构造时就抛错会让"先设配料后设尺寸"的调用顺序受限。

## 3. 从最笨的解法开始

```python
def total(items, discount_type, tax_rate):
    t = 0.0
    for it in items:
        t += it["price"] * it["qty"]
    if discount_type == "percent10":
        t = t * 0.9
    elif discount_type == "buy3get1":
        ...
    elif discount_type == "over100double": ...
    return t * (1 + tax_rate)
```
**具体错在哪**：
1. `float`：`0.1*3 != 0.3`；总额与行之和对不上。
2. **一个 `discount_type` 字符串只能选一种折扣**；"满额翻倍 + 买三送一 + 税"同时存在怎么办？
3. 顺序藏在 `if` 里；加一种规则要改这个函数。
4. 只返回一个数——客户问"为什么是这个价"答不上来，也没法对账、退款。
5. 不能处理阶梯、封顶、免费额度、去重——每个变体都要重写。

## 4. 一步一步改进

| 步 | 发现的问题 | 想法 | 为什么有效 | 代码变化 |
|---|---|---|---|---|
| 1 | 浮点误差 | `Money` 值对象，整数分，币种校验 | 精确、不可变、混币种直接报错 | `Money`（`of/scale/times/allocate`）|
| 2 | 折扣种类爆炸 | `PriceRule` 策略，`apply(ctx)` 返回调整项 | 新规则 = 新类，引擎不动 | `PercentOff`、`BuyXGetYFree`、`TaxRule`、`PercentFee` |
| 3 | 规则要组合/叠加 | 引擎按顺序执行并"记账"，规则只返回调整 | 顺序显式；规则是纯函数可单测 | `PricingEngine.price` |
| 4 | "满额翻倍""互斥券" | 装饰器 `ThresholdBoost`、组合器 `BestOf`（都是 `PriceRule`）| 规则也能嵌套 | 两个小类 |
| 5 | 看不懂价格 | `Receipt`：原价 + 每条调整（带标签）= 总价；`explain()` | 可审计、可展示、可按行退款 | `Adjustment`、`Receipt` |
| 6 | 折扣把价格压成负数 | 引擎末尾"价格下限"夹到 0 并标记 `floored` | 不变量由引擎保证，不靠每条规则自觉 | `Receipt.floored` |
| 7 | 披萨：定制 | 菜单数据 + Builder，输出行项目，复用引擎算税/折扣 | 新配料零新类 | `PizzaMenu`、`PizzaBuilder` |
| 8 | AWS 账单：用量计费 | `RatePlan` 策略（Flat / Tiered / FreeTierThen）+ `BillingService`：去重→聚合→计价→每行舍一次 | 阶梯、免费额度可任意组合 | `RatePlan` 系列 |
| 9 | 票价封顶：需要"历史" | `FareCalculator` 持有 `(乘客, 日期) → 当日已付`；`when` 由调用方传入 | 无状态规则放引擎，有状态的放计算器；时间不读系统时钟 | `FareCalculator` |

## 5. 逐段讲参考解

**5.1 `Money.scale` 与 `allocate`**
`scale(rate)` 把整数分乘比例后一次舍入。`allocate` 的算法：`base[i] = total*w[i] // sum(w)`；剩下的 `leftover` 分给 `total*w[i] % sum(w)` 最大的几份，并列靠前者先得（通过 `(余数, -i)` 排序实现确定性）。结果之和恒等于总额（测试：`10.00` 分 3 份 = `3.34/3.33/3.33`）。

**5.2 `CartContext` 与 `running_total`**
规则看到两样东西：`lines`（原价）和 `adjustments`（前面规则已产生的）。折扣类规则通常基于**原价**（`PercentOff` 用 `ln.gross`，所以折扣不会"折上折"）；税这类规则基于**折后总额**（`running_total`）。这就是 §1 的"顺序影响金额"的精确含义——基数是规则自己选的，顺序决定 `running_total` 里有什么。

**5.3 `BuyXGetYFree`**
"买 3 送 1" = 每 4 件里 1 件免费：`groups = qty // (buy + free)`，`free_units = groups * free`。7 件只有 1 组，免 1 件；8 件 2 组，免 2 件；3 件 0 组。**面试官最爱追问这个边界**。免费的是同 SKU 的单价（此处所有件同价）；若同 SKU 有不同价格要"免最便宜的"，需要按价格排序后取（追问 Q4）。

**5.4 `ThresholdBoost` 与 `BestOf`**
- `ThresholdBoost`：包一层，整单原价 ≥ 阈值则把内部规则的调整乘以 `factor`。内部规则不知道自己被包装了。
- `BestOf`：对同一个 ctx 试算几条，取**总优惠最大**的一条；并列取靠前，结果确定。这就是"优惠券互斥"。

**5.5 `TaxRule`**
税基 = `running_total` − 豁免类别的原价。**整单只舍入一次**（对 `base` 乘税率后 `scale`）。注释里写明了简化：豁免品如果也被打折，严格做法要把折扣按行分摊（`allocate`）才能得到准确的豁免税基。

**5.6 `PercentFee`（证券手续费）**
`rates: dict[类别 → 费率]`，另有最低收费 `min_fee` 和封顶 `cap`。题面"每种类型有费率和条件，规则适用于所有类型，可扩展"→ 费率是**数据**，条件是**规则对象**。新增类别 `crypto` 只改字典。

**5.7 `BillingService.invoice`**
去重 → 聚合 → 每个 `(service, metric)` 找 `RatePlan` → `plan.charge(总量)` 得到未舍入 `Decimal` → **每行舍一次** → 总额 = 各行之和。`RatePlan.charge` 返回 `Decimal`（美元），因为 `0.023 美元/GB` 是亚分价格，必须用 Decimal 累加，到行末才变成分。

**5.8 `FareCalculator.calculate_fare`**
`charge = min(本次原价, 封顶 − 当日已付)`，不会为负。周末封顶不同通过 `day.weekday() >= 5` 选择。`when` 参数（不是 `datetime.now()`）让测试能构造"周六""周一"。同站乘车费用 0；未知车站抛 `KeyError`。

## 6. SOLID 与设计选择

| 原则 | 体现 |
|---|---|
| S | `Money` 只管数；规则只管算调整；引擎只管顺序与记账；`Receipt` 只管展示 |
| O | 新折扣 / 新费率计划 / 新配料不改引擎（见追问 Q1） |
| L | 所有 `PriceRule`、`RatePlan` 可互换；`ThresholdBoost`、`BestOf` 自己也是 `PriceRule` |
| I | `PriceRule` 只有 `apply`；`RatePlan` 只有 `charge` |
| D | 引擎依赖抽象 `PriceRule`；`FareCalculator` 依赖传入的时间而不是系统时钟 |
| 其它 | 值对象不可变（`frozen=True`）；纯函数规则；显式顺序；解释性输出 |

## 7. 追问预演

**Q1. 加一种"第二件半价"的折扣，要改哪里？**
思考：它是一条新规则。答案：新增 `NthItemHalfOff(sku, n)` 子类，`apply` 里对该 SKU 每 n 件中的一件产生 `-单价/2` 的调整（`scale("0.5")`）；`PricingEngine` 和其它规则不变；在规则列表里选好位置。

**Q2. 两张优惠券不能同时用，只取最优。**
答案：`BestOf((券A, 券B))`。如果"券 A 与 B 互斥但都能与满减叠加"，则规则列表是 `[满减, BestOf((A, B))]`；如果优惠基数是折后价，要保证 `BestOf` 内部规则读取的是 `running_total`（本实现里 `PercentOff` 读原价，若要折上折需要另写一个基于 `running_total` 的规则）。

**Q3. 折扣金额要精确摊到每个行项目（为了退货）。**
答案：`allocate(整单折扣, [各行金额])`，用最大余数法保证之和精确；退货时按行金额占比退，最后一件退"剩余"以避免累计误差。

**Q4. 同一 SKU 有不同价格的件，买三送一免哪一件？**
答案：免**最便宜**的那件（对客户公平且是常见规定）：把该 SKU 的所有单件价格展开排序，取 `groups*free` 个最小的求和。需求要先和面试官确认。

**Q5. 价格会变（促销期、定价生效日期）。**
答案：价格不放在 `Line` 里写死，而是由 `PriceBook.lookup(sku, as_of)` 提供，条目带 `effective_from/to`；下单时把查到的价格**快照**进订单行（订单之后价格变了也不影响历史订单）。`as_of` 由调用方传入。

**Q6. 并发：同一用户同时下两单，折扣券只能用一次。**
答案：券的核销是一个原子操作（`UPDATE coupons SET used=1 WHERE id=? AND used=0`，看影响行数）；定价引擎本身是纯函数，无共享可变状态，天然线程安全；有状态的部分（封顶累计、券核销）要加锁或用数据库原子更新。`FareCalculator._paid` 在多线程下需要锁，或改成数据库里的 `UPDATE … SET paid = paid + x WHERE paid + x <= cap` 条件更新。

**Q7. AWS 账单：多账号合并计费（Consolidated billing）。**
答案：阶梯在**合并后的总量**上计算（所有关联账号的用量先聚合，再分档），然后把各档费用按用量占比（`allocate`）摊回各账号。这是"先聚合再分档"的自然延伸。

**Q8. 账单：中途开通的资源要按比例（proration）。**
答案：按秒/小时用量计价是用量模型本身；订阅制的月费才需要按天比例：`月费 × (剩余天数 / 当月天数)`，舍入到分一次，并写清是用实际天数还是 30 天制。

**Q9. 抵扣额（credits）和税的顺序。**
答案：顺序是显式规则：`[用量计价, 阶梯/免费额度, 折扣, 抵扣额, 税]` 还是 `[..., 税, 抵扣额]`，由法规/合同决定。我们的引擎里这就是规则列表的顺序；面试里要明说"我假设抵扣额在税前，因为……"。

**Q10. 地铁：加上"换乘 90 分钟内免费""高峰/非高峰价""月度封顶"。**
答案：`FareCalculator` 拆成：①**票价规则**（按站数、高峰系数，策略）；②**封顶策略**（日/周/月，策略，状态是 `(乘客, 周期) → 已付`）；③**换乘折扣**（看上一次行程的结束时间和站点）。每个都是可插拔对象，计算器按顺序应用。

**Q11. 把它做成服务，每秒上百万条用量记录。**
答案：用量上报进分区日志（按账户哈希），聚合器按 `(账户, service, metric, 小时)` 做**预聚合**（可合并的计数），账单生成读预聚合表；去重靠 `usage_id` 的去重窗口或确定性主键；账单生成是批处理，幂等可重跑（输出以 `(账户, 周期)` 为键覆盖）。见 `../sd/problems/metrics_timeseries_store.md` 的降采样与可合并聚合。

**Q12. 怎么测试？**
答案：属性测试：①原价 + 全部调整 = 总价；②总价 ≥ 0；③`allocate` 之和恒等；④规则顺序交换后的结果差异有明确断言；⑤聚合后分档 ≤ 逐条分档（当费率递减）；⑥重复用量记录不改变账单。再加边界：0 件、1 分、跨档边界恰好 51,200、封顶恰好等于剩余额度。

## 8. 常见误区

1. **用 `float` 存钱**，或 `Decimal(0.1)`（带着浮点误差构造）。→ 整数分 + `Decimal("0.1")` 字符串。
2. **每一步都舍入**：N 条规则舍 N 次，误差累积，与"一次舍入"的总额不同。→ 说清舍入位置，通常在客户可见的行末。
3. **把折扣写成 if/else 链**，加一种改一处，且顺序藏在代码里。
4. **阶梯计价按"总量落在哪一档就整体套那一档"**。→ 边际：每档只算落入该档的部分。
5. **逐条用量分档**。→ 先聚合再分档。
6. **用量记录不去重**。→ `usage_id`。
7. **买三送一写成 `qty // 3`**（买 3 送 1 要凑 4 件一组）。→ `qty // (buy+free)`。
8. **折扣叠加后价格为负**，且没有不变量守护。→ 引擎统一下限，标记 `floored`。
9. **在计价代码里调用 `datetime.now()`**。→ 时间由调用方传入。
10. **只返回一个总数**，无法解释。→ `Receipt` + `explain()`。

## 9. 自测题

1. `Money.of("10.00").scale("0.075")` 是多少？为什么不能用 `float` 做这件事？
<details><summary>答案</summary>`Money(75)`，即 0.75。`1000 * 0.075` 在浮点里可能是 `75.00000000000001`，舍入前累积误差；用 `Decimal` 先精确相乘再舍入。</details>

2. 先折扣后税 与 先税后折扣，对 1060.00、10% 折扣、8% 税，结果各是多少？
<details><summary>答案</summary>先折扣后税：954.00 + 76.32 = **1030.32**；先税（税基 1060.00 → 84.80）后折扣（按原价 −106.00）= **1038.80**。顺序是语义。</details>

3. 102,400 GB 的 S3 示例阶梯（前 51,200 @0.023，之后 @0.022）总价？
<details><summary>答案</summary>51,200×0.023 + 51,200×0.022 = 1177.60 + 1126.40 = **2304.00**。</details>

4. 为什么分摊用最大余数法，而不是每份都 `round(total*w/sum)`？
<details><summary>答案</summary>独立舍入各份的和可能比总额多一分或少一分（如 10.00 平均分 3 份，每份 3.33 → 9.99）。最大余数法保证和恒等于总额。</details>

5. 周六乘客 ann：G→I（8.00），I→G（8.00 原价），封顶 10.00。第二次实付多少？第三次 G→U 呢？
<details><summary>答案</summary>第二次 `min(8.00, 10.00 − 8.00) = 2.00`；第三次 `room = 0` → 0.00。</details>

6. （senior）如何让"封顶累计"在多实例部署下正确？
<details><summary>答案</summary>状态下沉到共享存储，用条件更新做原子累加（`paid + x <= cap`，或先读后写加版本号乐观锁）；幂等键（行程 ID）防止重试重复扣；跨日边界用乘客所在时区的"日期"作为分区键，注意夏令时造成的 23/25 小时。</details>

## 10. 延伸阅读（已核对）
- Fowler《Patterns of Enterprise Application Architecture》的 Money 模式（值对象 + 分摊算法）。Fowler 的 Money 页面确认其用途是"表示货币值"，并指出按最小货币单位舍入时"很容易丢零头"（lose pennies）；分摊算法在书第 18 章，网页本身未展开（来源：https://martinfowler.com/eaaCatalog/money.html ，2026-10-15 核对）。
- Python `decimal` 文档的舍入模式表（`ROUND_HALF_UP` / `ROUND_HALF_EVEN`；表中共 8 种模式，默认上下文 prec=28、rounding=`ROUND_HALF_EVEN`，不是 HALF_UP）（来源：https://docs.python.org/3/library/decimal.html ，2026-10-15 核对）；本文断言已在本地运行验证。
- 同一思想的系统设计版本：`../sd/problems/metrics_timeseries_store.md`（可合并聚合）。
