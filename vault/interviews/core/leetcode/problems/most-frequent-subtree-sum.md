---
slug: most-frequent-subtree-sum
---
## Q
**LC 508 出现次数最多的子树元素和**｜Medium

返回二叉树中出现次数最多的子树元素和；并列时全部返回。

## A
**一句话。** 后序 DFS 算出每个节点的子树和并用 `Counter` 计数，取次数等于最大值的所有和。

```python
def find_frequent_tree_sum(root):
    cnt = Counter()

    def dfs(node):
        if not node:
            return 0
        s = node.val + dfs(node.left) + dfs(node.right)
        cnt[s] += 1
        return s

    dfs(root)
    top = max(cnt.values())
    return [s for s, c in cnt.items() if c == top]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `most_common(1)`：并列时漏掉其他值，`[5,2,-3]` 三个和各一次，只返回一个。
- 只给根或叶子计数：每个节点的子树和都要计一次。

**追问。**
- 只要其中最小的众数？：`min(s for s, c in cnt.items() if c == top)`。
- 链状树 `10^4` 层爆栈？：先序入栈得到访问序，倒序处理（孩子先于父亲），子树和存进字典。

**同模式。** LC 563 二叉树的坡度、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 1339 分裂二叉树的最大乘积
