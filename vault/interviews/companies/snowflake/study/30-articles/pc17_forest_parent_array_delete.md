# pc17 · Forest Parent Array Delete Node：练的是"下标重新压缩 + 同时删除≠依次删除"

> [!tldr]
> - 这题考的是：森林用 `parent[i]` 数组编码，删除节点后要重建一个下标连续、指针合法的新 parent 数组；Part 2、Part 3 的具体语义 **(reconstructed)**
> - 三步套路：先决定"谁存活" → 建 `old_to_new` 双射 → 用双射重写每个存活节点的父指针
> - 最值得带走的一个模式：**批量"同时"删除要看原始结构里最近的存活祖先，不能靠重放单次删除的连续效果**——"依次"和"同时"在有传递性的操作下经常给出不同答案

## 1. 题目在说什么（人话版）

一片森林（多棵树）用一个数组编码：`parent[i] == i` 表示 `i` 是某棵树的根，否则 `parent[i]` 就是
`i` 的父节点下标。现在要删掉某个节点，删完之后剩下的节点要重新编号成 `0..剩余数-1`，不能有空洞，
每个存活节点的父指针也要跟着改成新编号。三个 Part 只是"删除规则"不同：删一个节点（孩子变根）、删
整棵子树、批量同时删多个节点。

小例子（链 `0 ← 1 ← 2 ← 3`，即 `parent = [0, 0, 1, 2]`）：
```
删单个节点 2（孩子变根）: [0, 0, 2]     # 3 原来的父是 2，现在自己变根，新下标 2
删整棵子树（从 1 开始）:   [0]          # 1、2、3 全部消失，只剩根 0
同时删 {1, 2}:            [0, 0]       # 3 的新父是 0（跳过 2、1 两层都被删的祖先）
```

## 2. 读题：把文字变成模型

- **实体**：节点（下标）、父指针、"存活"标记。
- **输入**：一个 `parent` 数组，长度就是节点数；`parent[i]==i` 是根。
- **输出**：重新压缩下标后的合法 `parent` 数组。
- **状态**：谁被删了（一个集合）、旧下标到新下标的映射。
- **一句话建模**：这是一个 **"先选出存活集合，再做一次下标重新编号"** 的问题；三个 Part 的区别只在
  "存活集合怎么算"和"存活节点的新父节点怎么找"。

> [!note] 为什么先决定"存活集合"，再统一重新编号
> 三个 Part 的重新编号逻辑完全一样（`{old: new for new, old in enumerate(remaining)}`），只有
> "谁存活"和"存活节点的新父指针指向谁"不同。把这两件事拆开，Part 2、Part 3 几乎是复制 Part 1 的
> 编号逻辑，只换一小段"怎么判断父指针"的代码。

## 3. 下笔顺序

1. **问清**：被删节点的孩子怎么办？（预览没说，这是本题唯一要主动澄清的语义分支；本 kit 选"孩子
   变根"。）越界下标要不要报错？
2. **Part 1 最小可用**：`remaining = [i for i in range(n) if i != delete_index]`；建
   `old_to_new`；对每个存活节点，若其原父指针恰好是 `delete_index` 就让它指向自己（变根），否则
   翻译成新下标。
3. **Part 2 叠加**：先用 children 邻接表从 `delete_index` 做一次 DFS/BFS 找出整棵子树集合
   `to_remove`，`remaining` 变成排除这整个集合；父指针翻译规则改成"父在 `to_remove` 里也变根"。
4. **Part 3 叠加**：`delete_indices` 去重校验；对每个存活节点，沿**原始** parent 指针向上爬，跳过
   所有在删除集合里的祖先，第一个存活祖先就是新父节点；爬到原根还在删除集合里就自己变根。
5. **收尾**：越界下标三个 Part 都要 `ValueError`；Part 3 重复下标要 `ValueError`；单节点森林删空
   （返回 `[]`）；空批量（恒等）。

## 4. 代码怎么组织

