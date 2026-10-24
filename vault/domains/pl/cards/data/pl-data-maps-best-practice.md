---
id: pl-data-maps-best-practice
node: data.maps-collections
type: qa
step: 10
---
## Q
资深工程师使用映射和集合时遵守哪些规则？Go、Java、Rust、Python、C++ 各怎样落实，何时破例？

## A
**通用规则**：
1. **键用不可变值**；自定义键类型保证 `hash` 与相等一致。
2. **不要依赖语言没承诺的顺序**；需要稳定输出就显式排序，或选有序结构。
3. **并发访问必须有同步**，或用并发安全的结构。
4. **预估大小就预分配**，减少 rehash。
5. **读取区分「不存在」与「零值」**。

按语言：
- **Go**：`make(map[K]V, n)` 预分配；`v, ok := m[k]` 判存在；稳定输出用 `slices.Sorted(maps.Keys(m))`；多 goroutine 共享时用 `sync.Mutex` 加 `map`，读多写少且键集合稳定时才考虑 `sync.Map`；永远不要写 nil map。
- **Java**：键用 `String`、`record` 或枚举；需要顺序时明确选 `LinkedHashMap` 或 `TreeMap`；并发用 `ConcurrentHashMap` 并使用它的原子方法 `computeIfAbsent`、`merge`；用枚举作键就用 `EnumMap`。
- **Rust**：先 `HashMap`，需要排序或范围查询就换 `BTreeMap`；用 `entry` API 避免二次查找；热路径且数据可信时换 `FxHashMap` 之类的快速哈希。
- **C++**：默认 `std::unordered_map`，要顺序或范围查询换 `std::map`；热路径上数据小或已排序时考虑 `flat_map` 或第三方的开放寻址表；用 `try_emplace`/`find` 避免 `operator[]` 的“不存在就插入”副作用（`m[k]` 读一个不存在的键会悄悄插入默认值）；自定义键提供与相等一致的哈希，并对不可信键自行选抗攻击的哈希。
- **Python**：用 `collections.defaultdict`、`Counter` 减少样板；`dict.get(k, default)`；需要有序集合运算可用 `dict.fromkeys` 去重保持顺序；`set` 做成员检测，不要在 `list` 里 `in`。

**何时破例**：确认键集合很小（几个到十几个）时，线性扫描一个小数组可能比哈希表更快更省内存；需要 LRU 等语义时用 `LinkedHashMap` 访问顺序模式或 `functools.lru_cache`，不要手写。
