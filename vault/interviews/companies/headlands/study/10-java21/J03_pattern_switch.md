# J03 · `switch` 模式匹配：按「类型」分派，编译器检查你有没有漏

> 版本：Java 21 正式（JEP 441）。之前经历了 Java 17（JEP 406）、18（420）、19（427）、20（433）四轮预览。
> 本课所有可运行代码在 `study/10-java21/examples/J03/`。
> 前置知识：J01（`record`）、J02（`sealed`）。本课是 sealed 的兑现：J02 里「把有几种写进类型」，这里是「让 switch 利用这件事」。
> 官方出处：JEP 441 Pattern Matching for switch — https://openjdk.org/jeps/441 ；语言规范 §14.11 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.11

---

## 1. 先看痛点：Java 8 的 switch 只会看「值」，不会看「类型」

Java 8 的 `switch` 只能对 `int`、`char`、枚举、`String` 这几类**常量**做分支。想按**类型**分派，只能写 `instanceof` 链
（完整代码：`examples/J03/J03Old.java`）：

```java
static double area(Shape s) {
    if (s instanceof Circle) {
        Circle c = (Circle) s;                 // 判断了类型，还要再强转一次
        return Math.PI * c.r * c.r;
    } else if (s instanceof Rect) {
        Rect r = (Rect) s;
        return r.w * r.h;
    }
    throw new IllegalArgumentException("unknown shape");   // 兜底靠人
}
```

痛点逐个列出：

1. **判断 + 强转是两步**，类型写两遍（`instanceof Circle` 和 `(Circle) s`），改一个忘改另一个就是 `ClassCastException`。（J06 的 `instanceof` 模式专门解决这一点。）
2. **if-else 链没有「一共几种」的概念**。漏一种，编译器不报；最后的 `throw` 只能在运行时才发现问题。
3. **老 `switch` 遇到 `null` 一定抛 `NullPointerException`**（`J03Old.main` 里实测），没有办法在 `switch` 里优雅地处理 `null`。
4. **老 `switch` 带 `:` 的写法会 fall-through**（忘了 `break` 就继续执行下一个分支），J05 会专门讲。
5. 想对某个类型再加一个条件（"是 `Limit` 并且 `price <= 0`"），只能在分支里再嵌一层 `if`，原来的平铺结构就乱了。

模式匹配 `switch` 把这五点一起解决：**直接写类型，自动转型，可以处理 null，可以加条件，漏了就编译报错。**

---

## 2. 语法逐条讲

### 2.1 类型模式（type pattern）作为 case 标签

```java
static String describe(Object o) {
    return switch (o) {
        case Integer i -> "int " + (i + 1);          // 如果 o 是 Integer：i 就是它，已经转好型了
        case Long l -> "long " + l;
        case String s -> "string of length " + s.length();
        case int[] a -> "int array of " + a.length;
        default -> "something else";
    };
}
```

* `case Integer i` 的意思：**如果 `o` 是 `Integer`，就把它绑定到新变量 `i`（类型是 `Integer`），执行这个分支**。
  `Integer i` 这个整体叫**类型模式**（type pattern），`i` 叫**绑定变量**（binding variable）。
* 绑定变量只在**它那个分支里**可见。不同分支可以重名。
* `switch (o)` 里的 `o` 叫**选择器**（selector）。在 Java 21，用了模式的 switch，选择器必须是**引用类型**
  （对 `int`/`long` 等基本类型直接用模式是不行的；基本类型的模式在后续版本的预览里才出现）。
* 分支之间是**从上到下依次尝试，第一个匹配的生效**。

### 2.2 处理 `null`

```java
return switch (o) {
    case null -> "null!";
    case String s -> ...;
    default -> ...;
};
```

* **没有写 `case null` 时，选择器是 `null` 就抛 `NullPointerException`**——和旧行为一致，不破坏兼容。
* 写了 `case null` 就由你处理。
* 可以和 `default` 合并：`case null, default -> "other/null"`。

