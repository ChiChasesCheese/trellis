---
id: lct-learn-list-tree-backtracking-2-3
node: list-tree-backtracking.2.3
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 自底向上 DFS（后序遍历）**｜学习卡

套路是什么？

## A
**一句话。** 自底向上 DFS 先让左右子树各自返回摘要（高度、和、是否相同），再用两个摘要加当前节点合并出自己的摘要往上传；比较两棵树则两个节点同步往下走，在「归」时比较。

下图：LC 110，每个节点在「归」时拿到左右子树的高度，合并后上交；失败用 `-1` 一路上传。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<line x1="100.8" y1="34.2" x2="64.2" y2="70.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="119.2" y1="34.2" x2="155.8" y2="70.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="158.0" y1="91.0" x2="137.0" y2="124.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="172.0" y1="91.0" x2="193.0" y2="124.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="110" cy="25" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="55" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="165" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="165" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<circle cx="130" cy="135" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<circle cx="200" cy="135" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="70" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑1</text>
<text x="150" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑2</text>
<text x="135" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑1</text>
<text x="200" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑1</text>
<text x="55" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0, 0 → 1</text>
<text x="230" y="30" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">左 1、右 2</text>
<text x="230" y="46" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">|1 - 2| ≤ 1</text>
<text x="230" y="62" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回 2 + 1 = 3</text>
<text x="170" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子先算完交上来，父亲合并两份摘要再往上交</text>
</svg>

```python
def is_balanced(root):               # LC 110
    def height(node):                # 返回高度；不平衡返回 -1
        if node is None:
            return 0
        l = height(node.left)
        r = height(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1:
            return -1                # 失败一路上传
        return max(l, r) + 1
    return height(root) != -1
def is_same(a, b):                   # LC 100：两树同步走
    if a is None or b is None:
        return a is b                # 同时为空才相同
    return (a.val == b.val and is_same(a.left, b.left)
            and is_same(a.right, b.right))
def is_mirror(a, b):                 # LC 101：左对右
    if a is None or b is None:
        return a is b
    return (a.val == b.val and is_mirror(a.left, b.right)
            and is_mirror(a.right, b.left))   # 外对外，内对内
```

**要点。**
- 为什么对？：后序保证处理节点时左右子树已有摘要；摘要必须可合并，父亲只靠孩子的摘要和自己的值就能算出自己的（高度 `1 + max(l, r)`，子树和 `l + r + val`）；`-1` 兼表示失败让每个节点只算一次，`O(n)`，分别求高度则是 `O(n²)`。
- 相同、对称、子树怎么改？：相同配 `(左,左)(右,右)`，对称配 `(左,右)(右,左)`；LC 572 外层遍历 `root` 每个节点，内层调 `is_same`。
- LC 508、LC 1339 怎么改？：摘要是子树和，每个节点算出后记入列表或计数器；1339 先求总和 `total`，枚举 `s * (total - s)` 取最大，最后才取模。
- LC 606、LC 1530 怎么改？：606 摘要是字符串，左空右不空要保留 `()`；1530 摘要是长度 `distance + 1` 的数组（距离恰为 `d` 的叶子数），在节点处用前缀和配对左右两边，再整体右移一位上传。

**易错点。**
- LC 110 只比较根的左右高度：`[1,2,2,3,null,null,3,4,null,null,4]` 应得 `False`，根两侧高度相同但左子树内部不平衡。
- 只比较值不比较结构：`[1,2]` 与 `[1,null,2]` 应得 `False`，用 `a is b` 处理一边为空。
- LC 1339 过早取模：先取模再比大小会选错切点，应取最大后再模。

**对应题目。** LC 110 平衡二叉树、LC 606 根据二叉树创建字符串、LC 1339 分裂二叉树的最大乘积、LC 508 出现次数最多的子树元素和、LC 1530 好叶子节点对的数量、LC 100 相同的树、LC 572 另一个树的子树、LC 101 对称二叉树
