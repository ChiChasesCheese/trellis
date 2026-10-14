# J01 · `record`：一行声明一个不可变的值对象

> 版本：Java 16 正式（JEP 395）。Java 14、15 是预览。
> 写法说明见 `study/TEXTBOOK.md`。本课所有可运行代码在 `study/10-java21/examples/J01/`。
> 前置知识：会写普通的类、构造器、`getXxx()`、`equals`/`hashCode` 的大概意思。不会也没关系，第 1 节会从零讲。
> 官方出处：JEP 395 Records — https://openjdk.org/jeps/395 ；语言规范 §8.10 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.10

---

## 1. 先看痛点：Java 8 里「装三个字段」要写多少字

交易系统里到处都是「一包数据」：一笔成交 `(代码, 价格, 数量)`、一条订单、一行解析好的 CSV。
这种东西的特点是：**它只是数据，创建之后不应该再变，两个内容相同的就该被认为是同一个东西。**
这类对象叫**值对象**（value object）。

Java 8 里写一个只有三个字段的值对象，是这样（完整代码：`examples/J01/J01Old.java`）：

```java
static final class Fill {
    private final String symbol;
    private final long priceTicks;
    private final long qty;

    Fill(String symbol, long priceTicks, long qty) {
        this.symbol = symbol;
        this.priceTicks = priceTicks;
        this.qty = qty;
    }

    String getSymbol() { return symbol; }
    long getPriceTicks() { return priceTicks; }
    long getQty() { return qty; }

    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Fill f = (Fill) o;
        return priceTicks == f.priceTicks && qty == f.qty && Objects.equals(symbol, f.symbol);
    }
    @Override public int hashCode() { return Objects.hash(symbol, priceTicks, qty); }
    @Override public String toString() {
        return "Fill{symbol=" + symbol + ", priceTicks=" + priceTicks + ", qty=" + qty + "}";
    }
}
```

三个字段，约 30 行。每多一个字段，要在 **7 个地方**同步改：字段声明、构造器参数、构造器赋值、getter、`equals`、
`hashCode`、`toString`。漏改任何一处都不会有编译错误，只会在运行时悄悄出错。

### 这些样板代码不是「废话」，每一块都有用

为了理解 record 到底替你做了什么，先搞清楚上面每一块为什么必须存在：

| 样板 | 没有它会怎样 |
|---|---|
| `private final` 字段 | 外部能直接改，或者构造后又被改，「值」就不稳定了 |
| 构造器 | 没法一次性把所有字段设好 |
| getter | `private` 字段外面读不到 |
| `equals` | 默认的 `equals` 是**引用比较**（`==`）：两个内容一模一样的对象被认为不同 |
| `hashCode` | 只重写 `equals` 不重写 `hashCode`，放进 `HashMap` 会出怪事（见下） |
| `toString` | 默认输出 `J01Old$Fill@1b6d3586`，调试时看不出内容 |

最阴险的是 `equals`/`hashCode`。`J01Old.java` 里故意写了一个忘记重写它们的 `ForgetfulFill`：

```java
Map<ForgetfulFill, String> m = new HashMap<>();
m.put(new ForgetfulFill("AAPL", 100), "first");
m.get(new ForgetfulFill("AAPL", 100));   // 运行结果：null
```

内容一模一样的对象，却查不到。原因：`HashMap` 先用 `hashCode()` 决定去哪个桶（bucket）找，
默认的 `hashCode()` 基于对象在内存里的身份，两个不同对象几乎一定落在不同的桶，根本不会走到 `equals` 那一步。
（哈希表的原理见 `study/00-foundations/` 与 oa01 讲义 §2.2。）

所以，**不能省，又很容易写错，又长。** 这就是 record 要解决的问题。

---

## 2. 语法逐条讲

### 2.1 最简形式

```java
record Fill(String symbol, long priceTicks, long qty) {}
```

一行。括号里的东西叫**记录组件**（record component）。它同时做了三件事：声明字段、声明构造器参数、声明访问器。

对比 Java 8 版：

