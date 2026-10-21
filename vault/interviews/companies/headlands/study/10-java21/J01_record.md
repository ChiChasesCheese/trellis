# J01 · `record`：一行声明一个不可变的值对象

> 版本：Java 16 正式（14、15 为预览）。可运行代码：`examples/J01/`。
> 前置：会写普通类、构造器、`getXxx()`，知道 `equals`/`hashCode` 大意即可，第 1 节从零讲。

---

## 1. 先看痛点：Java 8 里「装三个字段」要写多少字

交易系统里到处是「一包数据」：一笔成交 `(代码, 价格, 数量)`、一条订单、一行解析好的 CSV。
它们只是数据，创建后不再变，内容相同就该视为同一个东西——这叫**值对象**（value object）。

Java 8 里写三字段的值对象（`examples/J01/J01Old.java`）：

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

三个字段约 30 行。每多一个字段要同步改 **7 处**：字段、构造器参数、赋值、getter、`equals`、`hashCode`、`toString`；漏改不报编译错，只会运行时悄悄出错。

### 样板为什么必须存在

`private final` 字段保证值稳定；构造器一次设好所有字段；getter 让外部读到私有字段；默认 `equals` 是**引用比较**（内容相同也不等）；默认 `toString` 输出 `J01Old$Fill@1b6d3586`，看不出内容；`hashCode` 的坑见下。

最阴险的是 `equals`/`hashCode`。`J01Old.java` 里有个忘记重写它们的 `ForgetfulFill`：

```java
Map<ForgetfulFill, String> m = new HashMap<>();
m.put(new ForgetfulFill("AAPL", 100), "first");
m.get(new ForgetfulFill("AAPL", 100));   // 运行结果：null
```

内容一样的对象却查不到。原因：`HashMap` 先用 `hashCode()` 选桶（bucket）；默认 `hashCode()` 基于对象身份，两个对象几乎必落在不同桶，根本走不到 `equals`。

不能省、易写错、又长——record 就是为此而生。

---

## 2. 语法逐条讲

### 2.1 最简形式

```java
record Fill(String symbol, long priceTicks, long qty) {}
```

括号里的东西叫**记录组件**（record component），一次做三件事：声明字段、构造器参数、访问器。

访问器叫 `symbol()`（**没有 get 前缀**），`equals` 自动按内容比较，字段永远是 `private final`，改不了。

```java
Fill a = new Fill("AAPL", 18_950, 100);
a.symbol();            // "AAPL"
a.toString();          // Fill[symbol=AAPL, priceTicks=18950, qty=100]
a.equals(new Fill("AAPL", 18_950, 100));   // true
```

> `toString()` 格式是 `Fill[symbol=AAPL, ...]`（方括号）。规范只要求包含所有组件名和值，不固定格式，别拿它当序列化格式。

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

| 想做的事 | 结果 | 编译器报错 |
|---|---|---|
| 声明实例字段 | 不行 | `field declaration must be static (consider replacing field with record component)` |
| `extends` 别的类 | 不行（record 已经隐式继承了 `java.lang.Record`，Java 只有单继承） | `'{' expected` |
| 被别的类继承 | 不行，record 隐式是 `final` | — |
| 在方法里给字段赋值 | 不行，字段是 `final` | `cannot assign a value to final variable x` |
| 额外构造器不先调用 `this(...)` | 不行 | `constructor is not canonical, so its first statement must invoke another constructor of class P` |

这些限制是**故意**的：record 的全部状态就是括号里的组件，编译器才敢自动生成 `equals`/`hashCode`/`toString`，读者也一眼知道状态不多不少。

### 2.3 规范构造器与紧凑构造器

每个 record 都有一个**规范构造器**（canonical constructor）：参数列表与组件完全一致。不写则编译器生成，内容就是「把每个参数赋给同名字段」。

要在赋值前**校验**或**规范化**，有两种写法：

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

第 6 节的 `JobChains.Job` 就是用它在构造时拦下单行非法输入。

### 2.4 防御性拷贝：组件是集合时

```java
record Basket(String name, List<Order> orders) {
    Basket {
        orders = List.copyOf(orders);   // 拷贝一份不可修改的 List；null 元素会抛 NPE
    }
}
```

不拷贝的话，调用方仍持有原 `ArrayList`，随时能往里加东西，`Basket` 就被悄悄改了。拷贝后往原列表再加一单，`basket.orders().size()` 仍是 1（`J01Ex2`）。

### 2.5 局部 record 与泛型 record

record 可声明在**方法内部**（局部 record，隐式 static），适合「这个方法里临时要个小结构」：

