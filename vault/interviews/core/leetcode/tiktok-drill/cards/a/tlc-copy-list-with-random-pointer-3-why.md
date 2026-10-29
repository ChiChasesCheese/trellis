---
id: tlc-copy-list-with-random-pointer-3-why
node: a.copy-list-with-random-pointer
type: qa
step: 3
---
## Q
**LC 138 随机链表的复制**｜正确性

为什么要先建完所有新节点再连指针？为什么字典的键必须是节点对象而不是节点的值？如果直接把 `random` 抄过去会出什么问题？

## A
**不变量。** 第一遍结束后，字典里恰好有每个原节点对应的一个新节点；第二遍里，对每个原节点 `x`，新节点 `clone[x]` 的 `next` 是 `clone[x.next]`、`random` 是 `clone[x.random]`。因此新链表的指针关系是原链表关系的逐点翻译，且所有指针都落在新节点上。

**为什么分两遍。** `x.random` 可能指向链表后面还没遍历到的节点。如果边走边建，连 `random` 时目标的新节点可能还不存在；先建完，再连，查表一定有结果。

**为什么键是对象。** 不同的节点可以有相同的值。`[[3,null],[3,0],[3,null]]` 里三个节点的值都是 `3`：若以值为键，三个节点互相覆盖，字典里只剩一个新节点，三个位置的指针会全部指向同一个新节点。

**反例：直接复制 `random`。**
```text
new.random = node.random
```
- 输入 `[[1,1],[2,1]]`：新链表第一个节点的 `random` 就是原链表的第二个节点。
- 检查 `new_head.random is old_head.next` 得到 `True`，正确应该是 `False`（应指向新链表的第二个节点）。
- 修改原链表之后，新链表的 `random` 跟着变化，这就不是深拷贝。

**空指针。** 字典预置 `None -> None`，所以 `random` 为空的节点直接得到 `None`；没有这一项，`clone[node.random]` 会抛 `KeyError`。
