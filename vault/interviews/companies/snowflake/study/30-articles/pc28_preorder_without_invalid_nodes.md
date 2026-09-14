# pc28 · Preorder Without Invalid Nodes：题面有歧义时，先枚举读法再动笔

> [!tldr]
> - 这题考的是：迭代式（显式栈）前序遍历，外加对题面歧义的主动澄清——"跳过 invalid 节点"没说
>   清楚它的子树该怎么办
> - 三步套路：先写标准迭代前序（显式栈，深度可达 1e5 排除递归）→ 想清楚"跳过"至少有两种合理读
>   法 → 都实现、都测试，用"root 本身 invalid"这个极端例子验证两者的最大分歧
> - 最值得带走的一个模式：**拿到一句有歧义的需求时，先枚举可能的读法，再找一个能让这些读法"分
>   道扬镳"的极端输入去验证理解——而不是选一种自己觉得合理的读法就自信地写下去**

## 1. 题目在说什么（人话版）

`n` 个节点编号 `0..n-1`，`edges` 给出每条 `(parent, child)` 关系，子节点在同一个父节点下的相
对顺序就是 `edges` 里出现的顺序；给一个 `root` 和一个 `invalid` 节点列表，对这棵树做前序遍历，
跳过 invalid 节点。题面预览到此为止——**没说 invalid 节点的子节点算不算数**，这正是本题唯一值
得琢磨的地方。

三行小例子：
```
树：0 -> [1, 2]; 1 -> [3, 4]; 2 -> [5]
invalid = {1}
"透明化"读法：1 被跳过，但它的孩子 3、4 仍然被访问 -> [0, 3, 4, 2, 5]
"整棵剪掉"读法：1 连同 {3, 4} 一起消失          -> [0, 2, 5]
```

## 2. 读题：把文字变成模型

- **实体**：`n` 个编号节点、按 `edges` 顺序建出的 children 表、`invalid` 集合。
- **输入长什么样**：`n: int`、`edges: list[tuple[int,int]]`（顺序即遍历顺序，不能重排）、
  `root: int`、`invalid: list[int]`。
- **输出要什么**：前序遍历得到的节点编号列表；命令流里为空则输出 `-`。
- **状态**：一个显式栈（Python `list`），因为树的深度可以到 `1e5`。
- **一句话建模**：这是一个**带条件跳过的迭代前序遍历**，"跳过"本身有两种合理定义，题面没有
  说，需要都实现。

> [!note] 为什么必须用显式栈
> Python 默认递归深度限制是 1000，C 栈本身也有物理上限；题目明确给出"深度可达 1e5"的链表形树，
> 递归写法在这种输入上会直接 `RecursionError`。用一个 Python `list` 当栈，子节点按逆序 push，
> 保证弹出顺序符合 `edges` 给定的从左到右顺序，遍历深度只受内存限制，不受调用栈限制。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：先写 `_build_children(edges, n)` 把 `edges` 转成 `children: list[list[int]]`
   （按给定顺序，不重排），Part 1/2 共用。
2. **不带 invalid 的标准迭代前序**：栈里放 `root`，每次弹出一个节点就输出，把它的孩子逆序
   push——先用无 invalid 的样例验证这个骨架本身没写错。
3. **提出澄清问题**：「invalid 节点的孩子还要不要访问？」——这是这题真正的考点，不是"能不能写
   出迭代遍历"。
4. **两种读法都实现**：`preorder_skip_invalid_splice`（跳过自己，孩子照常入栈）和
   `preorder_skip_invalid_prune`（跳过自己，孩子也不入栈，`root` 本身 invalid 直接返回空）。
5. **收尾**：用 `invalid` 包含 `root` 的例子验证两个函数的行为在这一点上差异最大；跑一遍深度
   1e5 的链表形树确认没有用到递归。

## 4. 代码怎么组织

```
_build_children(edges, n) -> list[list[int]]        # 按 edges 给定顺序建 children 表，两个 part 共用
preorder_skip_invalid_splice(n, edges, root, invalid)  # Part1：跳过自己，孩子仍入栈（透明化）
preorder_skip_invalid_prune(n, edges, root, invalid)   # Part2：跳过自己，孩子也不入栈（整棵剪掉）
_parse_common(lines) / part1/part2(lines) / main()     # 命令流解析 + 格式化（空结果输出 "-"）
```
两个函数除了"跳过时孩子入不入栈"这一行分支之外，栈操作逻辑几乎一样——面试里可以主动提出"如果
要在同一次遍历里都支持，加一个 `mode` 参数就够了"，展示对代码可扩展性的判断，而不是真的现场重
构成那样（时间有限，先把两个独立函数写对更重要）。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def _build_children(edges, n):
    children = [[] for _ in range(n)]
    for parent, child in edges:
        children[parent].append(child)      # 保持 edges 给定的顺序，不按编号重排
    return children

def preorder_skip_invalid_splice(n, edges, root, invalid):
    children = _build_children(edges, n)
    bad = set(invalid)
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node not in bad:
            out.append(node)                # invalid 节点不输出，但……
        stack.extend(reversed(children[node]))  # ……它的孩子仍然入栈（"透明化"）
    return out

def preorder_skip_invalid_prune(n, edges, root, invalid):
    children = _build_children(edges, n)
    bad = set(invalid)
    if root in bad:
        return []                           # root 本身 invalid：整棵树都被剪掉
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node)
        stack.extend(c for c in reversed(children[node]) if c not in bad)  # invalid 的孩子不入栈
    return out
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「'跳过 invalid 节点'——它的子节点算不算数？如果 invalid 节点本身管理的子结构还有
  效，那应该是'透明化'；如果 invalid 表示这个节点及其管辖范围都被禁用了，那应该是'整棵剪掉'。
  我先把两种都实现，用一个例子对比它们的差异。」
- 写代码时：「深度可能到 1e5，我用显式栈模拟递归，孩子逆序 push 保证弹出顺序符合 `edges` 给定
  的顺序。」
- 交付时：「样例过了；两种读法在 root 本身 invalid 时差异最大，我用这个例子做了交叉验证。」

## 7. 常见跑偏（方法层面，3 条）

- 看到"跳过 invalid 节点"就直接选一种读法脑补写下去，没有意识到这里有歧义——面试官心里想的
  很可能是另一种，这一步没问出来，后面写得再对也是文不对题。
- 用递归写前序遍历，在深度 3000/100000 的链表形树上直接撞上 Python 默认递归深度限制。
- 子节点 push 顺序写反（忘记 `reversed`），导致遍历顺序和 `edges` 给定的从左到右顺序不一致。

## 8. 同族题 / 延伸

- 与 `od02_in_memory_file_system` 同族：都是树/文件系统结构上的遍历题，"迭代 vs 递归"在深度不
  可控时是同一个判断。
- 与 od13 的编码器一样，都用显式栈的迭代先序遍历应对深链输入，是"树的迭代式序列化/遍历"这条技
  能线的两个变体。
- 练习命令：`python3 loop/mock.py start pc28`
