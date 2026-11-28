---
id: lct-learn-list-tree-backtracking-1-8
node: list-tree-backtracking.1.8
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 合并链表**｜学习卡

套路是什么？

## A
**一句话。** 哨兵加尾指针搭结果链，同时扫两条链，每步决定接哪个节点（有序合并取小的，大数加法取两位之和加进位），最后挂上剩余部分或最后的进位。

下图：哨兵加尾指针搭结果链，每步把两个头里较小的接到 `tail` 后面。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="14" y="34" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a</text>
<rect x="40" y="16" width="30" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="55.0" y="33.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="90" y="16" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="105.0" y="33.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="140" y="16" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="33.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="70" y1="29.0" x2="89" y2="29.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="89.0,29.0 82.7,32.0 82.7,26.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="120" y1="29.0" x2="139" y2="29.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="139.0,29.0 132.7,32.0 132.7,26.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="14" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b</text>
<rect x="40" y="66" width="30" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="55.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="90" y="66" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="105.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<line x1="70" y1="79.0" x2="89" y2="79.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="89.0,79.0 82.7,82.0 82.7,76.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="214" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">比较两个头</text>
<text x="214" y="50" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">接较小的 3</text>
<rect x="40" y="120" width="30" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="55.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dm</text>
<rect x="90" y="120" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="140" y="120" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="190" y="120" width="30" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="205.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">?</text>
<line x1="70" y1="133.0" x2="89" y2="133.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,133.0 82.7,136.0 82.7,130.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="120" y1="133.0" x2="139" y2="133.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="139.0,133.0 132.7,136.0 132.7,130.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="133.0" x2="189" y2="133.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="189.0,133.0 182.7,136.0 182.7,130.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="155.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tail</text>
<line x1="105.0" y1="44" x2="205.0" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="205.0,118.0 198.1,116.6 201.7,111.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="168" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一方空了：剩余整段直接接上</text>
<text x="170" y="184" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大数加法同一骨架：每步接 (和 + 进位) % 10</text>
</svg>

```python
def merge(a, b):                     # LC 21
    dummy = tail = ListNode()
    while a and b:
        if a.val > b.val:
            a, b = b, a              # a 恒为较小者
        tail.next = a
        tail, a = a, a.next
    tail.next = a or b               # 剩余整段直接接上
    return dummy.next

def add(a, b):                       # LC 2，低位在前
    dummy = tail = ListNode()
    carry = 0
    while a or b or carry:           # 最后的进位也要再算一轮
        carry += (a.val if a else 0) + (b.val if b else 0)
        a, b = a and a.next, b and b.next
        carry, d = divmod(carry, 10)
        tail.next = ListNode(d)
        tail = tail.next
    return dummy.next
```

**要点。**
- 为什么对？：每轮开头 `carry` 是 `0` 或 `1`（和至多 `9 + 9 + 1`）；合并时结果链永远是已选出的最小若干个，取链头较小者不会比任何未选节点大。
- LC 445 怎么改？：高位在前，先反转两链，调用 `add`，结果再反转回来（或用两个栈）。
- LC 2816 怎么改？：一次正向扫描，每位 `val * 2 % 10`，后一位 `>= 5` 就加 `1`；最高位 `>= 5` 时补前导 `0`。
- LC 369 怎么改？：进位只沿末尾连续的 `9` 传，找最后一个非 `9` 节点加一，其后清零；哨兵 `0` 兜住全 `9`。

**易错点。**
- 循环条件漏 `carry`：`[5]` + `[5]` 应得 `[0,1]`，漏了得 `[0]`。
- 合并忘了接剩余部分：`[1,2,4]` 与 `[1,3,4,5,6]` 应得 `[1,1,2,3,4,4,5,6]`，漏接丢掉 `5,6`。
- LC 369 全是 `9`：`[9,9]` 应得 `[1,0,0]`，没有哨兵就没地方放那个 `1`。

**对应题目。** LC 2 两数相加、LC 445 两数相加 II、LC 2816 翻倍以链表形式表示的数字、LC 21 合并两个有序链表、LC 369 给单链表加一
