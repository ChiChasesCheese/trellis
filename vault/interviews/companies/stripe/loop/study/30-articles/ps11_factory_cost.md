# ps11 · Factory Cost：建厂成本 + 相邻距离惩罚，练的是"先枚举再优化成前缀和/DP"这条 A01 路线

> [!tldr]
> - 这题考的是：一条走廊上建工厂，每对相邻建成的工厂之间按距离查一张分档惩罚表；从"全建"到"最多跳过 1 个（前缀和 argmin）"到"最多跳过 k 个（DP + 回溯重建）"
> - 三步套路：先把"总成本 = 建设成本 + 相邻惩罚"写成能跑的最小版本 → 预计算每一对相邻惩罚，让"跳过某一个"的增量变成 O(1) → 再把"跳 1 个"推广成"跳 k 个"的标准区间 DP
> - 最值得带走的一个模式：**"跳过一个候选点"类的题，不要对每个候选都重新扫一遍**——先把不受影响的部分预计算好（这里是相邻惩罚数组），候选只算"和默认状态的差异"

这题是**重建题**：真实来源只确认了"建厂累计成本 + 相邻惩罚 + 可跳过工厂的 DP"这个主题方向，具体的成本公式、惩罚分档、Part 划分全部是本仓库自拟。**练的是里面的 A01（前缀和+argmin 带 tie-break）、S06（整数分金额）、S13（闭区间 off-by-one）技能，别背格式。**

## 1. 题目在说什么（人话版）
Stripe 要沿一条走廊建结算枢纽机房，候选站点已经按里程从西到东排好序。建一个机房要花钱；两个建成的机房离得太近也要花额外的"冗余对等成本"（按距离查一张分档惩罚表）。可以选择不建某些候选站点来省建设费，但这样它原本的两个邻居会直接相邻，惩罚可能变化（甚至可能落进分档表的"缺口"里变成不合法配置）。

四个 Part 递进：① 全建，只算建设成本；② 全建 + 相邻惩罚；③ 最多跳过 1 个站点，求最低总成本；④ 最多跳过 k 个站点，DP 求解并输出跳过了哪些。

```
f1(0,$100) f2(10,$50) f3(25,$80)，分档 [0,15]=$5 [16,inf]=$2
Part1: TOTAL $230.00                      （只加建设成本）
Part2: TOTAL $240.00                      （dist(f1,f2)=10 和 dist(f2,f3)=15 都落在 [0,15] 档）
```

## 2. 读题：把文字变成模型
- **实体**：工厂（`id, position, build_cost`，走廊顺序=输入顺序）、惩罚分档（`[min_dist, max_dist] -> penalty`，闭区间，`max_dist` 可以是 `inf`）。
- **输入长什么样**：`FACTORIES`/`PENALTIES`/（Part 4 起）`SKIP` 三段，金额是最多两位小数的字符串，必须转成整数分。
- **输出要什么**：`TOTAL $x.xx` 一行，Part 3/4 多一行 `SKIPPED ...`；找不到分档是显式的错误行，不是异常崩溃。
- **状态**：Part 2 起要一个"每对相邻建成工厂的惩罚"数组（`None` 代表落在缺口里）；Part 4 需要 DP 表 `dp[i][s]` 加一个回溯指针数组。
- **一句话建模**：这是一个 **序列上的区间 DP**，Part 3 是它的特例（k=1，可以用前缀和把 O(n) 枚举压成 O(1)）。

> [!note] 为什么 Part 3 要预计算而不是每个候选都重新扫一遍
> 候选是"对每个候选跳过点 j，重新算一遍全部相邻惩罚"（O(n) 每次，总共 O(n²)），或者"先算好原始的 n-1 条相邻惩罚，跳过 j 时只需要减掉它牵涉的最多两条、可能加一条桥接惩罚"（每个候选 O(1)）。后者是 A01（前缀和 + argmin）这一类题的标准动作：**先把"不变的部分"算一次，候选只算"变化量"**。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `PART n`，分发到 `part1..part4`；先写 `parse_money_to_cents`/`fmt_cents`（整数分，拒绝三位小数而不是四舍五入）。
2. **Part 1 最小可用**：`sum(f.build_cost for f in factories)`，格式化输出，零工厂给 `$0.00`。
3. **Part 2 叠加**：写 `_lookup(bands, dist)`（分档按 `min_dist` 排序后再查，输入顺序不可信）；写 `_pair_penalties(factories, bands)` 返回长度 n-1 的列表，`None` 代表缺口；`part2` 遍历这个列表，任意一个 `None` 就报第一个缺口的错误。
4. **Part 3 叠加**：复用 `_pair_penalties`；对每个候选"跳过 j"，只重算被它影响的最多 3 条惩罚（原有两条 + 新的桥接惩罚），其余部分直接用预计算的总和；候选集合是 `{skip-none} ∪ {skip-j}`，用 `(total_cost, rank)` 元组比较自然实现"skip-none 优先、同成本取最小 j"的 tie-break。
5. **Part 4 叠加**：把"跳一个"推广成标准区间 DP：`dp[i][s]` = 最后建成的是 `i`、之前跳过 `s` 个的最小成本；转移时按 tie-break 规则记录"从哪个前驱转移来的"，最后回溯还原被跳过的工厂列表。
6. **收尾**：确认三种错误文案逐字匹配；`SKIPPED` 是走廊顺序、逗号连接、无空格，不是按 id 字符串排序。

