---
id: tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-1-signal
node: a.convert-binary-search-tree-to-sorted-doubly-linked-list
type: qa
step: 1
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 11 次 · 最近 2024-01-16（CodeTop）

把一棵二叉搜索树原地转成已排序的循环双向链表：`left` 当前驱，`right` 当后继，首尾相连。返回最小节点。节点数 `[0, 2000]`，`-1000 <= Node.val <= 1000`，值互不相同。例：`root = [4,2,5,1,3]` → 后继方向依次 `1,2,3,4,5`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「二叉**搜索**树」+「**已排序**」→ **中序遍历**（inorder）天然升序。
- 「**原地**」→ 不新建节点，复用 `left` / `right` 指针；遍历的同时改指针，只需要记住**上一个**访问的节点 `prev`。
- 「**循环**」→ 遍历结束后补一条首尾连线。
- 节点数 `2000` 且树可能退化成链：Python 递归深度默认 `1000`，需要**迭代**中序（显式栈）。

**推导链。**
1. 暴力：中序遍历收集所有节点到列表，再逐对连接、首尾相连。`O(n)` 额外空间，不算原地。
2. 浪费在哪：连接只涉及相邻两个节点，不需要整张列表。
3. 洞察：中序访问到 `node` 时，上一个访问的 `prev` 就是它的前驱。令 `prev.right = node`、`node.left = prev`。第一个访问到的节点（`prev` 为空）记为 `first`。
4. 收尾：遍历结束，`prev` 是最后一个节点，`first.left = prev`、`prev.right = first`。`O(n)` 时间，`O(h)` 空间（显式栈）。

**同模式的题**：LC 94 二叉树的中序遍历、LC 230 二叉搜索树中第 K 小的元素、LC 114 二叉树展开为链表、LC 98 验证二叉搜索树。
