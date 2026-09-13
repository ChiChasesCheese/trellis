# ps01 · Transaction Stream Levels：一条交易流上"叠"四个 Part，练的是"按用户分组 + 时间窗口"这一个模型

> [!tldr]
> - 这题考的是：把一条乱序的交易流整理成"每个用户一条按时间排好的序列"，然后在这个序列上依次回答四个问题（总额 / 窗口超阈值 / 某时刻的 top-K / 小大小模式）
> - 三步套路：读题抽出 `Tx(user, amount, ts)` 这个记录 → 先跑通 Part 1 的"解析 + dict 累加 + 排序输出" → 后面每个 Part 只加一个 helper，解析和分组原样复用
> - 最值得带走的一个模式：**先 group-by-user 再 sort-by-time**，之后所有"每个用户各自看时间线"的问题都变成对一个 list 的顺序扫描

## 1. 题目在说什么（人话版）
Stripe 的风控要盯着每个用户"花钱的节奏"。输入是一堆交易记录，每行三个字段：谁、花了多少、什么时候（秒）。
行的先后顺序**不保证**是时间顺序——数据可能乱着到。面试分四关，每关是一个 `PART n`，过了一关才给下一关：

1. 每个用户一共花了多少；
2. 哪些用户在**任意 60 秒**内累计花到了阈值 `T`（报第一次触线时的窗口金额）；
3. 在时刻 `t`，过去 60 秒里花得最多的前 `K` 个用户；
4. 哪些用户出现过"小额 → 大额 → 小额"这种试探型消费模式。

小例子（Part 3，`t=90 K=2`）：
```
1,50,10  1,60,40  2,80,30  3,30,40  2,50,90     →   2: 130
                                                    1: 60
```
窗口是 `[30, 90]`：用户 2 有 80+50，用户 1 只有 40 秒那笔 60，用户 3 的 30 排第三没进 top-2。

"过一关给下一关"意味着：面试官不会提前告诉你后面三关是什么，但四关用的是同一份数据。所以第一关就把
"解析"和"计算"分开写，是这类题最划算的投资——后面三关都在白嫖第一关的解析。

## 2. 读题：把文字变成模型
- **实体**：用户（`user_id` 字符串）、交易（金额、时间戳）。就这两个，没有别的。
- **输入长什么样**：第一行 `PART n`；Part 2/3/4 紧接着一行参数 `T=100 W=60`（没有逗号）；其余每行 `user,amount,ts`（恰好两个逗号）。"有没有逗号"就是区分参数行和数据行的依据，这句要在面试里说出来。
- **输出要什么**：每个 Part 都是 `user_id: 值` 一行一个。Part 1/2/4 按 `user_id` 字符串序；Part 3 按**排名**输出（金额降序、同额按 `user_id` 升序）——这是唯一一个不按 id 排的 Part，容易顺手写错。
- **状态**：Part 1 只要一个 `dict[user] -> 总额`（因为求和不关心顺序，这是四问里唯一不用排序的）；Part 2/4 要"每个用户按时间排好的交易列表"；Part 2 扫描时额外要一个 `deque` 记"还在窗口里的交易"和一个 running sum。
- **一句话建模**：这是一个 **按用户分组、按时间排序后的顺序扫描** 问题，四个 Part 只是换了"扫描时判断什么"。

> [!note] 为什么选这个数据结构
> 候选是"全局按时间排序然后维护 `dict[user] -> deque`"，或"先按用户分组、每组各自排序"。两者复杂度一样，但后者让每个 Part 的核心逻辑只面对**一个用户的一个 list**，函数签名简单（`events: list[Tx]`），单测也好写。窗口用 `deque` 是因为只需要"尾部进、头部出"，running sum 跟着加减就不用每次重新求和。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 第一行取 `n` → 查表调 `partN(rest)` → `"\n".join` 打印。四个 `partN` 先都 `return []`，跑一下确认不报错。
2. **Part 1 最小可用**：写 `_parse_tx`（split 逗号、`int()`）和 `_totals`（`defaultdict(int)` 累加），`part1` = 解析 → 累加 → `sorted` 输出。用样例 `1,10 / 2,5 / 1,7 → 1: 17 / 2: 5` 自测。
3. **Part 2 叠加**：先补 `_split_params`（弹出参数行），再写 `_by_user_sorted`（分组 + 按 `(ts, 输入序号)` 排序），最后 `_first_crossing` 用 deque 扫一个用户。`part2` 就是三个 helper 串起来。
4. **Part 3 叠加**：不需要新的核心逻辑——把交易流先过滤到 `[t-60, t]`，**复用 `_totals`**，再 `sorted(key=(-sum, user))[:K]`。面试官看到你复用而不是重写会加分。
5. **Part 4 叠加**：复用 `_by_user_sorted`，新写 `_pattern_starts`：先把每笔标成 `small/large`，再滑一个长度 3 的窗口和 `PATTERN` 比较。
6. **收尾**：确认排序 key 都写全（Part 3 的 `(-sum, user)`）、参数默认值（`W` 缺省 60）、空输入直接返回。

