---
id: uth-python-objects-names-5-assign-order
node: python.objects-names
type: qa
step: 5
---
## Q
**多重赋值的顺序：链表反转那一行**｜Python · CPython 3.14

反转链表常写 `head.next, prev, head = prev, head, head.next`，一行搬完三个指针。为什么目标顺序换成 `head, head.next, prev` 就错了？

## A
**背景。** 一次改好几个名字时，右边的值如果在途中被改掉，结果就乱了。Python 得规定「先算什么、后改什么」。

**结构。** 两步走：先把右边所有表达式从左到右算完，得到一组值；再按从左到右的顺序，把值逐个赋给左边的目标。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 235">
<text x="10" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 → 2 → 3 反转第一步 head 指向节点 1</text>
<text x="10" y="44" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">对</text>
<text x="30" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">目标顺序 head.next, prev, head</text>
<text x="30" y="66" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先算右边  (None, 节点1, 节点2)</text>
<text x="30" y="86" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1) head.next = None (head 还是节点1)</text>
<text x="30" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2) prev = 节点1</text>
<text x="30" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3) head = 节点2</text>
<line x1="10" y1="142" x2="330" y2="142" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="166" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">错</text>
<text x="30" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">目标顺序 head, head.next, prev</text>
<text x="30" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先算右边  (None, 节点1, 节点2)</text>
<text x="30" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1) head = 节点2 (head 已经换了)</text>
<text x="30" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2) head.next = None (改到了节点2)</text>
</svg>
```

**细节。**

- `a, b = b, a` 能交换，因为右边 `(b, a)` 已经算好，之后才赋值。
- 目标里的子表达式（`head.next` 里的 `head`）要等轮到它赋值时才求值。那时 `head` 有没有被前面的目标改掉，决定了改的是哪个节点。
- 文档里的例子：`i, x[i] = 1, 2` 先改 `i`，再用新的 `i` 去找 `x[i]`。

**为什么。** 先算右边，交换就不需要临时变量；代价是目标之间只要互相依赖，顺序就是逻辑的一部分。

**例题：** LC 206 反转链表

给单链表的头节点 `head`，反转链表并返回新的头节点。节点数在 `[0, 5000]` 内。例：`[1,2,3,4,5]` 得 `[5,4,3,2,1]`。

```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next

def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev
```
