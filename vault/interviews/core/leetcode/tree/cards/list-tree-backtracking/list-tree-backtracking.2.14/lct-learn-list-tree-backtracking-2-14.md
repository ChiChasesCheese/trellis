---
id: lct-learn-list-tree-backtracking-2-14
node: list-tree-backtracking.2.14
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 链表+二叉树**｜学习卡

套路是什么？

## A
**一句话。** 树和链表互转时，按目标顺序遍历树，用一个 `prev` 记住上一个处理的节点，把当前节点和它接起来；要原地改指针时，倒着遍历（右、左、根）可以避免丢失子树。

下图：LC 114 倒着走（右、左、根），每个节点接到已经排好的链表头 `prev` 前面。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<line x1="63.1" y1="33.0" x2="46.9" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="76.9" y1="33.0" x2="93.1" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="35.0" y1="82.0" x2="25.0" y2="106.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="45.0" y1="82.0" x2="55.0" y2="106.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="106.0" y1="81.5" x2="119.0" y2="106.5" stroke-width="1.2" stroke="currentColor"/>
<circle cx="70" cy="22" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="40" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="100" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="20" cy="118" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="60" cy="118" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="125" cy="118" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="125" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<line x1="150" y1="70" x2="175" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="175.0,70.0 168.7,73.0 168.7,67.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180" y="20" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="37.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="222" y="20" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="37.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="264" y="20" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="277.0" y="37.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="206" y1="33.0" x2="221" y2="33.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="221.0,33.0 214.7,36.0 214.7,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="248" y1="33.0" x2="263" y2="33.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="263.0,33.0 256.7,36.0 256.7,30.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="180" y="60" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="222" y="60" width="26" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="264" y="60" width="26" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="277.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<line x1="206" y1="73.0" x2="221" y2="73.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="221.0,73.0 214.7,76.0 214.7,70.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="248" y1="73.0" x2="263" y2="73.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="263.0,73.0 256.7,76.0 256.7,70.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 277 46 L 277 52 L 193 52 L 193 60" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="193.0,60.0 190.0,53.7 196.0,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="240" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">处理顺序（右、左、根）：</text>
<text x="240" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6 5 4 3 2 1</text>
<text x="170" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">每个节点：node.right = prev，node.left = None，prev = node</text>
</svg>

```python
def flatten(root):                   # 展开成前序链表（LC 114）
    prev = None

    def dfs(node):                   # 右、左、根：逆前序
        nonlocal prev
        if node is None:
            return
        dfs(node.right)
        dfs(node.left)
        node.right = prev            # 接到已处理好的链表头前面
        node.left = None
        prev = node                  # 当前节点成为新的链表头

    dfs(root)
```

**要点。**
- 为什么对？：逆前序先处理的是前序序列的末尾，每个节点处理时，它的左右子树都已经被改完，`prev` 恰好是它在前序里的后继。
- LC 426 怎么改？：中序遍历（升序），`prev.right = node; node.left = prev`，记下第一个和最后一个，最后首尾相连。
- LC 116 / 117 怎么改？：逐层处理，同层相邻节点连 `next`；116 是满二叉树，利用上一层的 `next` 链横着走，`O(1)` 空间。

**易错点。**
- 正序展开会丢子树：先把 `right` 改成 `left` 后，原来的右子树没人保存。
- 忘了清 `left`：`node.left = None`，否则链表里还留着左指针。
- 426 漏了首尾相连：循环双向链表要 `first.left = last`、`last.right = first`。

**对应题目。** LC 426 将二叉搜索树转化为排序的双向链表、LC 114 二叉树展开为链表、LC 117 填充每个节点的下一个右侧节点指针 II、LC 116 填充每个节点的下一个右侧节点指针
