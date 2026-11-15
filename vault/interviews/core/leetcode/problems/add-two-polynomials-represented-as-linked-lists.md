---
slug: add-two-polynomials-represented-as-linked-lists
---
## Q
**LC 1634 求两个多项式链表的和**｜Medium

多项式用链表表示，节点有 `coefficient`、`power`，按 `power` 严格降序。给两个多项式链表，返回它们的和，系数为 `0` 的项不要保留。

## A
**一句话。** 像合并两个有序链表：指数大的先走，指数相等就系数相加，和为 `0` 时丢掉。

```python
def add_poly(a, b):
    dummy = tail = PolyNode()
    while a or b:
        if b is None or (a and a.power > b.power):
            c, p, a = a.coefficient, a.power, a.next
        elif a is None or b.power > a.power:
            c, p, b = b.coefficient, b.power, b.next
        else:                            # 指数相同，合并
            c = a.coefficient + b.coefficient
            p = a.power
            a, b = a.next, b.next
        if c != 0:
            tail.next = PolyNode(c, p)
            tail = tail.next
    return dummy.next
```

**复杂度。** 时间 `O(m + n)`，空间 `O(1)`（不计结果链表）。

**易错点。**
- 指数相同时直接拼两项：同类项要合并成一项。
- 合并后系数为 `0` 还接上去：多项式里不能留零项。

**追问。**
- 要原地复用节点？：把 `PolyNode(c, p)` 换成改写 `a` 的节点并摘下，指针处理多一步。

**同模式。** LC 21 合并两个有序链表、LC 617 合并二叉树、LC 2 两数相加、LC 138 随机链表的复制
