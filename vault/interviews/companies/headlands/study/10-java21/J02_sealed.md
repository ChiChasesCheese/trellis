# J02 · `sealed`：把「有哪几种」写进类型，让编译器替你数数

> 版本：Java 17 正式（JEP 409）。Java 15、16 是预览（JEP 360、JEP 397）。
> 本课所有可运行代码在 `study/10-java21/examples/J02/`。
> 前置知识：普通的 `interface` / `abstract class` / `extends` / `implements`；建议先读 J01（`record`），本课的例子大量用 record 做子类。
> 官方出处：JEP 409 Sealed Classes — https://openjdk.org/jeps/409 ；语言规范 §8.1.1.2 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.1.1.2

---

## 1. 先看痛点：Java 8 里「恰好这几种」只是一个口头约定

很多数据天然就是「**要么是 A，要么是 B，要么是 C，没有别的**」：

* 一次计算的结果：成功（带一个值）或失败（带一条错误信息）。
* 引擎发出的事件：成交、挂单、撤单、拒绝——就这四种。
* 一条指令：加载、存储、加法……

这种「固定几种、每种带不同数据」的结构，在类型理论里叫**和类型**（sum type）或**代数数据类型**（algebraic data type，ADT）。

Java 8 没有直接表达它的办法。你只能写一个 `interface Event`，再写几个实现类（完整代码：`examples/J02/J02Old.java`）：

```java
interface Event {}
static final class Trade implements Event { ... }
static final class Rested implements Event { ... }
static final class Cancelled implements Event { ... }

static String describe(Event e) {
    if (e instanceof Trade) {
        Trade t = (Trade) e;
        return "TRADE " + t.qty + "@" + t.price;
    } else if (e instanceof Rested) {
        ...
    } else if (e instanceof Cancelled) {
        ...
    } else {
        throw new IllegalStateException("unknown event: " + e);    // 兜底
    }
}
```

这段代码有两个根本性的问题：

**问题一：接口是开放的。** 任何人，在任何文件、任何包、甚至依赖你的另一个团队的代码里，都能再写一个 `class Rejected implements Event`。
`J02Old.java` 里真的这么做了：

```java
static final class Rejected implements Event {}
describe(new Rejected());   // 运行结果：IllegalStateException: unknown event: ...
```

**问题二：编译器不知道「一共几种」，所以没法帮你检查「处理全了没有」。** 那个 `else throw` 是人肉兜底：
一年后有人加了第四种事件，但忘了改 `describe`——编译照样通过，直到某天线上真的出现那种事件才炸。
这类 bug 的特点是：**离出错的原因（加了一个新类型）很远，出错的位置（某个角落的 if-else 链）又不会被编译器标红。**

用 `enum` 能解决「固定几种」，但 enum 的每个常量**只有一个实例、不能各带各的数据**（`Trade` 有价格和数量，`Cancelled` 只有一个 id）。
所以需要一种「像 enum 一样封闭，又像类一样各带各的字段」的东西。这就是 sealed。

