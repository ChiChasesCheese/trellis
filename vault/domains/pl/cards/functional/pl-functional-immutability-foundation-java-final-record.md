---
id: pl-functional-immutability-foundation-java-final-record
node: functional.immutability
type: qa
step: 2
---
## Q
Java 的 `final`、`record` 和不可变集合分别提供了什么级别的不可变？`List.of` 与 `unmodifiableList` 有什么区别？

## A
- **`final` 变量 / 字段**：只能赋值一次（绑定不可变）。`final List<String> xs` 之后 `xs.add(...)` 照样可以。
- **`record`**：声明时所有字段都是 `final`，自动生成构造器、访问器、`equals`、`hashCode`，是做**值对象**最省事的方式，但只是浅不可变：字段若是 `List`，列表本身仍可变。
- **不可变集合**有两种截然不同的东西：

```java
List<String> src = new ArrayList<>(List.of("ann"));
List<String> view = Collections.unmodifiableList(src);  // 视图
List<String> copy = List.copyOf(src);                   // 独立副本
src.add("bob");
// view -> [ann, bob]   视图跟着原列表变
// copy -> [ann]        副本不受影响
copy.add("z");          // UnsupportedOperationException
```

`unmodifiableList` 只是给原列表包了一层「不许调用修改方法」的视图，原列表改了，视图跟着变；`List.of` / `List.copyOf` 才是真正独立的、不可变的副本。

Java 内存模型给 `final` 字段一个特别保证：只要对象的构造器没有把 `this` 泄漏出去，其他线程看到这个对象引用时，**一定能看到已经初始化好的 `final` 字段**，不需要同步。这使得不可变对象可以通过数据竞争（比如不加锁地放进一个公共字段）安全发布，是 `String` 等核心类线程安全的基础。
