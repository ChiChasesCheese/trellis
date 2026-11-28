---
id: lct-learn-list-tree-backtracking-2-2
node: list-tree-backtracking.2.2
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 自顶向下 DFS（先序遍历）**｜学习卡

套路是什么？

## A
**一句话。** 自顶向下 DFS 把答案需要的信息当参数一路往下传（深度、路径和、路径最大值、拼出的数），到边界时结算；访问节点时调用栈正是根到它的路径，参数就是这条路径的摘要。

下图：LC 129 的例子，路径摘要 `acc` 当参数往下传，到叶子结算。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<line x1="101.3" y1="34.6" x2="68.7" y2="70.4" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="119.6" y1="33.8" x2="160.4" y2="71.2" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="53.0" y1="91.0" x2="32.0" y2="124.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="67.0" y1="91.0" x2="88.0" y2="124.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="110" cy="25" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="60" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="170" cy="80" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="25" cy="135" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="25" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="95" cy="135" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="70" y="48" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">acc=4</text>
<text x="155" y="48" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">acc=4</text>
<text x="20" y="104" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">acc=49</text>
<text x="102" y="104" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">acc=49</text>
<text x="25" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">495</text>
<text x="95" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">491</text>
<text x="170" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">40</text>
<text x="220" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">参数往下传</text>
<text x="220" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">acc·10 + val</text>
<text x="220" y="120" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">叶子结算</text>
<text x="220" y="136" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">495 + 491 + 40</text>
<text x="220" y="152" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">= 1026</text>
</svg>

```python
def sum_numbers(root):               # LC 129
    def dfs(node, acc):              # acc：根到父亲拼出的数
        if node is None:
            return 0                 # 空孩子不产生路径
        acc = acc * 10 + node.val    # 先用当前节点更新摘要
        if node.left is None and node.right is None:
            return acc               # 叶子：路径结束，结算
        return dfs(node.left, acc) + dfs(node.right, acc)
    return dfs(root, 0)
def right_side_view(root):           # LC 199：先右后左
    ans = []
    def dfs(node, depth):
        if node is None:
            return
        if depth == len(ans):        # 这一层第一次到达：最右
            ans.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)
    dfs(root, 0)
    return ans
```

**要点。**
- 为什么对？：参数是值传递（整数、元组），左右孩子互不干扰，不需要恢复现场；参数是可变对象时才要撤销，那是回溯。
- 什么时候用叶子当边界？：对象是「根到叶子的路径」（LC 111、112、129）必须在叶子结算；对象是任意节点（LC 104、199、1448）空节点边界就够。
- 怎么和自底向上区分？：这个值能在进入节点前算出来就是自顶向下，必须先看完孩子才知道就是自底向上。
- 各题换什么参数？：104 深度；112 还差多少；1448 路径最大值（`node.val >= mx` 计数）；298 以父亲结尾的连续长度。

**易错点。**
- LC 111、112 在空节点结算：`[2,null,3]` 最小深度是 `2`，空节点边界得 `1`；`[1,2]`、`target = 1` 应得 `False`。
- LC 129 在空节点返回 `acc`：`[1,2]` 应得 `12`，会重复计数得到 `25`。
- LC 1448 用 `>` 代替 `>=`：`[3,3]` 应得 `2`。

**对应题目。** LC 104 二叉树的最大深度、LC 111 二叉树的最小深度、LC 112 路径总和、LC 129 求根节点到叶节点数字之和、LC 199 二叉树的右视图、LC 1448 统计二叉树中好节点的数目、LC 298 二叉树最长连续序列
