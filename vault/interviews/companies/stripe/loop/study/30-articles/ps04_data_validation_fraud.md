# ps04 · Transaction Data Validation / Fraud Report：四类风控规则叠一个"优先级 + 截断"报表，练的是"规则表 + 累加式判定"

> [!tldr]
> - 这题考的是：把"这笔交易有没有问题"拆成四类独立规则（缺字段 / 越界 / 黑名单 / 行为异常），每类规则各自判断、互不影响，最后按优先级只保留最重要的两个
> - 三步套路：读题把"一行交易"抽成一个 `fields` 元组 → 先写"规则 1：缺字段"这一个最小闭环 → 后面每个 Part 只加一类规则判断，判定函数本身不变
> - 最值得带走的一个模式：**一个 `check_row` 函数、一个 `checks` 等级参数**——不是四个 `partN` 各写一遍规则，而是"规则等级"控制"评估到第几类"，输出格式才是四个 `partN` 的真正区别

## 1. 题目在说什么（人话版）
Stripe Radar 收到一笔交易，要依次问四个问题：这行数据本身完整吗？金额和支付方式踩雷了吗？跟这个用户
平时的行为像不像？如果好几个问题都答"有毛病"，报告里只留最要紧的两条。输入是四段配置（金额范围、
黑名单、用户历史画像）加一段交易流水，每行交易输出一行结果。

小例子（`RULES 10-5000`，`BLOCKLIST prepaid_card`）：
```
t1,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00   → t1: OK
t2,u1,150.00,USD,prepaid_card,US,2026-08-01T14:30:00  → t2: BLOCKED_METHOD
```
四关是渐进的：Part 1 只看"字段是否为空"，Part 2 加金额范围和黑名单，Part 3 加用户行为比对，Part 4
把 Part 3 的判定结果套上"优先级取前二、列对齐"的报表格式。

## 2. 读题：把文字变成模型
- **实体**：一条交易记录（7 个字段：`txn_id,user_id,amount,currency,payment_method,country,timestamp`），
  一份全局规则（金额区间 + 黑名单），一份按 `user_id` 索引的行为画像（`countries/hour 范围/amount 范围`）。
- **输入长什么样**：四个固定顺序的段（`RULES/BLOCKLIST/PROFILES/TRANSACTIONS`），段头独占一行，段内容
  逐行 CSV，空行随处忽略。四段**永远都在**，即使当前 Part 用不到——这句话决定了"解析"和"这个 Part 要不要
  用"必须分开写，不能"用不到就不解析"。
- **输出要什么**：每行交易一行结果，`txn_id: CODE1,CODE2` 或 `txn_id: OK`，顺序等于输入顺序（不排序）。
  Part 4 变成列对齐报表，且只保留优先级最高的两个码。
- **状态**：不需要跨行状态——每条交易的判定只依赖"这行自己的字段"加"全局规则/黑名单/该用户的画像"，
  三者都是只读查表。真正的状态是"规则等级"：Part n 该评估哪几类规则，这是一个整数开关，不是布尔组合。
- **一句话建模**：这是一个 **"一行数据 × 四类独立规则，规则数由 Part 决定，用查表代替级联 if"** 的验证
  与优先级截断问题。

> [!note] 为什么选这个数据结构
> 候选是"四个 `partN` 各写一份判定逻辑"，或"一个 `check_row(fields, checks)` 按 `checks` 等级累加式判断，
> `partN` 只负责调用 + 格式化"。后者的关键洞察是：Part 2 的规则**没有取代** Part 1 的规则，是**叠加**——
> 用一个整数等级 `checks∈{1,2,3}` 表达"评估到第几类"，比四个布尔开关或四份重复代码都干净，Part 4 更是
> 直接复用 `checks=3` 的判定，只在格式化那一步截断成前两个。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 按空行过滤 → 第一行拿 `PART n` → 查表调 `partN` → 打印。四个 `partN`
   先都 `return []`，`_load()` 把四段配置解析出来但先不管对不对。
2. **Part 1 最小可用**：写 `_split_sections`（按段头分组）和 `parse_transactions`（split 逗号、pad 到 7
   列），`check_row(fields, checks=1, ...)` 只判断"有没有空字段"。立刻用样例的 `t4`（country 空）自测。
3. **Part 2 叠加**：写 `parse_rules`（一行两个数）和 `parse_blocklist`（大小写不敏感的 set），`check_row`
   加 `checks >= 2` 分支：金额落区间、方法查黑名单。两条规则互相独立，都判断，不是 `elif`。
4. **Part 3 叠加**：写 `parse_profiles`，`check_row` 加 `checks >= 3` 分支：查这个用户的画像（没有就跳过
   这条规则），3 个属性各判断一次，数命中数，`< 2` 才算 `SUSPICIOUS`。
5. **Part 4 叠加**：不新增判定逻辑——`part4` 直接调 `check_row(f, 3, ...)`，拿到的 codes 天然是"插入顺序 =
   优先级顺序"（因为判定代码本来就按优先级顺序 append），所以只需要 `codes[:2]`，再算最长 `txn_id` 宽度
   做列对齐。
6. **收尾**：过一遍四个样例，确认"截断不重排"、"没有画像不判定"、"空 BLOCKLIST 不拦任何东西"这几个
   容易漏的点。

