---
id: tlc-binary-tree-right-side-view-2-code
node: p2.binary-tree-right-side-view
type: qa
step: 2
---
## Q
**LC 199 二叉树的右视图**｜写出 Python 实现

二叉树根节点 `root`（节点数 `0` 到 `100`，值在 `[-100, 100]`），返回站在树的右侧、从上到下所能看到的节点值。

## A
**思路。** 一层一层处理。`level` 是当前层从左到右的节点列表；每层把最后一个节点的值加入答案，再用列表推导生成下一层——对每个节点按先左后右的顺序取非空孩子。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)                  # 这一层最右的节点
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```

运行：`[1,2,3,null,5,null,4]` → `[1, 3, 4]`，`[1,2,3,4,null,null,null,5]` → `[1, 3, 4, 5]`，`[1,null,3]` → `[1, 3]`，`[]` → `[]`；一条长 `10^5` 的右链也能直接处理，因为没有递归。

**复杂度。** 时间 `O(n)`：每个节点恰好被访问一次；空间 `O(w)`，`w` 为最宽一层的节点数。

**写法要点。** 用「当前层列表」代替 `deque` 加 `for _ in range(len(queue))` 的写法，每层天然分好了组，不用记层大小；双层列表推导 `for node in level for kid in (node.left, node.right) if kid` 读作「对每个节点、对它的每个孩子、孩子非空就收」，顺序先左后右，保证 `level[-1]` 是最右；`[root] if root else []` 一次处理空树。每一层都是新列表，旧层随即被回收。
