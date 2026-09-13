# ps09 · Matching Contacts：把"字段相似度打分"变成一张隐式的图，练的是"建图一次、跑不同深度的遍历"

> [!tldr]
> - 这题考的是：用"字段完全相等按权重累加分数"算出两条联系人记录是否关联，然后在同一张关联图上分别回答 1 跳 / ≤2 跳 / 全连通分量三个问题
> - 三步套路：把"打分规则"抽成一个纯函数 `_score(a, b, weights)` → 用它一次性建出邻接表 `_adjacency` → 三个 Part 只是在这张邻接表上换遍历深度
> - 最值得带走的一个模式：**"两两打分"不等于"两两比较"**——先按字段值分组找候选对，再对候选对算全字段分数，避免 O(n²)

## 1. 题目在说什么（人话版）
Stripe 内部要把可能是同一个人/公司的联系人记录关联起来（客服工单、KYC 提交、拒付申诉各有各的记录，字段写法还可能不一致）。每条记录有 `name/email/company` 三个字段，任意一个字段可能是空字符串（代表"未知"，两个空字段不算相等）。两条记录的相似度分数 = 每个完全相等的非空字段的权重之和；分数达到阈值就算"直接关联"。

三个 Part 只是在这张关联图上问不同深度的问题：
1. 直接关联的（1 跳）；
2. 直接关联 + 它们的直接关联（≤2 跳）；
3. 整个连通分量（任意跳数）。

小例子（`weights: name=0.2, email=0.5, company=0.3, threshold=0.5`）：
```
1: Alice, alice@gmail.com, Stripe     2 与 1：email+company=0.8>=0.5 -> 关联
2: Alicia, alice@gmail.com, Stripe    2 与 3：都不满足；1 与 4：nothing
3: Alice, alice@yahoo.com, Google     -> Part1(1)=[2]  Part3(1)=[2]（分量只有 {1,2}）
4: Bob, bob@gmail.com, Stripe
```

这题是**真题**（PracHub 两份独立报告 + 1point3acres 三方互相印证，规则文本、权重、函数签名均有结构化原文佐证），可以放心背规则细节。

## 2. 读题：把文字变成模型
- **实体**：只有"记录"一种实体（`id, name, email, company`），没有其他领域对象。
- **输入长什么样**：`rows` 是记录列表，`weights` 是字段权重字典，`threshold` 是阈值，`target_user_id` 是要查的目标。
- **输出要什么**：id 列表，**升序、纯字符串序**（不是数值序），不含 target 自身。
- **状态**：核心状态是一张 `dict[id] -> set[id]` 的无向邻接表；Part 2/3 遍历时各自要一个 `visited`/`seen` 集合防止环。
- **一句话建模**：这是一个 **建一次图、按不同跳数遍历** 的问题，图的边定义（打分规则）和遍历深度（BFS 层数）是两个独立的关注点。

> [!note] 为什么选"分组找候选对"而不是两两比较
> 候选是"对所有 `C(n,2)` 记录对都算一次分数"，简单但 O(n²)，字段值大量重复时明显扛不住。换成
> "按每个字段的值分组，组内两两配对作为候选对，再对候选对算一次全字段分数"，重复字段值稀疏时接近线性；
> 即使某个字段值被大量记录共享导致某一组变大，这也是问题本身的性质（那些记录确实两两都要比较），不是实现选择的锅。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 读 stdin → 解析 `weights`/`threshold`/`rows` → 按 `PART n` 分发 → 打印 `",".join(ids)` 或 `"NONE"`。
2. **Part 1 最小可用**：先写 `_validate`（`rows` 转 `id -> row`，重复 id 报错）、`_score`（注意"两边都非空"）、`_adjacency`（先用最简单的两两比较版本），`part1` = 建图 → `adj.get(target, set())` → 排序。用样例自测。
3. **换成分组建图**：`_adjacency` 内部改成"按字段值分组找候选对"，接口不变，`part1` 一行都不改——这一步是给面试官看"先正确、再优化，且优化不影响调用方"的时机。
4. **Part 2 叠加**：拿到 1 跳集合，再并上"每个 1 跳邻居的 1 跳邻居"，`set` 自动去重，减掉 target 自身。
5. **Part 3 叠加**：从 target 做一次 BFS/多源扩散直到访问不到新节点，减掉 target 自身。
6. **收尾**：`target_user_id` 不在 `rows` 里 → `ValueError`；重复 `id` → `ValueError`；确认排序用的是纯字符串序（`"u10" < "u2"`）。

