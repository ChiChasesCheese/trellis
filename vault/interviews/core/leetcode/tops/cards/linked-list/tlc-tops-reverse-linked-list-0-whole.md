---
id: tlc-tops-reverse-linked-list-0-whole
node: linked-list.reverse-linked-list
type: qa
---
## Q
**LC 206 反转链表**｜Easy · 全公司热度第 35 名 · Blind 75、NeetCode 150、Hot 100、LeetCode 75

给你单链表的头节点 `head`，请你反转链表，并返回反转后的链表。链表中节点的数目范围是 `[0, 5000]`，`-5000 <= Node.val <= 5000`。进阶：链表可以选用迭代或递归方式完成反转，你能否用两种方法解决？

例：`head = [1,2,3,4,5]` → `[5,4,3,2,1]`；`head = [1,2]` → `[2,1]`；`head = []` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 单链表原地反转（in-place reversal），三个指针 `prev / cur / nxt` 的搬运顺序；它是 LC 25、92、143、234 的子程序。

**一句话。** 一个结点一个结点地摘下来，头插到已反转部分的前面；每一步只改一条 `next`，一趟 `O(n)`、额外空间 `O(1)`。

**识别。** 「反转」「原地」「只能改指针」是信号；`n` 只有 5000，任何线性解都够，难点全在指针改写的先后顺序。

**推导。** 最直观的想法是把值读进数组再倒着写回，但这改的是值不是结构，也要 `O(n)` 空间。要原地做，就把链表看成两段：左边是已经反转好的（头为 `prev`），右边是还没处理的（头为 `head`）。每次把右段的第一个结点接到左段前面，两段边界右移一格，右段空时左段就是答案。

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None                  # 已反转部分的头，初始为空
    while head:
        # 不变式：prev 之后是反转好的前缀，head 之后是还没处理的后缀
        nxt = head.next          # 先存后继：下一行断链后就找不到它了
        head.next = prev         # 反转这一条边
        prev, head = head, nxt   # 两段的边界各向右挪一格
    return prev                  # head 走到 None 时，prev 正好是新的头
```

**运行。** `[1,2,3,4,5]` → `[5, 4, 3, 2, 1]`；`[1,2]` → `[2, 1]`；`[]` → `[]`；`[7]` → `[7]`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 递归写法（进阶要求）：先相信后面 `head.next` 开头的那段已经反转好，再把 `head` 接到它的尾巴上。空间 `O(n)`（调用栈）。
```python
def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:                    # 空链表或只剩一个结点：自己就是反转结果
        return head
    new_head = reverse_list_recursive(head.next)     # 此后 head.next 是这段反转后的尾结点
    head.next.next = head                            # 让尾结点指回 head
    head.next = None                                 # head 成为新的尾，不置空就会成环
    return new_head
```
- 反转链表的一段（LC 92）、每 `k` 个一组（LC 25）：都是这个循环加上「循环次数」和「前后拼接」。

**易错点。**
- 忘记先存 `nxt`：`head.next = prev` 之后原来的后继丢了，`[1,2,3]` 只会得到 `[1]`。
- 递归版漏掉 `head.next = None`：`[1,2]` 变成 `1 ⇄ 2` 的环，遍历输出永远不结束。
- 递归版深度等于 `n`：`n = 5000` 时超过 CPython 默认约 1000 的递归上限，抛 `RecursionError`，需要调大上限或改用迭代版。

**同模式。** LC 92 反转链表 II、LC 25 K 个一组翻转链表、LC 234 回文链表、LC 143 重排链表。
