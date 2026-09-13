%% trellis:begin %%
# 枚举子集的非空子集（enumerate-nonempty-subsets-of-mask）
*位运算技巧（bitwise tricks / bitmask）*

当需要枚举一个具体集合 s（而非全集）的所有非空子集时，应使用 sub = (sub - 1) & s 这一跳转公式，而不是对全集逐个整数枚举再。

## Cards (3)
- [[leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-invariant]]
- [[leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-recognition]]
- [[leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-template]]
%% trellis:end %%

## Notes
