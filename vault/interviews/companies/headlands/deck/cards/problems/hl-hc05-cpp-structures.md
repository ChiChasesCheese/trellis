---
id: hl-hc05-cpp-structures
node: problems.hc05-market-order-book
type: qa
step: 20
---
## Q
C++ 订单簿的数据结构选型是什么？和 Java 版逐项对应怎样，迭代器稳定性为什么重要？

## A
| 需求 | C++ 结构 | 复杂度 |
|---|---|---|
| 取最好价位，价位按价格有序 | `std::map<价格, 价位>`（红黑树） | `begin()` O(1)，`rbegin()` O(log L)；插入删除 O(log L) |
| 同价位按到达顺序排队，撤单要从队伍中间拿掉 | `std::list<订单>` + 保存的迭代器 | 队尾插入、任意位置删除、移到队尾都 O(1) |
| 撤单 / 改量只给 `id` | `std::unordered_map<id, Locator>` | 平均 O(1)；`Locator` 存价位和订单节点的迭代器 |

对应 Java：`TreeMap` ↔ `std::map`；`LinkedHashMap` ↔ `list` + `unordered_map` 里存迭代器，`splice` 移到队尾；`sealed + record + switch` ↔ `std::variant + std::visit(overloaded{…})`；`addExact` ↔ `__builtin_add_overflow / mul_overflow`；`Long.parseLong` ↔ `std::from_chars` + 检查是否读完；`TradeSink` 接口 ↔ 模板参数（内联）；`numberOfTrailingZeros` ↔ `std::countr_zero`（`<bit>`）。

**迭代器稳定性**：`map` / `list` 是节点式容器，插入、删除别的元素不会移动已有节点，迭代器一直指向同一个节点；`vector` 增长时会搬家，迭代器、引用全部悬空。所以 `Locator` 可以存 `map/list` 的迭代器而不能存 `vector` 的。

**含迭代器的类不能拷贝**：拷贝出来的 `by_id_` 里迭代器仍指向原对象的节点，原对象销毁后悬空，对拷贝撤单会改坏别人的数据。移动是安全的（节点不动）；所以删除拷贝构造而保留移动。`unordered_map` rehash 后迭代器失效但元素的引用 / 指针仍有效，所以只存「值」（`Locator`）。

失败原因用 `std::string_view` 常量（静态存储）。
