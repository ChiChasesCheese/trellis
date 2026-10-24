---
id: pl-data-arrays-best-practice
node: data.arrays-slices
type: qa
step: 10
---
## Q
资深工程师怎样使用数组、切片和动态数组？通用规则是什么，Go、Java、Rust、Python 各自的具体做法，何时破例？

## A
**通用规则**：
1. **预分配容量**。知道大概元素数就一次分配到位，避免反复扩容复制。
2. **API 边界上明确所有权**：谁拥有、谁能改、返回的是视图还是副本。
3. **不要在持有视图时修改源容器的结构**。
4. **热路径上优先连续存放的原始值**。

按语言：
- **Go**：`make([]T, 0, n)` 预分配；函数返回子切片给外部持有前，用 `slices.Clone` 或三下标切片 `s[a:b:b]` 切断共享；对外 API 返回副本，文档写明是否会修改入参；追加永远 `s = append(s, ...)`。
- **Java**：`new ArrayList<>(n)` 预分配；热路径用原始数组 `int[]`，不用 `List<Integer>`；对外返回 `List.copyOf` 或 `Collections.unmodifiableList`，避免内部列表泄漏。
- **Rust**：参数写 `&[T]` 而非 `&Vec<T>`；`Vec::with_capacity(n)` 预分配；让编译器告诉你哪里有别名冲突，而不是用 `clone()` 绕过。
- **Python**：大批量数值用 `array`、NumPy，而不是 `list`；构造用列表推导；避免在头部 `insert(0, x)`，需要队列就用 `collections.deque`；复制嵌套结构时用 `copy.deepcopy` 或重新构造。

**何时破例**：数据量很小（几十个元素）时，这些优化都不重要，写清楚比快更要紧；原型阶段先写对，再用性能分析工具找热点。
