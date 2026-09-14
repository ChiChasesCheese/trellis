# pc17 · Forest Parent Array Delete Node — 重新压缩下标 → 删子树 → 批量同时删除

> TrueInterview 87 题清单第 4 题，2026-06 报告。Part 1 的"孩子怎么处理"是一手预览没给出的重建选择
> （已在下面写明）；Part 2、Part 3 **(reconstructed)**。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 4 行、§3）列出 Snowflake 一轮 Algorithm 题 "Forest Parent Array Delete Node"：用 `parent[i]`
编码一片森林，删除某个节点后返回**重新压缩下标**的合法 parent 数组。预览未说明"被删节点的孩子怎么办"，
这是本题唯一需要面试中主动澄清、也是本 kit 唯一重建的选择点；本 kit 选择"孩子变成根"（最自然、最常见的
教学答案），并在 Part 2/3 里探索另外两种常见追问方向。

## 输入

`parent: list[int]`，长度 `n`；`parent[i] == i` 表示 `i` 是根；否则 `parent[i]` 是 `i` 的父节点下标
（保证是森林，即无环）。

## API 契约（英文签名）

```python
def delete_node_children_become_roots(parent: list[int], delete_index: int) -> list[int]
def delete_subtree(parent: list[int], delete_index: int) -> list[int]
def delete_nodes_batch(parent: list[int], delete_indices: list[int]) -> list[int]
```
`delete_index` / `delete_indices` 中的下标越界 → `ValueError`；Part 3 中出现重复下标 → `ValueError`。

## 规则

删除后必须返回一个**合法**的 parent 数组：长度等于剩余节点数，下标从 0 到 `剩余数-1` 连续无缝
（原来下标大于被删下标的节点，新下标整体减一），且每个存活节点的 parent 指针都要用新下标重写。

### Part 1 — 删单个节点，孩子变成根 **(重建选择，已声明)**

`delete_node_children_become_roots(parent, delete_index)`：删除 `delete_index`；它的**直接孩子**
在结果里变成根（`parent[新下标] == 新下标`）；更深的后代不受影响，只是下标整体重新编号。

### Part 2 — 删整棵子树 **(reconstructed)**

`delete_subtree(parent, delete_index)`：删除 `delete_index` 以及它的**全部后代**（不管多深），
剩余节点重新压缩下标。

### Part 3 — 批量、同时删除多个节点 **(reconstructed)**

`delete_nodes_batch(parent, delete_indices)`：**同时**删除 `delete_indices` 里的所有下标（不是
"依次单个删除再重复 Part 1"——这两者结果一般不同，见下面 worked example）。每个存活节点的新父节点，
是它在**原始树**里最近的、没有被删除的祖先（可能要跳过好几层都被删的祖先）；如果一路往上到原来的根
都被删了，这个节点自己变成根。`delete_indices` 出现重复下标视为非法输入。

## Worked examples（全部由 `solution.py` 实际运行得出）

- 链 `0 ← 1 ← 2 ← 3`（`parent = [0, 0, 1, 2]`）：
  - `delete_node_children_become_roots(parent, 2)` = `[0, 0, 2]`（删掉 2，孩子 3 变成根，新下标 2）
  - `delete_subtree(parent, 1)` = `[0]`（删掉 1、2、3 整条尾巴，只剩根 0）
  - `delete_nodes_batch(parent, [1, 2])` = `[0, 0]`（**关键对比**：3 的新父节点是 0，不是它自己——
    如果先删 2（Part 1 语义，3 立刻变成根），再删 1，3 会一直停留在"根"状态；但批量同时删除时，3 往上
    找最近存活祖先，跳过 2、1，找到还活着的 0，所以 3 的新父节点是 0，不是根）
- `delete_node_children_become_roots([0], 0)` = `[]`（森林只剩空）
- `delete_nodes_batch([0, 1, 1], [])` = `[0, 1, 1]`（空批量 = 恒等，只是照抄原数组）

## `main()` 命令流

```
PART 1                    PART 2                PART 3
0 0 1 2 | 2                0 0 1 2 | 1            0 0 1 2 | 1 2
→ 0 0 2                    → 0                    → 0 0
```
每行格式：`p0 p1 ... p(n-1) | 索引`（Part 1/2 一个索引；Part 3 索引用空格分隔，可以为空）。

## 边界清单

- 只有一个节点的森林，删掉它 → 空数组
- 删除一个叶子（没有孩子/子树为空）
- 删除一个有孩子的根
- Part 2：删除叶子等价于只删自己
- Part 3：空批量（恒等，只重新编号）、批量删光整片森林（返回 `[]`）、批量里出现重复下标（`ValueError`）
- 越界下标（负数、`>= n`）在三个 Part 都要 `ValueError`

## 追问

1. **为什么"孩子变成根"是最自然的选择，而不是"孩子也一起删掉"？** 那正是 Part 2 单独考的另一种语义——
   面试里应该先问清楚要哪一种，本题把两种都做了。
2. **Part 3 为什么不能等价于"循环调用 Part 1"？** 因为 Part 1 每删一个节点都会**立即**把它的孩子提升为根，
   这个提升是不可逆的；批量删除应该看的是原始树结构里"最近的存活祖先"，而不是"删除顺序"，否则结果会依赖于
   一个题目没有规定的删除顺序（不确定性是接口设计的坏味道）。
3. **能不能不重新压缩下标，只是把被删位置标记为空洞？** 可以，且更省事，但题目明确要求"合法的 parent
   数组"，稀疏表示不满足这个契约。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，2026-06 报告，"Forest Parent Array Delete Node"，Algorithm。见
  `../../../catalog/raw/github_repos.md` §2 第 4 行、§3。
- "孩子变成根"是本 kit 对预览未说明部分的重建选择（已声明）；Part 2、Part 3 全部为重建。

## 考什么

S01 树 / 森林的数组编码 · S03 重新编号下标（同类题目：图的删点重标号）· 澄清题意的能力（"孩子怎么办"
必须主动问）· Part 3 考"同时"与"依次"语义差异是否分得清。