| | Java 8 手写 | record |
|---|---|---|
| 代码量 | 约 30 行 | 1 行 |
| 访问器 | `getSymbol()` | `symbol()`（**没有 get 前缀**） |
| 比较 | 自己写 `equals` | 自动按内容比较 |
| 能否改字段 | 看你有没有写 setter | 不能，字段永远是 `private final` |

```java
Fill a = new Fill("AAPL", 18_950, 100);
a.symbol();            // "AAPL"
a.toString();          // Fill[symbol=AAPL, priceTicks=18950, qty=100]
a.equals(new Fill("AAPL", 18_950, 100));   // true
```

> 注意 `toString()` 的格式：`Fill[symbol=AAPL, ...]` 用方括号，不是花括号。
> 官方规范只说「应该包含所有组件的名字和值」，没有固定格式，别写依赖这个格式的代码（比如拿它当序列化格式）。

### 2.2 record 里还能放什么

```java
record Order(long id, String symbol, Side side, long priceTicks, long qty) {
    // ① 静态字段、静态方法、静态嵌套类型：可以
    static final long MAX_QTY = 1_000_000;

    // ② 实例方法：可以，和普通类一样
    long notionalTicks() { return Math.multiplyExact(priceTicks, qty); }

    // ③ 额外的构造器：可以，但第一句必须是 this(...)
    Order(long id, String symbol, Side side, long priceTicks) {
        this(id, symbol, side, priceTicks, 1);
    }

    // ④ 实现接口：可以
    // record Fill(...) implements Comparable<Fill> { ... }
}
```

**不可以**放的：

| 想做的事 | 结果 | 编译器原话（实测） |
|---|---|---|
| 声明实例字段 | 不行 | `field declaration must be static (consider replacing field with record component)` |
| `extends` 别的类 | 不行（record 已经隐式继承了 `java.lang.Record`，Java 只有单继承） | `'{' expected` |
| 被别的类继承 | 不行，record 隐式是 `final` | — |
| 在方法里给字段赋值 | 不行，字段是 `final` | `cannot assign a value to final variable x` |
| 额外构造器不先调用 `this(...)` | 不行 | `constructor is not canonical, so its first statement must invoke another constructor of class P` |

这些限制不是偷懒，是**故意**的：一个 record 的全部状态就是括号里那几个组件，
这样编译器才敢自动生成 `equals`/`hashCode`/`toString`，别人看到 `record Fill(a, b, c)` 就知道状态不多不少正是这三样。

### 2.3 规范构造器与紧凑构造器

每个 record 都有一个**规范构造器**（canonical constructor）：参数列表和记录组件完全一致的那个构造器。
你不写，编译器生成一个，内容就是「把每个参数赋给同名字段」。

想在赋值前**校验**或**规范化**参数，有两种写法：

**写法 A：显式规范构造器**（啰嗦，要自己写所有赋值）

```java
record Order(long id, long qty) {
    Order(long id, long qty) {
        if (qty <= 0) throw new IllegalArgumentException("qty");
        this.id = id;
        this.qty = qty;
    }
}
```

**写法 B：紧凑构造器**（compact constructor，推荐）——省掉参数括号，**末尾自动赋值**：

```java
record Order(long id, String symbol, Side side, long priceTicks, long qty) {
    Order {                                      // 注意：Order 后面没有 (...)
        if (id <= 0) throw new IllegalArgumentException("id must be positive: " + id);
        if (qty <= 0) throw new IllegalArgumentException("qty must be positive: " + qty);
        symbol = symbol.strip().toUpperCase();   // 给「参数」重新赋值；末尾才会写进字段
    }
}
```

紧凑构造器的规则：

1. 组件名在函数体里就是**参数**（不是字段）。可以读，可以给它重新赋值（上面 `symbol = ...`）。
2. **不能**写 `this.symbol = ...`——编译器会报 `cannot assign a value to final variable symbol`。因为末尾的赋值是编译器加的，你再赋一次就是赋两次 `final`。
3. 不能 `return`（它不是一个会提前返回的函数，末尾的赋值必须执行）。
4. 可以抛异常——这是做校验的主要手段。

