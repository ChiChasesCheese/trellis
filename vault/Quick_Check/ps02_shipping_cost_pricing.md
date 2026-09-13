# ps02 · Shipping Cost Pricing：从"查表乘一下"到阶梯计费，练的是"规则表 + 单笔查询 + 错误即字符串"

> [!tldr]
> - 这题考的是：把费率表建成一张可查的表，然后对每一笔订单独立回答"多少钱，或者为什么算不出来"
> - 三步套路：读题分清"表"和"查询" → 先跑通 Part 1 的 dict 查表 + 整数分格式化 → Part 2 把表值换成区间列表，Part 3 只在"命中的档位"上加一个分支
> - 最值得带走的一个模式：**规则里 raise 自定义异常，输出边界统一 catch 成 `ERROR ...` 字符串**——三种错误信息只在一个地方拼

## 1. 题目在说什么（人话版）
一个电商平台要在结账时算运费。输入分两段：先是 `RATES` 费率表（某国某商品每件多少钱），然后是 `ORDERS`
订单列表（谁、哪国、什么商品、买几件）。每笔订单独立输出一行运费，顺序就是输入顺序，不合并不排序。

三关递进：Part 1 是"单价 × 数量"；Part 2 把单价换成**按数量分档**（1–10 件一个价、11–20 件另一个价、21 件以上再一个价），
整单按命中档位的单价算；Part 3 给每个档位加一个 `type`：`fixed` 和 Part 2 一样，`incremental` 则像个税——前 10 件按第一档、
第 11–15 件按第二档，逐档累加。

小例子（Part 3，同样是 15 件）：
```
US,widget,1,10,5.00,incremental   US,widget,11,20,4.50,incremental   →  o1: $72.50  (10×5.00 + 5×4.50)
CA,widget,1,10,5.00,fixed         CA,widget,11,20,4.50,fixed         →  o2: $67.50  (15×4.50)
```

## 2. 读题：把文字变成模型
- **实体**：费率（按 `(country, product)` 索引）、档位 `Band(min_qty, max_qty, cost, kind)`、订单（一个查询）。
- **输入长什么样**：`RATES` 和 `ORDERS` 两个字面标记行把 stdin 切成两段；费率行的列数随 Part 变（3 列 / 5 列 / 6 列），订单行永远 4 列。
  金额是 `5`、`5.5`、`5.50` 这种十进制字符串；`max_qty` 可能是字面 `inf`。
- **输出要什么**：`order_id: $x.xx` 或 `order_id: ERROR <三种固定文案之一>`，按输入顺序。
- **状态**：只有一张费率表。Part 1 是 `dict[(country, product)] -> cents`；Part 2/3 是 `dict[(country, product)] -> list[Band]`（按 `min_qty` 排好）。
  订单之间没有任何共享状态——这和 ps01 的"按用户累积"是相反的形状。
- **一句话建模**：这是一个 **规则表查找 + 逐条独立定价** 问题，三个 Part 只是把"表里存的是什么"从一个数字升级成一列区间。

> [!note] 为什么选这个数据结构
> 费率表天然是"以 (国家, 商品) 为 key"的，所以用 tuple 当 dict key；每个 key 下的档位是个小 list（通常 3–5 个），
> 线性扫描找"包含 qty 的那一档"就够了，`bisect` 留作追问答案。金额用整数分：`5.5` → 550，避免 `0.1 + 0.2` 那类浮点尴尬，
> 输出时再 `cents // 100`、`cents % 100` 拼回去。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → `PART n` → `partN(rest)` → 打印。再写 `_split_sections`：找到 `ORDERS` 的下标，一刀切成两段。
2. **Part 1 最小可用**：`parse_money_to_cents` / `fmt_cents` 两个小函数先写（这两个后面每个 Part 都用），
   `_parse_flat_rates` 建 dict，`_price_orders` 逐行查表输出。用样例过一遍，特别看 `o3` 的 `ERROR unknown product US/gadget`。
3. **Part 2 叠加**：新写 `Band` 和 `_parse_tiered_rates`（记得 `sort(key=min_qty)`——题面故意把档位乱序给你），
   `_price_tiered` = 找命中档位 → `qty * cost`。`_price_orders` 原样复用，只换传进去的定价函数。
4. **Part 3 叠加**：`_parse_tiered_rates` 多读一列 `kind`；`_price_tiered` 在命中档位后加一个 `if kind == "fixed"` 分支，
   `incremental` 分支单独写成 `_price_incremental`（逐档累加 + 链条连续性检查）。
5. **收尾**：三条错误文案对着题面逐字核对；`qty = 0` 的特判；空输入直接返回。

