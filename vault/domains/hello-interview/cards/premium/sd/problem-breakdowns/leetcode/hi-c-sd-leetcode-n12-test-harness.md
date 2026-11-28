---
id: hi-c-sd-leetcode-n12-test-harness
node: sd.problem-breakdowns.leetcode.notes
type: qa
step: 12
---
## Q
**在线判题平台 · 深入四：同一份测试用例跑在任意语言**｜摘要 · 必会

怎样做到每道题只写一份测试用例，却能判任意语言的提交？以二叉树最大深度为例。

## A
- **问题：** 给每道题每种语言各写一套用例没法维护。这个追问的用意，是逼你跳出画框图，讲清楚代码到底怎么跑。
- **做法：** 每道题存一份与语言无关的用例；约定每种数据结构的序列化格式；每种语言各带一个测试框架（harness），负责把序列化输入还原成该语言的对象，调用用户函数，把返回值和同样还原后的期望输出比较。
- **例子：** 最大深度的函数接收 `TreeNode`。用例存成 `{type: "tree", input: [3,9,20,null,null,15,7], output: 3}`，树按层序（BFS）展开成数组。容器内每种语言都带自己的 `TreeNode` 类和还原函数，放在用户代码同目录。
- **要点：** 链表、图等每种结构都要事先约定序列化方式，并保证各语言 harness 都实现。

```python
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr: list) -> Optional[TreeNode]:
    # 层序数组还原二叉树：None 是缺失的孩子，缺失节点的孩子不再占位
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        for side in ("left", "right"):
            if i < len(arr) and arr[i] is not None:
                child = TreeNode(arr[i])
                setattr(node, side, child)
                q.append(child)
            i += 1
    return root
```
