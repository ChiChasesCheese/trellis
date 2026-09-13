# 02 · 核心考点总纲（S01–S24 / A01–A16 中文详解）

> 这是本目录的**主文件**。`skills_matrix.md` 用英文列出了 24 个业务型考点和 16 个算法考点，
> 以及每个考点由哪些题驱动。这里把每一个考点讲透：**为什么考、怎么判断题目在考它、
> 标准做法是什么、最容易错在哪**。
>
> 读法：第一遍通读，第二遍每做完一题回来查对应的几条。

---

# 第一部分 · 业务型考点 S01–S24

## S01 · 先读完整份规格，为 Part N+1 而设计

**为什么考**：这类题的每个 part 都是在同一个程序上继续加需求。上来就闷头实现 Part 1，
到 Part 4 发现状态形状不对，只能重写 —— 时间就是这么没的。

**怎么识别**：题面出现 "Part 1 / Part 2 / ..."、"the following parts build on this"、
或者输入第一行是 `PART n`。

**标准做法**：见 `01-solving-framework.md` §2 的"倒着设计三问"。核心一句：
**保留原始记录，聚合值从它派生**，因为撤销类需求必须能回头找到那一条。

**典型翻车**：Part 2 只存 `count`，Part 4 要求"撤销某笔交易"→ 不知道该减哪个计数器。

---

## S02 · 面向行的解析（分隔符、类型化字段、坏行）

**为什么考**：几乎每道题的前 10 分钟都是解析。Stripe 员工在 Blind 上的原话是
"input parsing, creating classes, proper data structures, business logic" —— 解析排第一。

**怎么识别**：输入是 stdin 上的纯文本，多种记录类型混在一起，靠第一个 token 区分。

**标准做法**：

```python
def parse(lines):
    for raw in lines:
        line = raw.strip()
        if not line:                      # 空行永远先跳过
            continue
        parts = [p.strip() for p in line.split(",")]   # 容忍逗号周围的空格
        kind, rest = parts[0], parts[1:]
        ...
```

四条纪律：
1. **先 `strip()` 再判空**，空行不是错误。
2. **每个字段都 `strip()`**，题面写 "spaces around commas tolerated" 时这是必须的。
3. **用 `maxsplit` 保护含分隔符的字段**：`line.split(",", 2)` 让第 3 个字段里可以有逗号。
4. **setup 行可能出现在文件任何位置**，但语义上"先于所有事件生效" → **两遍扫描**：
   第一遍只收 setup，第二遍只处理事件。

**典型翻车**：把 setup 和事件放在一个循环里按出现顺序处理 —— 题面明确说
"Setup lines are applied **before** any event, wherever they appear"。

---

## S03 · 用小记录 + 按 id 索引的字典建模

**为什么考**：这是"proper data structures"那一句的直接考点。

**标准做法**：

```python
from dataclasses import dataclass, field

@dataclass
class Account:
    total: int = 0
    fraud: int = 0
    mcc: str | None = None

accounts: dict[str, Account] = defaultdict(Account)   # key = account_id
```

**什么时候用 `dict`，什么时候用 `@dataclass`，什么时候用真正的类：**

| 情况 | 用什么 |
|---|---|
| 3 个以下字段，只读不改 | `tuple` 或 `dict` |
| 4+ 个字段，要按名字取 | `@dataclass`（自带 `__repr__`，调试时是救命的） |
| 有不变量要维护（余额不能为负、状态机） | 真正的类，把校验放进方法里 |
| 只是"每个 id 一个计数器" | `defaultdict(int)`，别过度建模 |

**信号：当你有 3 个以上并行的 `dict[str, X]` 用同一个 key 时，它们应该是一个记录。**

**典型翻车**：`defaultdict` 的隐式建键 —— `if accounts[x].total > 0:` 这一句会**创建** `x`，
于是"从未出现过的账户"也进了输出。查询用 `.get()`，只有写入才用 `[]`。

---

## S04 · 分组聚合，规则"每组一次"而不是"每行一次"

**为什么考**：商户评分类题目的头号错因 —— 加分项被按行重复计算。

**怎么识别**：题面出现 "a merchant with more than one X gets a bonus"、
"apply the penalty once per account"、"repeat customers"。

**标准做法**：先分组，再对**组**应用规则：

