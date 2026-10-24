---
id: pl-rt-cpython-best-practice
node: runtime.cpython-internals
type: qa
step: 7
---
## Q
理解了 CPython 的解释器设计之后，资深工程师写 Python 时的性能策略是什么？

## A
**顺序：先测量，再按收益从大到小下手。**

1. **剖析**：`cProfile`（函数级）、`py-spy`（采样，可挂到线上进程，不改代码）、`line_profiler`（行级）。多数时候瓶颈集中在很少的函数里。
2. **先换算法和数据结构**：把列表里的 `in` 查找换成 `set`/`dict`，避免嵌套循环的 O(n²)，这比任何微优化大几个数量级。
3. **把循环交给 C**：能用内置函数（`sum`、`min`、`sorted`、`str.join`）、推导式、`itertools`，就不要手写 `for` 加 `append`；数值密集用 NumPy / pandas / Polars 向量化。对比：Python 循环 12 ns / 元素，`sum(list)` 约 2 ns，NumPy 约 0.3 ns（本机一次测量）。
4. **函数内写热代码**：局部变量是数组下标访问，全局变量要走字典查找。热点代码放在函数里，必要时把全局或属性提到局部变量。
5. **保持类型稳定**：自适应解释器基于“同一个位置的类型一直一样”特化。同一变量一会儿 `int` 一会儿 `str`，会不断去特化。
6. **减少对象**：对海量小对象用 `__slots__`、`dataclass(slots=True)`、元组或 NumPy 结构化数组，减少每个实例的字典与对象头开销。
7. **升级 Python 版本**：3.11 起的自适应解释器和后续改进是“免费”的提速；先升级，再谈重写。
8. **最后才下沉**：Cython、Numba、Rust（PyO3）重写热点。边界调用本身有成本，粒度要粗：一次调用处理一大批数据。

什么时候别优化：I/O 为主、CPU 占用不高的服务，Python 的开发效率比省下的 CPU 更值钱。