这正是 `JobChains.Job` 的写法（见第 6 节）：构造一行 `Job` 的时候就把单行能判断的非法情况拦下来。

### 2.4 防御性拷贝：组件是集合时

```java
record Basket(String name, List<Order> orders) {
    Basket {
        orders = List.copyOf(orders);   // 拷贝一份不可修改的 List；null 元素会抛 NPE
    }
}
```

如果不拷贝，调用方还握着原来那个 `ArrayList` 的引用，随时能往里面加东西，你的 `Basket` 就在你眼皮底下变了。
`examples/J01/J01Ex2.java` 里实测：往原列表里再加一单，`basket.orders().size()` 仍然是 1。

### 2.5 局部 record 与泛型 record

record 可以声明在**方法内部**（局部 record，隐式 static），非常适合「这个方法里临时需要一个小结构」：

```java
static long topNotional(List<String> lines) {
    record Row(String sym, long px, long qty) {}      // 只在这个方法里可见
    return lines.stream().map(l -> l.split(","))
            .map(t -> new Row(t[0], Long.parseLong(t[1]), Long.parseLong(t[2])))
            .mapToLong(r -> r.px() * r.qty()).max().orElse(0);
}
```

泛型也行：`record Tagged<T>(T value, boolean valid) {}`。
（本 kit 里 `ConcurrentMerge.Ready<T>(T value, int stream)` 就是泛型 record。）

---

## 3. 编译器和 JVM 到底做了什么

用 `javap`（JDK 自带的反编译器）看 `record Fill(String symbol, long priceTicks, long qty) {}` 编译出的类（实测输出，略有删减）：

```
final class J01Ex1$Fill extends java.lang.Record {
  private final java.lang.String symbol;
  private final long priceTicks;
  private final long qty;
  J01Ex1$Fill(java.lang.String, long, long);            // 规范构造器
  public final java.lang.String toString();             // invokedynamic ObjectMethods
  public final int hashCode();                          // invokedynamic ObjectMethods
  public final boolean equals(java.lang.Object);        // invokedynamic ObjectMethods
  public java.lang.String symbol();                     // 访问器
  public long priceTicks();
  public long qty();
}
```

逐项解释：

1. **`final class ... extends java.lang.Record`**：所有 record 的父类是 `java.lang.Record`（一个抽象类，几乎什么都不放，只规定 `equals`/`hashCode`/`toString` 要被重新声明）。类是 `final`，所以不能被继承。
2. **每个组件一个 `private final` 字段**。
3. **规范构造器**：访问级别和 record 本身一致（这里 record 是包内可见的，所以构造器也是包内可见；`public record` 的构造器就是 `public`）。
4. **每个组件一个访问器**，`public`，名字就是组件名。
5. **`toString`/`hashCode`/`equals` 是 `final` 的，实现只有一行 `invokedynamic`。**
   这是最有意思的部分：编译器**没有**把 30 行 `equals` 展开写进 class 文件，而是写了一条 `invokedynamic` 指令，
   指向引导方法（bootstrap method）`java.lang.runtime.ObjectMethods.bootstrap`。
6. 类文件里多了一个 `Record` 属性，登记了每个组件的名字和类型。反射的 `Class.isRecord()`、`getRecordComponents()` 就读它
   （`J01Ex3` 里实测：`[String symbol, Side side, long priceTicks, long qty]`）。

### 什么是 `invokedynamic`，为什么 record 用它

普通方法调用指令（`invokevirtual` 等）在编译时就写死了「调用哪个方法」。`invokedynamic` 不同：**第一次执行到它的时候**，
JVM 去调用一个指定的「引导方法」，由引导方法**现场**生成真正要执行的代码（一个方法句柄 `MethodHandle`），
之后这条指令就直接连到那段代码，不再走引导方法。

对 record 来说，引导方法 `ObjectMethods.bootstrap` 拿到的参数是：record 的类、组件名列表 `"symbol;priceTicks;qty"`、
每个字段的 getter 句柄。它据此造出 `equals`/`hashCode`/`toString`。好处：

