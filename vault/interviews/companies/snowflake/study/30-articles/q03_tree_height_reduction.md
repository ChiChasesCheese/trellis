# q03 · Tree Height Reduction：三合一树高题，练的是"契约先行"而不是急着写代码

> [!tldr]
> - 这题考的是：三个"压树高"的变体（删叶子输出 id / 剪子树只计数 / 换根求最小高度），三个来源三套不同的编号和深度约定
> - 三步套路：**先把每个 part 自己的编号/深度基准抄一遍写在纸上**（不要脑内假设它们一致）→ Part 1/2 各是一次 BFS 深度 + 一次线性判断 → Part 3 二分高度 + 树形 DP 判可行性
> - 最值得带走的一个模式：**多个 part 共享一个主题但契约不同时，写代码前先把契约表格写出来**——这题最容易失分的地方不是算法难，是把三套约定搞混

## 1. 题目在说什么（人话版）
三个 part 都是"给一棵树，想办法把它的高度/深度压到某个阈值以内"，但操作方式不同：

1. Part 1：只能删非根叶子，问该删哪些节点（输出 id 列表）。节点 1-indexed，根深度=1。
2. Part 2：一刀能删掉一整棵子树，问最少删几刀（只要数量）。节点 0-indexed，根深度=0。
3. Part 3：不删节点，而是把某棵子树整体"挪到根下面"（换根），最多 `max_operations` 次，问能压到的最小高度。
   节点 1-indexed，高度按边数算（只有根时高度=0）。

三行小例子（Part 1）：
```
parent=[1,1,2,2,3,4], k=3
节点7的路径 1→2→4→7，深度4>3 -> 要删
其余节点深度都<=3 -> 答案 [7]
```

## 2. 读题：把文字变成模型
- **实体**：树节点、父子关系、深度/高度。
- **输入长什么样**：`PART <1|2|3>` 决定后续格式；三种格式各不相同（数组长度、0/1-indexed、是否给显式边表）。
- **输出要什么**：Part 1 是 id 列表（升序空格分隔），Part 2/3 是一个整数。
- **状态**：Part 1/2 只需要每个节点的深度（一次 BFS）；Part 3 还需要每个节点的原始子树高度，加上"某个候选高度
  H 下，该子树最少要挪几次"这个递归结果（按 `(节点, 假设深度)` 记忆化）。
- **一句话建模**：Part 1/2 是 **BFS 求深度 + 一次线性规则判断**；Part 3 是 **二分答案高度 + 树形 DP 判可行性**。

> [!note] 为什么选这个数据结构
> 三个 part 都用 `children: dict[int, list[int]]` 存树（不管输入是 parent 数组还是边表，先统一转成孩子表），
> 因为后续的 BFS/DFS 都要"从一个节点走向它的孩子"。Part 3 额外要"每个节点原始子树里最深能走多远"（`height`），
> 因为"要不要挪当前节点"的决策依赖它整棵原始子树能不能不挪就达标。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **契约先行**：拿到题面先写三行注释——"Part 1: 1-indexed，根深度1，parent 长度 n-1"；"Part 2: 0-indexed，
   根深度0，parent[root]=-1"；"Part 3: 1-indexed，高度按边数，边表输入"。这一步不写代码，但能省下后面改错约定的时间。
2. **Part 1 最小可用**：建孩子表 → BFS 求深度（根深度按约定初始化）→ 输出所有深度 `>k` 的非根节点，升序排列。
3. **Part 2 叠加**：同样 BFS 求深度，但判断条件变成"自己 `>k` 且父节点 `<=k`"（顶层去重，见第 7 节）。
4. **Part 3 叠加**：先算每个节点的原始子树高度（迭代后序遍历，不用递归防止链状树栈溢出），再写
   `total_ops(H)`：对每个节点判断"原地够不够 / 换根要花 1 刀+孩子重算 / 留给孩子自己决定"取更便宜的，
   最后在 `[0, original_height]` 上二分找最小可行 H。**H=0 要单独特判**（见第 7 节）。
5. **收尾**：三个 part 各自的输出格式核对一遍（空列表要输出空行，不是省略这一行）。