### 2.3 守卫：`when`

```java
return switch (o) {
    case Integer i when i < 0 -> "negative";
    case Integer i when i < 10 -> "small";
    case Integer i -> "big";
    ...
};
```

`when` 后面跟一个布尔表达式，叫**守卫**（guard）。分支匹配 = 类型匹配 **并且** 守卫为真。
守卫为假时，继续往下试后面的分支（包括同一个类型的下一个分支）。

守卫里可以使用刚绑定的变量（`i < 0`）。

### 2.4 顺序很重要：支配（dominance）

因为是从上到下第一个匹配生效，**范围大的分支不能写在范围小的分支前面**——否则后面的永远走不到。
编译器会直接拒绝这种代码（实测）：

```java
case Object x -> "obj";
case String s -> "str";       // error: this case label is dominated by a preceding case label
```

规则：如果标签 A 能匹配的值**包含**标签 B 能匹配的所有值（A 是 B 的父类型，且 A 没有守卫），则 A **支配**（dominates）B，B 必须写在 A 前面。常见情形：

| 写法 | 结果 |
|---|---|
| `case CharSequence cs` 然后 `case String s` | 后者被支配，编译错误 |
| `case String s when s.length() > 3` 然后 `case String s` | **合法**：带守卫的不支配，因为守卫可能为假 |
| `case String s` 然后 `case String s when ...` | 后者被支配，编译错误 |
| `default` 写在模式分支前面 | 编译错误：`default` 之后的模式分支被支配 |
| `case Object x` 和 `default` 同时有 | 编译错误：`switch has both an unconditional pattern and a default label` |

写顺序的口诀：**先具体、后一般；带守卫的在前、不带的在后；`default`/兜底在最后。**

### 2.5 穷尽性（exhaustiveness）——这一节最重要

**switch 表达式**（`return switch ...` / `var x = switch ...`）必须**覆盖选择器类型的所有可能值**，否则编译错误：

```
error: the switch expression does not cover all possible input values
```

**用了模式或 `case null` 的 switch 语句**也必须穷尽（实测：`error: the switch statement does not cover all possible input values`）。
只有「老式」的 switch 语句（对 `int`/`String`/`enum` 的常量分支，没有模式没有 null）才可以不穷尽——兼容旧代码。

什么算「覆盖了所有可能值」？一组 case 对类型 `T` 是穷尽的，如果满足以下任意一条（JLS §14.11.1.1 的简化）：

1. 有一个**无条件**的模式（类型是 `T` 或 `T` 的父类型、没有守卫）或者有 `default`；
2. `T` 是 **sealed 接口 / 抽象 sealed 类**，且**每一个**许可子类型都被这组 case 覆盖（递归，子类型自己是 sealed 的就继续往下展开）；
3. `T` 是 enum，且每个枚举常量都有 `case`；
4. （record 模式的情形见 J04。）

带守卫的分支**不算**覆盖（守卫可能为假）。所以：

```java
case String s when s.length() > 3 -> "long";
case Integer i -> "int";
// 对 Object 不穷尽：String 且长度 <= 3 的情形没人处理（实测编译错误）
```

### 2.6 enum 常量作为 case 标签，和 sealed 配合

Java 21 允许用**限定名**写 enum 常量当 case，即使选择器是 sealed 接口而不是那个 enum：

```java
sealed interface Signal permits Level, Tick {}
enum Level implements Signal { LOW, MID, HIGH }
record Tick(long px, long qty) implements Signal {}

switch (s) {
    case Level.LOW -> ...
    case Level.MID -> ...
    case Level.HIGH -> ...
    case Tick t -> ...
}
```

只要列全 `LOW/MID/HIGH` 三个常量，`Level` 就算被覆盖。（`J03Ex2.java`）

### 2.7 箭头 `->` vs 冒号 `:`