* class 文件小：不管 record 有多少组件，`equals` 都只占一条指令。
* 以后 JDK 想改进生成方式（更快的哈希算法等），只要改引导方法，不用重新编译你的代码。

（后面 J03 讲的模式匹配 `switch` 也用同一套机制。）

生成的 `equals` 的语义：先 `instanceof` 同一个 record 类型，然后逐个组件比较——基本类型 `int`/`long` 直接比，
`float`/`double` 用 `Float.compare`/`Double.compare`，引用类型用 `Objects.equals`。
`hashCode` 把各组件的哈希值组合起来，规范只要求「相同内容 → 相同哈希」，不规定具体公式。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——声明、读取、比较、当 Map 的 key

`examples/J01/J01Ex1.java`：

```java
record Fill(String symbol, long priceTicks, long qty) {}

Fill a = new Fill("AAPL", 18_950, 100);
Fill b = new Fill("AAPL", 18_950, 100);
System.out.println(a);                              // Fill[symbol=AAPL, priceTicks=18950, qty=100]
System.out.println(a.equals(b));                    // true
System.out.println(a == b);                         // false —— 引用比较，两个不同对象
Map<Fill, String> notes = new HashMap<>();
notes.put(a, "first");
System.out.println(notes.get(b));                   // first —— 内容相同的另一个对象也查得到
```

实测输出：

```
Fill[symbol=AAPL, priceTicks=18950, qty=100]
AAPL 100
true
false
true
first
```

和第 1 节 `ForgetfulFill` 的 `null` 对比：record 的 `equals`/`hashCode` 是自动配套生成的，不会漏。

### 例 2：进阶——校验、规范化、默认值、静态工厂

`examples/J01/J01Ex2.java`（节选）：

```java
record Order(long id, String symbol, Side side, long priceTicks, long qty) {
    Order {
        if (id <= 0) throw new IllegalArgumentException("id must be positive: " + id);
        if (priceTicks <= 0) throw new IllegalArgumentException("price must be positive: " + priceTicks);
        if (qty <= 0) throw new IllegalArgumentException("qty must be positive: " + qty);
        if (side == null) throw new NullPointerException("side");
        symbol = symbol.strip().toUpperCase();
    }
    long notionalTicks() { return Math.multiplyExact(priceTicks, qty); }
    Order(long id, String symbol, Side side, long priceTicks) { this(id, symbol, side, priceTicks, 1); }
    static Order parse(String line) { ... }
}
```

实测输出：

```
Order[id=7, symbol=AAPL, side=BUY, priceTicks=18950, qty=100]     <- " aapl " 被规范成 "AAPL"
1895000
Order[id=8, symbol=MSFT, side=SELL, priceTicks=41000, qty=1]       <- 4 参数构造器默认 qty=1
拒绝: id must be positive: 0
basket 里还是 1 单                                                  <- List.copyOf 的效果
basket.orders() 不可修改
```

这个例子体现了 record 的一个核心用法：**非法的值根本造不出来**。只要你拿到了一个 `Order` 对象，
它的 `qty` 一定 > 0，不需要在每个用到它的地方再检查一次。这叫「让非法状态无法表示」（make illegal states unrepresentable）。

### 例 3：贴近真实——聚合、复合 key、反射、浅不可变陷阱

`examples/J01/J01Ex3.java`（节选）：

```java
record BookKey(String symbol, Side side) {}       // 复合 key：以前要手写类，或拼字符串 "AAPL|BUY"

Map<BookKey, Long> qtyByBook = new TreeMap<>(Comparator.comparing(BookKey::symbol).thenComparing(BookKey::side));
for (String line : lines) {
    Fill f = Fill.parse(line);
    qtyByBook.merge(new BookKey(f.symbol(), f.side()), f.qty(), Long::sum);
}
```

实测输出：

```
BookKey[symbol=AAPL, side=BUY] -> 175
BookKey[symbol=AAPL, side=SELL] -> 30
BookKey[symbol=MSFT, side=BUY] -> 10
```

拼字符串当 key 是常见的偷懒做法（`symbol + "|" + side`）：它丢掉了类型信息，symbol 里恰好有 `|` 就会串，改字段顺序时没有编译器帮你检查。
用 `BookKey` record，编译器全程检查。