```java
static long topNotional(List<String> lines) {
    record Row(String sym, long px, long qty) {}      // 只在这个方法里可见
    return lines.stream().map(l -> l.split(","))
            .map(t -> new Row(t[0], Long.parseLong(t[1]), Long.parseLong(t[2])))
            .mapToLong(r -> r.px() * r.qty()).max().orElse(0);
}
```

泛型也行：`record Tagged<T>(T value, boolean valid) {}`。

---

## 3. 编译器和 JVM 到底做了什么

用 `javap`（JDK 自带反编译器）看 `record Fill(String symbol, long priceTicks, long qty) {}` 编译出的类（略有删减）：

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

1. **`final class ... extends java.lang.Record`**：所有 record 的父类是 `java.lang.Record`（几乎什么都不放的抽象类）；类是 `final`，不能被继承。
2. **每个组件一个 `private final` 字段**。
3. **规范构造器**：访问级别与 record 本身一致（`public record` 的构造器就是 `public`）。
4. **每个组件一个 `public` 访问器**，名字就是组件名。
5. **`toString`/`hashCode`/`equals` 是 `final` 的，实现只有一条 `invokedynamic`**：编译器没把 30 行 `equals` 展开进 class 文件，而是指向引导方法（bootstrap method）`java.lang.runtime.ObjectMethods.bootstrap`。
6. 类文件多了 `Record` 属性，登记每个组件的名字和类型；反射的 `Class.isRecord()`、`getRecordComponents()` 读的就是它（`J01Ex3`：`[String symbol, Side side, long priceTicks, long qty]`）。

### 什么是 `invokedynamic`，为什么 record 用它

普通调用指令（`invokevirtual` 等）在编译时就写死了调用哪个方法。`invokedynamic` 则是：**第一次执行时**，JVM 调用指定的引导方法，由它**现场**生成真正要执行的代码（方法句柄 `MethodHandle`），之后这条指令直连那段代码。

record 的引导方法拿到：record 类、组件名列表 `"symbol;priceTicks;qty"`、各字段 getter 句柄，据此造出 `equals`/`hashCode`/`toString`。好处：

* class 文件小：不管多少组件，`equals` 都只占一条指令。
* JDK 以后想换更快的生成方式，只改引导方法，你的代码不用重编译。
* J03 的模式匹配 `switch` 用同一套机制。

生成的 `equals`：先 `instanceof` 同一 record 类型，再逐组件比较——`int`/`long` 直接比，`float`/`double` 用 `Float.compare`/`Double.compare`，引用类型用 `Objects.equals`。`hashCode` 组合各组件哈希，规范只要求「相同内容 → 相同哈希」，不规定公式。

---

## 4. 三个例子（由浅入深）

### 例 1：声明、读取、比较、当 Map 的 key

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

输出：

```
Fill[symbol=AAPL, priceTicks=18950, qty=100]
AAPL 100
true
false
true
first
```

对比第 1 节 `ForgetfulFill` 的 `null`：record 的 `equals`/`hashCode` 自动配套，不会漏。

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

输出：

```
Order[id=7, symbol=AAPL, side=BUY, priceTicks=18950, qty=100]     <- " aapl " 被规范成 "AAPL"
1895000
Order[id=8, symbol=MSFT, side=SELL, priceTicks=41000, qty=1]       <- 4 参数构造器默认 qty=1
拒绝: id must be positive: 0
basket 里还是 1 单                                                  <- List.copyOf 的效果
basket.orders() 不可修改
```

这是 record 的核心用法：**非法的值根本造不出来**。拿到 `Order` 就知道 `qty > 0`，不必处处重检。这叫「让非法状态无法表示」（make illegal states unrepresentable）。

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

输出：

```
BookKey[symbol=AAPL, side=BUY] -> 175
BookKey[symbol=AAPL, side=SELL] -> 30
BookKey[symbol=MSFT, side=BUY] -> 10
```

拼字符串当 key（`symbol + "|" + side`）会丢类型信息，symbol 含 `|` 就串，改字段顺序时编译器也不管。`BookKey` record 全程受编译器检查。

---

## 5. 坑与限制

### 5.1 浅不可变（shallow immutability）

record 保证的是「**字段引用**不变」，**不**保证「引用指向的东西不变」。

```java
record Leaky(int[] data) {}
Leaky l = new Leaky(new int[]{1, 2, 3});
l.data()[0] = 99;        // 合法！数组内容被改了
```

`l.data()` 变成 `[99, 2, 3]`。组件是 `ArrayList`、`Date`、`StringBuilder`、数组时都一样。解决：构造时拷贝（`List.copyOf`），或直接用不可变类型（`List.of`、`String`、`long`）。

数组还有个坑：`equals` 对数组组件是 `Object.equals`，即**引用比较**，`new Leaky(new int[]{99,2,3}).equals(l)` 为 `false`，哪怕内容一样。**别把数组放进 record**，用 `List<Long>` 或自己包一层。

