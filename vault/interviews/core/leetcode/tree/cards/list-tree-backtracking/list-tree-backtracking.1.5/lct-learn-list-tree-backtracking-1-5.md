---
id: lct-learn-list-tree-backtracking-1-5
node: list-tree-backtracking.1.5
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 前后指针**｜学习卡

套路是什么？

## A
**一句话。** 前指针先走 `n` 步，再前后指针同速前进，间距恒为 `n`，前指针到末尾时后指针恰在目标的前驱，不用先数长度。

下图：`right` 先走 `n` 步后两指针同速走；`right` 停在最后一个节点时 `left` 正是目标的前驱。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="8" y="50" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dm</text>
<rect x="62" y="50" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="50" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="170" y="50" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="186.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="224" y="50" width="32" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="240.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="278" y="50" width="32" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="294.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="40" y1="63.0" x2="61" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="61.0,63.0 54.7,66.0 54.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="94" y1="63.0" x2="115" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="115.0,63.0 108.7,66.0 108.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="148" y1="63.0" x2="169" y2="63.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="169.0,63.0 162.7,66.0 162.7,60.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="202" y1="63.0" x2="223" y2="63.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="223.0,63.0 216.7,66.0 216.7,60.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="256" y1="63.0" x2="277" y2="63.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="277.0,63.0 270.7,66.0 270.7,60.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="186.0" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">left</text>
<text x="294.0" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">right</text>
<line x1="186.0" y1="110" x2="186.0" y2="116" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="294.0" y1="110" x2="294.0" y2="116" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="186.0" y1="110" x2="294.0" y2="110" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="240.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">间距恒为 n = 2</text>
<path d="M 186 50 C 211 14, 269 14, 294 50" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="294.0,50.0 289.0,45.1 294.6,43.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="240.0" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">删倒数第 2 个</text>
<text x="60" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">right 先走 n 步</text>
</svg>

```python
def remove_nth_from_end(head, n):    # LC 19
    dummy = ListNode(0, head)        # 哨兵：可能删头
    left = right = dummy
    for _ in range(n):
        right = right.next           # 前指针先走 n 步，间距为 n
    while right.next:                # 停在最后一个节点
        left = left.next
        right = right.next
    left.next = left.next.next       # left 是被删节点的前驱
    return dummy.next
```

**要点。**
- 为什么对？：哨兵算第 `0` 个，链表有 `L` 个节点，倒数第 `n` 个是第 `L - n + 1` 个，前驱是第 `L - n` 个；`right` 在第 `L` 个，`left` 恒落后 `n` 步，正好是前驱。
- 为什么从哨兵出发？：`n = L` 时被删的是头，前驱就是哨兵，不用特判。
- 为什么循环条件写 `right.next`？：要让 `left` 停在前驱而不是目标本身。
- LC 1721 怎么改？：先走 `k - 1` 步得到正数第 `k` 个 `first`，`left` 从头、`right` 从 `first` 同步走到末尾，`left` 就是倒数第 `k` 个。

**易错点。**
- 不加哨兵：`[1]`、`n = 1` 应得 `[]`，没有前驱可改。
- 循环写成 `while right:`：`left` 多走一步停在目标上，删不掉；`[1,2,3]`、`n = 1` 应得 `[1,2]`。
- 先走的步数差一：`[1,2]`、`n = 2` 应得 `[2]`，差一步会删错节点。

**对应题目。** LC 19 删除链表的倒数第 N 个节点