| | 开放 `interface` | `enum` | `sealed interface` + `record` |
|---|---|---|---|
| 有哪几种 | 谁都能加 | 固定 | 固定（`permits` 列出） |
| 每种能带不同字段 | 能 | 不能（所有常量字段一样） | 能 |
| 每种能有多个实例 | 能 | 不能（每个常量一个） | 能 |
| 编译器能检查 switch 是否处理完 | 不能 | 能 | 能（J03 详讲） |

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
sealed interface Result permits Ok, Err {}
record Ok(long value) implements Result {}
record Err(String message) implements Result {}
```

* `sealed`：这个类型被「封印」了，**只有 `permits` 后面列出的类型**才允许直接继承/实现它。
* `permits A, B`：许可名单。
* 子类的名字出现在父类的名单里，**同时**子类自己也要写 `implements Result`——名单是双向确认，缺任何一边都不行。

`sealed` 可以修饰 `interface`、`class`、`abstract class`。

### 2.2 子类必须选一个修饰符

每个被许可的直接子类，**必须**明确写下面三个之一（否则编译错误 `sealed, non-sealed or final modifiers expected`）：

| 修饰符 | 含义 | 什么时候选 |
|---|---|---|
| `final` | 到此为止，不能再有子类 | 最常见。**record 和 enum 隐式就是 final，不用写** |
| `sealed` | 继续封闭：自己也要 `permits` 一份名单 | 层级有多层，例如「Update 指令」下面还有 15 种 |
| `non-sealed` | 在这里重新开放，任何人都能继承它 | 想留一个扩展点，例如「用户自定义指令」 |

`non-sealed` 是 Java 里少见的带连字符的关键字（上下文关键字，不影响你把变量叫 `sealed`）。

`examples/J02/J02Ex2.java` 把三种都用了一遍：

```java
sealed static abstract class Instrument { abstract String ticker(); }
static final class Stock extends Instrument { ... }                       // final
static sealed abstract class Option extends Instrument { ... }            // sealed：继续封闭
static final class CallOption extends Option {}
static final class PutOption extends Option {}
static non-sealed class Custom extends Instrument { ... }                  // non-sealed：重新开放
static class UserDefined extends Custom {}                                 // 合法，因为 Custom 是 non-sealed
```

### 2.3 什么时候可以省略 `permits`

如果所有子类和父类**在同一个 `.java` 文件里**，可以不写 `permits`，编译器把同文件里直接继承它的类自动当成名单。
`J02Ex2` 的 `Instrument` 就没写 `permits`。

建议：**子类分散在多个文件时一定要写 `permits`**（强制的）；子类都在同一个文件时可省略，但显式写出来读代码的人更容易看懂「一共几种」。
本 kit 的参考解全部显式写了 `permits`。

### 2.4 位置限制

* 子类必须和父类在**同一个模块**里；如果没用模块系统（`module-info.java`），就是在**同一个包**里。
  （这是为了保证「封印」真的封得住——名单里的类你要么都能看见，要么压根不是同一个团队的代码。）
* 许可的子类必须**直接**继承父类。
* 匿名类和局部类**不能**继承 sealed 类型（实测错误：`anonymous classes must not extend sealed classes` / `local classes must not extend sealed classes`）。
  所以 `new Result() { ... }` 不行；lambda 也不行（本来 sealed interface 就不能是函数式接口的目标）。
* 一个 `sealed` 类型必须至少有一个子类（`sealed class must have subclasses`）。

### 2.5 泛型和 enum

* sealed 接口可以带类型参数：`sealed interface Either<L, R> permits Left, Right {}`，子类是 `record Left<L, R>(L value) implements Either<L, R>`。本 kit 的 `Poll<T>`、`Trampoline<T>` 都是这样。
* enum 隐式 final，可以出现在 `permits` 里：`sealed interface Signal permits Tick, Bar {}` + `enum Tick implements Signal { UP, DOWN }`。

### 2.6 分层：sealed 接口继承 sealed 接口

```java
sealed interface Instr permits Update, Query {}
sealed interface Update extends Instr permits And, Or, Xor /* ... 共 15 个 */ {}
sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}
```

这是 `RegisterSim.java` 的真实结构。好处：既可以对 `Instr` 做一个大 switch，也可以只对 `Update` 做 switch（只需处理 15 种）。
中间层接口必须是 `sealed` 或 `non-sealed`，不能是 `final`（接口不能 final；实测写成普通 `interface V extends U` 报 `sealed or non-sealed modifiers expected`）。

---

## 3. 编译器和 JVM 到底做了什么

### 3.1 class 文件里多了一个 `PermittedSubclasses` 属性

`javap -v` 看 `sealed interface Result permits Ok, Err` 的 class 文件（实测）：

```
PermittedSubclasses:
  J02Ex1$Ok
  J02Ex1$Err
