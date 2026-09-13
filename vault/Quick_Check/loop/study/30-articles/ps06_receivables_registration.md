# ps06 · Receivables registration：CSV 聚合题的标准流水线——解析 → 聚合 → 渲染

> [!tldr]
> - 这题考的是：把"按几个字段分组求和"写成一条清晰的流水线，然后在第二个 part 里**只换解析层**就吃下"坏行 + 周末顺延"
> - 三步套路：把一行 CSV 抽象成 `Row(merchant, card_type, payout_date, cents)` → 先用 `defaultdict(int)` 跑通 Part 1 → Part 2 换一个"带校验的解析函数"，聚合和输出原样复用
> - 最值得带走的一个模式：**"归一化要在数据进入 key 之前做"**——周六和周一要合成一组，就得在 `totals[key] +=` 之前把日期改掉

## 1. 题目在说什么（人话版）
Stripe 在巴西给商户收款。巴西央行要求：钱打给商户之前，先按"哪个商户、哪种卡、哪天打款"报一份汇总表。
你拿到的是一堆逐笔交易（谁、在哪家商户、哪天打款、什么卡、多少钱），要产出这份汇总表。

Part 1 数据是干净的：分组、求和、按规定顺序输出。
Part 2 数据变脏了：有的行少了字段、金额写成 `BAD`、日期写成 13 月——这些行要跳过并**数一下**；
另外打款日落在周末的要顺延到下周一（周六 +2 天、周日 +1 天），顺延后再分组。

小例子：
```
c1,m1,2026-08-03,visa,150.00        m1,mastercard,2026-08-03,20.00
c2,m1,2026-08-03,visa,50.00    →    m1,visa,2026-08-03,200.00
c3,m1,2026-08-03,mastercard,20.00
```

## 2. 读题：把文字变成模型
- **实体**：交易行（5 个字段，`customer_id` 用不上）；分组 key `(merchant_id, card_type, payout_date)`；每组一个整数分总额。
- **输入长什么样**：第一行 `PART n`，第二行 CSV 表头，之后每行一笔。金额是两位小数字符串，**要转成整数分**。
- **输出要什么**：每组一行 `merchant,card_type,date,total`；排序 key 是 `(merchant, date, card_type)`——注意**输出列顺序和排序顺序不是一回事**。Part 2 末尾多一行 `SKIPPED n`。
- **状态**：只需要一个 `dict[key, cents]`；不需要保留原始行。
- **一句话建模**：这是一个"**按三元组 key 分组累加整数分**"的聚合问题，Part 2 在解析层加"校验 + 日期归一化"。

> [!note] 为什么选这个数据结构
> 候选：列表存所有行再 `groupby`（要先排序，且内存 O(n)）；`defaultdict(int)` 边读边加（内存 O(组数)）。
> 后者一行 `totals[key] += cents` 就是全部逻辑，天然支持流式读入，面试官追问"1000 万行怎么办"时答案就在代码里。
> 钱用整数分：`150.00` → `15000`，永远不 `float` 相加，输出时再格式化回两位小数。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 取头行 → 查表分发 → 打印。定义 `Row = NamedTuple(merchant, card_type, payout_date, cents)`，写好 `_data_lines`（去表头、去空行）。
2. **Part 1 最小可用**：三个小函数——`_parse_row_trusted(raw) -> Row`、`_aggregate(rows) -> dict`、`_render(totals) -> list[str]`。`part1` 就是这三个的串联。立刻用样例自测，**特别核对排序顺序**。
3. **Part 2 叠加**：
   - 新写 `_parse_row_checked(raw) -> Row | None`：字段数 ≠ 5、金额不匹配 `-?\d+\.\d{2}`、日期不是真实日期 → `None`。
   - 新写 `_roll_weekend(row) -> Row`：查表 `{SAT: 2, SUN: 1}` 加天数。
   - `part2` 的循环：`None` 就 `skipped += 1`，否则 `rows.append(_roll_weekend(row))`。**`_aggregate` 和 `_render` 一个字不改。**
4. **收尾**：`SKIPPED n` 永远打印（包括 0）；负数、`0.00` 都照实输出；跑两个样例。

