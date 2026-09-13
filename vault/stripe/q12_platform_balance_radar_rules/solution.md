# q12 · 平台余额 API + Radar 规则引擎

> `problems/q12_platform_balance_radar_rules/` · 3 个 part
> **主题：query string 解析 + 手写一个小语言（tokenizer + 递归下降）。**

## 一句话题意

Part 1 是一个按 query string 更新的余额账本；Part 2 在前面加一个 `==`/`!=` 的拦截规则；
Part 3 把规则换成真正的 Radar 语法（引号常量、布尔属性、`AND`/`OR`、括号）。

## 输入 / 输出

```
PART n
API:  k1=v1&k2=v2…       更新余额；缺 amount/merchant 或 amount 非整数 → 畸形，忽略
BAL:  merchant=121212    打印该商户余额（没见过 → 0）
RULE: <rule>             注册规则，只对**之后**的行生效；解析失败则忽略
TXN:  k1=v1&…            对规则求值，打印 ACCEPT / BLOCK
```
值**不做 URL 解码**，允许含空格。重复 key **后者覆盖**。最多 10^5 行。

输出：`BAL:` 打印裸整数（`750` / `-250` / `0`），`TXN:` 打印 `ACCEPT` / `BLOCK`，按输入序。

## 核心考点

`S02` query string 解析 + 畸形输入 · `S03` 按 id 的状态 · `S06` 整数分 · `S10` 有序命令流 ·
**`S18` 校验 / 缺 key** · **`S19` tokenizer + 递归下降与账本解耦** · `S24` Radar/Connect 词汇

## 解题思路

### Part 1

```python
def parse_query(s: str) -> dict[str, str]:
    d = {}
    for pair in s.split("&"):
        if "=" not in pair: continue
        k, v = pair.split("=", 1)          # 只切第一个 = ，值里可以有 =
        d[k.strip()] = v                   # 后者覆盖 = 天然的 last-wins
    return d
```

`balances[merchant] += int(amount)`，余额可为负。`BAL:` 未见过的商户 → `0`。

### Part 2 — 简单拦截规则

`RULE: field OP value`，`OP ∈ {==, !=}`（也支持 `< > <= >=`，仅数值）。
**操作符两边的空格可有可无** → 用正则而不是 `split`：

```python
m = re.fullmatch(r"\s*(\w+)\s*(==|!=|<=|>=|<|>)\s*(.*?)\s*", rule)
```

比较语义：**两边都能解析成整数就按数值比**（`amount==0100` 匹配 `100`），否则按 trim 后的字符串比。
**query 里缺这个字段就永远不匹配（`!=` 也不匹配）** —— 这是 Radar 的语义。

Part 2 的规则全是 **block** 规则：`API:` 行匹配**任意一条**已注册规则 → 拒绝（余额不动，不输出）。

### Part 3 — Radar 语法

```
rule     := ("ACCEPT" | "BLOCK") "if" expr
expr     := and_expr ("OR" and_expr)*        # AND 比 OR 紧
and_expr := primary ("AND" primary)*
primary  := "(" expr ")" | operand ("=" | "!=") operand | field
operand  := field | '"' constant '"'          # 常量可含空格；两边可互换
field    := ":" name ":"
```

**分成三层写**（这也是这题隐含的"如何改进代码"的答案）：
1. `tokenize(rule) -> list[Token]`
2. `parse(tokens) -> AST`（递归下降，`expr → and_expr → primary`，天然表达优先级）
3. `evaluate(ast, txn) -> bool`

语义要点：
- 裸 `field` 是**布尔属性**：`txn[name].lower() == "true"` 才为真。`"True"` 也真（大小写不敏感），`"1"` 假。
- **缺字段 ⇒ 该比较/布尔为 `False`**，`!=` 也是 False。
- **按顺序求值，第一条条件为真的规则决定结果**（`ACCEPT` → True，`BLOCK` → False）。
- **没有规则匹配 ⇒ 接受**；空规则表 ⇒ 接受。
- 语法非法的规则：`should_accept_transaction` 抛 `ValueError`，stdin 驱动跳过该 `RULE:` 行。

## 坑

1. key 任意顺序；**重复 key 后者覆盖**；未知 key 忽略但**规则仍能看到**。
2. 负数和零金额；`BAL:` 未知商户 → `0`；畸形行跳过**不崩溃**。
3. 操作符两边空格的三种写法都要支持。
4. **`!=` 对缺失字段不匹配。**
5. **规则只对之后的行生效**，不追溯。
6. Part 3：含空格的常量；操作数可互换；**`AND` 比 `OR` 紧**（`a OR b AND c` = `a OR (b AND c)`）；
   嵌套括号；**第一条匹配的规则说了算**（即使后面有相反的）；无匹配 → accept；
   空规则表 → accept；缺失的布尔字段 → false；只有大小写不敏感的 `true` 为真。
7. 输出格式：余额是**裸整数**，`ACCEPT`/`BLOCK` **大写**。
8. **性能**：不要在每次求值时重新 tokenize 规则 —— 注册时解析成 AST 存起来。
   （仓库记录：这个改动把耗时从 3.98 s 降到 0.28 s。）

## 变体

- **charge-evaluation 变体**（GitHub `RadarRules.java` / Python 移植）：
  `["CHARGE: …", "ALLOW:amount<100", "BLOCK:card_country != ip_country AND amount > 100"]` → `0`/`1`，
  操作符 `> < >= <= == !=`，最多 2 个条件用 `AND`/`OR` 连接，支持字段对字段比较。
- OA 2024 的第二题是问答："如何改进第一题的代码" —— 答案就是这里的 parse → model → evaluate 分层。

## Code Core 节点

**`input.structured`**（query string） · **`input.grammar`**（tokenizer + 递归下降） ·
`input.malformed` · `model.entity-state` · **`performance.hot-loop`**（预编译规则） · `rules.thresholds`

## 自测清单

- [ ] key 乱序 / 重复 key / 未知 key / 缺 amount / amount 非整数
- [ ] 负数、零、未知商户的 `BAL:`
- [ ] `amount==100` / `amount == 100` / `amount ==100`
- [ ] `!=` 对缺失字段
- [ ] 规则注册在 API 行之后 → 不追溯
- [ ] `a OR b AND c` 的优先级、嵌套括号
- [ ] 第一条匹配的规则决定、无匹配 → ACCEPT、空规则表
- [ ] `"true"` / `"True"` / `"1"` 三种布尔值
- [ ] 10^5 行 + 多条规则的耗时（AST 要预编译）
