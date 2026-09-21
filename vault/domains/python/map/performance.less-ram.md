%% trellis:begin %%
# 省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构
*性能与数据处理*

掌握流式处理代替物化、同质数据用 `array`/NumPy 代替 list 的对象开销、`memoryview` 零拷贝切片，以及概率数据结构（布隆过滤器）的适用场景。

**Requires:** [[domains/python/map/memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]]

## Readings
- [[hpp-05-iterators-generators|High Performance Python 2e · 第 5 章 迭代器与生成器]]
- [[hpp-11-using-less-ram|High Performance Python 2e · 第 11 章 减少内存占用]]
- [[pydocs-array-module|array 模块：紧凑数值数组]]

## Cards (6)
1. [[lessram-array-typecode-sizes]]
2. [[lessram-array-vs-list-layout]]
3. [[lessram-memoryview-equality-gotcha]]
4. [[lessram-memoryview-zero-copy]]
5. [[lessram-slots-inheritance-gotcha]]
6. [[lessram-slots-mechanism]]
%% trellis:end %%

## Notes