## 4. 代码怎么组织
```
parse_money_to_cents(s) -> int ; fmt_cents(c) -> str   # 金额层，整数分，格式化集中一处
_parse_factories(rows) / _parse_bands(rows)             # 解析层
_lookup(bands, dist) -> int | None                      # 分档查表（先排序）
_pair_penalties(factories, bands) -> list[int | None]   # 相邻惩罚，Part2/3/4 共用的预计算
part1(lines) / part2(lines)                             # 全建，Part2 加惩罚求和
part3(lines)                                             # 跳 1 个：枚举候选，O(1) 增量
part4(lines)                                             # 跳 k 个：DP + 回溯
main(stdin, stdout)
```
拆分原则：**"惩罚怎么查"和"怎么枚举/优化跳过方案"分层**。`_pair_penalties` 只依赖工厂列表和分档表，不知道"跳过"这个概念存在；Part 3/4 都是在它的结果上做增量或 DP，面试官追问"如果换成允许跳过任意多个，只用贪心不用 DP 行不行"时，你能明确指出贪心为什么会错（局部最优的跳过选择会互相影响相邻惩罚）。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：分档查表 -> 相邻惩罚预计算 -> Part3 的 O(1) 增量枚举。省略 Part4 的 DP 与解析。
def _lookup(bands, dist):                         # bands 已按 min_dist 排序
    for lo, hi, penalty in bands:
        if lo <= dist <= hi:                      # 闭区间，两端都算在内
            return penalty
    return None                                   # 落在缺口里

def _pair_penalties(factories, bands):
    return [_lookup(bands, factories[i + 1].position - factories[i].position)
            for i in range(len(factories) - 1)]

def part3(factories, bands):
    pairs = _pair_penalties(factories, bands)      # 预计算一次，O(n)
    build_total = sum(f.build_cost for f in factories)
    base_penalty_sum = sum(p for p in pairs if p is not None)
    candidates = []                                # (total_cost, rank) ; rank=-1 表示 skip-none
    if all(p is not None for p in pairs):
        candidates.append((build_total + base_penalty_sum, -1))
    for j, f in enumerate(factories):               # 每个候选只算"变化量"，不重扫整条链
        removed = [p for k, p in enumerate(pairs) if k in (j - 1, j)]
        if any(p is None for p in removed):
            continue                                # 跳过 j 之前就已经缺口的惩罚，本来就不该算作它的
        bridge = None
        if 0 < j < len(factories) - 1:
            bridge = _lookup(bands, factories[j + 1].position - factories[j - 1].position)
            if bridge is None:
                continue                             # 桥接惩罚落进缺口 -> 这个候选无效
        new_penalty_sum = base_penalty_sum - sum(p for p in removed) + (bridge or 0)
        candidates.append((build_total - f.build_cost + new_penalty_sum, j))
    if not candidates:
        return "ERROR no valid configuration"
    total, rank = min(candidates)                    # 元组比较天然实现三级 tie-break
    return total, (None if rank == -1 else factories[rank].factory_id)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「先确认几个边界：距离分档是闭区间两端都算，`inf` 是字面 token；分档表顺序不可信，我会先按 `min_dist` 排序。」
- 写 Part 2 时：「相邻惩罚我抽成一个独立数组，`None` 代表这一对没有匹配的分档——这样报错时我能直接定位到第几对。」
- 写 Part 3 时：「我不想对每个候选跳过点都重新扫一遍全部相邻对，所以先把原始的 n-1 条惩罚算一次，每个候选只需要减去它牵涉的最多两条、可能加一条桥接惩罚——这是前缀和/增量计算的标准套路。」
- 写 Part 4 时：「这本质是区间 DP，状态是'最后建成的是哪个、跳过了几个'；为了输出具体跳过了谁，我在转移时记录前驱，最后回溯一遍。」
- 交付时：「四个 Part 的样例都过了；Part 4 的 tie-break 我按题面的四级优先级实现，构造了一个人工同分场景验证不是随便选中一个合法方案。」

## 7. 常见跑偏（方法层面，3 条）
- **Part 3 对每个候选都重新扫一遍相邻对**：能算对但是 O(n²)，而且往往是从 Part 2 复制一份逻辑改小一点点——读题看到"跳过一个"就该反应过来这是 A01 的前缀和/增量模式，不是"再写一个大循环"。
- **DP 只求最优成本，没有设计怎么回溯方案**：写 `dp[i][s]` 的转移时只存了值没存"从哪来"，到输出 `SKIPPED` 列表时才发现要重构，只能加一层单独的回溯扫描——转移时就该同步维护前驱指针。
- **tie-break 写成"先满足的候选就赢"而不是"按规则显式比较"**：Part 3/4 的多级 tie-break（skip-none 优先、小 j 优先、跳得少的优先）如果不是显式写成排序 key 或元组比较，很容易因为循环遍历顺序偶然"蒙对"了小样例，遇到 hidden test 构造的真实平局就翻车。

## 8. 同族题 / 延伸
- `ps02_shipping_cost_pricing`：同样是"按区间/档位查表 + 排序容错"的模式（那题是运费分档，这题是距离惩罚分档），两题的"表可能乱序、要先排序"这条纪律是共通的，可以互相当复习。
- 同族模式：任何"选一个子集使总成本最小，相邻/相关项之间有额外代价"的题，都是这题 Part 3→4 的推广路径——先想清楚"跳过一个"的边际影响，再决定要不要上 DP。
- 延伸思考：如果允许跳过的不是"至多 k 个"而是"预算 B 元"，DP 的第二维从"跳过数"换成"剩余预算"，转移逻辑基本不变。
- 练习命令：`python3 loop/mock.py start ps11 -m 45`