```

这是 Java 17 起 class 文件格式新增的属性：一个类名列表。**这份名单在运行时由 JVM 自己检查**，不是只有 `javac` 才管：

* 你用 `javac` 编译一个不在名单里的子类，`javac` 报错：
  ```
  error: class is not allowed to extend sealed class: S (as it is not listed in its 'permits' clause)
  ```
* 你绕过 `javac`（比如用字节码工具生成一个 class，或者只重新编译父类、留着旧的子类 class 文件），JVM 在**加载子类**的时候拒绝：
  ```
  java.lang.IncompatibleClassChangeError: class Y cannot implement sealed interface S
  ```
  （实测：先编译 `S permits X, Y`，再把 `S` 改成 `permits X` 单独重新编译，不动旧的 `Y.class`，运行 `new Y()` 就得到上面的异常。）

所以 sealed 不是编译期的君子协定，而是 JVM 强制执行的规则。反射也能看到它：

```java
Result.class.isSealed();                         // true
Result.class.getPermittedSubclasses();           // [class J02Ex1$Ok, class J02Ex1$Err]
```

### 3.2 `non-sealed` 在 class 文件里没有痕迹

`non-sealed` 只存在于源码。编译后的 `Custom` 类没有 `PermittedSubclasses`、也没有 `ACC_FINAL`，和一个普通的可继承类一模一样。
编译器靠的是「父类有名单，Custom 在名单里，Custom 自己没有名单也不 final」这个事实，在编译 switch 时知道 `Custom` 下面可能有任意多后代。

### 3.3 sealed 对 `switch` 的影响（预告，J03 详讲）

`javac` 在检查 `switch` 是否「穷尽」（exhaustive）时，会从 sealed 类型出发**递归展开 `PermittedSubclasses`**：
`switch (result)` 只要有 `case Ok` 和 `case Err`，编译器就知道没有第三种了，不需要 `default`。
漏掉一种就是编译错误（实测）：

```
error: the switch expression does not cover all possible input values
```

这就是 sealed 的**真正价值**：它让「新增一个变体」变成一个**编译期事件**——把 `permits` 加一项，所有没处理它的 `switch` 当场报错，而不是线上炸。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——两种结果

`examples/J02/J02Ex1.java`：

```java
sealed interface Result permits Ok, Err {}
record Ok(long value) implements Result {}
record Err(String message) implements Result {}

static String show(Result r) {
    return switch (r) {              // 没有 default：编译器知道只有 Ok 和 Err
        case Ok ok -> "ok " + ok.value();
        case Err err -> "err " + err.message();
    };
}
```

实测输出：

```
ok 42
err boom
true               <- Result.class.isSealed()
[Ok, Err]          <- getPermittedSubclasses() 的简单类名
false              <- Ok.class.isSealed()：record 是隐式 final，不是 sealed
```

对比 Java 8 的 `Optional<T>` / 返回 `null` / 抛异常来表示失败：`Result` 把「可能失败」写进了返回类型，调用方**不得不**处理 `Err`（否则 switch 编译不过）。

### 例 2：进阶——三种修饰符、泛型、enum

`examples/J02/J02Ex2.java` 实测输出：

```
AAPL -> stock
AAPL240621C00200000 -> call
AAPL240621C00200000 -> put
CUSTOM -> custom              <- UserDefined 是 Custom 的后代，被 case Custom 覆盖
left:bad
right:7
tick UP
```

这个例子里有一个值得记住的细节：`Option` 一开始我写成了普通的 `sealed class`（非抽象），`switch` 立刻编译失败，
报 `does not cover all possible input values`。原因：`Option` **自己**也能被 `new` 出来，它就是第四种东西，需要一个 `case Option`。
改成 `abstract` 后，`Option` 不再有直接实例，只有 `CallOption`、`PutOption` 两种，switch 就穷尽了。
**sealed 的父类如果不是抽象的，它自己也算一种变体。**（接口天然没有直接实例，所以 sealed interface 没有这个问题。）

### 例 3：贴近真实——引擎的 Command / Event

`examples/J02/J02Ex3.java`：

```java
sealed interface Command permits Limit, Cancel { long id(); }       // 接口里可以放所有变体共有的方法
record Limit(long id, Side side, long px, long qty) implements Command {}
record Cancel(long id) implements Command {}