### 5.2 `BigDecimal` 的 scale 会让 equals 失败

record 的 `equals` 对引用组件用 `Objects.equals`，所以含 `BigDecimal` 的两个 record 可能「数值相同但不 equal」。所以金额用 `long` 最小单位；非用 `BigDecimal` 不可，就在紧凑构造器里 `stripTrailingZeros()` 或统一 `setScale`。

### 5.3 `float`/`double` 组件的 `NaN` 与 `-0.0`

这对「按内容比较」合理但易让人意外。金额别用 `double`。

### 5.4 自己重写访问器要小心

允许重写访问器（必须 `public`、返回类型相同）。但若让 `symbol()` 返回的值与字段不同，`equals`/`toString` 仍按**字段**算，两者就不一致了。约定访问器应返回对应组件的值（编译器不强制）；要「加工后的视图」就另起方法名。

### 5.5 `toString` 会打印所有组件

含密码、令牌、个人信息的组件会被打进日志。要么重写 `toString`，要么别把这种东西放进 record。

### 5.6 不适合的场景

* 需要可变状态（计数器、累加器）：用普通类。
* 需要继承层次：record 不能 extends；但它可以 `implements` 一个 `sealed interface`——这正是 J02 的主题。
* 框架要求无参构造器 + setter（比如经典的 JPA 实体、部分老序列化框架）：record 不满足。
* 组件特别多（十几个）：构造时参数顺序容易错，考虑构建器（builder）模式。
* 版本兼容：给 record **增加组件**会改变构造器签名，二进制不兼容；公共 API 里的 record 要想清楚再发布。

---

## 6. 真实代码里的 record
* **`JobChains`**（job chain 题）—— 紧凑构造器做单行校验：
  ```java
  public record Job(int id, long runtimeSeconds, int nextId) {
      public Job {
          if (id <= 0) throw new MalformedInputException("job_id must be positive: " + id);
          if (runtimeSeconds < 0) throw new MalformedInputException("negative runtime: " + runtimeSeconds);
          ...
  ```
  同文件的 `Chain(int startJob, int lastJob, int count, long totalSeconds)` 带派生方法 `averageSeconds()`；`Ok(List<Chain>)`、`Malformed(String)` 是结果类型（J02 讲它们怎么配合 sealed）。
* **`QueueEvents`** —— 防御性拷贝：
  ```java
  public record Correct(List<Long> contents) implements Event {
      public Correct { contents = List.copyOf(contents); } // 防御性拷贝；null 元素直接 NPE
  }
  ```
  `Push(long value)`、`Pop()`、`Query()` 是**零组件 record**，当「只有类型、没有数据」的事件标签。
* **`OrderBook`** —— 紧凑构造器做空值检查：
  ```java
  public record Limit(long id, Side side, long price, long qty) implements Command {
      public Limit { Objects.requireNonNull(side, "side"); }
  }
  ```
* **`RecursiveSum`** —— `Wide(long hi, long lo)`：带静态常量 `ZERO` 和实例方法 `plus`/`merge`，是「record 当不可变数值类型」的完整例子。
* **`QueueMean`/`SharedMean`** —— `I128(long hi, long lo)`、`Mean(BigInteger numerator, long denominator)`；`Stat(long seq, int size, I128 sum)` 是「发布给其他线程的不可变快照」，配 `VarHandle` 原子替换（J16）。
* 几乎所有 `sealed interface` 下挂的都是 record（`Poll`/`Msg`/`Op`/`Result`/`Instr`/`Event`/`Command`）。

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

1. record 不能声明实例字段，报 `field declaration must be static`。要加状态就加组件：`record P(int x, int y)`。
2. 紧凑构造器末尾由编译器自动插入「参数赋给同名字段」；你再写一次就是给 `final` 字段赋两次。要改写入值，改的是**参数**：`qty = Math.max(qty, 1);`。
   或在构造器里 `data = data.clone()`，并且访问器也返回克隆（要重写访问器）。更推荐直接换成不可变集合。
4. 方法体只有一条 `invokedynamic`，指向 `java.lang.runtime.ObjectMethods.bootstrap`，由它在运行时生成逐组件比较的代码。
   `equals` 与 `hashCode` 总是同时按全部组件生成，保证「equals 为真则 hashCode 相同」，所以放进 `HashMap` 不会像 `ForgetfulFill` 那样查不到。
5. 字符串拼接丢失类型、有分隔符冲突风险（symbol 本身含 `|`）、字段变化时没有编译检查、还要自己解析回来。
   record 是真正的类型：访问器有类型，`equals`/`hashCode` 自动正确。只有 key 要序列化成文本（如 Redis key）时字符串才有理由，且只在边界处拼。

</details>

「延伸」J02 `sealed`：record 最常见的搭档。
