---
id: tlc-create-binary-tree-from-descriptions-0-whole
node: p4.create-binary-tree-from-descriptions
type: qa
---
## Q
**LC 2196 根据描述创建二叉树**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-17（美国面试记录）

给二维整数数组 `descriptions`，其中 `descriptions[i] = [parent_i, child_i, isLeft_i]` 表示 `parent_i` 是 `child_i` 的父节点，二叉树中各节点的值互不相同；`isLeft_i == 1` 表示 `child_i` 是 `parent_i` 的左子节点，`isLeft_i == 0` 表示右子节点。按描述构造二叉树并返回根节点，测试保证能构造出有效的二叉树。`1 <= descriptions.length <= 10^4`，`descriptions[i].length == 3`，`1 <= parent_i, child_i <= 10^5`，`0 <= isLeft_i <= 1`。例：`[[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]` → 层序 `[50,20,80,15,17,19]`；`[[1,2,1],[2,3,0],[3,4,1]]` → `[1,2,null,null,3,4]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用字典 `值 -> TreeNode` 按需创建节点并连边，边的顺序无关紧要；根是「出现过当父节点、却从没当过子节点」的那个值，用集合差一次得到。`O(n)`。

**识别。** 树以「边的列表」给出、顺序任意 → 不能依赖输入顺序递归，要先有节点再连边；「值互不相同」→ 值可以直接当字典键；「保证是有效二叉树」→ 恰好有一个没有父亲的节点，就是根。

**推导。** 暴力：反复扫描描述，只在父节点已经建好时才挂上子节点，直到全部挂完，最坏 `O(n^2)`；或先排序 / 拓扑排序再建，多出 `O(n log n)` → 浪费：这些做法都是为了处理「父亲还没出现」，而节点只需要在第一次被提到时创建 → 洞察：节点按需创建，之后任意顺序连边；根就是入度为 `0` 的点，`parents - children` 一步到位。

```python
def create_binary_tree(descriptions: list[list[int]]) -> TreeNode | None:
    nodes: dict[int, TreeNode] = {}
    parents: set[int] = set()
    children: set[int] = set()
    for parent, child, is_left in descriptions:
        for v in (parent, child):
            if v not in nodes:                          # 第一次见到才创建节点
                nodes[v] = TreeNode(v)
        if is_left:
            nodes[parent].left = nodes[child]
        else:
            nodes[parent].right = nodes[child]
        parents.add(parent)
        children.add(child)
    (root,) = parents - children                        # 只出现过当父、从没当过孩子的就是根
    return nodes[root]
```

运行：示例 1 的根值 `50`，层序 `[50, 20, 80, 15, 17, 19]`；示例 2 的层序 `[1, 2, None, None, 3, 4]`；`[[5,1,0]]` → `[5, None, 1]`；`[[5,1,1],[5,2,0]]` → `[5, 1, 2]`；`10^4` 条描述连成一条左链 → 深度 `10001`，没有递归所以不会溢出。

**复杂度。** 时间 `O(n)`，每条描述常数次字典和集合操作；空间 `O(n)`。

**易错点。**
- 把第一条描述的父节点当根：示例 1 会返回 `20`，层序只有 `[20, 15, 17]`，正确是 `50`。
- 每条描述都重新 `TreeNode(...)`：同一个值被建成多个对象，边连到不同对象上，树断开。示例 2 会得到 `[1, 2]`，正确是 `[1, 2, None, None, 3, 4]`。
- 根的唯一性靠题目保证；`(root,) = ...` 解包在集合元素不是恰好一个时会抛 `ValueError`，正好暴露输入有问题。

**追问。**
- 输入不保证有效：校验 `len(parents - children) == 1`，同一个父节点的同一侧不能出现两次，一个孩子不能有两个父亲。
- 输出层序序列：用 `deque` 做 BFS，缺失的孩子记 `None`，最后去掉末尾的 `None`。
- 描述很多、内存紧：字典里一个值只存一个节点，总内存 `O(节点数)`，与描述条数无关。

**同模式。** LC 105 从前序与中序遍历序列构造二叉树、LC 297 二叉树的序列化与反序列化、LC 1361 验证二叉树、LC 1110 删点成林。