```python
by_merchant = defaultdict(list)
for tx in txs:
    by_merchant[tx.merchant].append(tx)

for m, group in by_merchant.items():
    score = sum(base(t) for t in group)          # 每行一次的部分
    if len({t.customer for t in group}) < len(group):
        score += REPEAT_BONUS                     # ← 每组一次，只加一遍
```

**判断准则**：把规则的主语读出来。主语是"这笔交易"→ 每行一次；
主语是"这个商户 / 这个用户 / 这一天"→ 每组一次。

**典型翻车**：在遍历交易的循环里写 `if seen_before: score += BONUS`，
于是有 5 笔重复交易就加了 5 次。

---

## S05 · 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛

**为什么考**：一个 `>` 写成 `>=`，翻掉的隐藏测试往往不止一个（"恰好等于"是必测的）。

**英文 → 比较符对照表**（背下来）：

| 英文 | 含义 |
|---|---|
| exceeds N / more than N / above N | `> N` |
| at least N / N or more / no fewer than N | `>= N` |
| up to N / at most N / no more than N | `<= N` |
| fewer than N / below N / under N | `< N` |
| reaches N / hits N | `>= N` |
| between A and B（未说明） | **歧义**，默认 `A <= x <= B`，写注释 |

**计数阈值 vs 比例阈值**：有些题用字面量的**形状**区分 ——
`3` 是计数阈值，`0.25` 甚至 `1.0` 是比例阈值。判断方法是**看有没有小数点**，不是看值：

```python
is_ratio = "." in literal            # "1.0" → 比例；"1" → 计数
```

**最小量门槛（min volume）**：比例阈值几乎总是配一个"至少要有 N 笔才判定"的门槛，
否则第一笔就是欺诈的商户会 1/1 = 100% 立刻被封。门槛用 `>=`：
`total >= min_count and fraud * den >= num * total`。

**典型翻车**：
- `total == 0` 时算比例 → 除零；正确答案是"永不判定"。
- 门槛用了 `>` 而不是 `>=`。
- 比例用浮点比较（见 S06 / `04-money-and-rounding.md`）。

---

## S06 · 金额用整数最小单位；显式舍入；两位小数格式

**为什么考**：Stripe 的 API 本身就是整数最小单位（`amount: 1099` = $10.99）。
浮点累加的漂移会在第 1000 笔上显形，而 perf 测试正好用 10^5 条数据。

**铁律**（详见 `04-money-and-rounding.md`）：

1. **解析时立刻变成整数分**：`cents = int(round(Decimal(s) * 100))`，
   或者更安全：`d = Decimal(s); cents = int(d.scaleb(2))`（输入保证两位小数时）。
2. **中间计算全程用 `int`**。
3. **只在输出时格式化一次**：`f"{cents // 100}.{cents % 100:02d}"`，
   负数要单独处理符号，别指望 `//` 和 `%` 对负数的行为。
4. **零小数货币**（JPY、KRW、UGX 等）没有"分"，1 = 1 日元。题面给了货币列表就必须分开处理。

**如果必须用 `Decimal`**：显式给舍入模式，不要依赖默认：

```python
from decimal import Decimal, ROUND_HALF_UP
amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

Python 的 `round()` 是**banker's rounding**（四舍六入五成双）：`round(2.5) == 2`。
题面说 "round half up" 时用它就是错的。

---

## S07 · 阶梯 / 计量 / 按比例分摊

**为什么考**：Billing 团队的题直接对应 Stripe 的定价模型。

**两种阶梯，务必分清**：

| | Graduated（累进） | Volume（整量） |
|---|---|---|
| 含义 | 每一档的量按该档单价计费，逐档累加 | 总量落在哪一档，**全部**按该档单价 |
| 类比 | 个人所得税 | 批发价 |
| 1200 单位，0–1000 @ 10¢，1000+ @ 5¢ | 1000×10 + 200×5 = 11000 | 1200×5 = 6000 |

题面不说清楚时，**"tiered"/"graduated"→ 累进，"volume"→ 整量**，并在注释里写明假设。

**累进的标准写法**（左闭右闭的整数档，`upper=None` 表示无上界）：

```python
def graduated(units, tiers):          # tiers = [(upper, price_per_unit), ...]
    total, prev = 0, 0
    for upper, price in tiers:
        if units <= prev:
            break
        take = (min(units, upper) - prev) if upper is not None else (units - prev)
        total += take * price
        prev = upper if upper is not None else units
    return total
