# J14 · Stream 与 Collector 的新工具：`toList()`、`mapMulti`、`teeing`、三参数 `iterate`

> 版本：`Collectors.teeing` 12 · `takeWhile/dropWhile`、三参数 `Stream.iterate`、`Stream.ofNullable`、`Collectors.filtering/flatMapping` 9 · `Stream.toList()`、`Stream.mapMulti` 16。**全部是正式特性，不是预览。**
> 可运行代码：`examples/J14/`。前置：Java 8 的 `stream().filter().map().collect(...)`、lambda、方法引用；1.1 从零讲「流」是什么。

---

## 1. 先看痛点

### 1.1 从零讲：Stream 是什么

**流**（Stream）不是集合。集合（`List`、`Map`）**存**数据；流是**对数据做的一条流水线**：

| 阶段 | 做什么 | 例子 |
|---|---|---|
| 来源（source） | 产生流 | `list.stream()` |
| 中间操作（intermediate） | 一步步加工，可以接很多个 | `filter` → `map` → `sorted` |
| 终止操作（terminal） | 拉动整条流水线，产出结果 | `collect` / `count` / `findFirst` / `toList` |

三个必须记住的性质：

1. **懒（lazy）**：只写中间操作不执行任何东西，遇到终止操作才开始跑（例 4）。
2. **一次性**：一个流只能终止一次，再用抛 `IllegalStateException: stream has already been operated upon or closed`。
3. **逐元素下推**：不是"全部 filter 完再全部 map"，而是每个元素依次穿过整条流水线（例 4），所以 `findFirst()` 能提前停、`limit(3)` 能处理无限流。

### 1.2 Java 8 的 Stream 缺了什么（`examples/J14/J14Old.java`）

```java
// 痛点 1：一次遍历同时算两个量（VWAP = 总名义金额 / 总数量），只能手写可变累加器
long notional = 0, qty = 0;
for (Trade t : trades) { notional += t.px() * t.qty(); qty += t.qty(); }

// 痛点 2：最后一步啰嗦，而且返回的 List 具体是什么类型，规范不保证
List<String> symbols = trades.stream().map(Trade::symbol).distinct().collect(Collectors.toList());

// 痛点 3：Java 8 的 iterate 是无限的，要配 limit；"到某个条件就停"没法直接写
List<Integer> powers = Stream.iterate(1, x -> x * 2).limit(8).collect(Collectors.toList());

// 痛点 4：一个元素产出 0..n 个结果，只能 flatMap，且每个元素都要建一个小 Stream
.flatMap(t -> t.qty() >= 100 ? Stream.of(t.qty()) : Stream.empty())
```

输出：

```
VWAP = 21406.666666666668
[AAPL, MSFT]
[1, 2, 4, 8, 16, 32, 64, 128]
[100, 300]
```

结果都对，但每处都有更好的写法。

---

## 2. 语法逐条讲

### 2.1 `Stream.toList()`（Java 16）

```java
List<Integer> a = stream.toList();
```

与 `collect(Collectors.toList())` 的区别：

| | `toList()` | `collect(Collectors.toList())` | `Collectors.toUnmodifiableList()` |
|---|---|---|---|
| 可修改？ | **不可修改**（`add` 抛 `UnsupportedOperationException`） | 可修改（实际是 `ArrayList`，规范不保证） | 不可修改 |
| 允许 `null` 元素？ | **允许** | 允许 | **不允许**（NPE） |
| 写法 | 短 | 长 | 长 |

输出：

```
toList() 不可修改 -> UOE
collect(toList()) 可修改: [3, 1, 2, 4]
toList 带 null: [x, null, y]
toUnmodifiableList 遇到 null -> NPE
```

准则：**默认用 `toList()`**；确实要继续 `add`/`sort` 才用 `new ArrayList<>(...)` 或 `collect(toCollection(ArrayList::new))`。

### 2.2 三参数 `Stream.iterate(seed, hasNext, next)`（Java 9）

与 `for (T x = seed; hasNext(x); x = next(x))` 一一对应，天然有限：

```java
Stream.iterate(1, x -> x < 200, x -> x * 3).toList();   // [1, 3, 9, 27, 81]
```

Java 8 的 `Stream.iterate(1, x -> x * 3).limit(5)` 得先知道要几个；新写法是"到条件不成立为止"。

### 2.3 `takeWhile` / `dropWhile`（Java 9）

