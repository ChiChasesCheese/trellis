---
id: lct-learn-list-tree-backtracking-1-4
node: list-tree-backtracking.1.4
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 反转链表**｜学习卡

套路是什么？

## A
**一句话。** 反转链表就是边走边把 `cur` 摘下来接到「已反转部分」前面；局部或分组反转时，用 `p0` 记住段前一个节点，段反转完把两头接回。

下图：上半是组内逐个改向；下半是组反转完后用 `p0` 和组尾 `tail` 接回前后两段。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<text x="10" y="20" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">组内反转中（k = 3）</text>
<rect x="10" y="32" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="27.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="70" y="32" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="32" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="147.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="190" y="32" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="207.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="250" y="32" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="44" y1="45.0" x2="69" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="69.0,45.0 62.7,48.0 62.7,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="224" y1="45.0" x2="249" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="249.0,45.0 242.7,48.0 242.7,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="45" x2="105" y2="45" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="105.0,45.0 111.3,42.0 111.3,48.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="147.0" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pre</text>
<text x="207.0" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">cur</text>
<text x="267.0" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nxt</text>
<text x="10" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">组反转完，把两头接回</text>
<rect x="10" y="118" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="27.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="70" y="118" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="87.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="130" y="118" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="147.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="190" y="118" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="207.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="250" y="118" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="44" y1="131.0" x2="69" y2="131.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="69.0,131.0 62.7,134.0 62.7,128.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="104" y1="131.0" x2="129" y2="131.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="129.0,131.0 122.7,134.0 122.7,128.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="164" y1="131.0" x2="189" y2="131.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="189.0,131.0 182.7,134.0 182.7,128.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="224" y1="131.0" x2="249" y2="131.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="249.0,131.0 242.7,134.0 242.7,128.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="57.0" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p0.next = pre</text>
<text x="237.0" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tail.next = cur</text>
<text x="207.0" y="180" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新 p0 = tail</text>
</svg>

```python
def reverse_k_group(head, k):        # LC 25
    n, p = 0, head
    while p:
        n += 1; p = p.next           # 先数长度，不足 k 的尾组不动
    dummy = ListNode(0, head)        # 哨兵：头会变
    p0, cur = dummy, head
    while n >= k:
        n -= k
        pre = None
        for _ in range(k):
            nxt = cur.next           # 先存后继，否则改向后断链
            cur.next = pre
            pre, cur = cur, nxt
        tail = p0.next               # 原组首，现为组尾
        tail.next = cur              # 组尾接下一组
        p0.next = pre                # 前驱接本组新头
        p0 = tail
    return dummy.next
```

**要点。**
- 为什么对？：每步开头 `pre` 是 `[head, cur)` 的逆序、`cur` 起是未处理部分，两链不相连；摘一个、接一个，不变量保持，每个节点只改一次指针，`O(n)`。
- LC 206、LC 92 怎么改？：206 是整条（`k = n`，不需要哨兵）；92 让 `p0` 先走 `left - 1` 步，只反转 `right - left + 1` 个节点，接法不变。
- LC 24 怎么改？：就是 `k = 2` 的分组反转。
- LC 2074 怎么改？：第 `i` 组名义长 `i`，先数这一组的真实长度，是偶数才反转。

**易错点。**
- 忘了先存后继：`cur.next = pre` 之后后继丢失，链断成一个节点。
- 局部反转漏接两头：`[1,2,3,4,5]`、`2..4` 应得 `[1,4,3,2,5]`，漏掉 `tail.next = cur` 得 `[1,4]`。
- 不先数长度就反转尾组：`[1,2,3,4,5]`、`k = 3` 应得 `[3,2,1,4,5]`，不是 `[3,2,1,5,4]`。

**对应题目。** LC 206 反转链表、LC 92 反转链表 II、LC 24 两两交换链表中的节点、LC 25 K 个一组翻转链表、LC 2074 反转偶数长度组的节点
