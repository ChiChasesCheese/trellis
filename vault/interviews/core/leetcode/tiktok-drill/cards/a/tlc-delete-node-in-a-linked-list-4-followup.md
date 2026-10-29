---
id: tlc-delete-node-in-a-linked-list-4-followup
node: a.delete-node-in-a-linked-list
type: qa
step: 4
---
## Q
**LC 237 删除链表中的节点**｜追问

面试官接着问：（1）如果要删的是尾节点？（2）外部还有代码持有后继节点的引用，这个做法有什么问题？（3）给 `head` 和一个值，删掉值等于它的节点（剑指 Offer 18）？

## A
1. **尾节点**：没有后继可搬，必须有 `head`，从头找到前驱，`prev.next = None`，`O(n)`。把尾节点的值改成特殊值来「假删」违反题意。
2. **外部引用**：真正脱链的是**后继对象**，`node` 对象还留在链表里但值换了。若别处（如 LRU 缓存的哈希表里）存着「值 → 节点」的映射，后继的值仍映射到已脱链的对象，`node` 原来的值映射到一个值已经变了的节点，两处都错。工程里节点身份有意义时，必须拿到前驱真删。
3. **给 `head` 和值**：用哑节点（dummy node）挂在 `head` 前面，删除头节点和删除中间节点走同一条路径。

```python
def delete_by_value(head: ListNode | None, val: int) -> ListNode | None:
    dummy = prev = ListNode(0, head)
    while prev.next and prev.next.val != val:
        prev = prev.next
    if prev.next:                    # 找到了：前驱直接跳过它
        prev.next = prev.next.next
    return dummy.next
```

**Python 提醒**：给参数重新赋值（`node = ...`）只改本地名字，不影响调用方；`del node` 也只是删掉名字，不会删除对象，也不会把它从链表中摘掉。
