---
id: uth-python-sort-1-runs
node: python.sort
type: qa
step: 1
---
## Q
**sort 为什么对有序数据几乎免费**｜Python · CPython 3.14

Python 的 `sort` 是怎么排的？对已经有序、完全倒序、完全随机的 10 万个元素分别调用 `sorted`，比较次数各是多少？

## A
**背景。** 好的通用排序是归并（merge sort）：切成小段各自排好，再两两合并，O(n log n)。但真实数据常常已经部分有序（比如按时间追加的日志），从头开始切、再合并，等于白白重复劳动。

**结构。** Timsort 先扫一遍，找出数据里已有的升序段或严格降序段（run，降序段原地翻转），太短的段用二分插入排序补长，再把相邻的 run 归并。例（示意，真实数据要长得多）：`1 3 5 9 | 8 6 4 | 7 10`：三段，中间一段翻成 `4 6 8`，再合并成 `1 3 4 5 6 7 8 9 10`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="35" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="65" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="95" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="125" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="155" y="22" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="185" y="22" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="215" y="22" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="230" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="245" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="275" y="22" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<line x1="37" y1="58" x2="153" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="37" y1="54" x2="37" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="153" y1="54" x2="153" y2="58" stroke-width="1.5" stroke="currentColor"/>
<text x="95" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升序 run</text>
<line x1="157" y1="58" x2="243" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="157" y1="54" x2="157" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="243" y1="54" x2="243" y2="58" stroke-width="1.5" stroke="currentColor"/>
<text x="200" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">降序 翻转</text>
<line x1="247" y1="58" x2="303" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="247" y1="54" x2="247" y2="58" stroke-width="1.5" stroke="currentColor"/>
<line x1="303" y1="54" x2="303" y2="58" stroke-width="1.5" stroke="currentColor"/>
<text x="275" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升序 run</text>
<line x1="170" y1="88" x2="170" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,112.0 167.0,106.0 173.0,106.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="184" y="105" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">归并 相邻的 run</text>
<rect x="35" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="65" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="95" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="125" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="140" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="155" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="185" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="215" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="230" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="245" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="275" y="120" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="290" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已有的顺序直接利用 不从头切</text>
</svg>
```

**细节。**

- 实测比较次数：有序 99999，倒序 99999，随机约 153 万（`n·log2 n` 约 166 万）。
- `minrun`（run 的最小长度）在 32 到 64 之间，取值让 run 数接近 2 的幂，归并尽量平衡。
- 值全相等也只要 99999 次。

**为什么。** 利用已有的顺序就能把最好情况降到 O(n)；最坏仍是 O(n log n)。

**例题：** LC 148 排序链表

给链表头节点 `head`，把链表按升序排列后返回。链表长度在 `[0, 5 * 10^4]` 内。

```python
def sort_list(head: ListNode | None) -> ListNode | None:
    def merge(a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    if not head or not head.next:
        return head
    slow, fast = head, head.next        # fast 先走一步：偶数长度时 slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None    # 断开成两半
    return merge(sort_list(head), sort_list(mid))
```
