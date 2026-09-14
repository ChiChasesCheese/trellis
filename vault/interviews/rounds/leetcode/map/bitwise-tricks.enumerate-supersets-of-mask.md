%% trellis:begin %%
# 枚举掩码的超集（enumerate-supersets-of-mask）
*位运算技巧（bitwise tricks / bitmask）*

当需要枚举某个集合 t 的所有超集（在大小为 n 的全集范围内）时，应使用 s = (s + 1) | t 递推公式，而不是对全集所有子集逐一过。

## Cards (3)
- [[leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-invariant]]
- [[leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-recognition]]
- [[leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-template]]
%% trellis:end %%

## Notes
