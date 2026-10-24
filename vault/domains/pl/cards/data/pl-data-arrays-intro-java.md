---
id: pl-data-arrays-intro-java
node: data.arrays-slices
type: qa
step: 4
---
## Q
Java 的数组和 `ArrayList` 各是什么？数组的协变（covariance）、`Arrays.asList` 和 `List.of` 的行为有什么需要知道的？

## A
**数组 `int[]`**：堆上的对象，长度固定，创建后不能改。每次访问都做越界检查，越界抛 `ArrayIndexOutOfBoundsException`（真实消息：`Index 3 out of bounds for length 3`）。基本类型数组（`int[]`）连续存放原始值；对象数组（`Integer[]`）存的是引用，元素对象散落在堆上。

**`ArrayList<E>`**：库类，内部持有一个 `Object[]` 和一个 `size`，满了就扩容为约 1.5 倍。因为泛型只能装对象，`ArrayList<Integer>` 里每个元素都是装箱的 `Integer` 对象的引用，不是裸的 `int`。本机观察到的容量序列：10、15、22、33、49、73、109、163、244。

**没有切片视图**：想处理数组的一部分，要么复制（`Arrays.copyOfRange`），要么传（数组，起点，终点）三个参数。`list.subList(a, b)` 给出视图，但对原列表做结构性修改后使用它会抛异常。

**数组协变**：`String[]` 可以赋给 `Object[]`，编译器放行，运行时才检查：

```java
Object[] o = new String[1];
o[0] = 1;   // ArrayStoreException: java.lang.Integer
```

这是 Java 早期没有泛型时留下的设计，现在泛型集合是不变的（`List<String>` 不能赋给 `List<Object>`）。

**包装列表**：`Arrays.asList(1,2,3)` 是对数组的定长视图：`set` 可以，`add` 抛 `UnsupportedOperationException`。`List.of(...)` 是完全不可变的，`set` 也抛异常。

**要记住的一点**：Java 的序列类型分两层：语言内置的定长数组，和库提供的可增长列表，中间没有 Go 那样的统一视图。