同一个文件的最后一段演示了陷阱（见第 5 节）。

---

## 5. 坑与限制

### 5.1 浅不可变（shallow immutability）

record 保证的是「**字段引用**不变」，**不**保证「引用指向的东西不变」。

```java
record Leaky(int[] data) {}
Leaky l = new Leaky(new int[]{1, 2, 3});
l.data()[0] = 99;        // 合法！数组内容被改了
```

实测：`l.data()` 变成 `[99, 2, 3]`。组件是 `ArrayList`、`Date`、`StringBuilder`、数组时都一样。
解决：构造时拷贝（`List.copyOf`），或者干脆用不可变类型（`List.of`、`String`、`long`）。

数组还有另一个坑：`equals` 对数组组件用的是 `Object.equals`，即**引用比较**。
`new Leaky(new int[]{99,2,3}).equals(l)` 是 `false`，哪怕内容一样（`J01Ex3` 里实测）。**别把数组放进 record 当组件**，用 `List<Long>` 或自己包一层。

### 5.2 `BigDecimal` 的 scale 会让 equals 失败

`new BigDecimal("1.0").equals(new BigDecimal("1.00"))` 是 `false`（scale 不同）。
record 的 `equals` 对引用组件用 `Objects.equals`，所以含 `BigDecimal` 的两个 record 可能「数值相同但不 equal」。
本 kit 按 CONVENTIONS 用 `long` 最小单位表示金额，就是为了回避这个问题；非用 `BigDecimal` 不可时，在紧凑构造器里 `stripTrailingZeros()` 或统一 `setScale`。

### 5.3 `float`/`double` 组件的 `NaN` 与 `-0.0`

生成的 `equals` 用 `Double.compare`，所以 `NaN` equals `NaN`（和 `==` 相反），而 `0.0` 不 equals `-0.0`。
这对「按内容比较」是合理的，但会让人意外。金额别用 `double`。

### 5.4 自己重写访问器要小心

允许重写访问器（必须 `public`，返回类型相同）。但如果让 `symbol()` 返回的东西和字段不同，
record 的 `equals`/`toString` 依旧按**字段**算，两者就不一致了。`java.lang.Record` 的 Javadoc 约定访问器应返回对应组件的值（编译器不强制，但违反约定会让人困惑）。
需要「加工后的视图」就另起一个方法名。

### 5.5 `toString` 会打印所有组件

含密码、令牌、个人信息的组件会被打进日志。要么重写 `toString`，要么别把这种东西放进 record。

### 5.6 不适合的场景

* 需要可变状态（计数器、累加器）：用普通类。
* 需要继承层次：record 不能 extends；但它可以 `implements` 一个 `sealed interface`——这正是 J02 的主题。
* 框架要求无参构造器 + setter（比如经典的 JPA 实体、部分老序列化框架）：record 不满足。
* 组件特别多（十几个）：构造时参数顺序容易错，考虑构建器（builder）模式。
* 版本兼容：给 record **增加组件**会改变构造器签名，二进制不兼容；公共 API 里的 record 要想清楚再发布。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。

* **`00_oa/oa01_job_chain/reference/JobChains.java`** —— 紧凑构造器做单行校验：
  ```java
  public record Job(int id, long runtimeSeconds, int nextId) {
      public Job {
          if (id <= 0) throw new MalformedInputException("job_id must be positive: " + id);
          if (runtimeSeconds < 0) throw new MalformedInputException("negative runtime: " + runtimeSeconds);
          ...
  ```
  同文件的 `Chain(int startJob, int lastJob, int count, long totalSeconds)` 带一个派生方法 `averageSeconds()`；
  `Ok(List<Chain> chains)`、`Malformed(String reason)` 是结果类型（J02 会讲它们怎么和 sealed 配合）。