模式标签用 `case X x ->` 最自然。也可以用 `case X x:`（经典风格），但：
* 不允许 fall-through 进入模式标签（实测错误：`illegal fall-through to a pattern`）——因为绑定变量在 fall-through 时没有值。
* 一个 `case` 标签里不能同时放多个会绑定变量的模式（实测：`case String a, Integer b` 报 `illegal fall-through from a pattern`）。Java 21 预览里的 `case A _, B _`（未命名模式，J13）可以。

---

## 3. 编译器和 JVM 到底做了什么

用 `javap -c` 看 J02Ex1 里那个只有两个分支的 `show(Result r)`（实测输出，略有删减）：

```
 0: aload_0
 1: dup
 2: invokestatic  java/util/Objects.requireNonNull   // 选择器为 null -> NPE（因为没写 case null）
 5: pop
 6: astore_1                                         // 选择器存局部变量 1
 7: iconst_0
 8: istore_2                                         // 「从第几个标签开始试」，初值 0
 9: aload_1
10: iload_2
11: invokedynamic typeSwitch:(Object,int)I           // 魔法发生在这里：返回「第几个标签匹配」
16: lookupswitch { 0: 54   1: 71   default: 44 }
44: new MatchException ... athrow                    // default：不应该走到
54: aload_1; checkcast J02Ex1$Ok;  ... 分支 0 的代码
71: aload_1; checkcast J02Ex1$Err; ... 分支 1 的代码
```

分步骤解释：

1. **`invokedynamic typeSwitch`**：和 J01 里 record 的 `equals` 同一种机制（`invokedynamic`，第一次执行时调用引导方法生成实际逻辑）。
   这里的引导方法是 `java.lang.runtime.SwitchBootstraps.typeSwitch`，它的静态参数是**标签列表**（这里是 `Ok.class`、`Err.class`）。
   调用时传入 `(选择器, 起始下标)`，返回「第一个匹配的标签的下标」；都不匹配返回标签个数；选择器为 `null` 返回 `-1`。
2. **返回值上再做一个普通的 `lookupswitch` / `tableswitch`** 跳到对应分支。分支里先 `checkcast` 转型再使用——就是你在 Java 8 里手写的那个强转，现在由编译器生成，并且保证和判断是同一个类型。
3. **没写 `case null`** 时编译器在最前面插一个 `Objects.requireNonNull(selector)`；写了 `case null` 则让 `typeSwitch` 返回的 `-1` 直接跳到你的分支（`J03Ex2.sizeBucket` 的字节码里有 `-1: 142`）。
4. **守卫失败时怎么「继续往下试」**：看 `sizeBucket` 里 `case Integer i when i < 0` 的字节码：

   ```
   48: aload_1; checkcast Integer; astore_3
   53: aload_3; invokevirtual Integer.intValue; iflt 65   // 守卫 i < 0 为真，跳到分支体
   60: iconst_1; istore_2                                 // 守卫为假：把「起始下标」改成 1
   62: goto 4                                             // 回到第 4 行，重新调用 typeSwitch，从标签 1 开始再试
   ```

   所以 `typeSwitch` 的第二个参数就是这个「重启下标」。这是整个设计里最巧妙的地方：**类型匹配交给 `typeSwitch`，守卫是普通字节码，二者通过重启下标衔接。**
5. **`default -> throw new MatchException(null, null)`**：对 sealed 层级且没有写 `default` 的 switch，编译器仍然生成一个 `default` 目标，里面抛 `MatchException`。
   正常情况永远走不到；只有当层级在**编译之后**被改过（新增了子类但没重新编译这个 switch）才会到。我做了实验：

   ```
   先编译 sealed interface S permits X, Y 和 switch (s) { case X x -> 1; case Y y -> 2; }
   再把 S 改成 permits X, Y, Z 并只编译 S 和 Z，不碰 switch 所在的类
   运行 f(new Z())  ->  java.lang.MatchException
   ```

   同样的，对 enum 的 switch 表达式（没有 `default`），在编译后枚举多出新常量，运行时也是 `MatchException`（J05）。
   **这就是「不要给 sealed 的 switch 写 `default`」的原因**：写了 `default`，新增变体时编译器不再报错，会悄悄落入 default。
