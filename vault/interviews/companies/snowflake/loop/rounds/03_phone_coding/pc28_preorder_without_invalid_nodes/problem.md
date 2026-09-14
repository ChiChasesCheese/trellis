# pc28 · Preorder Without Invalid Nodes — 澄清一个歧义题面，两种读法都实现并测试

> 一手预览给出输入形状（nodes/edges/root/invalid）与"跳过 invalid 节点做前序遍历"，但**没说
> invalid 节点的子树怎么办**——这正是本题唯一有意思的地方，两种读法都标 **(reconstructed)**。

## 背景

TrueInterview 题单预览：`n` 个节点编号 `0..n-1`，`edges = [parent, child]`（子节点按 edges 给
出的顺序排列），一个 `root`，一个 `invalid` 列表；对树做前序遍历，跳过 invalid 节点。预览原文
止步于"跳过 invalid 节点"，没有说清楚——**一个 invalid 节点的子节点算不算数**？这在真实面试里
是候选人必须主动问出来的澄清问题，而不是自己脑补一种读法就开始写代码。本 kit 把两种合理读法都
实现、都测试，题面里显式标出这是"面试里该问的问题"而不是"随便选一种就行"。

## 输入

- `n: int`（节点数，编号 `0..n-1`）
- `edges: list[tuple[int, int]]`：`(parent, child)`，**子节点在同一个父节点下的相对顺序就是
  `edges` 里出现的顺序**（前序遍历要遵守这个顺序，不能重新排序）
- `root: int`
- `invalid: list[int]`

## API 契约（英文签名）

```python
def preorder_skip_invalid_splice(n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]) -> list[int]
def preorder_skip_invalid_prune(n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]) -> list[int]
```

两个函数都**必须是迭代实现**（显式栈），因为树的深度可以到 `1e5`——一棵退化成链表的树用递归前
序遍历会直接撑爆 Python 的递归深度限制（默认 1000）和 C 栈。

## 规则

### Part 1 — 读法一：invalid 节点被"透明化"，子节点顶替它的位置 **(reconstructed 选择 A)**

`preorder_skip_invalid_splice`：invalid 节点本身不出现在输出里，但**它的子节点仍然被遍历**
（就像这个节点被"剪掉"、子节点直接接到它父节点下面一样，只是遍历顺序不变）。适合"invalid 表示
这个节点本身的数据损坏了，但它管理的子结构还是好的"这种业务语义。

### Part 2 — 读法二：invalid 节点连同整棵子树一起剪掉 **(reconstructed 选择 B)**

`preorder_skip_invalid_prune`：invalid 节点和它**整个子树**都不出现在输出里。适合"invalid 表
示这个节点及其管辖范围都被禁用了"这种业务语义（比如权限被吊销的部门，下属部门也一起不可见）。

两种读法在"root 本身是 invalid"时差异最大：读法一仍然遍历 root 的所有子节点（只是不输出 root
自己），读法二整个结果为空。

## Worked examples（全部由 `solution.py` 实际运行得出）

```python
# 树：0 -> [1, 2]; 1 -> [3, 4]; 2 -> [5]
edges = [(0,1), (0,2), (1,3), (1,4), (2,5)]
n = 6
```

**例 1**（无 invalid，标准前序）
```python
preorder_skip_invalid_splice(n, edges, 0, []) -> [0, 1, 3, 4, 2, 5]
```

**例 2**（invalid={1}，读法一：1 被跳过但 3、4 仍被访问）
```python
preorder_skip_invalid_splice(n, edges, 0, [1]) -> [0, 3, 4, 2, 5]
```

**例 3**（invalid={1}，读法二：1 连同子树 {3,4} 一起剪掉）
```python
preorder_skip_invalid_prune(n, edges, 0, [1]) -> [0, 2, 5]
```

**例 4**（root 本身 invalid，两种读法的最大分歧）
```python
preorder_skip_invalid_splice(n, edges, 0, [0]) -> [1, 3, 4, 2, 5]   # root 被跳过，子节点仍遍历
preorder_skip_invalid_prune(n, edges, 0, [0])  -> []                # 整棵树都被剪掉
```

## `main()` 命令流

```
PART 1                          PART 2
NODES 6                         NODES 6
N 5                             N 5
0 1                             0 1
0 2                             0 2
1 3                             1 3
1 4                             1 4
2 5                             2 5
ROOT 0                          ROOT 0
INVALID 1                       INVALID 1
→ 0 3 4 2 5                     → 0 2 5
```

结果为空时输出一行 `-`（例如 `INVALID 0` + Part 2）。

## 边界清单

- `invalid` 为空 → 标准前序遍历（例 1）
- `invalid` 包含 `root` 本身（两种读法结果差异最大，见例 4）
- `invalid` 包含所有节点（读法一：只剩 root 一个都跳过后其它节点仍会被访问到但都不输出 → 空；
  读法二：从 root 开始就整棵剪掉 → 空）
- `invalid` 包含叶子节点（两种读法结果相同：都只是少输出这一个节点）
- 单节点树（`n=1`，`root` 是唯一节点）
- 深度 `1e5` 的链表形树（必须迭代实现，不能递归）
- 子节点顺序必须严格遵守 `edges` 给出的顺序，不能按节点编号重新排序
- `invalid` 里出现不存在的节点编号——本题不特别校验（视为"这个编号反正不会被访问到就无影响"），
  但如果它恰好是某个真实节点的编号，仍然按跳过处理

## 追问

1. **候选人应该怎么问出这个歧义？** 面试里正确的做法是在看到"跳过 invalid 节点"这句话时立刻问
   "invalid 节点的子节点怎么处理"，而不是默认选一种开始写；本 kit 把两种读法都实现，就是在提醒
   "拿到题目先找歧义，不要脑补"。
2. **如果两种语义要在同一次遍历里都支持，怎么设计接口？** 加一个 `mode: Literal["splice",
   "prune"]` 参数，内部按 mode 决定"跳过节点时子节点入不入栈"，两个函数的栈操作逻辑几乎一样，
   只是 `preorder_skip_invalid_prune` 在入栈前多一层"父节点不是 invalid"的过滤。
3. **为什么必须迭代？** Python 默认递归深度 1000（`sys.setrecursionlimit` 可调但 C 栈本身也有
   物理上限），题目给出的"深度到 1e5"直接排除了递归解法，这是这题除了"消歧义"之外唯一的技术考
   点。
4. **如果 `edges` 里出现环（不是树）呢？** 本题假设输入保证是一棵合法的树（`root` 可达所有节
   点，无环）；如果要防御性处理环，需要在栈里额外维护一个 `visited` 集合防止重复访问，题面没有
   要求这个健壮性。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 28 项「Preorder Traversal Without
  Invalid Nodes」，经 `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览的
  输入形状 + "跳过 invalid 节点"一句可见），见 `../../../catalog/raw/github_repos.md` §2 第 28
  行、§3 "pc28"。
- invalid 节点子树的两种处理方式均为重建，已标注 **(reconstructed)**；预览原文没有说清楚，本
  kit 选择"两种读法都实现"而不是猜一种，作为"面试要主动澄清歧义"的示范。

## 考什么

S05（树的迭代式前序遍历，显式栈模拟递归）· 对题面歧义的敏感度（拿到题目先找不确定的地方问清
楚，而不是自己脑补一种然后自信地写下去）· 大深度输入下递归 vs 迭代的选择。
