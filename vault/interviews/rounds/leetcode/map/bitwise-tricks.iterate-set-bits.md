%% trellis:begin %%
# lowbit 剥离法（t & -t）（iterate-set-bits）
*位运算技巧（bitwise tricks / bitmask）*

当集合是稀疏的（全集范围很大但集合内元素很少）时，遍历集合元素应优先选择 lowbit 剥离法（t & -t），而不是对 0..n-1 逐位扫描。

## Cards (3)
- [[leetcode-c-endlesscheng-caoj45-iterate-set-bits-invariant]]
- [[leetcode-c-endlesscheng-caoj45-iterate-set-bits-recognition]]
- [[leetcode-c-endlesscheng-caoj45-iterate-set-bits-template]]
%% trellis:end %%

## Notes
