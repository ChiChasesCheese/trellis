# cd07 · Transactions + Rules（AI Programming Exercise）：递归下降解析三步走，外加"AI 轮"怎么答

> [!tldr]
> - 这题考的是：把 `ALLOW|BLOCK if <condition>` 这种规则语言解析成可执行的判断，三个 Part 依次加
>   `==`、加比较运算符和 `in [...]`、加 `AND/OR/NOT` 布尔逻辑——是"写一个 mini 表达式语言"这一大类
>   面试题的标准模板
> - 三步套路：**tokenize（切词）→ parse（按优先级建树）→ eval（对着一条数据求值）**，三层各管各的，
>   后面加语法只改 parse 这一层
> - 最值得带走的一个模式：递归下降解析器的优先级不是写在表里的，是**函数调用顺序**——优先级越高的
>   运算符，对应的解析函数离"叶子"越近

## 1. 题目在说什么（人话版）
Stripe 要做一个交易过滤器：一堆规则，每条形如 `BLOCK if country == US and amount > 5000`；一批
交易；每笔交易走一遍规则，第一条为真的规则决定放行还是拦截，没有规则命中就默认放行。三个 Part 依次
解锁更复杂的条件语法：

```
Part 1: country == US                              # 只有等值
Part 2: amount > 5000 / country in [US, CA]         # 加比较运算符和成员判断
Part 3: country == US and amount > 5000             # 加 AND/OR/NOT/括号
```

小例子（Part 1）：
```
RULES
ALLOW if country == US
BLOCK if amount == 10000
TRANSACTIONS
t1,500,USD,US,visa,acme
t2,10000,USD,CA,visa,acme
```
→ `t1 ALLOW (rule 1)` / `t2 BLOCK (rule 2)`。

这题还有一层特殊身份：它是 Stripe 2026 新增的 **"AI Programming Exercise"** 轮的原型题——candidate
在 HackerRank 里带一个 AI 聊天窗口，30 分钟内"和 AI 一起"把这题做完，评分标准是"你怎么指挥 AI"，不是
打字速度。这篇文章除了讲这题本身的建模方法，也会专门讲这种新轮次该怎么应对（第 6 节）。

## 2. 读题：把文字变成模型
- **实体**：规则（动作 + 条件表达式）、交易（六个字段的一行记录）。
- **输入长什么样**：`RULES` 段一行一条规则、`TRANSACTIONS` 段一行一笔交易，两段之间靠 header 行
  区分；交易字段用逗号分隔，没有转义、没有内嵌逗号。
- **输出要什么**：每笔交易一行，命中规则要报"第几条规则"（1-indexed，且要数进后面判定为无效的
  规则），没命中就是纯 `ALLOW`，没有后缀。
- **状态**：不需要维护"跨交易"的状态——每条规则编译一次、每笔交易独立求值。真正需要维护的是**每条
  规则的语法树**，编译一次、复用给所有交易，避免对 10 万笔交易各重新解析一遍规则文本。
- **一句话建模**：这是一个 **"文本 → 语法树 → 对每条数据求值"** 的 mini 解释器问题，三个 Part 只是
  语法树的节点类型从"一个比较"逐步扩展到"任意布尔组合"。

> [!note] 为什么选递归下降而不是正则拼接
> 候选方案是"用一堆正则或字符串 split 硬解析"，在 Part 1（只有一种形状 `field == value`）阶段能跑，
> 但 Part 3 一旦出现括号嵌套和运算符优先级，正则会迅速失控。递归下降解析器把"优先级"直接编码成
> **函数之间的调用关系**——`or_expr` 调 `and_expr`，`and_expr` 调 `unary`——不需要额外维护一张优先级
> 表，也是这类语法题面试官最想看到的组织方式。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 按 `PART n` 分发 → `partN` 解析规则和交易 → 打印。三个 `partN`
   先都 `return []`，跑一下确认不报错。
2. **Part 1 最小可用**：写 `_tokenize`（把条件文本切成 `field`/`OP`/`value` 三种 token）和一个只认
   `field == value` 的 `_comparison`；`_evaluate` 把规则和交易都解析出来，逐条规则测逐笔交易，第一个
   命中就停。立刻用样例自测。