6. **性能**：`typeSwitch` 在 JDK 21 里的实现是按顺序依次检查标签（`isInstance`），不是哈希表；对只有几个分支的 switch 完全不是问题。
   如果在热路径上有几十个分支，要实测（实现细节随版本改进，不要当规范依赖）。

### javac 怎么证明「穷尽」

编译器在类型检查阶段，把所有无守卫的 `case` 模式收集起来，对选择器类型做**递归覆盖检查**：

* `Result`（sealed）→ 展开成 `Ok`、`Err`（读的是 J02 讲的 `PermittedSubclasses`）；
* 每个子类型在 case 里能找到无守卫的类型模式吗？找到就覆盖；该子类型自己又是 sealed 就再展开；
* 全部覆盖 → 穷尽，没有 `default` 也可以；否则报 `does not cover all possible input values`。

整个检查是**编译期**做的，不产生任何运行时代价；运行时只多一个永远走不到的 `MatchException` 分支。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——对 `Object` 做类型分派 + `null`

`examples/J03/J03Ex1.java`：

```java
static String describe(Object o) {
    return switch (o) {
        case null -> "null!";
        case Integer i -> "int " + (i + 1);
        case Long l -> "long " + l;
        case String s -> "string of length " + s.length();
        case int[] a -> "int array of " + a.length;
        default -> "something else: " + o.getClass().getSimpleName();
    };
}
```

输入 `{null, 41, 7L, "hello", new int[]{1,2,3}, 3.14}`，实测输出：

```
null!
int 42
long 7
string of length 5
int array of 3
something else: Double
没有 case null -> NPE          <- 另一个没写 case null 的 switch，选择器为 null
```

### 例 2：进阶——守卫、`case null, default`、enum 常量

`examples/J03/J03Ex2.java`：

```java
static String classify(Signal s) {
    return switch (s) {
        case Level.LOW -> "low level";
        case Level.MID -> "mid level";
        case Level.HIGH -> "high level";
        case Tick t when t.qty() == 0 -> "empty tick";
        case Tick t when t.px() > 100_000 -> "expensive tick";
        case Tick t -> "tick " + t.px() + "x" + t.qty();     // 兜底：不带 when
    };
}
```

输入 `MID, Tick(1,0), Tick(200000,5), Tick(100,3)`，实测输出：

```
mid level
empty tick
expensive tick
tick 100x3
```

注意最后一个 `case Tick t` **没有守卫**——它既是兜底，也是让编译器相信 `Tick` 被完整覆盖的那一行（带守卫的两行不算覆盖）。

### 例 3：贴近真实——订单校验

`examples/J03/J03Ex3.java`：

```java
static String validate(Command cmd, Set<Long> knownIds) {
    return switch (cmd) {
        case Limit l when l.id() <= 0 -> "INVALID_ID";
        case Limit l when l.price() <= 0 -> "INVALID_PRICE";
        case Limit l when l.qty() <= 0 -> "INVALID_QTY";
        case Market m when m.id() <= 0 -> "INVALID_ID";
        case Market m when m.qty() <= 0 -> "INVALID_QTY";
        case Cancel c when c.id() <= 0 -> "INVALID_ID";
        // 以下三行没有守卫：状态检查 + 让编译器验证 sealed 被覆盖
        case Limit l -> knownIds.contains(l.id()) ? "DUPLICATE_ID" : null;
        case Market m -> knownIds.contains(m.id()) ? "DUPLICATE_ID" : null;
        case Cancel c -> knownIds.contains(c.id()) ? null : "UNKNOWN_ID";
    };
}
```

这是 `OrderBook.validate` 的简化版。它的好处：

1. 校验顺序就是代码顺序（题面规定 id → price → quantity → 状态），一眼能对照。
2. 将来新增 `Modify` 命令，这个 switch 立刻编译失败，不会漏掉对新命令的校验。
3. 没有 `instanceof`/强转，没有嵌套 `if`。

