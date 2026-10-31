---
id: tlc-maximum-width-of-binary-tree-4-followup
node: b.maximum-width-of-binary-tree
type: qa
step: 4
---
## Q
**LC 662 二叉树最大宽度**｜追问

面试官接着问：（1）不想用 BFS，能用 DFS 吗？（2）为什么要归零，不归零在 Python 里有什么后果？（3）要求空间 `O(h)` 而不是 `O(w)`？

## A
1. **DFS。** 先序遍历（先左后右）时，每层第一次被访问到的节点一定是该层最左的。用字典 `first` 记每层最左编号，访问节点时宽度 = `idx - first[depth] + 1`：
```python
def width_dfs(root: TreeNode | None) -> int:
    first: dict[int, int] = {}                 # 深度 -> 该层第一个访问到的编号（最左）
    best = 0

    def dfs(node: TreeNode | None, depth: int, idx: int) -> None:
        nonlocal best
        if node is None:
            return
        first.setdefault(depth, idx)           # 只在该层第一次出现时写入
        best = max(best, idx - first[depth] + 1)
        dfs(node.left, depth + 1, 2 * idx)
        dfs(node.right, depth + 1, 2 * idx + 1)

    dfs(root, 0, 0)
    return best
```
空间 `O(h)`（递归栈）加每层一个字典项，也是 `O(h)`，满足第 3 问；但没有归零，编号可能长到 `h` 位的大整数。
2. **不归零的后果。** 深度 3000 的链，编号可达 `2^3000`。Python 整数不会溢出，只是每次运算随位数变慢；在 C++ / Java 里会溢出成负数导致错误，面试官问这个多半是想确认你知道原因。
3. **DFS 的递归深度。** 链状树 3000 层超过默认递归上限，要么调高 `sys.setrecursionlimit`，要么用 BFS。

**Python 提醒**：`dict.setdefault(key, value)` 只在键不存在时写入，且返回现有值；用它记录「第一次出现」比先 `if key not in d` 再赋值少一次查找。