```java
List.of(1, 2, 3, 10, 2, 1).stream().takeWhile(x -> x < 5)   // [1, 2, 3]   遇到第一个不满足就停
List.of(1, 2, 3, 10, 2, 1).stream().dropWhile(x -> x < 5)   // [10, 2, 1]  丢到第一个不满足，剩下全留
List.of(1, 2, 3, 10, 2, 1).stream().filter(x -> x < 5)      // [1, 2, 3, 2, 1] 对照：filter 对每个元素都判断
```

**只对"有序"流有可预期结果**，无序流（`HashSet.stream()`）不确定。它们是**短路**操作：`takeWhile` 遇到第一个不满足就不再读，对无限流有用。

### 2.4 `Stream.ofNullable(x)`（Java 9）

`null` → 空流，否则单元素流。用于 `flatMap(x -> Stream.ofNullable(map.get(x)))` 这种"查不到就跳过"。

### 2.5 `mapMulti`（Java 16）

```java
.<Fill>mapMulti((e, sink) -> {
    if (e instanceof Fill f && f.qty() > 0) sink.accept(f);   // 往 sink 里"推"0 个或多个结果
})
```

* `(元素, sink)`：`sink` 是 `Consumer`，调几次 `accept` 就产出几个元素。
* `<Fill>` 是显式类型参数：lambda 没有返回值，编译器推不出输出类型，不写就是 `Object`。
* 与 `flatMap` 的取舍：`flatMap` 要为每个输入元素**创建新 `Stream`**（哪怕 `Stream.empty()` 或单元素流也有分配和管线开销）；`mapMulti` 直接把结果推给下游，**没有中间流**。每个输入产出**少量**（甚至 0）个结果、或命令式循环更方便时用 `mapMulti`；结果很多时 `flatMap` 的惰性更好。

### 2.6 `Collectors.teeing`（Java 12）

tee 是 T 形三通管。**把同一个流同时喂给两个收集器，最后用一个函数合并两个结果**：

```java
Collectors.teeing(
    Collectors.summingLong(Trade::qty),                         // 收集器 1：总数量
    Collectors.summingLong(t -> t.pxTicks() * t.qty()),         // 收集器 2：总名义金额
    Vwap::new)                                                  // 合并：(qty, notional) -> Vwap
```

它解决痛点 1：**一次遍历得到两个结果，没有可变累加器**。流只能消费一次，没有 `teeing` 时要么收集成 `List` 再遍历两次，要么手写累加器。

### 2.7 其他收集器：`filtering`、`flatMapping`、`summarizingLong`

* `Collectors.filtering(pred, downstream)`（Java 9）：**在分组的每一组内部**过滤。与"先 `filter` 再 `groupingBy`"的区别：前者**保留空组**（例 3）。
* `Collectors.flatMapping(fn, downstream)`（Java 9）：在每组内部展开。
* `Collectors.summarizingLong/Int/Double`：一次得到 count、sum、min、max、average（`LongSummaryStatistics`）。

---

## 3. 编译器和 JVM 到底做了什么

### 3.1 编译器

几乎什么都不做：都是库方法，无新语法。唯一麻烦是**类型推断**：`teeing` 和 `mapMulti` 泛型很深，推导失败报错很长。例如：

```java
Collectors.teeing(Collectors.minBy(Comparator.naturalOrder()),
                  Collectors.maxBy(Comparator.naturalOrder()), (lo, hi) -> ...)
```

编译失败：`inference variable T#1 has incompatible upper bounds ...`。修复：`Comparator.<Long>naturalOrder()`。**经验：`teeing`/`mapMulti` 推导不动时，先给泛型方法加显式类型参数。**

### 3.2 JVM / 库的实现：一条逐元素下推的 Sink 链

流水线在 `java.util.stream` 内部是一串 `Sink` 对象，每个中间操作包一层。终止操作开始后，库从来源**一个一个**取元素，调 `sink.accept(x)` 往下推（例 4）：

```
--- 逐元素下推 + 短路(findFirst)
  source 1
  filter 1
  source 2
  filter 2
  map    2
结果 = 20
```

* 元素 1：在 `filter` 被拒，**不会**走到 `map`；
* 元素 2：通过 `filter`、`map`，`findFirst` 拿到结果后通知上游"别再给了"（短路），元素 3–6 根本没被读；
* `sorted()`、`distinct()` 是**有状态的屏障**：必须看完全部输入才能往下推（`before sort 3, 1, 2` 全部出现后才有 `after sort 1, 2, 3`）。

### 3.3 三个新方法的实现取向

* **`toList()`**：把元素 `toArray()` 出来包成不可修改列表（允许 `null`），不经过 `Collector` 的累加器/合并器，路径更短。
* **`mapMulti`**：每个元素调一次你的 lambda，`sink` 就是下游的 `Sink`，不建中间 `Stream`。
* **`teeing`**：组合收集器——累加器同时持有两个下游的中间状态；`finisher` 调两个下游的 `finisher` 再调你的合并函数；并行下 `combiner` 分别合并两份状态。

