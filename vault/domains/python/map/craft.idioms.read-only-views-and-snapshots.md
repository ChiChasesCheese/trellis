%% trellis:begin %%
# 只读视图与快照返回（MappingProxyType / tuple / frozenset）
*编码功力（Coding Craft） / 高级写法（Idioms）*

内部容器永不外交：对外给 tuple 快照或只读视图，模块级常量表用 MappingProxyType 包住。

**Requires:** [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]], [[domains/python/map/model.copy|浅拷贝、深拷贝与切片复制]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (5)
1. [[craft-read-only-views-and-snapshots-1-dont-hand-out-internals]]
2. [[craft-read-only-views-and-snapshots-2-view-vs-snapshot]]
3. [[craft-read-only-views-and-snapshots-3-constant-tables]]
4. [[craft-read-only-views-and-snapshots-4-across-problems]]
5. [[craft-read-only-views-and-snapshots-5-scales-copy-on-write]]
%% trellis:end %%

## Notes