```

**included allowance（免费额度）**：先减额度再进阶梯，`units = max(0, used - included)`。

**proration（按比例分摊）**：中途换套餐时，两段各按**天数占比**计费。
坑在于"天数"的定义：是 `(end - start).days` 还是 `+1`（含首含尾）？
题面通常在样例里透露 —— 用样例反推，别猜。

---

## S08 · 确定性排序与完整 tie-break

**为什么考**：几乎每道题的输出都是 "sorted by X"，而隐藏测试一定会构造平手。

**标准做法**：把整个排序键写成一个元组，一次排完：

```python
rows.sort(key=lambda r: (-r.score, r.name))        # score 降序，name 升序
```

**降序和升序混在一起怎么办**：
- 数值列降序：取负号 `-r.score`。
- 字符串列降序：**不能取负号**。要么先按字符串升序排一遍再按其他列稳定排（利用 `sort` 的稳定性，
  从最次要的键开始逐个排），要么用 `functools.cmp_to_key` 写比较函数。

```python
rows.sort(key=lambda r: r.name)          # 最次要的键，先排
rows.sort(key=lambda r: r.score, reverse=True)   # 最主要的键，后排（稳定性保住前一次）
```

**字典序 vs 数值序**：`"acct_10" < "acct_2"` 是**真的**（字符 `1` < `2`）。
题面写 "lexicographically sorted" 就是这个意思，不要偷偷按数字排。

**没说 tie-break 怎么办**：按一个天然唯一的键（id）升序，并写注释。
沉默的平手是不确定输出，一定挂 perf/fmt 测试。

---

## S09 · 字节级精确的输出格式

**为什么考**：候选人报告里反复出现 "spacing/commas errors causing rejection"。

**清单**：
- 分隔符：`,` 还是 `, `？题面的样例是唯一真相，**复制粘贴样例**去对照。
- 小数位：`$0.00` 要两位，`0` 不行，`0.0` 也不行 → `f"{x:.2f}"`。
- 补零：`f"{n:016d}"`（16 位卡号）、`f"{h:02d}:{m:02d}"`。
- 千分位：`f"{n:,}"`（题面要求才加）。
- 空结果：`NONE`？空行？不输出？三选一，题面里找。
- 末尾换行：`print()` 自带 `\n`；用 `sys.stdout.write` 时自己补。
- **格式化只写在一个函数里**（`render`），改一次全对。

**自查方法**：

```python
assert out == expected, f"{out!r} != {expected!r}"   # repr 能看见空格和 \r
```

---

## S10 · 事件流 + 反向事件

**为什么考**：这是 Part 3–5 的固定套路 —— 后来的事件会**改变前面已经得出的结论**。

**典型反向事件**：`DISPUTE`（撤销一笔 charge）、`REFUND`、`CANCEL`、`DEALLOCATE`、
`plan change`（旧套餐的排期作废）、`server shutdown`（连接要重路由）。

**标准做法**：

```python
charges: dict[str, Charge] = {}      # 保留原始记录 ← 关键
def apply(ch):     accounts[ch.acct].total += 1; accounts[ch.acct].fraud += ch.is_fraud
def unapply(ch):   accounts[ch.acct].total -= 1; accounts[ch.acct].fraud -= ch.is_fraud
```

`apply` / `unapply` 成对写，逐字对称 —— 不对称就是 bug。

**四个必测边界**（题面几乎一定有）：
1. 撤销一个**不存在**的 id → 忽略（不是报错）。
2. **重复撤销**同一个 id → 第二次是 no-op。
3. 撤销一笔**非欺诈**的记录 → 只减分母，可能让比例**上升**、把账户推**过**阈值。
4. 全部撤销后 `total == 0` → 不判定（避免 0/0）。

第 3 条最容易漏：直觉上"撤销"总是让情况变好，实际上撤销分母会让比例变差。

---

## S11 · 幂等 / 去重

**为什么考**：对应真实世界的 idempotency key 和 webhook event id。

**怎么识别**：题面出现 "a repeated X is ignored"、"duplicate ids"、"already exists"、
"a second DISPUTE is a no-op"、"double free"。

**标准做法**：用一个 `set` 或 `dict` 记住已见过的 id，**在处理之前**查：

```python
if charge_id in charges:      # 已存在 → 整条忽略，不是覆盖
    continue
