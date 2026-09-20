---
nodes: [problems.components.lru-cache]
url: https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/lru_cache
---
# system-design-primer — object_oriented_design/lru_cache

值得读：Python，但只是一份带 `pass` 桩代码的骨架（`LinkedList.move_to_front`/`append_to_front`/
`remove_from_tail` 都未实现），价值在于把"为什么必须哈希表 + 双向链表缺一不可"讲得很直白：
哈希表单独用查找是 O(1) 但没有顺序，链表单独用有顺序但查找是 O(n)。骨架里没有哨兵节点，
`remove_from_tail` 要单独判断链表是否为空；本文用头尾哨兵消掉了这类边界判断，见"关键设计决策"。
仓库根目录的 `LICENSE.txt` 是 CC BY 4.0。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer/tree/master/solutions/object_oriented_design/lru_cache)

## Archived copy
![[src-donnemartin-lru-cache-clip]]
%% trellis:end %%
