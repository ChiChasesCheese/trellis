---
nodes: [abstraction.equality-hashing, abstraction.operator-overloading, memory.ownership-borrowing]
tags: [drill]
---
# 练习：缓存明明有这个键，却总是未命中

一个会话缓存用自定义对象 `Key(id)` 当映射的键。上线后监控显示：命中率下降，缓存条目数只增不减，重启后恢复正常。排查发现有代码在把 `Key` 放进缓存之后又修改了它的 `id`。你要预测同一类操作在四门语言里的后果，并解释每门语言的设计怎样让这类错误更容易或更难发生。

```java
Key k = new Key(1);                  // equals/hashCode 都基于 id
m.put(k, "alice"); k.id = 2;
m.get(k); m.get(new Key(1)); m.containsKey(new Key(2)); m.size();
```

Python 里同样的类（定义了 `__eq__` 与 `__hash__`），再加一个只定义 `__eq__` 的类 `K2`；Go 里 `map[Key]string` 的 `Key` 是结构体；Rust 里想把带 `Cell<i32>` 的类型放进 `HashMap`。

**要你给出的**
- Java 四个调用的结果，以及 Python 的 `m.get(k)`、`{K2(1): 1}`、`{[1]: 1}` 的结果。
- Go 与 Rust 的对应情形：改了原变量之后能不能再找到，能不能通过编译。
- `NaN` 当键时（`float("nan")` 放三次、Go `map[float64]int` 放两次）会怎样。
- 一条跨语言适用的键类型规则。

**评分要点**
- Java 输出 `null null false 1`：对象按旧哈希值放在旧桶里，改字段后用新哈希去找，找不到；用旧值构造的新对象虽然哈希匹配，但桶里那个条目的 `equals` 已经对不上了；条目还在，只是永远取不出来，所以 `size` 仍是 1 且只增不减 ([[pl-abstraction-equality-hashing-pitfall-mutable-key]], [[pl-abstraction-equality-hashing-mechanism]])。
- Python 同样得到 `None`；只定义 `__eq__` 的类会让 `__hash__` 变成 `None`，当键时抛出 `TypeError: unhashable type`，`list` 当键也是同样的 `TypeError`。Python 的选择是：可变的内置容器干脆不可哈希，自定义类自己负责 ([[pl-abstraction-equality-hashing-foundation-python-eq-hash]], [[pl-abstraction-operator-overloading-foundation-python-dunder]])。
- Go 的结构体键在放入时被复制，改原变量不影响已有条目：`m[k]` 找不到（`ok` 为 `false`）、`m[Key{1}]` 仍能取到 `alice`、长度仍是 1；切片、map、函数不可比较，当键直接编译失败，装进接口再比较则是运行时 panic（`comparing uncomparable type []int`） ([[pl-abstraction-equality-hashing-foundation-go-comparable]])。
- Rust 的 `HashMap<K, V>` 取得键的所有权，调用者手里不再有可变引用，这类错误在借用检查下无从发生；想绕过要靠 `Cell` 之类的内部可变性，此时 `get` 同样返回 `None`、长度为 1。`f64` 没有实现 `Eq`，`HashSet<f64>` 的 `insert` 不能编译 ([[pl-memory-ownership-borrowing-principle]], [[pl-abstraction-equality-hashing-foundation-rust-eq-traits]])。
- `NaN`：Python 的 `{nan, nan, float("nan")}` 长度是 2（同一个对象靠同一性去重，另一个 `NaN` 对象被当成新元素），`nan == nan` 为 `False` 而 `nan in [nan]` 为 `True`；Go 放两次得到两个条目且永远取不回（取值为 `0`）；Java 的 `Double.NaN.equals(Double.NaN)` 为 `true`，`HashSet` 里只留一个。三种答案来自「`==` 遵循 IEEE 754」与「容器需要自反性」的冲突 ([[pl-abstraction-equality-hashing-unique-nan-equality]])。
- 规则：键必须是不可变的值，并且相等与哈希只依赖不可变字段；Java 用 `record` 或字段全 `final`，Python 用 `frozen=True` 的 `dataclass` 或元组，Go 用只含可比较字段的结构体，Rust 靠所有权天然满足 ([[pl-abstraction-equality-hashing-best-practice]], [[pl-abstraction-equality-hashing-table]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
