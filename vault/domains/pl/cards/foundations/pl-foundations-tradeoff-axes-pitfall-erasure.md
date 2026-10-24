---
id: pl-foundations-tradeoff-axes-pitfall-erasure
node: foundations.tradeoff-axes
type: qa
step: 9
---
## Q
Java 为了「向后兼容」付出的代价能举一个具体例子吗？为什么 `List<String>` 和 `List<Integer>` 在运行时是同一个类？

## A
Java 5（2004）加入泛型时，数百万行旧代码里已经有了不带类型参数的 `List`。要让旧代码和新代码在同一个虚拟机里互相调用，设计者选择了类型擦除（type erasure）：泛型只在编译期检查，编译完把类型参数擦掉，字节码里只剩 `List`。

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
System.out.println(a.getClass() == b.getClass());   // true
System.out.println(a.getClass().getName());         // java.util.ArrayList
```

实际输出 `true` 和 `java.util.ArrayList`：运行时根本没有 `ArrayList<String>` 这个类。

后果：

- 不能写 `new T()` 或 `T.class`，因为运行时不知道 `T`。
- 对 `Object` 做 `o instanceof List<String>` 编译不过：`error: Object cannot be safely cast to List<String>`。
- 基本类型不能做类型参数，`List<int>` 不合法，只能装箱成 `List<Integer>`，多一层对象开销。

这是「兼容与演进」轴上的典型账单：兼容旧字节码换来了平滑过渡，也换来了十几年没法修的限制。Rust 设计时没有历史包袱，选了单态化（为每个具体类型生成一份代码），所以 `Vec<i32>` 和 `Vec<String>` 在编译结果里是两份不同的代码。C++ 的模板（编译期按类型参数生成代码的机制）也是这条路，`std::vector<int>` 与 `std::vector<std::string>` 是两个不同的类，代价同样是编译时间和二进制体积。
