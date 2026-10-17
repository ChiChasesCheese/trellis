---
nodes: [amazon.amz-closest-store]
url: https://docs.python.org/3/library/bisect.html
---
# bisect — Array bisection algorithm（Python 标准库文档）

值得读：英文官方文档，讲 `bisect_left` / `bisect_right` / `insort` 的语义与复杂度：查找是 O(log n)，`insort` 因为要移动元素是 O(n)。左右两侧的区别只在元素已存在时，这正是前驱（`floor`）与后继（`ceiling`）取值不同的原因。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/bisect.html)

## Archived copy
![[src-pydocs-stock-brokerage-clip]]
%% trellis:end %%