* **`01_video/hc04_queue_mean_snapshot/reference/QueueEvents.java`** —— 防御性拷贝：
  ```java
  public record Correct(List<Long> contents) implements Event {
      public Correct { contents = List.copyOf(contents); } // 防御性拷贝；null 元素直接 NPE
  }
  ```
  `Push(long value)`、`Pop()`、`Query()` 是**零组件 record**，当作「只有类型、没有数据」的事件标签。
* **`01_video/hc05_market_order_book/reference/OrderBook.java`** —— 紧凑构造器做空值检查：
  ```java
  public record Limit(long id, Side side, long price, long qty) implements Command {
      public Limit { Objects.requireNonNull(side, "side"); }
  }
  ```
* **`01_video/hc03_recursive_sum/reference/RecursiveSum.java`** —— `Wide(long hi, long lo)`：record 里带静态常量 `ZERO` 和实例方法 `plus`/`merge`，是「record 当不可变数值类型」的完整例子。
* **`01_video/hc04_queue_mean_snapshot/reference/QueueMean.java`** —— `I128(long hi, long lo)`、`Mean(BigInteger numerator, long denominator)`；
  **`SharedMean.java`** 的 `Stat(long seq, int size, I128 sum)` 作为「发布给其他线程的不可变快照」，配合 `VarHandle` 原子替换（J16）。
* 几乎所有题的 `sealed interface` 下面挂的都是 record（`Poll`/`Msg`/`Op`/`Result`/`Instr`/`Event`/`Command`），见 J02。

---

## 7. 自测题

1. 下面的代码有什么问题？
   ```java
   record P(int x) { int y; }
   ```
2. 紧凑构造器里为什么不能写 `this.qty = qty;`？它在什么时候给字段赋值？
3. 为什么 `record Leaky(int[] data)` 被说成「浅不可变」？怎么改成真正不可变？
4. `record Fill(String symbol, long qty) {}` 编译后 `equals` 的方法体是什么样的？它为什么能和 `HashMap` 配合？
5. 以下两种写法有什么区别？什么时候后者更合适？
   `symbol + "|" + side` 当 Map key，对比 `record BookKey(String symbol, Side side)`。

<details><summary>答案</summary>

1. record 不能声明实例字段，编译错误 `field declaration must be static`。要加状态就加记录组件：`record P(int x, int y)`。
2. 紧凑构造器的末尾由编译器自动插入「把参数赋给同名字段」；你再写一次就是给 `final` 字段赋两次，编译器报错。
   要修改写入字段的值，改的是**参数**：`qty = Math.max(qty, 1);`，末尾自动把改后的参数写进字段。
3. record 只保证字段的引用不变；数组的元素可以随便改。改法：用 `List<Integer>` + 紧凑构造器里 `List.copyOf`；
   或在构造器里 `data = data.clone()`，并且访问器也返回克隆（要重写访问器）。更推荐直接换成不可变集合。
4. 方法体只有一条 `invokedynamic`，指向 `java.lang.runtime.ObjectMethods.bootstrap`，由它在运行时生成逐组件比较的代码。
   `equals` 与 `hashCode` 总是同时按全部组件生成，保证「equals 为真则 hashCode 相同」，所以放进 `HashMap` 不会像 `ForgetfulFill` 那样查不到。
5. 字符串拼接丢失类型、有分隔符冲突风险（symbol 本身含 `|`）、字段变化时没有编译检查、还要自己解析回来。
   record 是真正的类型：访问器有类型，`equals`/`hashCode` 自动正确。只有在 key 要序列化成文本（比如写进 Redis key）时，字符串才有存在理由，且应在边界处才拼。

</details>

---

## 8. 延伸阅读

* JEP 395 Records — https://openjdk.org/jeps/395 —— 读 Motivation 和 Description；里面解释了为什么「transparent carrier（透明载体）」是 record 的定位。
* JEP 359 Records (Preview) — https://openjdk.org/jeps/359 —— 第一版预览，能看到设计是怎么收敛的。
* JLS §8.10 Record Classes — https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.10 —— 所有规则的最终来源，包括紧凑构造器的精确定义。
* `java.lang.Record` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Record.html —— 第一段就是 equals/hashCode/toString 的语义约定。
* 下一课：J02 `sealed`，record 最常见的搭档。
