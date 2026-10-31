---
id: tlc-populating-next-right-pointers-in-each-node-3-why
node: p4.populating-next-right-pointers-in-each-node
type: qa
step: 3
---
## Q
**LC 116 填充每个节点的下一个右侧节点指针**｜正确性

为什么处理第 `d` 层时，沿 `next` 链走就一定可用？为什么不需要判断孩子是否存在？给出漏掉跨父亲连线、循环条件写错时的具体输入。

## A
**不变量。** 处理第 `d` 层之前，第 `0` 到第 `d` 层的所有 `next` 都已经连好。第 `0` 层只有根，`next` 为 `None`，天然成立。处理第 `d` 层时，沿 `next` 链能恰好遍历这一层的所有节点；对每个节点，连下一层的两类边：同父亲的 `left -> right`，以及跨父亲的 `right -> 右邻居.left`。下一层的任意相邻两个节点，要么是同一个父亲的左右孩子，要么是相邻父亲的右孩子和左孩子，两类边覆盖了全部相邻对；最右边的节点的 `next` 保持初始的 `None`。所以第 `d + 1` 层也连好了。

**为什么不判空。** 完美二叉树里，同一层要么全是叶子、要么全有两个孩子；外层条件 `leftmost.left` 保证本层不是叶子层，所以 `node.left`、`node.right` 对本层所有节点都存在；右邻居存在时它同样有左孩子。

**反例一：漏掉跨父亲的连线。** `[1,2,3,4,5,6,7]`，只写 `node.left.next = node.right`：
- 第 `2` 层只有 `4 -> 5`、`6 -> 7`，`5.next`、`7.next` 都是 `None`。
- 正确是 `4 -> 5 -> 6 -> 7`，即 `5.next = 6`。

**反例二：外层循环写成 `while leftmost:`。** 树 `[1,2,3]`：
- 第一轮连好 `2.next = 3`，`leftmost` 变成 `2`；第二轮 `2` 是叶子，`node.left` 是 `None`，执行 `node.left.next = ...` 抛 `AttributeError`。
- 外层条件必须检查 `leftmost.left`，在叶子层停止。