实测输出（`knownIds = {1, 2}`）：

```
Limit[id=0, side=BUY, price=100, qty=5] -> INVALID_ID
Limit[id=3, side=BUY, price=0, qty=5] -> INVALID_PRICE
Limit[id=3, side=SELL, price=100, qty=0] -> INVALID_QTY
Limit[id=1, side=BUY, price=100, qty=5] -> DUPLICATE_ID
Limit[id=3, side=BUY, price=100, qty=5] -> null
Market[id=4, side=SELL, qty=-1] -> INVALID_QTY
Cancel[id=1] -> null
Cancel[id=9] -> UNKNOWN_ID
```

---

## 5. 坑与限制

### 5.1 对 sealed 层级写 `default`，等于关掉了穷尽检查

```java
return switch (event) {
    case Trade t -> ...;
    case Rested r -> ...;
    default -> "?";          // 新增 Cancelled 时，这里不报错，悄悄走 default
};
```

只在**真的想把剩下的都当一类处理**时才写 `default`。本 kit 的约定：sealed 层级的 switch 不写 `default`。

### 5.2 守卫里的副作用

守卫在「类型匹配之后」才求值，且**每次尝试都求值一次**。别在守卫里做有副作用的事（修改变量、读流、计数），否则顺序一变行为就变了。守卫里能引用的外部局部变量必须是 `final` 或事实上的 final（有效不可变，effectively final），否则报 `local variables referenced from a guard must be final or effectively final`（实测）。

### 5.3 `null` 与 `default` 不是一回事

`default` **不处理 `null`**。没写 `case null`，`null` 一进来就是 NPE，不会落进 `default`。要同时处理就写 `case null, default`。

### 5.4 绑定变量不能与外层局部变量同名

`String s = ...; switch (o) { case String s -> ... }` 编译错误（变量已定义）。给模式变量起不同的名字。

### 5.5 选择器必须是引用类型（Java 21）

对 `int` 选择器用 `case Integer i` 之类的模式在 21 里不可用（实测：`pattern of type Integer is not applicable at int`）。需要时先装箱成 `Integer`/`Object`，或者用传统的常量标签。

### 5.6 泛型擦除

`case List<String> l` 对 `Object` 选择器会因为擦除（erasure）而无法在运行时检查 `<String>`，编译器拒绝（实测：`Object cannot be safely cast to List<String>`）。
选择器本身是 sealed 泛型类型（比如 `Poll<T>`）时，`case Ready<T> r` 是可以的，因为类型参数能由选择器推出。

### 5.7 新增变体 ≠ 向后兼容

前面第 3 节第 5 点：不重新编译的旧 switch 会抛 `MatchException`。公共库里 sealed 层级加成员要当作破坏性变更。

### 5.8 不适合的场景

* 变体 > 20 种且在热路径上：先实测（见第 3 节第 6 点）；这时用「虚方法调用」（每个 record 实现 `apply()`）可能更快，也更符合开闭原则。
* 分派逻辑属于对象自己、会被很多地方复用：把它写成接口方法，而不是在外面反复 switch。
* 只有一个条件：`if (o instanceof Foo f && ...)` 更直接（J06）。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。

* **`01_video/hc05_market_order_book/reference/OrderBook.java`** —— 用 `when` 守卫写校验顺序（就是上面例 3 的原型）：
  ```java
  private String validate(Command cmd) {
      return switch (cmd) {
          case Limit l when l.id() <= 0 -> INVALID_ID;
          case Limit l when l.price() <= 0 -> INVALID_PRICE;
          ...
          case Cancel _, Modify _ -> byId.containsKey(cmd.id()) ? null : UNKNOWN_ID;
      };
  }
  ```
  注释写着：「从上到下第一个匹配的分支生效，所以『更具体的错误』写在前面；最后两行没有守卫，让编译器检查 sealed 层级被穷尽了」。
  （`case Limit _, Market _` 用了未命名模式 `_`，是 Java 21 的**预览**特性，见 J13。）
  `execute(Command)` 是同一个文件里的另一个 switch：`case Limit(var id, var side, var px, var q) -> {...}`（J04）。
