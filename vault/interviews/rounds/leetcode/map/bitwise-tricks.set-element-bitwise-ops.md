%% trellis:begin %%
# 位运算判断集合成员（set-element-bitwise-ops）
*位运算技巧（bitwise tricks / bitmask）*

当需要判断整数 i 是否属于位压缩集合 s 时，应使用 (s >> i) & 1 而不是遍历集合逐一比较。
%% trellis:end %%

## Notes