## 4. 代码怎么组织
```
part1(parent, k) -> list[int]                          # BFS 深度 + 全部超标节点
part2(parent, k) -> int                                # BFS 深度 + 顶层超标点计数
_compute_height(children, root) -> dict[int,int]        # 迭代后序，Part 3 专用
_total_ops(H, root, children, height) -> int            # 树形 DP 判 H 是否可行
part3(tree_nodes, tree_from, tree_to, max_operations)   # 二分 H + _total_ops
main(stdin, stdout)                                      # 按 PART 分派到三套不同的解析格式
```
Part 1/2 结构几乎一样（BFS 深度 + 一次线性判断），但**不合并成一个共享函数**——它们的判断条件本质不同
（"自己超标"vs"自己超标且父节点不超标"），强行复用只会让面试官更难看出你分清楚了两者的区别。Part 3 单独
成一组（高度计算 + DP 判可行 + 二分），因为它是完全不同的算法家族。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def part1(parent, k):                            # 1-indexed，根深度=1，只删非根叶子
    n = len(parent) + 1
    children = {v: [] for v in range(1, n + 1)}
    for i, p in enumerate(parent):
        children[p].append(i + 2)
    depth = {1: 1}
    dq = deque([1])
    while dq:
        v = dq.popleft()
        for c in children[v]:
            depth[c] = depth[v] + 1
            dq.append(c)
    return sorted(v for v in range(1, n + 1) if v != 1 and depth[v] > k)

def part2(parent, k):                            # 0-indexed，根深度=0，一刀删一整棵子树
    n = len(parent)
    children = {v: [] for v in range(n)}
    root = next(v for v, p in enumerate(parent) if p == -1)
    depth = {root: 0}
    dq = deque([root])
    while dq:
        v = dq.popleft()
        for c in children[v]:
            depth[c] = depth[v] + 1
            dq.append(c)
    return sum(1 for v in range(n) if v != root
               and depth[v] > k and depth[parent[v]] <= k)   # 只数"顶层"违规点

def _total_ops(H, root, children, height):       # H=0 特判：换根新深度恒为1，不可能是0
    if H == 0:
        return 0 if not children[root] else float("inf")
    memo = {}
    def fix(v, d):                               # v 现在深度 d，让它整棵原始子树满足 H
        if (v, d) in memo:
            return memo[(v, d)]
        if d + height[v] <= H:
            res = 0
        elif d > H:                              # 自己已超标，必须换根（新深度恒为1）
            res = 1 + sum(fix(c, 1) for c in children[v])
        else:                                     # 现在剪 vs 交给孩子决定，取更便宜的
            cut = 1 + sum(fix(c, 1) for c in children[v])
            keep = sum(fix(c, d + 1) for c in children[v])
            res = min(cut, keep)
        memo[(v, d)] = res
        return res
    return sum(fix(c, 1) for c in children[root])  # 根永远不能被剪
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「这三个 part 来自不同来源，编号和深度基准都不一样，我先把三套约定写成注释，避免写着写着搞混。」
- 写 Part 1 时：「深度沿路径严格递增，所以一个节点该不该删只取决于自己深度是否 `>k`——不存在只删更浅祖先
  就能救它的情况，答案就是所有超标节点的 id，BFS 一遍就够。」
- 写 Part 2 时：「这里一刀删一整棵子树，所以不能把所有超标节点都数一遍，要去重成『顶层』超标点——
  父节点没超标但自己超标的那些，否则会把同一刀重复计数。」
- 写 Part 3 时：「换根有个容易漏掉的边界：挪动后新深度恒为 1，不可能是 0，所以 `H=0` 时只要树里还有别的
  节点就永远不可行，不管预算给多少——我在 `_total_ops` 里把这个当成特判单独处理，而不是让通用递归去处理它。」
- 交付时：「三个样例都过了；Part 3 在链状树上的复杂度我会诚实说明——虽然单次调用看起来是 O(n)，但链状
  树上 `(v,d)` 的组合数会退化到接近 O(n²)，没有找到已知的更优精确算法。」

## 7. 常见跑偏（方法层面，3 条）
- **把三个 part 的编号/深度约定当成一套来写**：Part 1 用了 Part 2 的 0-indexed 或反过来，是这题最常见、
  最容易被隐藏测试抓住的错误，写代码前先把三套约定列成表格。
- **Part 2 把"所有超标节点"都算一遍而不去重**：同一个已超标祖先下的一串超标后代应该只算 1 次（那一刀已经
  把它们都带走了），worked example 里"答案是 1 不是 4"就是在测这个。
- **Part 3 假设换根总能把节点救回合规**：漏掉"新深度恒为 1"这个事实，导致 `H=0` 时错误地判定为可行。

## 8. 同族题 / 延伸
- Part 3 的"二分答案 + 树形 DP 判可行性"是一个通用模式，换皮成"最多砍 K 刀让树宽/树高/子树和满足某约束"
  都是同一套框架。
- 延伸思考：如果 Part 3 反过来问"给定目标高度，求最少操作数"，`total_ops(H)` 本身就是答案，不需要二分。
- 与 OOD 侧 `od01_priority_task_scheduler`/`od05_cron_scheduler` 没有直接关系，但"契约先行"这个方法论
  同样适用于类设计题——先把每个方法的输入输出契约写清楚，再动手实现。
- 练习命令：`python3 loop/mock.py start q03`