3. **Part 2 叠加**：`_comparison` 加 `!=`、`>`、`<`、`>=`、`<=` 和 `in [...]` 分支；**tokenizer 和
   主循环 `_evaluate` 原样不动**——这一步的教训是"只改语法层，不要碰求值层"。
4. **Part 3 叠加**：在 `_comparison` 外面包一层 `_or → _and → _not → _primary`，`_primary` 里处理
   括号和"回退到 `_comparison`"。这四个函数就是优先级表本身：写的时候按"结合最松的写在最外层"的顺序
   一个个写，`_or` 最外层，`_not` 最内层。
5. **收尾**：`ERROR line k` 只在 Part 3 出现，其余 Part 静默跳过写错的规则——这是没在题面里明说的
   选择，面试时主动说出来；确认规则编号在跳过无效规则后不会错位。

## 4. 代码怎么组织
```
_tokenize(text) -> list[(kind, value)]        # 只管切词，不关心语法
_Parser                                        # 递归下降：_or -> _and -> _not -> _primary -> _comparison
  .parse() -> AST                              # AST = ('and'|'or'|'not'|'cmp'|'in', ...)
parse_condition(text, part) -> AST             # 按 part 决定是否放开布尔层（allow_bool）
_resolve(token, txn)                           # 字段名 -> 查交易；其它 -> 当字面量
_compare(op, lv, rv) -> bool                   # 数字优先、否则按字符串比较
_eval(node, txn) -> bool                       # 对着一条交易递归求值 AST
_split_sections(lines) -> (rules, txns)        # 只管按 header 切两段
_parse_txn(line) -> dict                       # 只管把一行变成六个字段的 dict
_evaluate(lines, part) -> list[str]            # 编译规则 -> 逐笔求值 -> 格式化，partN 的唯一实现
part1/2/3(lines) -> list[str]                  # 各自调 _evaluate(lines, N)
main(stdin, stdout)                            # 只做分发
```
拆分原则：**tokenize / parse / eval 三层各管各的**，`part` 参数只影响 parser 放开哪些语法产生式
（`allow_bool`、运算符白名单），eval 层完全不知道当前是第几个 Part。这样一个陌生人 60 秒内能从
`_evaluate` 追到 `parse_condition` 再追到 `_eval`，三个 Part 共用同一条链路，面试官问"如果要加
`XOR` 运算符"时，你能准确指出只需要在 `_or`/`_and` 之间插一层新函数。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：切词 -> 递归下降建树 -> 求值。省略 _split_sections/_parse_txn 等纯格式化代码，
# _and() 从略：结构与 _or() 完全一致，只是把 "or"/self._and 换成 "and"/self._not。
def _tokenize(text):
    tokens, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        m = TOKEN_RE.match(text, i)          # 括号/中括号/逗号/比较符/裸词，五选一
        tokens.append((m.lastgroup, m.group(m.lastgroup)))
        i = m.end()
    return tokens

class _Parser:                                # 优先级 = or 最松 -> and -> not 最紧 -> 括号/比较
    def _or(self):
        node = self._and()
        while self._is_kw(self._peek(), "or"):
            self._advance()
            node = ("or", node, self._and())
        return node

    def _not(self):
        if self._is_kw(self._peek(), "not"):
            self._advance()
            return ("not", self._not())
        return self._primary()               # 括号在这里回退到 self._or()，否则落到比较

def _resolve(token, txn):                     # 字段名查交易，否则当字面量
    return txn[token] if token in FIELDS else token

def _eval(node, txn):                         # 对着一条交易递归求值语法树
    kind = node[0]
    if kind == "and":
        return _eval(node[1], txn) and _eval(node[2], txn)
    if kind == "or":
        return _eval(node[1], txn) or _eval(node[2], txn)
    if kind == "not":
        return not _eval(node[1], txn)
    _, op, left, right = node                 # kind == "cmp"
    return _compare(op, _resolve(left, txn), _resolve(right, txn))