```
_check_index(parent, index)                        # 越界校验，三个 Part 共用
_renumber(remaining) -> old_to_new dict             # 建双射，三个 Part 共用
delete_node_children_become_roots(parent, i)        # Part 1
delete_subtree(parent, i)                           # Part 2：多一步 DFS 收集整棵子树
delete_nodes_batch(parent, indices)                 # Part 3：多一步"沿原始指针找最近存活祖先"
part1 / part2 / part3(lines)                        # 命令行驱动
```
三个删除函数的骨架都是"算存活集合 → `_renumber` → 逐个存活节点翻译父指针"，差异集中在"存活集合
怎么算"和"父指针的判定条件"这两行，面试里可以直接说"这三个函数共享同一个模板"。

## 5. 核心代码（骨架）

```python
def _renumber(remaining):
    return {old: new for new, old in enumerate(remaining)}

# Part 1：孩子变根
def delete_node_children_become_roots(parent, delete_index):
    n = len(parent)
    remaining = [i for i in range(n) if i != delete_index]
    old_to_new = _renumber(remaining)
    result = [0] * len(remaining)
    for old in remaining:
        p = parent[old]
        result[old_to_new[old]] = old_to_new[old] if p == delete_index else old_to_new[p]
    return result

# Part 3：同时删除，找最近存活祖先（核心区别）
def delete_nodes_batch(parent, delete_indices):
    seen = set(delete_indices)  # 已校验无重复
    def nearest_live_ancestor(node):
        prev, cur = node, parent[node]
        while cur in seen and cur != prev:
            prev, cur = cur, parent[cur]
        return None if cur == prev else cur   # 爬到根仍被删 -> 自己变根
    remaining = [i for i in range(len(parent)) if i not in seen]
    old_to_new = _renumber(remaining)
    return [
        old_to_new[old] if (a := nearest_live_ancestor(old)) is None else old_to_new[a]
        for old in remaining
    ]
```

## 6. 面试里怎么说

- 开始前：「我先确认一下：被删节点的直接孩子会变成新的根，对吗？」
- 写 Part 1 时：「我先决定存活集合，再建一个 `old_to_new` 的映射，最后统一翻译父指针——这样
  Part 2、Part 3 只需要换'存活集合怎么算'这一步。」
- 到 Part 3 时：「批量同时删除不能等价于依次调用 Part 1——Part 1 每删一个节点会立刻把孩子提升为
  根，这个提升不可逆；同时删除应该看原始树里'最近的存活祖先'，我用一个 worked example
  （链 `0←1←2←3` 批量删 `{1,2}`）来说明两者结果不同。」
- 交付时：「样例过了；如果时间允许，我会讨论一下能不能不重新压缩下标，只是把删除位置标空洞——但
  题目要求'合法的 parent 数组'，稀疏表示不满足这个契约。」

## 7. 常见跑偏

- 上来就想用递归表示树结构，反而丢了数组下标本身携带的信息（存活集合、越界校验都直接对下标操作
  更简单，不需要先建出一棵"真的树"）。
- Part 3 写成"循环调用 Part 1 三次"——两者语义不同，且结果依赖于一个题目没有规定的删除顺序，这是
  接口设计的坏味道。
- 忘记越界校验和重复下标校验，把这些异常情况留到"以后再说"，导致 Part 3 的 `ValueError` 分支
  没有被覆盖。

## 8. 同族题 / 延伸

- 与 `pc19`（完全二叉树数组的下标单调性）同一类"数组编码的树结构"考法，但 pc19 考的是子树和的
  反向扫描，pc17 考的是删除后的重新编号。
- 与 `pc24`（依赖图上的环检测、DAG 语义）同样强调"某个操作在某种输入形状下没有良定义，要显式报
  错"的诚实表达。
- 练习命令：`python3 loop/mock.py start pc17`

## 索引行

| [pc17_forest_parent_array_delete](pc17_forest_parent_array_delete.md) | `../../loop/rounds/03_phone_coding/pc17_forest_parent_array_delete/` | 电面 coding | 批量"同时"删除要看原始结构里最近的存活祖先，不能靠重放单次删除的连续效果——"依次"和"同时"在有传递性的操作下经常给出不同答案 |