charges[charge_id] = Charge(...)
```

**三种不同语义，别混**：
- **忽略**（ignore）：第二次完全不处理，第一次的效果保留。
- **覆盖**（last wins）：第二次替换第一次。题面写 "last one wins if repeated" 时用它。
- **报错**：输出一行错误。

**一个真实的细节**：id 被撤销/释放之后**再次出现**，算新记录还是重复？
不同题不同答案 —— `q01` 的澄清说"被 dispute 过的 charge id 再出现算新的一笔"。
规格没说时，写注释声明假设。

---

## S12 · 时间与日期

详见 `05-time-and-intervals.md`。总纲：

- 统一成**一种表示**再计算：要么全部 epoch 秒，要么全部 `datetime`。
- **不要用浮点秒**。
- 小时桶：`ts // 3600`；天：`ts // 86400`（UTC）。
- `HH:MM` → 分钟数：`h * 60 + m`，比较和排序都用它。
- 月末夹取（Jan 31 + 1 month = Feb 28/29）要手写，`timedelta` 没有"月"。
- 时区偏移是**分钟**级的（印度是 +5:30），别用整小时假设。

---

## S13 · 闭区间、补齐空隙、off-by-one 纪律

**为什么考**：BIN 区间、部署窗口、营业时段全是区间题，而端点是唯一的难点。

**做法**：在函数顶端用注释**声明区间惯例**，然后全程只用这一种：

```python
# 全文件惯例：[lo, hi] 闭区间，整数域
```

**闭区间的三个基本操作**：

```python
overlap  = a.lo <= b.hi and b.lo <= a.hi
adjacent = a.hi + 1 == b.lo            # 整数域才有"相邻"
merged   = (min(a.lo, b.lo), max(a.hi, b.hi))
gap      = (a.hi + 1, b.lo - 1)        # 仅当 a.hi + 1 <= b.lo - 1
```

半开区间 `[lo, hi)` 的对应式子里没有 `+1`，这就是为什么必须先声明惯例。

**典型翻车**：`merge` 时用了 `a.hi < b.lo` 判断"不重叠"，整数域里 `[1,3]` 和 `[4,6]` 相邻应合并。

---

## S14 · 字符串归一化 / 规范化

**为什么考**：公司名注册、邮箱、语言标签、卡号 —— 都要先归一化再比较。

**做法：归一化是一个纯函数，在边界调用一次，全程只比较归一化后的值。**

```python
def canonical(name: str) -> str:
    s = name.casefold()                       # 不是 lower()：处理 ß → ss
    s = re.sub(r"[^a-z0-9 ]+", " ", s)        # 标点变空格
    s = re.sub(r"\s+", " ", s).strip()        # 折叠空白
    for suffix in ("inc", "llc", "ltd", "corp"):   # 公司后缀
        if s.endswith(" " + suffix):
            s = s[: -len(suffix) - 1]
    return s
```

**必须留住原文**：输出通常要求原始拼写，归一化的值只做 key。
`registry[canonical(name)] = name`。

**顺序有讲究**：先去标点还是先去后缀？题面的样例决定。`"A.B.C. Inc."` 两种顺序结果不同。

---

## S15 · 掩码输入上的小规模组合

**为什么考**：卡号里有 `*` 要补全、有 `?` 要试一位。

**做法**：先算规模再决定。`*` 的个数 k → `10^k` 种。k ≤ 6 时暴力枚举没问题（10^6）；
更大就要用**数位性质**剪枝（例如 Luhn 校验和对每一位是线性的，
可以先算已知位的贡献，再解出未知位需要凑出的余数）。

**单编辑枚举**（`?` 表示某一位被改坏了）：只有 `10 * n` 种可能，直接枚举。
相邻交换（transposition）是 `n-1` 种。

---

## S16 · 滑动窗口计数器 / 令牌桶

见 `05-time-and-intervals.md` §4 和 `08-algorithm-patterns.md` §3。要点：

- **滑动窗口**：每个 key 一个 `deque`，新事件进来先从左边弹出所有过期的。
  "过期"的判定是 `ts - dq[0] >= window`（还是 `>`？题面决定）。
- **令牌桶**：只存 `(tokens, last_refill_ts)`，用时再补：
  `tokens = min(cap, tokens + (now - last) * rate)`。**不要**用定时器。
- **空闲清理**：长时间没请求的 key 要从字典里删掉，否则 10^6 个 key 撑爆内存。

---

## S17 · 台账式余额跟踪

**为什么考**：Stripe 的核心业务就是账。

