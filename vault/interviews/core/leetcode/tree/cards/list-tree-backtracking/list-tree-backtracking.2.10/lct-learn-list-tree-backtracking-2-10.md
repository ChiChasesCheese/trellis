---
id: lct-learn-list-tree-backtracking-2-10
node: list-tree-backtracking.2.10
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 创建二叉树**｜学习卡

套路是什么？

## A
**一句话。** 造树就是把问题切成「一个根 + 左子问题 + 右子问题」，函数返回子树的根让父亲接住；子问题用下标区间 `[l, r)` 表示，根在中序里的位置用哈希表一步查到，左子树大小由中序算出再同步切开其他序列。

下图：先序第一个是根，在中序里查到它的位置就知道左子树大小，再把两个序列同步切开。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="14" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先序</text>
<rect x="60" y="22" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="100" y="22" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="140" y="22" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="180" y="22" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<rect x="220" y="22" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="14" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中序</text>
<rect x="60" y="94" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="100" y="94" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="140" y="94" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<rect x="180" y="94" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="220" y="94" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<line x1="80.0" y1="50" x2="120.0" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="120.0,92.0 113.5,89.5 117.8,85.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="140" y="78" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pos[3] = 1 → size = 1</text>
<line x1="100" y1="16" x2="100" y2="10" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140" y1="16" x2="140" y2="10" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="100" y1="16" x2="140" y2="16" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="120.0" y="12" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左</text>
<line x1="140" y1="16" x2="140" y2="10" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260" y1="16" x2="260" y2="10" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140" y1="16" x2="260" y2="16" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="200.0" y="12" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">右</text>
<line x1="60" y1="124" x2="60" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="100" y1="124" x2="100" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="60" y1="124" x2="100" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="80.0" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左</text>
<line x1="140" y1="124" x2="140" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260" y1="124" x2="260" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140" y1="124" x2="260" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="200.0" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">右</text>
<text x="170" y="156" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个序列按同一个 size 切开，左右各递归一次</text>
</svg>

```python
def build_tree(preorder, inorder):   # LC 105
    pos = {v: i for i, v in enumerate(inorder)}   # 值 -> 下标
    def build(pl, pr, il, ir):       # 先序 [pl,pr)，中序 [il,ir)
        if pl == pr:
            return None              # 空区间：空树
        val = preorder[pl]           # 先序第一个就是根
        k = pos[val]                 # 根在中序里的位置
        size = k - il                # 左子树节点数
        left = build(pl + 1, pl + 1 + size, il, k)
        right = build(pl + 1 + size, pr, k + 1, ir)
        return TreeNode(val, left, right)
    return build(0, len(preorder), 0, len(inorder))

def invert(root):                    # LC 226
    if root is None:
        return None
    left, right = invert(root.left), invert(root.right)
    root.left, root.right = right, left   # 先各自翻好，再互换
    return root
```

**要点。**
- 为什么对？：先序首个是根，它在中序里恰出现一次（值互异），把中序切成左右两段，左段长度就是左子树大小，同一棵子树的先序、中序等长，所以能同步切开；哈希表让每个节点 `O(1)`，切片则 `O(n²)`。
- LC 106、LC 889 怎么改？：106 根是后序区间最后一个，后序切成 `[pl, pl+size)` 和 `[pl+size, pr-1)`；889 先序第二个是左子树的根，在后序里的位置加一就是左子树大小，只剩一个节点要特判。
- LC 108、LC 617 怎么改？：108 取中点当根、左右半递归；617 两树同步走，一边为空就整棵接过来，否则值相加再合并左右。
- LC 2196 怎么改？：没有遍历序列，用字典按需建点、按边连接，根是出现过当父亲却从没当过孩子的值。

**易错点。**
- 区间开闭混用差一：统一 `[l, r)`，空区间是 `l == r`。
- LC 226 先改 `node.left` 再读它：`[1,2,3]` 应得 `[1,3,2]`，错写得 `[1,3,3]`。
- LC 106 从后往前读后序却先建左子树：`[9,3,15,20,7]` 与 `[9,15,7,20,3]` 应得 `[3,9,20,null,null,15,7]`，要先建右子树。

**对应题目。** LC 226 翻转二叉树、LC 617 合并二叉树、LC 108 将有序数组转换为二叉搜索树、LC 2196 根据描述创建二叉树、LC 105 从前序与中序遍历序列构造二叉树、LC 106 从中序与后序遍历序列构造二叉树、LC 889 从前序与后序遍历序列构造二叉树