sealed interface Event permits Rested, Cancelled, Rejected {}
record Rested(long id, long px, long qty) implements Event {}
record Cancelled(long id) implements Event {}
record Rejected(long id, String why) implements Event {}
```

两棵层级：输入（命令）和输出（事件）。引擎的 `execute(Command)` 是唯一的入口，所有「按命令种类分派」都集中在一处 switch；
`render(Event)` 是输出的唯一出口。以后加一种命令，编译器会逼你把这两处（以及所有别的按种类分派的地方）都补上。

实测输出：

```
REST id=1 px=100 qty=5
REJECT id=2 why=qty
CANCEL id=1
REJECT id=9 why=unknown id
2 种命令, 3 种事件
```

这正是 hc05（订单簿）的结构：`OrderBook.Command permits Limit, Market, Cancel, Modify`、`Event permits Trade, Rested, Cancelled, Modified, Rejected`。

---

## 5. 坑与限制

### 5.1 sealed 保护的是「新增变体时的 switch」，不是「新增方法」

经典的「表达式问题」（expression problem）：

* **面向对象（开放继承）**：新增一种子类很容易，新增一个「对所有子类都做的操作」要改所有子类。
* **sealed + switch（和类型）**：新增一个操作很容易（再写一个 switch），新增一种变体要改所有 switch——但编译器会**列出**所有要改的地方。

所以 sealed 适合「变体很少变、操作经常加」的场景（协议消息、命令、事件、AST）。
变体经常由别人扩展的场景（插件、驱动）应该用开放接口。

### 5.2 `permits` 不是越长越好

本 kit 的 `RegisterSim.Update` 有 15 个子类，写起来已经很啰嗦。如果变体多到几十种，考虑把它们分层（`Instr` → `Update`/`Query`），或者干脆换成 `enum` + 策略。

### 5.3 子类要么同包要么同模块

库作者想让用户**实现**你的接口（比如你发布一个 `Handler`），就不能用 sealed；
库作者想让用户**只能消费**你返回的类型（比如你返回 `sealed interface Result`），sealed 正好。

### 5.4 二进制兼容

给 `permits` 加一项会让所有「旧的 switch」在**重新编译**时报错——这正是目的；但**不重新编译**直接运行旧的 class 文件，旧 switch 遇到新变体会在运行时抛 `MatchException`（J03 讲）。
所以 sealed 层级放在公共 API 里时，加变体算「不兼容变更」。

### 5.5 `final` 与 record 不要重复写

`final record Ok(...)` 不是错误，但多余（record 隐式 final）。`final enum` 同理。

### 5.6 sealed 不等于不可变

sealed 管的是「**类型**有几种」，不管「对象的字段能不能改」。可变性靠 `record` / `final` 字段，两者互相独立。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。几乎每道参考解都有一棵 sealed 树。

* **`00_oa/oa01_job_chain/reference/JobChains.java`**
  ```java
  public sealed interface Outcome permits Ok, Malformed {}
  public record Ok(List<Chain> chains) implements Outcome {}
  public record Malformed(String reason) implements Outcome {}
  ```
  「分析可能成功也可能失败」→ 返回类型就是答案；`render` 对它做 switch，没有 `default`。
* **`01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java`**
  ```java
  public sealed interface Poll<T> permits Ready, Pending, Done {}      // 对外
  private sealed interface Msg<T> permits Item, End, Failed {}         // 内部队列里的消息
  ```
  `private sealed interface` 说明 sealed 也可以只在类内部使用。`tryNext()` 的返回值有三种：有值、暂无、已结束——全部写进类型里。
* **`01_video/hc03_recursive_sum/reference/RecursiveSum.java`**
  `SumResult permits Ok, Overflow`（注释写着「`sealed` 的 `Ok/Overflow` 把『可能溢出』写进类型，调用方的 switch 不处理 `Overflow` 就编译不过」）；
  `Trampoline<T> permits Done, More`（注释：「因为 Trampoline 是 sealed 的，switch 不需要 default：新增一种变体时这里会编译报错」）。
* **`01_video/hc04_queue_mean_snapshot/reference/QueueEvents.java`**
  `Event permits Push, Pop, Query, Correct` 和 `Answer permits Value, Empty`。
* **`01_video/hc05_market_order_book/reference/OrderBook.java`**
  `Command permits Limit, Market, Cancel, Modify`（接口里还声明了 `long id();`，所有变体共有）、`Event permits Trade, Rested, Cancelled, Modified, Rejected`。
* **`01_video/hc06_cpu_register_bitwise/reference/RegisterSim.java`**
  三层 sealed：`Instr` → `Update`（15 种）/ `Query`（3 种）。`apply(int reg, Update u)` 只接受 `Update`，注释：「为什么 switch 没有 default：`Update` 是 sealed，编译器知道 15 个实现类一个不少」。
* **`01_video/hc08_order_sequence_api/reference/OrderSequence.java`**
  `Op permits Put, Delete, CountUpTo, QtyUpTo, IdAt`、`Result permits Ok, Num, Err`。

---

## 7. 自测题

1. 下面的代码为什么编译不过？应该怎么改？
   ```java
   sealed interface Shape permits Circle, Square {}
   record Circle(double r) implements Shape {}
   class Square implements Shape {}
   ```
2. `sealed`、`final`、`non-sealed` 分别什么时候用？record 为什么不用写 `final`？
3. 为什么说「sealed 的父类如果不是抽象类，它自己也算一种变体」？举例说明会导致什么编译错误。
4. 有人说「sealed 只是编译器的检查，运行时没用」。怎么反驳？写出两个运行时可观察到的证据。
5. 在什么场景下你应该选开放的 `interface` 而不是 `sealed`？

<details><summary>答案</summary>

1. `Square` 是普通 `class`，没有 `final` / `sealed` / `non-sealed`，编译错误 `sealed, non-sealed or final modifiers expected`。改成 `final class Square implements Shape {}`（或者改成 record）。
2. `final`：到此为止（最常见）；`sealed`：这一层还要继续分几种；`non-sealed`：特意在此处留扩展点。record 与 enum 语言规定隐式 `final`，不用写。
3. 如果 `sealed class Option` 不是 `abstract`，`new Option()` 合法，所以 `Option` 本身是一个具体变体。
   `switch` 若只有 `case CallOption`、`case PutOption`，编译器报 `the switch expression does not cover all possible input values`，要么补 `case Option`，要么把 `Option` 改成 `abstract`。
4. 证据一：class 文件有 `PermittedSubclasses` 属性，`javap -v` 能看到；反射 `Class.isSealed()` / `getPermittedSubclasses()` 返回真值。
   证据二：绕过 javac，让一个不在名单里的子类被加载，JVM 抛 `IncompatibleClassChangeError: class Y cannot implement sealed interface S`。
5. 需要让使用者（别的团队、插件、测试替身）自己提供实现的场合，比如 `Comparator`、`Runnable`、`Handler`；以及变体很多且经常新增时。sealed 适合「变体由你控制、几乎不变」的场合。

</details>

---

## 8. 延伸阅读

* JEP 409 Sealed Classes — https://openjdk.org/jeps/409 —— 读 Motivation 和 Description；Description 里把三种修饰符和位置规则都列全了。
* JEP 360 Sealed Classes (Preview) — https://openjdk.org/jeps/360 —— 初版设计，对比能看出后来为什么加了「同包/同模块」的规则。
* JLS §8.1.1.2 sealed / non-sealed — https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.1.1.2 —— 规则的权威来源。
* JVMS §4.7 Attributes（在页面里搜 `PermittedSubclasses`）— https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7 —— class 文件格式里这条记录长什么样。
* 下一课：J03 `switch` 模式匹配——sealed 的价值要靠它兑现。