**不变量优先**（写在类的注释里，然后在每个方法末尾维持它）：

```
balance == sum(credits) - sum(debits)
balance >= 0        （除非题面允许透支 / 有平台授信额度）
```

**做法**：

```python
def debit(self, acct, cents):
    if self.bal[acct] < cents:            # 严格还是非严格？看题面
        return f"REJECTED:{acct}"         # 拒绝时**不要**修改余额
    self.bal[acct] -= cents
    return None
```

**两个常见变体**：
- **平台授信**：余额不足时可以向平台借，但借款总额有上限 `MAX_RESERVE`。
- **储备金**：一部分余额被冻结，可用余额 = 余额 − 储备。

**典型翻车**：拒绝的路径上改了余额（先扣再判断再加回来，中间抛异常就漏了）。
**先判断，后修改。**

---

## S18 · 校验与错误路径

**为什么考**：phone screen 的评分表里明确写着 "dictionary key presence / number validity checks"。

**做法**：错误策略在一个函数里集中决定，而不是散落的 `try`：

```python
def parse_row(fields):
    """返回 (record, None) 或 (None, reason)。调用方决定跳过还是报错。"""
    if len(fields) != 5:            return None, "wrong arity"
    if not fields[2].isdigit():     return None, "bad amount"
    ...
```

**三类错误，行为不同**：
1. **格式坏**（字段数不对、数字解析失败）→ 通常"跳过这一行"。
2. **引用坏**（引用了不存在的 id）→ 通常"忽略这条事件"。
3. **业务坏**（余额不足、状态不允许）→ 通常"输出一行拒绝信息"。

题面的 "Edge cases" 一节会说明是哪一类。**不要用 `try/except` 兜底所有情况** ——
你会把真 bug 也吞掉，然后在隐藏测试里静默地输出错误答案。

---

## S19 · 增量式设计：parse → model → compute → render

见 `01-solving-framework.md` §3。这里补一条：

**后面的 part 应该调用前面的 part，而不是复制它。** 例如 Part 3 是
"Part 2 的结果 + 一条新规则"，那就 `def part3(lines): return apply_rule(part2(lines))`。
这样 Part 2 的 bug 修一次两处都对。

---

## S20 · 自测纪律

见 `09-debug-and-selftest.md`。核心三条：
1. 样例**复制粘贴**跑，不手敲。
2. 每个 part 自己编 2–3 个边界。
3. **确认测试真的会失败** —— 把实现改坏一行，测试必须变红。不会红的测试等于没写。

---

## S21 · 语言熟练度与标准库

见 `03-python-cheatsheet.md`。Stripe 的工程师公开建议**不要用 Java**做这个 OA ——
不是因为 Java 不好，是因为 60 分钟里你输不起打字的时间。

必须闭着眼睛写出来的：`defaultdict` / `Counter` / `heapq.heappush,heappop` /
`bisect_left,bisect_right` / `sorted(key=)` / `deque` / `Decimal(...).quantize` /
`datetime.strptime` / `csv.DictReader` / `json.loads` / `functools.cmp_to_key`。

---

## S22 · 时间盒

见 `01-solving-framework.md` §1。报告过的结果：18/20 过、22/25 过、14/20 挂。
**部分通过能进下一轮**，所以"把已完成的部分做到全绿"比"多做一个 part 做到一半"更划算。

---

## S23 · 浏览器 IDE 里的打印调试

HackerRank 记录切换标签页的次数，也没有断点。因此：

- **只往 stderr 打印**：`print(x, file=sys.stderr)`。stdout 上多一个字符就全挂。
- 打印**结构化**的东西：`print(f"{acct=} {total=} {fraud=}", file=sys.stderr)`
  （`f"{x=}"` 自动带变量名，Python 3.8+）。
- 交卷前全部删掉。

---

## S24 · 领域词汇（支付）

看不懂业务词就读不懂规格。最小词表：

