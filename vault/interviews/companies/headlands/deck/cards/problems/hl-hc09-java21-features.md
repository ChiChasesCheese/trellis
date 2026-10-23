---
id: hl-hc09-java21-features
node: problems.hc09-top-trades-by-notional
type: qa
step: 15
---
## Q
这个题用到哪些 Java 特性（record 紧凑构造器、sealed 加 `when` 守卫、Sequenced Collections、`teeing`、Comparator 组合子等）？各自好处与不该用的场景？

## A
- **record + 紧凑构造器**：`Trade` 构造器里校验并 `multiplyExact`；旧写法 final 类 + 私有字段 + getter + 手写 `equals/hashCode/toString` 约 40 行。需要可变字段（如 `Acc`）或继承别的类时不该用。
- **sealed + 模式匹配 switch + record 模式 + `when` 守卫**：`Feed permits Fill, Tick, Ask`；查穷尽性，同时判断类型和解构；旧写法 `instanceof` 链加强转、编译器不查漏。
- **Sequenced Collections**：`reversed()` 取倒序**视图**（改原列表它也变；要独立副本用 `List.copyOf`）；`getFirst()/getLast()`、`peekFirst/removeFirst`。
- **Stream 新工具**：`toList()`（Java 16）返回不可变列表；`teeing`（Java 12）一趟喂两个收集器。热路径简单聚合手写循环更快。
- **精确算术**：`multiplyExact / addExact`（旧写法 `r = a * b; if (a != 0 && r / a != b) throw ...` 多一次除法还易错）。
- **Comparator 组合子**：`comparingLong(...).reversed().thenComparing(...).thenComparingInt(...)` 一条链写出全序。
- **虚拟线程 / `StructuredTaskScope`**（预览）、`ConcurrentHashMap.merge`、`CountDownLatch`、`formatted`、文本块。
- `var` 局部变量。

C++ 差异：`priority_queue` 存 16 字节 `Key`，需要时再查数组（没有 GC，复制字符串有真实成本）；`TreeSet.remove+add` 对应 `set::extract + insert(node)`（相等键陷阱 + 不分配）；`string_view` 可能悬空——视图借用，结果拥有（结果里放 `std::string`）；返回 `std::vector<Trade>` 值，不可变用 `const`；`span<const string_view>` 没有 null；`resize` 需要默认构造，截断用 `erase(begin()+k, end())`。