## 4. 代码怎么组织
```
_validate(rows) -> dict[id, row]              # 建索引，顺带查重复 id
_require_target(by_id, target) -> None        # target 不存在就报错
_score(a, b, weights) -> float                # 纯函数：两条记录的相似度分数
_adjacency(by_id, weights, threshold) -> dict # 建图：分组找候选对 -> 逐对打分 -> 无向边
part1/part2/part3(rows, weights, threshold, target) -> list[str]  # 只做"遍历深度"的区别
main(stdin, stdout)                           # 解析协议 + 分发
```
拆分原则：**打分规则、建图、遍历深度三层各管各的**。`_score` 不知道图的存在，`_adjacency` 不知道要遍历几跳，三个 `partN` 除了遍历深度之外完全一样——面试官问"如果分数规则改成任意两个字段都要相等才算匹配"，你能明确说"只改 `_score`，图和三个 Part 都不用动"。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：打分 -> 建图 -> 三种深度的遍历。省略输入解析与两处 ValueError 校验。
def _score(a, b, weights):
    total = 0.0
    for field, weight in weights.items():
        va, vb = a.get(field, ""), b.get(field, "")
        if va and vb and va == vb:          # 两边都非空才算相等；空对空不算匹配
            total += weight
    return total

def _adjacency(by_id, weights, threshold):
    groups = {f: defaultdict(list) for f in weights}
    for rid, row in by_id.items():
        for field in weights:
            if row.get(field, ""):
                groups[field][row[field]].append(rid)
    candidates = set()
    for field_groups in groups.values():
        for ids in field_groups.values():
            candidates.update(combinations(sorted(ids), 2))   # 只比较共享过某个字段值的对
    adj = defaultdict(set)
    for a, b in candidates:
        if _score(by_id[a], by_id[b], weights) >= threshold:
            adj[a].add(b); adj[b].add(a)
    return adj

def part3(rows, weights, threshold, target):                  # 全连通分量：BFS（Part2 是它的"限深"版本）
    adj = _adjacency(_validate(rows), weights, threshold)
    seen, queue = {target}, deque([target])
    while queue:
        node = queue.popleft()
        for nb in adj.get(node, set()):
            if nb not in seen:
                seen.add(nb); queue.append(nb)
    seen.discard(target)
    return sorted(seen)
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：两个空字段不算匹配，对吧？否则'两条记录都没填 company'会被误判成强证据。」
- 写 `_adjacency` 时：「我先用最朴素的两两比较跑通正确性，如果时间允许我会换成按字段值分组找候选对，避免 O(n²)。」
- 写 Part 2 时：「Part 2 就是 Part 1 的邻居集合再并一层邻居的邻居，用 `set` 天然去重，环不会导致重复计数。」
- 写 Part 3 时：「这是标准 BFS/并查集都能做的连通分量问题，但我用 BFS 是因为它和 Part 2 复用同一个 `adj`，改动最小。」
- 交付时：「三个样例都过了；`target` 不存在我用 `ValueError` 而不是空列表，因为'零链接'和'联系人不存在'是两回事。」

## 7. 常见跑偏（方法层面，3 条）
- **一上来就写 O(n²) 两两比较，且不留优化的接口**：把打分逻辑和"怎么找候选对"揉在一个大循环里，后面想优化就要重写整个函数。先把 `_score` 抽成纯函数，`_adjacency` 换实现时调用方一行不改。
- **三个 Part 各写一遍图遍历**：Part 2 抄一遍 Part 1 的建图代码再自己写 BFS，Part 3 又抄一遍——建图只应该做一次，三个 Part 之间唯一的差异应该只是"遍历深度"这一个变量。
- **把"零结果"和"输入本身有问题"混为一谈**：`target_user_id` 不存在时偷懒返回 `[]`，测试要求的是 `ValueError`——读题时就该把"合法但为空"和"非法输入"两种情况分开列出来，不要等写测试时才发现漏了这条。

## 8. 同族题 / 延伸
- `problems/q18_collusion_ring` Part 4（`weighted_links`）是这题的近亲：用的是同一套加权打分规则（甚至默认权重都一样），但只对单个 target 算 1 跳，没有本题 Part 2/3 的多跳要求——两题的评分公式可以互相印证，但不要把 q18 的"只算 1 跳"当成本题的完整规则去用。
- 同族模式：任何"记录去重/实体解析"类题目（fuzzy matching、去重合并）都是"打分函数 + 图 + 遍历深度"这一套，区别只在打分规则本身。
- 延伸思考：如果 `weights` 里的字段值本身很长（比如整段地址），`_score` 换成模糊匹配（编辑距离）也不影响 `_adjacency`/三个 Part 的结构。
- 练习命令：`python3 loop/mock.py start ps09 -m 45`