```

## 6. 面试里怎么说（边写边讲，AI 轮额外要讲什么）
- 开始前：「我先确认协议：`RULES`/`TRANSACTIONS` 两段靠 header 行区分，交易少于 6 列时缺的字段我当
  空字符串处理，不报错。」
- 写 Part 1 时：「我把切词和求值分成两层，这样后面加运算符、加布尔逻辑都只改解析这一层。」
- 写 Part 2 时：「等值比较我先看两边是不是都能转成整数，能就按数字比，不能就按字符串比，这样
  `amount == 0100` 才能匹配 `amount == 100`。」
- 写 Part 3 时：「优先级我用函数调用顺序表达——`or` 调 `and`、`and` 调 `not`——不用额外维护一张
  优先级表，加新运算符只要在中间插一层函数。」
- 写错误处理时：「题面只要求 Part 3 报 `ERROR line k`，Part 1/2 我选择静默跳过写错的规则；这是我的
  选择，不是题面写死的，如果你们想要 Part 1/2 也报错，我现在就能改。」
- 交付时：「三个样例都过了；如果时间允许，我会给按字段建一个索引，减少大量规则都不涉及某个字段时的
  无效比较。」

如果这轮真的带 AI 助手（HackerRank 内嵌聊天窗），评分轴变成"你怎么指挥它"，方法论是**让 AI 写、你写
测试、你抓过度工程**三步：
1. **让 AI 写**：先把协议、语法、边界情况喂给它，让它复述需求、和你对齐一个实现方案，达成一致后再要
   代码——直接要完整解法、跳过对齐这一步，是这轮最容易失分的地方。
2. **你写测试**：不要把 AI 生成的测试当验收标准，自己写几个能"证伪"的用例，专盯这题里 AI 最容易
   翻车的地方——`in [US, CA]` 有没有被写成子串匹配（`country == USA` 不该命中 `in [US]`）、`and`/
   `or` 优先级有没有被拍平成从左到右同级、默认方向有没有被写反成 `BLOCK`。自己的测试锁住行为之后，
   才有资格说"这段代码我验证过"。
3. **你抓过度工程**：AI 常见的毛病是"顺手"多做——题面只要两层布尔逻辑，它却生成一个支持任意嵌套、
   可插拔函数、字符串转义的通用表达式引擎。这不是加分项，是在预算有限的轮次里烧时间做没人要的东西。
   审查 AI 输出的第一件事，是把它的实现范围和题面的语法产生式逐条对一遍，多出来的部分直接砍掉。

## 7. 常见跑偏（方法层面，3 条）
- **一上来就想着写一个通用表达式引擎**：支持任意运算符、任意嵌套、可扩展插件——题面只要三层语法
  （比较 → 布尔组合 → 括号），先把这三层做对，通用性是没人要的过度工程，AI 生成代码尤其容易在这里
  跑偏（见第 6 节"你抓过度工程"）。
- **把 tokenize 和 parse 揉在一起**：一边扫字符一边判断语法结构，Part 2 加运算符还能改，Part 3 加
  括号和优先级就要推倒重写。先把"切词"做成一个独立、跟语法无关的函数，语法结构完全交给递归下降层。
- **优先级写成 if-else 拍平判断**：`a and b or c` 用字符串里找 `and`/`or` 位置来决定结合顺序，这种
  写法处理不了嵌套和括号。递归下降的"函数调用顺序即优先级"是唯一能优雅扩展到任意深度嵌套的写法。

## 8. 同族题 / 延伸
- OA 侧：`problems/q12_platform_balance_radar_rules` 是同一个"规则字符串 → AST → 求值"骨架的
  生产级版本，语法更复杂（`:field:`/`"const"` 标记、`API:`/`BAL:` 余额账本），值得对照读一遍。
- 其他轮：`loop/rounds/03_phone_screen/ps03_brace_expansion` 是另一个"递归下降/回溯解析小型语言"
  的练习，虽然语义不同，但"tokenize → 结构化解析"的方法论是共通的。
- 延伸思考：把 `ERROR line k` 的要求从"只在 Part 3"放宽到"每个 Part 都要"，只需要把 `_evaluate` 里
  `if part == 3` 的判断去掉；把布尔逻辑从两元 `and`/`or` 扩展成变长参数链不需要重新设计 AST 节点
  形状，因为左结合的二叉链本来就等价于变长链，只是遍历顺序不同。
- 练习命令：`python3 loop/mock.py start cd07`
