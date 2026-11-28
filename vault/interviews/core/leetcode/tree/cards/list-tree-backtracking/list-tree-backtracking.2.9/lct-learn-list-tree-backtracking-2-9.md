---
id: lct-learn-list-tree-backtracking-2-9
node: list-tree-backtracking.2.9
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 二叉搜索树**｜学习卡

套路是什么？

## A
**一句话。** 二叉搜索树（BST）的中序遍历是严格递增序列，所以 BST 题都是有序序列题：把中序写成生成器，相邻、第 `k` 个、逆序全按有序数组来做。

下图：BST 的中序就是一个有序数组；所有 BST 题都按有序数组做。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<line x1="158.7" y1="28.4" x2="111.3" y2="55.6" stroke-width="1.2" stroke="currentColor"/>
<line x1="181.3" y1="28.4" x2="228.7" y2="55.6" stroke-width="1.2" stroke="currentColor"/>
<line x1="91.4" y1="71.8" x2="73.6" y2="92.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="108.6" y1="71.8" x2="126.4" y2="92.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="231.4" y1="71.8" x2="213.6" y2="92.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="248.6" y1="71.8" x2="266.4" y2="92.2" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="22" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="100" cy="62" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="240" cy="62" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<circle cx="65" cy="102" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="135" cy="102" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="205" cy="102" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="275" cy="102" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<line x1="65" y1="115" x2="65" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="50" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="65" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="100" y1="75" x2="100" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="85" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="100" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="135" y1="115" x2="135" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="120" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="135" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="170" y1="35" x2="170" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="155" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="205" y1="115" x2="205" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="190" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="205" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="240" y1="75" x2="240" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="225" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="240" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<line x1="275" y1="115" x2="275" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<rect x="260" y="140" width="30" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="275" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="170" y="182" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">中序遍历 = 把节点竖直投影到一条线上：严格递增</text>
</svg>

```python
def walk(node):                      # 中序生成节点（BST 即升序）
    if node:
        yield from walk(node.left)
        yield node
        yield from walk(node.right)
def adj(root):                       # 相邻两个节点
    return pairwise(walk(root))

def is_valid_bst(root):              # LC 98：严格递增
    return all(a.val < b.val for a, b in adj(root))
def min_diff(root):                  # LC 530 / 783：只看相邻
    return min(b.val - a.val for a, b in adj(root))
def kth_smallest(root, k):           # LC 230：取到第 k 个就停
    return next(islice(walk(root), k - 1, None)).val

def recover_tree(root):              # LC 99：交换了两个节点
    bad = [(a, b) for a, b in adj(root) if a.val > b.val]
    x, y = bad[0][0], bad[-1][1]     # 首个逆序的大者，末个逆序的小者
    x.val, y.val = y.val, x.val
```

**要点。**
- 为什么对？：BST 要求整个左子树 `<` 根 `<` 整个右子树，中序先左后根再右，输出必升序；反之中序严格递增的树一定是 BST，所以验证只比相邻，不用逐层传区间。
- 为什么恢复取首个逆序的大者和末个逆序的小者？：相邻节点被交换时只有一处逆序，两个都在其中；不相邻时有两处逆序，被换到前面的大值在第一处，被换到后面的小值在最后一处。
- LC 255 怎么改？：不建树，用单调递减栈加下界 `low`：遇到比栈顶大的数就弹出所有更小的，最后弹出的成为 `low`，之后任何数 `< low` 即非法。

**易错点。**
- LC 98 只比较父子，或允许相等（`[2,2,2]` 应得 `False`）：`[5,1,4,null,null,3,6]` 应得 `False`，`3` 在 `5` 的右子树里却小于 `5`。
- LC 230 把计数放在左子树之前（变成先序）：`[3,1,4,null,2]`、`k = 1` 应得 `1`，不是 `3`。
- LC 255 弹栈后不更新下界：`[5,2,6,1,3]` 应得 `False`，`[5,2,1,3,6]` 应得 `True`。

**对应题目。** LC 230 二叉搜索树中第 K 小的元素、LC 530 二叉搜索树的最小绝对差、LC 783 二叉搜索树节点最小距离、LC 99 恢复二叉搜索树、LC 98 验证二叉搜索树、LC 255 验证前序遍历序列二叉搜索树
