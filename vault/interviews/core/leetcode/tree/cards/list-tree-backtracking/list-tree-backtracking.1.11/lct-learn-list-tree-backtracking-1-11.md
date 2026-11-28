---
id: lct-learn-list-tree-backtracking-1-11
node: list-tree-backtracking.1.11
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 这一节本质都是重连指针：先写出每个节点最终的 `next`（`random`、`child`）该指谁，再用辅助手段消掉特例，旋转用「连成环再剪断」，复制用「旧节点 → 新节点」字典，展平用「递归返回尾节点」。

下图：旋转 = 先把尾接回头连成环，再在新尾后面剪断。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="30" y="50" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="47.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="50" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="107.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="150" y="50" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="167.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="210" y="50" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="270" y="50" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="287.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="64" y1="63.0" x2="89" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,63.0 82.7,66.0 82.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="63.0" x2="149" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.0,63.0 142.7,66.0 142.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="244" y1="63.0" x2="269" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="269.0,63.0 262.7,66.0 262.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="184" y1="63" x2="209" y2="63" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="197.0" y="84" text-anchor="middle" font-size="14" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">✂</text>
<path d="M 287 76 C 257 120, 77 120, 47 76" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="47.0,76.0 51.4,81.4 45.6,82.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tail.next = head：连成环</text>
<text x="167.0" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">新尾</text>
<text x="227.0" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新头</text>
<text x="170" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k = 2：从尾走 n - k = 3 步到新尾，在它后面剪断</text>
</svg>

```python
def rotate_right(head, k):           # LC 61
    if not head:
        return head
    n, tail = 1, head
    while tail.next:                 # 数长度，同时找尾
        tail, n = tail.next, n + 1
    tail.next = head                 # 连成环
    p = tail
    for _ in range(n - k % n):       # 走 n - k 步到新尾
        p = p.next
    head, p.next = p.next, None      # 新头紧跟新尾，在此剪断
    return head
```

**要点。**
- 为什么对？：右移 `k` 位就是把最后 `k` 个整体搬到最前，成环后「新头」自然是新尾的下一个，新尾是正数第 `n - k` 个；`k %= n` 是因为转 `n` 次等于没转。
- LC 138 怎么改？：两遍扫描，第一遍给每个旧节点造新节点存进字典（`mp[None] = None` 省判空），第二遍用字典翻译 `next` 和 `random`；必须两遍，因为 `random` 可能指向后面还没造的节点。
- LC 430 怎么改？：`dfs(node)` 展平这一层并**返回尾节点**；遇到 `child` 先递归，把子链整段插在 `node` 与原后继 `nxt` 之间，子链尾接回 `nxt`，同时维护 `prev` 并清空 `child`。

**易错点。**
- 旋转忘了取模：`[1,2]`、`k = 3` 应得 `[2,1]`；空链表要先判空。
- 复制时直接 `new.random = old.random`：新链表仍指向旧节点，不是深拷贝。
- 展平先改 `node.next` 再读 `nxt`，或忘了清 `child` 与改 `prev`：后继丢失或结构仍是多级。

**对应题目。** LC 138 随机链表的复制、LC 430 扁平化多级双向链表、LC 61 旋转链表
