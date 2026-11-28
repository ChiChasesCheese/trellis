---
id: lct-learn-list-tree-backtracking-1-6
node: list-tree-backtracking.1.6
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 快慢指针**｜学习卡

套路是什么？

## A
**一句话。** 快指针每次走两步、慢指针走一步：快指针到头时慢指针在中点；有环则快必从背后追上慢，相遇后头与相遇点同速各走，会合处就是环入口。

下图：`a` 是头到入口、`b` 是入口到相遇点、`c` 是相遇点绕回入口；所以头和相遇点同速走，会合在入口。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="31.0" y1="95.0" x2="59.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="59.0,95.0 52.7,98.0 52.7,92.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="81.0" y1="95.0" x2="127.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="127.0,95.0 120.7,98.0 120.7,92.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="143.5" y1="85.47372055837117" x2="163.49999999999997" y2="50.83270440699364" stroke-width="1.2" stroke="currentColor"/>
<polygon points="163.5,50.8 162.9,57.8 157.7,54.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="179.99999999999997" y1="41.30642496536481" x2="219.99999999999994" y2="41.30642496536478" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220.0,41.3 213.7,44.3 213.7,38.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="236.49999999999994" y1="50.8327044069936" x2="256.5" y2="85.47372055837117" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.5,85.5 250.7,81.5 255.9,78.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256.5" y1="104.52627944162882" x2="236.50000000000003" y2="139.16729559300637" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.5,139.2 237.1,132.2 242.3,135.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220.00000000000003" y1="148.6935750346352" x2="179.99999999999994" y2="148.69357503463516" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,148.7 186.3,145.7 186.3,151.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="163.49999999999994" y1="139.16729559300634" x2="143.5" y2="104.52627944162883" stroke-width="1.2" stroke="currentColor"/>
<polygon points="143.5,104.5 149.3,108.5 144.1,111.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="20" cy="95" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="70" cy="95" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="138" cy="95" r="11" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<circle cx="169.0" cy="41.3" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="231.0" cy="41.3" r="11" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<circle cx="262.0" cy="95.0" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="231.0" cy="148.7" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="169.0" cy="148.7" r="11" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="75" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">head</text>
<text x="134" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">入口</text>
<text x="248.99999999999994" y="33.306424965364776" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">相遇点</text>
<text x="70" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<text x="174" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<text x="230" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">c</text>
<text x="10" y="160" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快走 2(a+b) = a+b+k·环长</text>
<text x="10" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⇒ a = c + (k-1)·环长</text>
</svg>

```python
def middle(head):                    # LC 876
    slow = fast = head
    while fast and fast.next:        # 先判 fast 再判 fast.next
        slow = slow.next
        fast = fast.next.next
    return slow                      # 偶数长度取后一个中点


def cycle_entry(head):               # LC 142
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:             # 先移动再判相遇
            while head is not slow:  # 头与相遇点同速，会合处是入口
                head = head.next
                slow = slow.next
            return head
    return None                      # 快指针走到尽头：无环
```

**要点。**
- 为什么能找到入口？：头到入口 `a`，入口到相遇点 `b`，环长 `c`；相遇时慢走 `a + b`、快走 `2(a + b)`，故 `a + b = k * c`，即 `a = k * c - b`：从相遇点再走 `a` 步正好绕回入口。
- 为什么一定相遇？：进环后快每步比慢多走一格，距离每步减 `1`，不会跳过。
- LC 234、LC 143 怎么改？：用 `middle` 切开，反转后半段，再与前半段逐个比较（234）或交错合并（143，循环条件 `while head2.next`）。
- LC 287 怎么改？：把 `i → nums[i]` 当作链表，`0` 起步，求环入口就是重复数；第一阶段用 `while True` 先走后比。

**易错点。**
- 判环先比较后移动：起点相同，无环链表也会判成有环。
- 偶数长度的中点：`[1,2,3,4,5,6]` 的 `middle` 返回值为 `4` 的节点；`[1,2]` 的回文判断应得 `False`。
- LC 287 第一阶段写 `while slow != fast`：初值都是 `0`，一次不进，直接返回 `0`；`[3,1,3,4,2]` 应得 `3`。

**对应题目。** LC 876 链表的中间结点、LC 234 回文链表、LC 143 重排链表、LC 141 环形链表、LC 142 环形链表 II、LC 287 寻找重复数