## 4. 代码怎么组织
```
_split_params(lines) -> (params, body)     # 只管弹参数行 + 去空行
_parse_tx(lines) -> list[Tx]               # 只管把每行变成 Tx(user, amount, ts, order)
_by_user_sorted(txs) -> {user: [Tx...]}    # 分组 + 稳定时间排序，Part 2/4 共用
_totals(txs) -> {user: sum}                # Part 1 的规则，Part 3 复用
_first_crossing(events, T, W) -> int|None  # Part 2 的规则：一个用户一条 deque
_pattern_starts(events, S) -> [ts...]      # Part 4 的规则：标签 + 滑窗比 PATTERN
part1..part4(lines) -> list[str]           # 解析 → 调规则 → 格式化，每个 ≤ 8 行
main(stdin, stdout)                        # 只做分发
```
拆分原则：**解析、分组、规则、格式化四层各管各的**。`partN` 本身不含任何 `for` 循环——它只是把三个 helper
串起来，60 秒内能从 `main` 追到任何一个 Part 的核心循环。规则层的函数只吃"一个用户的排好序的 list"，这样它们不知道 stdin 也不知道输出格式，面试官问"如果改成流式输入"或"如果模式变成 4 段"时，你能指着一个函数说"只改这里"。常量（`WINDOW_P3`、`DEFAULT_W`、`PATTERN`）放文件顶部，让规则可见、可改。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：分组 → 规则 → 输出。省略 _parse_tx（split 逗号 + int）、参数行弹出与空输入处理。
class Tx(NamedTuple):
    user: str; amount: int; ts: int; order: int   # order = 输入序号，时间戳相同时保持输入顺序

def _by_user_sorted(txs):                          # user -> 按 (ts, order) 排好的交易
    grouped = defaultdict(list)
    for tx in txs:
        grouped[tx.user].append(tx)
    for events in grouped.values():
        events.sort(key=lambda e: (e.ts, e.order))
    return grouped

def _totals(txs):                                  # Part 1 规则；Part 3 复用
    totals = defaultdict(int)
    for tx in txs:
        totals[tx.user] += tx.amount
    return totals

def _first_crossing(events, threshold, window):    # Part 2 规则：闭区间 [ts-W, ts]
    live, total = deque(), 0
    for tx in events:
        live.append(tx); total += tx.amount
        while live[0].ts < tx.ts - window:         # 踢掉严格更老的
            total -= live.popleft().amount
        if total >= threshold:
            return total                           # 第一次触线就返回
    return None

def _pattern_starts(events, split):                # Part 4 规则：标签序列滑窗比 PATTERN
    labels = ["small" if tx.amount < split else "large" for tx in events]
    n = len(PATTERN)
    return [events[i].ts for i in range(len(events) - n + 1) if tuple(labels[i:i + n]) == PATTERN]

def part3(lines):                                  # 过滤到窗口 → 复用 _totals → 排名
    params, body = _split_params(lines)
    t, k = params["t"], params["K"]
    in_window = (tx for tx in _parse_tx(body) if t - 60 <= tx.ts <= t)
    ranked = sorted(_totals(in_window).items(), key=lambda kv: (-kv[1], kv[0]))
    return [f"{u}: {s}" for u, s in ranked[:k]]
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：窗口我按闭区间 `[ts-60, ts]` 处理，恰好 60 秒前的那笔算在内；时间戳相同的交易按输入顺序处理。如果定义不同我改一行。」
- 写 Part 1 时：「我先把每行解析成一个 `Tx` 记录，用 `defaultdict(int)` 按用户累加，输出时 `sorted` 一下。解析单独一个函数，后面几个 Part 都要用。」
- 写 Part 2 时：「我先按用户分组、每组按时间排序，然后每个用户用一个 `deque` 维护还在窗口内的交易和 running sum，这样每笔交易只进出一次，整体是线性的。」
- 写 Part 3 时：「这一问其实是 Part 1 的规则加一个时间过滤，所以我直接复用 `_totals`。数据量这么小用 `sorted` 就够；如果 K 远小于用户数，可以换成 size-K 的最小堆。」
- 写 Part 4 时：「我把每笔先标成 small/large，再滑一个长度 3 的窗口和 `PATTERN` 比。重叠的匹配我都算，`s,l,s,l,s` 会报两次。」
- 交付时：「四个样例都过了；Part 4 我把模式写成了常量 `PATTERN`，如果要改成四段模式只需要改这个元组。」
- 被追问复杂度时：「Part 2 每笔交易进出 deque 各一次，线性；Part 3 是 `O(n + m log m)`，m 是窗口内的用户数。」

## 7. 常见跑偏（方法层面，3 条）
- **每个 Part 各写一套解析**：Part 2 里 `split(",")`、Part 3 里又 `split(",")`——第三个 Part 开始就在复制粘贴，改一处漏一处。先写好 `_parse_tx` / `_split_params`，后面只调用。
- **全局排序然后在一个大循环里同时管所有用户**：`dict[user] -> deque` 加 `if user not in ...` 判断，逻辑正确但函数 30 行起步、不好单测。先分组，让规则函数只面对一个用户的 list。
- **Part 3 顺手按 `user_id` 排序输出**：前两问都按 id 排，第三问是按排名——写之前把"输出顺序"单独念一遍题面，再写 `sorted` 的 key。

## 8. 同族题 / 延伸
- OA 侧：q13 `account_balance_ledger`（按账户分组、按时间顺序累加）与 Part 1/2 是同一个"分组 + 顺序扫描"骨架；q37 `fraud_rule_timestamps` 是"时间窗口内计数"的另一个皮。
- 其他轮：cd06 `suspicious_users_window` 是 Part 2 的加强版（闭区间 `[t-60, t]` 同一套约定，1 分钟内 >3 笔）；ps04 `data_validation_fraud` 的 Part 3 同样是"每个用户按时间扫描、和历史比对"。
- 延伸思考：把 `_first_crossing` 改成"报告窗口内最大值而非首次触线"只动一个 `return`；把输入改成无限流，`_totals` 与 deque 本来就是在线的，只是被"先读完 stdin"挡住了。
- 练习命令：`python3 loop/mock.py start ps01`
