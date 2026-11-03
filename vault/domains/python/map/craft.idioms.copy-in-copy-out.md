%% trellis:begin %%
# 边界拷贝：进来拷、出去拷（deepcopy / tuple / 回放式 copy）
*编码功力（Coding Craft） / 高级写法（Idioms）*

可变数据穿过边界时拷贝一次：Table.insert 存副本，select 返回副本；Game.copy 用落子序列回放。

**Requires:** [[domains/python/map/model.copy|浅拷贝、深拷贝与切片复制]], [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]

## Cards (5)
1. [[craft-copy-in-copy-out-1-copy-both-sides]]
2. [[craft-copy-in-copy-out-2-shallow-or-deep]]
3. [[craft-copy-in-copy-out-3-copy-by-replay]]
4. [[craft-copy-in-copy-out-4-tuple-snapshot]]
5. [[craft-copy-in-copy-out-5-scales-snapshot-isolation]]
%% trellis:end %%

## Notes