## 4. 代码怎么组织
```
_split_sections(lines) -> {段名: 行列表}        # 只管按段头分组，不关心内容格式
parse_rules/parse_blocklist/parse_profiles/parse_transactions(body) -> 结构化数据   # 每段各管各的解析
check_row(fields, checks, rules, blocklist, profiles) -> [CODE...]   # 唯一的判定逻辑，四个 Part 共用
_report_line(txn_id, codes) -> str              # Part 1-3 的格式化，集中一处
part1..part4(lines) -> list[str]                # 调 _load + check_row(checks=n) + 格式化，不含判定逻辑
main(stdin, stdout)                             # 只做分发
```
拆分原则：**"评估哪几类规则"和"怎么格式化输出"是两件事**，前者是 `check_row` 的 `checks` 参数，后者
是 `partN` 自己的事。这样 Part 4 才能做到"零新增判定代码，只改格式化"——面试官问"如果再加一类规则"，
你能指着 `check_row` 说"这里加一段 `if checks >= 4`"，指着 `PRIORITY` 常量说"这里加一个码"，别的都不用动。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：分段解析 → 累加式判定 → 格式化。省略参数校验和 Decimal 转换细节。
PRIORITY = ("MISSING_FIELD", "BLOCKED_METHOD", "AMOUNT_OUT_OF_RANGE", "SUSPICIOUS")

def check_row(fields, checks, rules, blocklist, profiles):
    txn_id, user_id, amount_s, currency, method, country, timestamp = fields
    codes = []
    if any(f == "" for f in fields):                     # 规则 1：任意字段为空
        codes.append("MISSING_FIELD")

    amount = _try_decimal(amount_s)                       # 缺失/非法一律 None，不额外报错
    if checks >= 2:
        if method.lower() in blocklist:                   # 规则 2a：黑名单，大小写不敏感
            codes.append("BLOCKED_METHOD")
        if amount is not None and rules is not None:
            lo, hi = rules
            if not (lo <= amount <= hi):                  # 规则 2b：金额闭区间
                codes.append("AMOUNT_OUT_OF_RANGE")

    if checks >= 3:
        profile = profiles.get(user_id)
        if profile is not None:                           # 没有画像 = 这条规则直接跳过
            matches = 0
            matches += country.upper() in profile.countries
            hour = _parse_hour(timestamp)
            matches += hour is not None and profile.hour_min <= hour <= profile.hour_max
            matches += amount is not None and profile.amount_min <= amount <= profile.amount_max
            if matches < 2:                                # 3 项里 <2 项命中才算可疑
                codes.append("SUSPICIOUS")
    return codes                                           # append 顺序天然 == PRIORITY 顺序

def part4(lines):                                          # 复用 checks=3，只做截断 + 列对齐
    rules, blocklist, profiles, txns = _load(lines)
    rows = [(f[0], check_row(f, 3, rules, blocklist, profiles)[:2]) for f in txns]
    width = max((len(t) for t, _ in rows), default=0)
    return [f"{t:<{width}}  {','.join(c) if c else 'OK'}" for t, c in rows]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我确认一下：四段配置每个 Part 都会解析，但只有对应等级的规则会被评估，对吗？这样 Part 1
  拿到的输入格式和 Part 4 完全一样，只是规则少。」
- 写 `check_row` 时：「我用一个 `checks` 等级而不是四个布尔参数，因为规则本来就是'评估到第几类'，
  Part n 就是 `checks=n`，Part 4 复用 `checks=3`。」
- 讲黑名单/越界并列判断时：「这两条规则互相独立，一笔交易可能同时命中，所以我都用 `if` 不用 `elif`，
  各自 append 自己的码。」
- 讲 SUSPICIOUS 时：「没有画像的用户我选择不判定可疑——没有历史数据没法比较，这是我的假设，如果反过来
  要求'没画像更可疑'，改一行判断就行。」
- 写 Part 4 时：「codes 列表 append 的顺序本来就是优先级顺序，所以我不需要再排序，直接切片取前两个。」
- 交付时：「四个样例都过了；如果要加第五类规则，只需要在 `check_row` 加一段 `checks >= 4` 和一个新的码，
  `partN` 那层完全不用动。」

## 7. 常见跑偏（方法层面，3 条）
- **四个 `partN` 各写一份判定逻辑**：Part 2 复制 Part 1 的空字段检查，Part 3 又复制一遍——改一条规则要
  改四处。先把"判定"抽成一个按等级累加的函数，`partN` 只负责调用等级和格式化。
- **Part 4 重新排序或去重再截断**：如果判定逻辑本身已经按优先级顺序 append，截断只需要切片；一旦额外
  加一次 `sorted`，反而可能把顺序搞乱或掩盖判定逻辑里的顺序 bug。先保证"生成顺序即优先级"，截断就是
  免费的。
- **"评估等级"和"输出格式"揉在一个大 `if part == n` 分支里**：一旦两者绑死，加新 Part 就得复制整个
  分支再改一半。先把"评估到第几类"抽成一个参数，格式化各自独立，新增 Part 通常只改格式化那几行。

## 8. 同族题 / 延伸
- 其他轮：q02 `merchant_fraud_score` 是同一个"分段 stdin + 规则打分"骨架的打分版本（这里是布尔命中集合，
  q02 是加权求和）；q15 `kyc_verification` 看起来像同题但规则集完全不同（CSV 引号、描述符规则、循环依赖
  检查），不要混用两题的解析逻辑。
- ps01 `transaction_stream_levels` 也是"Part n 只加一类判断、判定函数被后续 Part 复用"的同一套方法论，
  只是那题的状态是时间窗口，这题的状态是查表。
- 延伸思考：如果规则从 4 类扩展到任意 N 类，`checks` 整数会不够用——换成 `set[str]`（比如
  `{"missing", "range", "blocklist", "suspicious"}`）按需传入,`check_row` 的每个分支只在 `"suspicious" in
  checks` 时执行，比整数等级更灵活但可读性略降，这是"要不要为可能的未来扩展多做一层抽象"的典型取舍。
- 练习命令：`python3 -m pytest loop/rounds/03_phone_screen/ps04_data_validation_fraud`