## 4. 代码怎么组织
```
parse_money_to_cents(s) -> int / fmt_cents(c) -> str   # 钱的进出只在这两处
_split_sections(lines) -> (rate_rows, order_rows)      # 切段
_parse_flat_rates / _parse_tiered_rates -> table       # 建表；Band 是 NamedTuple，带 contains(qty)
_price_flat(table, c, p, qty) -> int                   # Part 1 规则，算不出就 raise PricingError
_price_tiered(table, c, p, qty) -> int                 # Part 2/3 规则：找档位 → fixed 直接乘 / incremental 走下面
_price_incremental(bands, qty, label) -> int           # 逐档累加 + 缺口检查
_price_orders(order_rows, price_one) -> list[str]      # 唯一把 int / 异常变成字符串的地方
part1..part3(lines) -> list[str]                       # 切段 → 建表 → 把定价函数交给 _price_orders
```
关键决定是**定价函数只返回整数分或 raise**：它们不知道 `$`、不知道 `ERROR` 前缀，三种错误文案都在 `PricingError` 的消息里，
`_price_orders` 一个 `try/except` 统一格式化。这样 Part 3 复用 Part 2 时不需要碰任何输出代码，面试官问"再加一种错误"时你只加一行 `raise`。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：找档位 → 按类型定价 → 输出边界。省略切段、建表（split 逗号 + 按 min_qty 排序）、Part 1、main。
class Band(NamedTuple):
    min_qty: int; max_qty: int | None; cost: int; kind: str      # max_qty None == 'inf'
    def contains(self, qty):                                    # 闭区间 [min, max]
        return self.min_qty <= qty and (self.max_qty is None or qty <= self.max_qty)

class PricingError(Exception): ...                              # 消息就是题面三种文案之一

def _price_incremental(bands, qty, label):                      # 个税式逐档累加
    total, expected_start = 0, 1
    for band in bands:
        if band.min_qty != expected_start:                      # 链条断了且订单要穿过它
            raise PricingError(f"incremental gap for {label} at qty={qty}")
        upper = qty if band.max_qty is None else min(qty, band.max_qty)
        total += (upper - band.min_qty + 1) * band.cost
        if upper == qty:
            return total
        expected_start = band.max_qty + 1

def _price_tiered(table, country, product, qty):
    label = f"{country}/{product}"
    if (country, product) not in table:
        raise PricingError(f"unknown product {label}")
    if qty == 0:
        return 0
    bands = table[(country, product)]
    matched = next((b for b in bands if b.contains(qty)), None)
    if matched is None:
        raise PricingError(f"no tier for {label} at qty={qty}")
    return qty * matched.cost if matched.kind == "fixed" else _price_incremental(bands, qty, label)

def _price_orders(order_rows, price_one):                       # 唯一的字符串出口
    out = []
    for row in order_rows:
        oid, c, p, q = (x.strip() for x in row.split(","))
        try:
            out.append(f"{oid}: {fmt_cents(price_one(c, p, int(q)))}")
        except PricingError as err:
            out.append(f"{oid}: ERROR {err}")
    return out
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：档位区间我按闭区间 `[min_qty, max_qty]` 处理，边界值归本档；费率表行的顺序我不信任，会先按 `min_qty` 排序；每笔订单独立输出，不合并。」
- 写 Part 1 时：「金额我全部转成整数分，`5.5` 是 550 分而不是 505——注意小数部分要右补零。输出时再格式化，所以中间没有浮点。」
- 写 Part 2 时：「我把每个档位做成一个 `Band`，给它一个 `contains(qty)` 方法，这样'找命中档位'就是一行 `next(...)`。」
- 写 Part 3 时：「`fixed` 分支就是 Part 2 的那一行乘法，我直接复用；`incremental` 我单独写一个函数，从 1 开始逐档走，
  每档只收它自己区间内的件数，走到包含 qty 的那档就停。链条中间断了、而且订单必须跨过去，才报 `incremental gap`。」
- 交付时：「四组样例都过了。错误都是 `PricingError` 在规则里 raise、在输出函数里统一 catch，所以三条文案只出现一次。
  如果时间允许，我会把 `_find_band` 换成 `bisect`，不过每个商品只有几个档位，线性扫描其实更合适。」

## 7. 常见跑偏（方法层面，3 条）
- **用 float 存钱**：`float("5.5") * 15` 然后 `f"{x:.2f}"`——这题恰好不会炸，但面试官一定会追问舍入；一开始就用整数分，`parse/fmt` 各一个函数，没有后患。
- **错误处理散在每个 Part 里**：Part 1 返回 `"ERROR ..."` 字符串、Part 2 返回 `None` 再判断、Part 3 又返回 tuple——
  三种约定混在一起，复用不了。定下"规则 raise、边界 catch"一条约定，三个 Part 共用一个 `_price_orders`。
- **把 Part 3 写成一个大 if/else**：找档位、fixed、incremental、缺口检查全塞进一个 30 行函数。先把"找档位"和"逐档累加"拆成两个小函数，
  每个只做一件事，追问"改成半开区间"或"预校验整张表"时才知道该改哪里。

## 8. 同族题 / 延伸
- OA 侧：q22 `shipping_cost` 是"路径版"运费（同名不同题，图搜索）；q21 `currency_conversion` 与本题共享"整数分 + 规则表查找"；
  q30 `stripe_capital_loans` 的分期计算也是"逐段累加"的形状。
- 其他轮：cd02 `payment_ledger` 同样把钱当整数分进出；ps04 `data_validation_fraud` 也是"每条记录独立判定、错误文案定死"。
- 延伸思考：追问 4（三位小数货币）只需改 `parse_money_to_cents` / `fmt_cents` 里的 `100`；追问 7（读表时静态校验 incremental 链条）
  就是把 `_price_incremental` 的连续性检查搬到 `_parse_tiered_rates` 末尾跑一遍。
- 练习命令：`python3 loop/mock.py start ps02`