| 词 | 含义 |
|---|---|
| charge | 一笔扣款 |
| dispute / chargeback | 持卡人向发卡行发起的争议，会把钱扣回去 |
| refund | 商户主动退款（与 dispute 不同） |
| payout | Stripe 把余额打给商户 |
| MCC | Merchant Category Code，商户品类码（4 位数字） |
| BIN | 卡号前 6–8 位，决定发卡行和卡组织 |
| Luhn | 卡号校验算法 |
| idempotency key | 幂等键，重复请求只生效一次 |
| minor units | 最小货币单位（分） |
| zero-decimal currency | 没有"分"的货币（JPY、KRW） |
| proration | 中途变更时按比例计费 |
| Connect / platform / connected account | 平台模式：平台代收，再分账给子账户 |
| Radar | Stripe 的风控规则引擎 |
| KYC | 商户身份/资质核验 |
| reserve | 平台冻结的一部分余额 |
| statement descriptor | 出现在持卡人账单上的商户名 |

---

# 第二部分 · 算法考点 A01–A16

> 这些主要出现在 phone screen 和 onsite，也是 LeetCode "Stripe" tag 的高频题。
> 模板代码见 `08-algorithm-patterns.md`。

| id | 考点 | 一句话要点 | 最易错处 |
|---|---|---|---|
| **A01** | 前缀和 + 带 tie-break 的 argmin | 答案区间是 `[0, n]`（比元素多一个），不是 `[0, n-1]` | 平手取**最小**下标 |
| **A02** | 图上的路径乘积 / 除法求值 | 用带权图 + DFS/BFS，权重相乘；反向边取倒数 | 未知节点、除零、自己到自己 = 1.0 |
| **A03** | ≤K 跳的最短路 | **Bellman-Ford 按轮松弛**，不是 Dijkstra | 每轮必须基于**上一轮**的 dist 副本，否则一轮走多跳 |
| **A04** | 栈 / 回溯做字符串展开 | 嵌套花括号用递归下降或显式栈 | 输出要求排序 & 去重；空组 `{}` |
| **A05** | 哈希 + 排序做记录校验 | 先按 name 分组，组内按时间排，再滑窗 | "60 分钟内"是 `<= 60` 还是 `< 60`；同一条不能和自己比 |
| **A06** | 累进税 / 阶梯 | 见 S07 | 最后一档无上界；档位边界恰好命中 |
| **A07** | 每 key 上按时间排序的滑动窗口 | `deque` + 从左弹出过期 | 窗口是"≥3 次"还是"第 3 次触发"；同一分钟多次 |
| **A08** | 带校验的模拟 / 设计题 | 状态 + 方法 + 不变量；先校验后修改 | 账号从 1 还是 0 开始编号；转账两端都要校验 |
| **A09** | 区间合并 / 被覆盖区间 | 先按 `(start, -end)` 排序 | 相邻整数区间要合并；完全覆盖 vs 部分重叠 |
| **A10** | 最少转账次数结清债务 | 先**净额化**（每人一个净值，扔掉 0），再 DFS 剪枝 / 状压 DP | 净额化之前就想算最优 = 错；n ≤ 12 才能状压 |
| **A11** | 带权拓扑序 | Kahn + `finish[v] = max(finish[u] + w[v])` | 有环时入队总数 < n；起点是入度为 0 的所有点 |
| **A12** | 一次编辑距离 | 等长 → 只能是替换，恰好 1 处不同；长度差 1 → 跳过一位后必须全等 | 长度差 ≥ 2 直接 `False`；完全相同返回 `False`（"one" 是恰好一次） |
| **A13** | 网格 / 哈希计数 | 只统计被涂黑格子影响到的 2×2 块，用 dict 计数 | 块的合法坐标范围；一个黑格影响最多 4 个块 |
| **A14** | LRU / 时间键缓存 | `OrderedDict.move_to_end` 或 dict + 双向链表；时间键用 `bisect` | `get` 也算一次使用；TTL 过期与容量淘汰的优先级 |
| **A15** | 堆做 top-k / 选最闲的 | `heapq` + 元组键 `(load, id)`；**惰性删除**处理过期条目 | 负载变化后旧条目还在堆里 → 弹出时校验是否最新 |
| **A16** | 并查集 / 连通分量 | 路径压缩 + 按秩合并 | "共享标识符"要建的是 **实体–标识符** 二部图，不是实体之间的边 |

---

## 怎么用这份总纲

做完一道题、看了参考解之后，回到这里：

1. 找出**你没想到**的那个点属于哪个 S/A 编号。
2. 去 `07-pitfalls.md` 看这个类别下还有哪些坑你也会踩。
3. 去 SystemDesign 仓库的 `code-core` 牌组里，把对应叶子的卡片加进复习。

**不要"再刷十道题"。** 这 53 道题的考点是重叠的 —— 补上编号，比补上题号有用得多。
