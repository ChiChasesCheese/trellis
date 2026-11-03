%% trellis:begin %%
# __slots__ 与 slots=True：该用在哪、不能用在哪
*编码功力（Coding Craft） / 高级写法（Idioms）*

大量小对象（节点、记录）用 slots 省掉 __dict__；内部可变记录和对外冻结值对象都可以 slots。

**Requires:** [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]], [[domains/python/map/memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]], [[domains/python/map/performance.less-ram|省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构]]

## Cards (5)
1. [[craft-slots-and-memory-1-what-slots-removes]]
2. [[craft-slots-and-memory-2-what-slots-takes-away]]
3. [[craft-slots-and-memory-3-dataclass-slots-recreates-the-class]]
4. [[craft-slots-and-memory-4-mutable-internal-frozen-external]]
5. [[craft-slots-and-memory-5-scales-memory-budget]]
%% trellis:end %%

## Notes
