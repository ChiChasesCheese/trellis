---
id: tlc-lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof-2-code
node: a.lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 22 链表中倒数第k个节点**｜写出 Python 实现

单链表头节点 `head`（长度 `1..100`，值 `0..100`）和整数 `cnt`（`1..长度`）。返回倒数第 `cnt` 个节点。要求一遍扫描、`O(1)` 空间。

## A
**思路。** `fast` 和 `slow` 都从头出发。`fast` 先走 `cnt` 步，两者之间隔 `cnt` 个节点。然后一起前进，直到 `fast` 变成 `None`，此时 `slow` 就是倒数第 `cnt` 个节点。

```python
def training_plan(head: ListNode | None, cnt: int) -> ListNode | None:
    fast = slow = head
    for _ in range(cnt):                         # fast 先走 cnt 步，与 slow 拉开 cnt 的间距
        if fast is None:                         # cnt 比链表还长：不存在倒数第 cnt 个
            return None
        fast = fast.next
    while fast:                                  # 同步前进，fast 走出链表时 slow 恰在倒数第 cnt 个
        fast, slow = fast.next, slow.next
    return slow
```

**运行。** `[2,4,7,8], 1` → 值为 `8` 的节点；`[2,4,7,8], 4` → 值为 `2` 的头节点；`[5], 1` → 值为 `5` 的节点；`[1,2], 3` → `None`。

**复杂度。** 时间 `O(n)`：`fast` 恰好走 `n` 步；空间 `O(1)`，只有两个指针。

**写法要点。** `fast = slow = head` 链式赋值让两个指针同起点；`for _ in range(cnt)` 用 `_` 表示不使用的循环变量；元组赋值 `fast, slow = fast.next, slow.next` 同时前进，右边先整体求值，不会先改 `fast` 再用它；`while fast:` 用节点的真值判断是否走出链表；返回类型是 `ListNode | None`（Python 3.10+ 的联合写法）。
