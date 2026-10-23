---
id: hl-hc08-java21-features
node: problems.hc08-order-sequence-api
type: qa
step: 13
---
## Q
订单序列实现用到哪些 Java 21 特性？各自的好处是什么？

## A
- **record**：`Entry(long id, long qty)`、全部 `Op` 与 `Result`；`equals` 按字段，测试可直接 `entries()` 与 `List.of(new Entry(1,10), ...)` 比较。
- **sealed**：`Op permits Put, Delete, CountUpTo, QtyUpTo, IdAt`；`Result permits Ok, Num, Err`；新增命令时旧写法（`instanceof` 链）编译通过但运行时落入 else，新写法因 switch 未穷尽而编译报错。
- **模式匹配 switch + record 解构**：`case Put(var id, var q) -> { put(id, q); yield new Ok(); }`，`case Delete(var id, var q) -> new Num(delete(id, q))`。
- **switch 表达式 + `yield`**：`parse` 每个 case 先校验参数个数再 `yield`。
- **Sequenced Collections**：`entries().getFirst()` / `getLast()` / `reversed()` 取代 `get(size() - 1)`；空列表抛 `NoSuchElementException`，比 `IndexOutOfBounds` 清楚。
- **未命名模式 `_`**（预览）：`case Ok _ -> "OK"`。
- **`IntStream` + `toList()`**：`entries()` 用 `IntStream.range(1, nextIndex).filter(i -> qtyByIdx[i] > 0).mapToObj(i -> new Entry(...)).toList()`，返回不可变快照；热路径不该用流。
- **`Math.addExact`** 守住 `totalQty`；文本块写脚本样例。

C++ 对应：`delete` 是关键字，改名 `remove`；异常 `UnknownId`（自定义）、`out_of_range`、`overflow_error`、`invalid_argument`；`std::variant` + `std::visit`；`__builtin_add_overflow`；`std::bit_ceil`；`from_chars` 拒绝 `+5` 必须检查结束指针；`catch` 四个异常类型，不要 `catch (const std::exception&)`（会把 `bad_alloc` 变成 `ERR`）。