---

## 4. 三个例子（由浅入深）+ 一个懒执行实验

### 例 1：最简单——小工具合集（`J14Ex1.java`）

见 2.1–2.4。输出：

```
toList() 不可修改 -> UOE
collect(toList()) 可修改: [3, 1, 2, 4]
toList 带 null: [x, null, y]
toUnmodifiableList 遇到 null -> NPE
[1, 3, 9, 27, 81]
takeWhile(<5): [1, 2, 3]
dropWhile(<5): [10, 2, 1]
filter(<5)   : [1, 2, 3, 2, 1]
ofNullable(null).count = 0
sum 1..100 = 5050
```

### 例 2：进阶——`mapMulti` 与 `flatMap` 的对照（`J14Ex2.java`）

事件流里只要 `qty > 0` 的 `Fill`：

```java
List<Fill> viaFlat = events.stream()
        .flatMap(e -> e instanceof Fill f && f.qty() > 0 ? Stream.of(f) : Stream.empty())
        .toList();
List<Fill> viaMulti = events.stream()
        .<Fill>mapMulti((e, sink) -> { if (e instanceof Fill f && f.qty() > 0) sink.accept(f); })
        .toList();
```

输出：两个结果相同（`相同? true`）。再看"一个元素展开成几个"：多腿订单拆腿，`P2` 有 0 条腿（贡献 0 个元素）：

```
[P1-leg1, P1-leg2, P3-leg1, P3-leg2, P3-leg3]
```

### 例 3：贴近真实——一次遍历算多个指标（`J14Ex3.java`）

5 笔成交，`AAPL` 三笔、`MSFT` 两笔。

```java
Vwap all = trades.stream().collect(Collectors.teeing(
        Collectors.summingLong(Trade::qty),
        Collectors.summingLong(t -> Math.multiplyExact(t.pxTicks(), t.qty())),
        Vwap::new));
```

输出：

```
总体 VWAP = 26186.721 (qty=610)
价格范围(全部) = 18940..41010
  AAPL VWAP=18957.073 qty=410
  MSFT VWAP=41007.500 qty=200
qty 统计: LongSummaryStatistics{count=5, sum=610, min=10, average=122.000000, max=300}
每个代码的大单(qty>=200): {AAPL=[300], MSFT=[]}
先 filter 再分组        : {AAPL=[300]}
```

手算核对：总名义金额 = 18950×100 + 18960×300 + 41000×50 + 41010×150 + 18940×10 = 15 973 900，除以 610 = 26186.72…；AAPL = (1 895 000 + 5 688 000 + 189 400) / 410 = 18957.07…，吻合。

最后两行是 `filtering` 的重点：`MSFT` 没有 ≥200 的单，`filtering` 版本**仍保留 `MSFT=[]` 这一组**，先 `filter` 再 `groupingBy` 则直接没有 `MSFT`。需要"每个分组都出现，即使为空"的报表用前者。`Math.multiplyExact` 的用意：价格乘数量溢出时宁可抛异常，也不要悄悄变成负数。

### 例 4：懒与逐元素下推（`J14Ex4Lazy.java`）

输出见 3.2。第一段"没有终止操作"无任何输出——`peek` 里的 `println` 一次都没执行。

---

## 5. 坑与限制

### 5.1 `toList()` 与 `Collectors.toList()` 不能互相替换

返回不可修改列表。旧代码 `list = stream.collect(toList()); list.add(...)` 换成 `toList()` 会运行时抛 `UnsupportedOperationException`，**编译器发现不了**，改时逐处看有无后续修改。

### 5.2 流只能用一次

```java
var s = list.stream();
s.count();
s.count();   // IllegalStateException
```

### 5.3 `peek` 只用于调试，逻辑别放里面

"为什么 `peek` 没打印"——短路或没有终止操作；JDK 9 起 `count()` 若能直接从来源算出大小会**跳过整条流水线**，`peek` 的副作用就不执行。

### 5.4 基本类型流 vs 装箱

`Stream<Long>` 每个元素是 `Long` 对象；热路径用 `LongStream`/`IntStream`（`mapToLong`、`summaryStatistics`）。`Arrays.stream(out).boxed().toList()` 的 `boxed()` 就是装箱。

### 5.5 并行流不是免费的

`.parallel()` 用公共 `ForkJoinPool`，适合 CPU 密集、数据量大、操作无状态、来源易分割（数组、`ArrayList`）。阻塞 I/O 用它是错的（占住公共池线程，该用虚拟线程）。`teeing`、`groupingBy` 并行下需要 `combiner`，自定义收集器要实现正确。

