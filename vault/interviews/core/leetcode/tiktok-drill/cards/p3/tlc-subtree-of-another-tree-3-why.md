---
id: tlc-subtree-of-another-tree-3-why
node: p3.subtree-of-another-tree
type: qa
step: 3
---
## Q
**LC 572 另一个树的子树**｜正确性

为什么「根值相等且左右子树分别相同」就能判定两棵树完全相同，而外层递归又为什么能找到所有候选？比较写松（子树不比到叶子）或外层不继续往下找，会分别出什么错？给出具体输入。

## A
**不变量。** `is_same(a, b)` 为真，当且仅当 `a` 与 `b` 的形状和每个位置上的值都相同；它靠两条归纳假设成立：两棵都为空时为真，只有一棵为空时为假；否则要求根值相等，并且左右子树分别满足同样的性质。`is_subtree(root, sub)` 为真，当且仅当 `root` 的某个节点（含 `root` 自己）满足 `is_same(节点, sub)`；外层递归恰好枚举了每个节点一次。

**反例 1：只比较到 `sub` 的节点为止。** 若 `is_same` 在 `b is None` 时直接返回 `True`（只要求 `a` 包含 `b` 的形状）：
- `root = [3,4,5,1,2,null,null,null,null,0]`，`subRoot = [4,1,2]`。
- 节点 `2` 在 `root` 里有一个左孩子 `0`，在 `subRoot` 里没有；`is_same(0, None)` 被判为 `True` → 输出 `True`。
- 正确是 `False`：子树必须连全部后代一起相同。
- 现在的写法在一边为空另一边不空时返回 `False`，得到 `False`。

**反例 2：外层不继续往下找。** 若 `is_subtree` 只检查 `is_same(root, sub_root)`：
- `root = [3,4,5,1,2]`，`subRoot = [4,1,2]`，根 `3` 与 `4` 不同 → 输出 `False`。
- 正确是 `True`：`4` 为根的子树就是 `subRoot`。
- 外层递归到左、右子树之后得到 `True`。
