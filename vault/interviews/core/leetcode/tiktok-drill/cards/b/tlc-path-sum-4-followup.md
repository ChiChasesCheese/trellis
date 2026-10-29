---
id: tlc-path-sum-4-followup
node: b.path-sum
type: qa
step: 4
---
## Q
**LC 112 路径总和**｜追问

面试官接着问：（1）返回所有满足条件的路径（LC 113）？（2）不用显式栈，递归怎么写，会遇到什么问题？（3）路径可以从任意结点开始、到任意结点结束（LC 437）？

## A
1. **所有路径**：DFS 时维护当前路径 `path`，进入结点 `path.append(val)`，叶子且 `remain == 0` 时 `ans.append(path[:])`（必须拷贝），离开结点时 `path.pop()` 回溯。显式栈版本需要把路径一并存进栈元素，或存父指针事后回溯。
2. **递归**：`if not root: return False`；`if not root.left and not root.right: return root.val == target`；`return rec(root.left, target - root.val) or rec(root.right, target - root.val)`。简洁，但最深 `5000` 层时 Python 会 `RecursionError`；`sys.setrecursionlimit` 不稳妥，面试里说明风险并给出迭代版。
3. **任意起点终点（LC 437）**：不再是「根到叶子」，用前缀和哈希表：记录根到当前结点链上的前缀和出现次数，查 `当前和 - target`；见那一题。

**Python 提醒**：`or` 的短路求值让递归版找到一条路径后不再探索另一侧；但 `any(...)` 搭配生成器也可以；不要写成 `rec(l) + rec(r) > 0`，布尔值相加会失去短路。另外调试时别用 `print(root)` 打印 `TreeNode` 对象（没有 `__repr__`），打印 `root.val`。