### 5.6 `takeWhile`/`dropWhile` 依赖顺序

对 `HashSet.stream()` 之类的无序流没有意义。

### 5.7 `Collectors.toMap` 遇到重复 key 会抛 `IllegalStateException`

要处理重复写第三个参数 `(a, b) -> a`。不是新 API，却是 Stream 里最常见的运行时错误之一。

### 5.8 后续版本：Stream Gatherers

流水线的中间操作（`filter`、`map`、`sorted`……）是固定的一组。**JDK 24 转正的 Stream Gatherers**（22 预览）让你自定义中间操作：`Stream::gather(Gatherer)`，内置 `fold`、`mapConcurrent`、`scan`、`windowFixed`、`windowSliding`。"滑动窗口平均"在 JDK 21 要写自己的 `Spliterator` 或绕路，24 起一行 `stream.gather(Gatherers.windowSliding(3))`。（面试说法："21 里没有；24 起有 Gatherers，我知道有这件事。"）

---

## 6. 真实代码里的 Stream

* `BatchMatcher`：`events.stream().<OrderBook.Trade>mapMulti((e, sink) -> { if (e instanceof OrderBook.Trade t) sink.accept(t); }).toList();` —— 2.5 `mapMulti`：从混合事件里只挑 `Trade`，配 `toList()` 和 `instanceof` 模式。
* `OrderBook`：`book(side).entrySet().stream().limit(n).map(e -> new Level(...)).toList();` —— 取最优 n 档，靠短路 `limit(n)` 只遍历前 n 个。
* `RegisterSim`：`lines.stream().filter(l -> !l.isBlank() && !l.strip().startsWith("#")).toList()`；`Arrays.stream(out).boxed().toList()` —— 2.1；5.4（`boxed()`）。
* `QueueEvents`：`run(parse(lines)).stream().map(QueueEvents::render).toList();`
* `OrderSequence`：`IntStream.range(1, nextIndex).filter(i -> qtyByIdx[i] > 0).mapToObj(i -> new Entry(...)).toList();` —— 基本类型流 + `toList()`。
* `RecursiveSum`：`IntStream.range(0, chunks).parallel().mapToObj(...).reduce(Wide.ZERO, Wide::merge).toResult();` —— 5.5 并行流，对 CPU 密集求和合理。
* `Main`：`in.lines().toList()` —— `BufferedReader.lines()` 返回 `Stream<String>`。

没有用 `teeing` 和三参数 `iterate`。`teeing` 最贴近的场景是队列均值里"同时求和与个数"，现有实现用增量维护的字段，没必要换。面试被问"一次遍历怎么同时算 VWAP 分子分母"，答 `teeing`，并说明增量/流式场景用累加器字段更合适。

---

## 7. 自测题

1. `stream.toList()` 和 `stream.collect(Collectors.toList())` 有哪三点区别？
2. 为什么 `Stream.of(1,2,3).peek(System.out::println)` 什么都不打印？
3. 写出 `takeWhile(x -> x < 3)` 和 `filter(x -> x < 3)` 在 `[1, 2, 5, 1]` 上的结果，并说明区别。
4. 用 `teeing` 写出：对 `List<Long> qtys` 同时求最大值和个数，返回 `String`，形如 `"max=300 n=5"`。
5. `mapMulti` 和 `flatMap` 什么时候选前者？为什么要写 `.<Fill>mapMulti(...)`？

<details><summary>答案</summary>

1. `toList()` 返回不可修改列表（`collect(toList())` 通常可修改）；`toList()` 允许 `null`（`toUnmodifiableList` 不允许）；`toList()` 更短，实现上少一层收集器开销。
2. 没有终止操作，流水线是懒的，不执行。
3. `takeWhile` → `[1, 2]`（遇到 5 就停）；`filter` → `[1, 2, 1]`（对每个元素都判断）。
4. ```java
   qtys.stream().collect(Collectors.teeing(
       Collectors.maxBy(Comparator.<Long>naturalOrder()),
       Collectors.counting(),
       (mx, n) -> "max=" + mx.orElseThrow() + " n=" + n));
   ```
5. 每个输入产出少量（尤其 0 或 1 个）结果、或命令式循环更好写时用 `mapMulti`（不建中间 `Stream`）；产出很多、或结果本来就是现成集合/流时用 `flatMap`。lambda 没有返回类型，编译器推不出输出元素类型，需 `<Fill>` 显式指定。

</details>

---

「延伸」J15 数学与字符串工具：`Math.xxxExact`、`String` 新方法。