* **`00_oa/oa01_job_chain/reference/JobChains.java`** —— `render(Outcome)`：
  ```java
  return switch (outcome) {
      case Malformed _ -> List.of("Malformed Input");
      case Ok(var chains) -> { ... yield lines; }
  };
  ```
* **`01_video/hc04_queue_mean_snapshot/reference/QueueEvents.java`** —— `run(...)` 里 `switch (e)` 处理 `Push/Pop/Query/Correct` 四种事件（作为 switch **语句**，没有 `default`，同样要穷尽）；`render(Answer)` 有一条带守卫的 record 模式：
  ```java
  case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();
  case Value(QueueMean.Mean(var n, var d)) -> n + "/" + d;
  ```
* **`01_video/hc06_cpu_register_bitwise/reference/RegisterSim.java`** —— `apply(int reg, Update u)` 对 15 种指令的 switch，没有 `default`。
* **`01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java`** —— `switch (m)` 处理队列里的 `Item/End/Failed` 三种消息。

---

## 7. 自测题

1. 下面哪一行编译不过？为什么？
   ```java
   return switch (o) {
       case CharSequence cs -> "cs";
       case String s -> "str";
       default -> "d";
   };
   ```
2. `switch (o)` 里 `o == null`，下列三种写法分别发生什么？(a) 没有 `case null` 也没有 `default`；(b) 有 `default` 但没有 `case null`；(c) 有 `case null, default`。
3. 对 `sealed interface Shape permits Circle, Square, Tri`，只写 `case Circle`、`case Square when x > 0`、`case Tri`，switch 表达式能编译吗？
4. 写了 sealed 层级的 switch 后，团队新增了一个 record 实现。如果 switch 末尾有 `default`，会发生什么？如果没有呢？
5. `invokedynamic typeSwitch` 的返回值是什么？守卫失败时字节码怎么「继续往下试」？

<details><summary>答案</summary>

1. `case String s` 那一行：`CharSequence` 是 `String` 的父类型，且没有守卫，它支配了后面的 `String`，报 `this case label is dominated by a preceding case label`。要先写 `String` 再写 `CharSequence`。
2. (a) NPE；(b) 也是 NPE（`default` 不处理 `null`）；(c) 进入 `case null, default` 分支，不抛异常。
3. 不能。`case Square when x > 0` 带守卫，不算覆盖 `Square`（守卫为假时没有人处理），报 `does not cover all possible input values`。要再加一行无守卫的 `case Square` 或者 `default`。
4. 有 `default`：编译通过，新类型悄悄落入 `default`，没人提醒你要不要特殊处理；没有 `default`：编译失败，逼你补分支（如果没有重新编译这个 switch 而直接运行旧 class，则运行时抛 `MatchException`）。
5. 返回第一个匹配的标签的下标（不匹配返回标签数、`null` 返回 `-1`）。字节码随后用 `lookupswitch`/`tableswitch` 跳转。守卫为假时，字节码把一个局部变量（重启下标）设为「当前下标 + 1」，`goto` 回到调用 `typeSwitch` 的位置，从下一个标签重新匹配。

</details>

---

## 8. 延伸阅读

* JEP 441 Pattern Matching for switch — https://openjdk.org/jeps/441 —— 读 Description，特别是 "Dominance of case labels" 和 "Exhaustiveness of switch expressions and statements" 两节，规则都在那里。
* JLS §14.11 The switch Statement — https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.11 —— 穷尽性的精确定义在 §14.11.1.1。
* `SwitchBootstraps` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/runtime/SwitchBootstraps.html —— `typeSwitch` 的契约（参数、返回值的含义）。
* `MatchException` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/MatchException.html —— 为什么、何时抛。
* 下一课：J04 record 模式——在 `case` 里直接拆开 record 的字段。