## 4. 代码怎么组织
```
FIELD_COUNT / AMOUNT_RE / DATE_RE / ROLL_FORWARD_DAYS   # 规则常量集中在顶部
Row(NamedTuple)                                         # 一行解析后的样子
_data_lines(lines) -> list[str]                         # 去表头 / 空行
_amount_to_cents(s) -> int ; _is_valid_date(s) -> bool  # 字段级转换 / 校验
_parse_row_trusted(raw) -> Row                          # Part 1 解析
_parse_row_checked(raw) -> Row | None                   # Part 2 解析（None = 坏行）
_roll_weekend(row) -> Row                               # Part 2 归一化
_aggregate(rows) -> dict[key, cents]                    # 核心：两个 part 共用
_fmt_cents(cents) -> str ; _render(totals) -> list[str] # 格式化 + 排序，集中一处
part1 / part2 / PARTS / main                            # 串联与分发
```
这样拆的好处：面试官从 `part2` 往下读，只看到"解析 → 判坏 → 顺延 → 聚合 → 渲染"五个动词；
金额格式、日期规则、排序 key 各自只出现在一个地方，追问"改成整数分输入 / 加节假日"时你知道改哪一行。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
ROLL_FORWARD_DAYS = {5: 2, 6: 1}                 # weekday(): Sat=5 -> +2, Sun=6 -> +1

class Row(NamedTuple):
    merchant_id: str; card_type: str; payout_date: str; cents: int

def _amount_to_cents(amount):                    # '150.00' -> 15000, '-15.50' -> -1550
    sign = -1 if amount.startswith("-") else 1
    whole, frac = amount.lstrip("-").split(".")
    return sign * (int(whole) * 100 + int(frac))

def _parse_row_checked(raw):                     # Part 2：坏行返回 None
    fields = [p.strip() for p in raw.split(",")]
    if len(fields) != 5:
        return None
    _c, merchant, payout_date, card_type, amount = fields
    if not AMOUNT_RE.fullmatch(amount) or not _is_valid_date(payout_date):
        return None
    return Row(merchant, card_type, payout_date, _amount_to_cents(amount))

def _roll_weekend(row):
    d = date.fromisoformat(row.payout_date)
    d += timedelta(days=ROLL_FORWARD_DAYS.get(d.weekday(), 0))
    return row._replace(payout_date=d.isoformat())

def _aggregate(rows):                            # 两个 part 共用
    totals = defaultdict(int)
    for r in rows:
        totals[(r.merchant_id, r.card_type, r.payout_date)] += r.cents
    return totals

def _render(totals):                             # 排序 key ≠ 输出列顺序
    ordered = sorted(totals.items(), key=lambda kv: (kv[0][0], kv[0][2], kv[0][1]))
    return [f"{m},{c},{d},{_fmt_cents(cents)}" for (m, c, d), cents in ordered]

def part2(lines):
    rows, skipped = [], 0
    for raw in _data_lines(lines):
        row = _parse_row_checked(raw)
        if row is None:
            skipped += 1
        else:
            rows.append(_roll_weekend(row))      # 归一化在进入 key 之前
    return _render(_aggregate(rows)) + [f"SKIPPED {skipped}"]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：金额是两位小数字符串，我内部转整数分；输出不带货币符号；负数总额照实输出；排序是 merchant → date → card_type，和输出列顺序不同，对吗？」
- 写 Part 1 时：「我用 `defaultdict(int)` 按三元组 key 累加整数分，因为只需要保留组总额，不用存原始行，流式读也行。」
- 写 Part 2 时：「坏行我选择跳过并计数，而不是静默丢或抛异常——央行报送需要审计痕迹。周末顺延我放在入 key 之前，否则周六和周一会分成两组。」
- 交付时：「两个样例过了；如果时间允许，Part 2 我会把节假日日历做成和 `ROLL_FORWARD_DAYS` 同级的一个查表，不改聚合层。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 2 复制 Part 1 再改**：两份聚合循环，改一处漏一处。正确做法是只新增"解析/归一化"函数，聚合与渲染复用。
- **先算完再修**：把周末顺延写在聚合之后（对输出行改日期），结果周六组和周一组各自一行。归一化属于解析层，必须在 key 之前。
- **用 float 存钱、输出时 `round`**：`0.1 + 0.2` 的老问题；面试官对"钱"类题第一眼就看这个。整数分进、整数分出。

## 8. 同族题 / 延伸
- ps01 Transaction stream levels、cd02 Payment ledger：同样是"逐行解析 → 按 key 聚合 → 定序输出"，换了业务外衣。
- OA 里所有"CSV → 报表"类题：这条 `parse → aggregate → render` 流水线可以原样搬过去。
- 练习命令：`python3 loop/mock.py start ps06`
