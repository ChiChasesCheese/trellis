---
id: lct-learn-list-tree-backtracking-2-16
node: list-tree-backtracking.2.16
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 这一节没有统一模板，每题都是三种遍历之一加一个额外性质：带坐标就先序收集后排序（987），用完全二叉树结构就比左右链层数（222），要暂停继续就显式存栈（173），要序列化就先序加空占位符（297）。

下图：这一节没有统一模板，按题目给的额外性质选三种遍历之一。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<polygon points="96.0,20.0 105.0,7.5 235.0,7.5 244.0,20.0 235.0,32.5 105.0,32.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">题目额外给了什么性质？</text>
<rect x="17.0" y="55.0" width="136" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带坐标（987）</text>
<text x="85" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先序收集坐标，再排序</text>
<rect x="194.6" y="55.0" width="120.9" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">完全二叉树（222）</text>
<text x="255" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">比左右链层数</text>
<rect x="14.1" y="115.0" width="141.8" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要暂停 / 继续（173）</text>
<text x="85" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">显式存栈</text>
<rect x="205.6" y="115.0" width="98.8" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">序列化（297）</text>
<text x="255" y="146.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先序 + 空写 #</text>
<path d="M 96.0 20.0 L 85.0 20.0 L 85.0 55.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,55.0 82.0,48.7 88.0,48.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 244.0 20.0 L 255.0 20.0 L 255.0 55.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,55.0 252.0,48.7 258.0,48.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 85.0 95.0 L 85.0 115.0" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="85.0,115.0 82.0,108.7 88.0,108.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<path d="M 255.0 95.0 L 255.0 115.0" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="255.0,115.0 252.0,108.7 258.0,108.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
</svg>

```python
def serialize(root):                 # LC 297：先序，空写 #
    out = []
    def dfs(node):
        out.append(str(node.val) if node else '#')
        if node:
            dfs(node.left)
            dfs(node.right)
    dfs(root)
    return ','.join(out)

def deserialize(data):
    it = iter(data.split(','))
    def build():
        v = next(it)
        if v == '#':
            return None
        return TreeNode(int(v), build(), build())   # 先左后右
    return build()
```

**要点。**
- 为什么要空占位符？：`[1,2]` 与 `[1,null,2]` 的先序都是 `1,2`，空标记补上结构信息；读回按同样的先序消费，遇 `#` 返回，每段恰好用完。
- LC 987、LC 222 怎么做？：987 `dfs(node, row, col)` 收集 `(col, row, val)`，元组排序恰是列、行、值三个键，再按列切段；222 最左链与最右链层数相等就返回 `2^h - 1`，否则 `1 + 左 + 右`，必有一边是满树，`O(log² n)`。
- LC 173 怎么做？：栈只存左链，`next` 弹出栈顶后把它右孩子的整条左链压栈，摊还 `O(1)`，空间 `O(h)`。
- LC 2673 怎么做？：数组下标 `2i+1`、`2i+2` 找孩子，从 `n // 2 - 1` 到 `0` 自底向上，`ans += abs(l - r)`，`cost[i] += max(l, r)`。

**易错点。**
- 空孩子不写占位符：`[1,2]` 与 `[1,null,2]` 序列化后一样；反序列化先建右后建左会让树左右颠倒。
- LC 987 只按 DFS 顺序分组不排序行：`[1,2,6,null,3,7,null,null,4,null,null,5]` 的第二列应是 `[1,3,7,5]`（行 `0,2,2,4`）。
- LC 173 把中序结果全放进数组：空间 `O(n)`，面试会追问 `O(h)`。

**对应题目。** LC 987 二叉树的垂序遍历、LC 173 二叉搜索树迭代器、LC 222 完全二叉树的节点个数（Count Complete Tree Nodes）、LC 297 二叉树的序列化与反序列化、LC 2673 使二叉树所有路径值相等的最小代价
