---
id: pl-meta-reflection-mechanism
node: metaprogramming.reflection
type: qa
step: 6
---
## Q
Java、Go、Python、Rust、C++ 的反射在底层各靠什么实现？一次反射调用比直接调用慢多少？

## A
- **Java**：类加载后，字段和方法的描述保留在元空间（Metaspace）里的 `Class` 对象中。`Method.invoke` 要做访问检查、参数装箱；JDK 18 起（JEP 416）反射调用改为基于方法句柄（method handle）实现。
- **Go**：接口值是（类型指针，数据指针）两个字。`reflect.ValueOf` 把这对指针拆开，类型描述（type descriptor）是链接进二进制的只读数据。
- **Python**：属性本来就存在对象的 `__dict__` 里，`getattr` 只是把名字从编译期固定变成运行期传入，几乎不多付费。
- **Rust**：类型信息编译后被擦除，只剩 `TypeId`。`Any` 只能回答「它是不是 `i32`」（向下转换），不能枚举字段。
- **C++**：有虚函数的类，其虚表里多放一个指向 `type_info` 的指针，`typeid` 和 `dynamic_cast` 就靠它，能问“是不是 `Derived`”，不能列字段。可用 `-fno-rtti` 关掉，省下这份元数据（零开销原则）。

本机一次测量（量级参考，不是基准结论）：

| 操作 | 每次耗时 |
|---|---|
| Java 直接调用（被 JIT 内联） | 接近 0 |
| Java `Method.invoke` / `MethodHandle` | 约 3 ns / 约 1.3 ns |
| Go 直接调用 / `Value.Call` / `FieldByName` | 约 0.5 / 62 / 18 ns |
| Python `p.x` / `getattr(p, 'x')` | 约 4 / 12 ns |

规律：Python 里反射几乎免费，因为整门语言本来就是动态的；Java 和 Go 的代价来自两点：每次按名字查表，以及丢掉内联这类编译器优化。一两次调用无所谓，进入热循环就是一到两个数量级。
