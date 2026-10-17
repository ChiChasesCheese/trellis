---
nodes: [amazon.amz-closest-store]
url: https://docs.python.org/3/library/bisect.html
---
# bisect — Array bisection algorithm（Python 标准库文档）

值得读：英文官方文档，讲 `bisect_left` / `bisect_right` / `insort` 的语义与复杂度：查找是 O(log n)，`insort` 的插入因为要移动元素是 O(n)。本题解的 `SortedListIndex.floor` 与 `ceiling` 就分别建立在 `bisect_right` 与 `bisect_left` 上；文档强调的「左右两侧的区别只在元素已存在时」正是前驱与后继取值不同的原因。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/bisect.html)

## Archived copy
![[src-pydocs-stock-brokerage-clip]]
%% trellis:end %%
