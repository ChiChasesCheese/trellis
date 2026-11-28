---
id: lct-learn-list-tree-backtracking-1-9
node: list-tree-backtracking.1.9
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 链表 › 分治**｜学习卡

套路是什么？

## A
**一句话。** 链表没有随机访问，排序用归并：快慢指针找中点并剪断，两半各自递归，再用合并两个有序链表拼回去，`O(n log n)`。

下图：向下是找中点剪断，向上是两两合并有序链表。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="128.0" y="8" width="84" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4 2 1 3</text>
<rect x="71.0" y="54" width="48" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4 2</text>
<rect x="221.0" y="54" width="48" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1 3</text>
<rect x="45.0" y="100" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="115.0" y="100" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="195.0" y="100" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="265.0" y="100" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="71.0" y="146" width="48" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2 4</text>
<rect x="221.0" y="146" width="48" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="245" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1 3</text>
<rect x="128.0" y="183" width="84" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="199" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 2 3 4</text>
<line x1="170" y1="32" x2="95" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="95.0,54.0 100.2,49.3 101.9,55.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="32" x2="245" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="245.0,54.0 238.1,55.1 239.8,49.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="95" y1="78" x2="60" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,100.0 63.8,94.1 67.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="95" y1="78" x2="130" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,100.0 123.0,99.2 126.2,94.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="245" y1="78" x2="210" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,100.0 213.8,94.1 217.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="245" y1="78" x2="280" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,100.0 273.0,99.2 276.2,94.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="60" y1="124" x2="95" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95.0,146.0 88.0,145.2 91.2,140.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="130" y1="124" x2="95" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95.0,146.0 98.8,140.1 102.0,145.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="210" y1="124" x2="245" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="245.0,146.0 238.0,145.2 241.2,140.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="280" y1="124" x2="245" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="245.0,146.0 248.8,140.1 252.0,145.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="95" y1="170" x2="150" y2="183" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150.0,183.0 143.2,184.5 144.5,178.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="245" y1="170" x2="190" y2="183" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,183.0 195.5,178.6 196.8,184.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="300" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快慢指针</text>
<text x="300" y="40" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">找中点剪断</text>
<text x="318" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">merge</text>
</svg>

```python
def merge(a, b):                     # 合并两条有序链表
    dummy = tail = ListNode()
    while a and b:
        if a.val > b.val:
            a, b = b, a              # a 恒为较小者，相等取 a 保持稳定
        tail.next = a
        tail, a = a, a.next
    tail.next = a or b               # 剩余整段直接接上
    return dummy.next

def sort_list(head):                 # LC 148
    if not head or not head.next:
        return head                  # 0 或 1 个节点已有序
    pre, slow, fast = None, head, head
    while fast and fast.next:
        pre, slow = slow, slow.next
        fast = fast.next.next
    pre.next = None                  # 必须剪断，否则递归不收敛
    return merge(sort_list(head), sort_list(slow))
```

**要点。**
- 为什么对？：两半都严格短于 `n`（左 `n // 2`，右 `n - n // 2`，均至少 `1`），递归必终止；`merge` 每次取两个队头中较小者，不会比任何未选节点大。
- 复杂度？：每层扫全部节点一次，共 `log n` 层，`O(n log n)`；额外空间只有递归栈 `O(log n)`，要严格 `O(1)` 改成自底向上（段长 `1, 2, 4…` 两两合并）。
- 合并 K 个有序链表怎么改？：对下标区间 `[l, r)` 二分，不用找中点，积木 `merge` 不变，`O(N log k)`；逐条累加会退化成 `O(kN)`。

**易错点。**
- 忘了剪断：`[2,1]` 不做 `pre.next = None`，左半仍是 `2 -> 1`，递归不收敛；应得 `[1,2]`。
- `merge` 里忘了推进 `tail`：合并 `[1,3]` 与 `[2]` 只剩 `[3]`，应得 `[1,2,3]`。

**对应题目。** LC 148 排序链表
