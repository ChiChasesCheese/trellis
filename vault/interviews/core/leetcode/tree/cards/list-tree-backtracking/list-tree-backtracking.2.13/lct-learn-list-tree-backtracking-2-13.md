---
id: lct-learn-list-tree-backtracking-2-13
node: list-tree-backtracking.2.13
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 二叉树 BFS**｜学习卡

套路是什么？

## A
**一句话。** 用队列做 BFS，每轮开头用 `len(q)` 把本层节点数定死，内层循环恰好弹出这么多个；所有题只是在「处理这一层」的几行里换内容。

下图：BFS 一轮处理一层；每轮开头的 `len(q)` 就是这一层的节点数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="8" y="5" width="210" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="230" y="29" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 0 层：len(q) = 1</text>
<rect x="8" y="55" width="210" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="230" y="79" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 1 层：len(q) = 2</text>
<rect x="8" y="105" width="210" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="230" y="129" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 2 层：len(q) = 3</text>
<line x1="100.8" y1="34.2" x2="69.2" y2="65.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="119.2" y1="34.2" x2="150.8" y2="65.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="54.2" y1="86.6" x2="40.8" y2="113.4" stroke-width="1.2" stroke="currentColor"/>
<line x1="154.2" y1="86.6" x2="140.8" y2="113.4" stroke-width="1.2" stroke="currentColor"/>
<line x1="165.8" y1="86.6" x2="179.2" y2="113.4" stroke-width="1.2" stroke="currentColor"/>
<circle cx="110" cy="25" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="60" cy="75" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="60" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="160" cy="75" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="160" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<circle cx="35" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="35" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="135" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="135" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<circle cx="185" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮先定住 len(q)，恰好弹完这一层；孩子排到队尾</text>
</svg>

```python
def level_order(root):               # LC 102
    ans = []
    q = deque([root] if root else [])
    while q:
        level = []
        for _ in range(len(q)):      # 快照：本层节点数
            node = q.popleft()       # popleft 是 O(1)
            level.append(node.val)
            if node.left:
                q.append(node.left)  # 孩子属于下一层
            if node.right:
                q.append(node.right)
        ans.append(level)            # 汇总换成别的就是别的题
    return ans
```

**要点。**
- 为什么对？：每轮开始时队列恰是第 `d` 层全部节点且从左到右；每个节点的孩子先左后右追加到队尾，下一层不多不少、次序不变；快照保证内层循环吃不到下一层。
- 汇总怎么换？：515 取 `max`，637 取 `sum / 层宽`，1302 取最后一层的和，107 最后整体反转，103 只在写入答案时按层号奇偶反转 `level`（队列本身不反转）。
- LC 958、LC 662 怎么改？：958 空孩子也入队，出队遇到 `None` 后再见到真节点就不是完全二叉树；662 队列存 `(节点, 编号)`，孩子是 `2i`、`2i + 1`，每层先减去首编号防膨胀，宽度是末减首加一。
- LC 863 怎么改？：先 DFS 补父指针，把树当无向图，从 `target` 起 BFS `k` 轮并用 `seen` 防回头，最后一层就是答案。

**易错点。**
- 不拍快照一直弹：`[3,9,20,null,null,15,7]` 得 `[[3,9,20,15,7]]`，应得 `[[3],[9,20],[15,7]]`。
- 层平均值用整除：应得 `[3.0, 14.5, 11.0]`。
- LC 958 只看局部「有右无左」：`[1,2,3,null,null,4]` 应得 `False`，要看整条层序序列。

**对应题目。** LC 863 二叉树中所有距离为 K 的结点、LC 637 二叉树的层平均值（Average of Levels in Binary Tree）、LC 107 二叉树的层序遍历 II、LC 102 二叉树的层序遍历、LC 103 二叉树的锯齿形层序遍历、LC 958 二叉树的完全性检验、LC 1302 层数最深叶子节点的和、LC 515 在每个树行中找最大值、LC 662 二叉树最大宽度
