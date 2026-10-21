# J02 · `sealed`：把「有哪几种」写进类型，让编译器替你数数

> 版本：Java 17 正式（15、16 为预览）。可运行代码：`examples/J02/`。
> 前置：普通的 `interface` / `abstract class` / `extends` / `implements`；建议先读 J01（`record`），本课大量用 record 做子类。

---

## 1. 先看痛点：Java 8 里「恰好这几种」只是一个口头约定

很多数据天然是「**要么 A、要么 B、要么 C，没有别的**」：计算结果（成功带值 / 失败带错误信息）、引擎事件（成交、挂单、撤单、拒绝）、一条指令（加载、存储、加法……）。

这种「固定几种、每种带不同数据」的结构叫**和类型**（sum type），也叫代数数据类型（ADT）。

Java 8 只能写开放的 `interface Event` 加几个实现类（`examples/J02/J02Old.java`）：

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

有两个根本问题。

**一，接口是开放的。** 任何人在任何文件、任何包、别的团队的代码里都能再写 `class Rejected implements Event`（`J02Old.java`）：

```java
static final class Rejected implements Event {}
describe(new Rejected());   // 运行结果：IllegalStateException: unknown event: ...
```

**二，编译器不知道「一共几种」，没法检查「处理全了没有」。** 那个 `else throw` 是人肉兜底：一年后有人加了第四种事件却忘改 `describe`，编译照样过，直到线上炸。这类 bug 离原因（加了新类型）很远，出错处（某角落的 if-else 链）也不会被标红。

`enum` 能固定几种，但每个常量只有一个实例、不能各带各的数据。我们要「像 enum 一样封闭，又像类一样各带字段」的东西——sealed。

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

同一个 `.java` 文件里的子类可省略 `permits`，编译器自动把同文件里直接继承它的类当名单（`J02Ex2` 的 `Instrument`）。子类分散在多个文件时必须写；即使可省，显式写出更易读。

### 2.4 位置限制

* 子类与父类须在**同一模块**；没用模块系统就是**同一个包**——这样「封印」才封得住。
* 许可的子类必须**直接**继承父类。
* 匿名类、局部类、lambda 都不能继承/实现 sealed 类型（`anonymous classes must not extend sealed classes`）。
* `sealed` 类型至少要有一个子类。

### 2.5 泛型和 enum

* sealed 接口可带类型参数：`sealed interface Either<L, R> permits Left, Right {}`，子类 `record Left<L, R>(L value) implements Either<L, R>`。
* enum 隐式 final，可以出现在 `permits` 里：`sealed interface Signal permits Tick, Bar {}` + `enum Tick implements Signal { UP, DOWN }`。

### 2.6 分层：sealed 接口继承 sealed 接口

```java
sealed interface Instr permits Update, Query {}
sealed interface Update extends Instr permits And, Or, Xor /* ... 共 15 个 */ {}
sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}
```

这是真实指令集的结构（15 种更新 + 3 种查询）。好处：可对 `Instr` 做大 switch，也可只对 `Update` 做（只处理 15 种）。中间层接口必须是 `sealed` 或 `non-sealed`（接口不能 `final`）。

---

## 3. 编译器和 JVM 到底做了什么

### 3.1 class 文件里多了一个 `PermittedSubclasses` 属性

`javap -v` 看 `sealed interface Result permits Ok, Err`：

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
  （先编译 `S permits X, Y`，再把 `S` 改成 `permits X` 单独重编译、保留旧 `Y.class`，运行 `new Y()` 即得此异常。）

所以 sealed 是 JVM 强制的规则，不是君子协定；反射也能看到：

```java
Result.class.isSealed();                         // true
Result.class.getPermittedSubclasses();           // [class J02Ex1$Ok, class J02Ex1$Err]
```

### 3.2 `non-sealed` 在 class 文件里没有痕迹

`non-sealed` 只存在于源码：编译后的 `Custom` 既没有 `PermittedSubclasses` 也没有 `ACC_FINAL`，和普通可继承类一样。编译器靠「父类有名单、Custom 在名单里、自己无名单也不 final」得知 Custom 下可能有任意后代。

### 3.3 sealed 对 `switch` 的影响（预告，J03 详讲）

`javac` 检查 `switch` 是否**穷尽**（exhaustive）时，会从 sealed 类型出发**递归展开 `PermittedSubclasses`**：有 `case Ok` 和 `case Err` 就知道没有第三种，不需要 `default`；漏一种就是编译错误：

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

输出：

```
ok 42
err boom
true               <- Result.class.isSealed()
[Ok, Err]          <- getPermittedSubclasses() 的简单类名
false              <- Ok.class.isSealed()：record 是隐式 final，不是 sealed
```

对比返回 `null` / 抛异常表示失败：`Result` 把「可能失败」写进返回类型，调用方**不得不**处理 `Err`。

### 例 2：进阶——三种修饰符、泛型、enum

`examples/J02/J02Ex2.java` 输出：

```
AAPL -> stock
AAPL240621C00200000 -> call
AAPL240621C00200000 -> put
CUSTOM -> custom              <- UserDefined 是 Custom 的后代，被 case Custom 覆盖
left:bad
right:7
tick UP
```

细节：`Option` 若写成普通（非抽象）`sealed class`，switch 立刻编译失败（`does not cover all possible input values`），因为 `Option` 自己也能 `new`，是第四种变体，需要 `case Option`。改成 `abstract` 后只剩 `CallOption`、`PutOption`，就穷尽了。**sealed 父类若不是抽象的，它自己也算一种变体**（接口天然没有直接实例，无此问题）。

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

两棵层级：输入（命令）和输出（事件）。`execute(Command)` 是唯一入口，所有按命令种类分派集中在一处 switch；`render(Event)` 是唯一出口。以后加一种命令，编译器逼你补全所有分派点。

输出：

```
REST id=1 px=100 qty=5
REJECT id=2 why=qty
CANCEL id=1
REJECT id=9 why=unknown id
2 种命令, 3 种事件
```

这正是订单簿题的结构：`Command permits Limit, Market, Cancel, Modify`、`Event permits Trade, Rested, Cancelled, Modified, Rejected`。

---

## 5. 坑与限制

### 5.1 sealed 保护的是「新增变体时的 switch」，不是「新增方法」

经典的**表达式问题**（expression problem）：开放继承里加子类容易，但加一个对所有子类的操作要改全部子类；sealed + switch 里加操作容易（再写个 switch），加变体要改所有 switch——但编译器会**列出**所有要改处。

所以 sealed 适合「变体少变、操作常加」（协议消息、命令、事件、AST）；变体常由别人扩展（插件、驱动）就该用开放接口。

### 5.2 `permits` 不是越长越好

指令集的 `Update` 有 15 个子类已经啰嗦；变体到几十种就分层（`Instr` → `Update`/`Query`），或换 `enum` + 策略。

### 5.3 要让用户实现，就别用 sealed

要让用户**实现**你的接口（如 `Handler`）就不能用 sealed；只想让用户**消费**你返回的类型（如 `sealed interface Result`），sealed 正好。

### 5.4 二进制兼容

给 `permits` 加一项会让旧 switch 在**重新编译**时报错（正是目的）；但**不重编译**直接跑旧 class，旧 switch 遇到新变体会抛 `MatchException`（J03）。所以公共 API 里加变体是不兼容变更。

### 5.5 `final` 与 record 不要重复写

`final record Ok(...)` 不是错误，但多余（record 隐式 final）。`final enum` 同理。

### 5.6 sealed 不等于不可变

sealed 管的是「**类型**有几种」，不管「对象的字段能不能改」。可变性靠 `record` / `final` 字段，两者互相独立。

---

## 6. 真实代码里的 sealed

几乎每道参考解都有一棵 sealed 树。

* **`JobChains`**
  ```java
  public sealed interface Outcome permits Ok, Malformed {}
  public record Ok(List<Chain> chains) implements Outcome {}
  public record Malformed(String reason) implements Outcome {}
  ```
  「分析可能成功也可能失败」→ 返回类型就是答案；`render` 对它做 switch，没有 `default`。
* **`ConcurrentMerge`**
  ```java
  public sealed interface Poll<T> permits Ready, Pending, Done {}      // 对外
  private sealed interface Msg<T> permits Item, End, Failed {}         // 内部队列里的消息
  ```
  `private sealed interface` 说明 sealed 也可只在类内部使用。`tryNext()` 返回三种：有值、暂无、已结束——全写进类型。
* **`RecursiveSum`** —— `SumResult permits Ok, Overflow`：把「可能溢出」写进类型，调用方不处理 `Overflow` 就编译不过；`Trampoline<T> permits Done, More`：switch 无需 default，新增变体时编译报错。
* **`QueueEvents`** —— `Event permits Push, Pop, Query, Correct`、`Answer permits Value, Empty`。
* **`OrderBook`** —— `Command permits Limit, Market, Cancel, Modify`（接口声明共有的 `long id();`）、`Event permits Trade, Rested, Cancelled, Modified, Rejected`。
* **`RegisterSim`** —— 三层 sealed：`Instr` → `Update`（15 种）/ `Query`（3 种）；`apply(int reg, Update u)` 只接受 `Update`，switch 无需 default，因为 15 个实现类一个不少。
* **`OrderSequence`** —— `Op permits Put, Delete, CountUpTo, QtyUpTo, IdAt`、`Result permits Ok, Num, Err`。

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

「延伸」J03 `switch` 模式匹配——sealed 的价值要靠它兑现。
