# J03 · `switch` 模式匹配：按「类型」分派，编译器检查你有没有漏

> 版本：Java 21 正式（17–20 为预览）。可运行代码：`examples/J03/`。
> 前置：J01（`record`）、J02（`sealed`）。J02 把「有几种」写进类型，本课让 `switch` 利用它。

---

## 1. 先看痛点：Java 8 的 switch 只会看「值」，不会看「类型」

Java 8 的 `switch` 只能对 `int`、`char`、枚举、`String` 这类**常量**分支。想按**类型**分派只能写 `instanceof` 链（`examples/J03/J03Old.java`）：

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

痛点：

1. **判断 + 强转是两步**，类型写两遍，改一个忘另一个就是 `ClassCastException`。
2. **if-else 链不知道「一共几种」**：漏一种编译器不报，末尾的 `throw` 只能运行时才暴露。
3. **老 `switch` 遇 `null` 必抛 `NullPointerException`**，没法优雅处理。
4. **带 `:` 的老写法会 fall-through**（忘 `break` 就执行下一分支）。
5. 想对某类型再加条件（"是 `Limit` 且 `price <= 0`"）只能在分支里嵌 `if`，平铺结构乱了。

模式匹配 `switch` 一次解决：**直接写类型、自动转型、可处理 null、可加条件、漏了就编译报错。**

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

* `case Integer i`：**若 `o` 是 `Integer`，就绑定到新变量 `i`（类型 `Integer`）并执行该分支**。`Integer i` 叫**类型模式**（type pattern），`i` 叫**绑定变量**（binding variable）。
* 绑定变量只在**本分支**可见，不同分支可重名。
* `switch (o)` 的 `o` 叫**选择器**（selector）。Java 21 里用模式的 switch，选择器必须是**引用类型**。
* 分支**从上到下依次尝试，第一个匹配的生效**。

### 2.2 处理 `null`

```java
return switch (o) {
    case null -> "null!";
    case String s -> ...;
    default -> ...;
};
```

* 没写 `case null`，选择器为 `null` 就抛 `NullPointerException`（兼容旧行为）。
* 写了 `case null` 由你处理；可与 `default` 合并：`case null, default -> "other/null"`。

### 2.3 守卫：`when`

```java
return switch (o) {
    case Integer i when i < 0 -> "negative";
    case Integer i when i < 10 -> "small";
    case Integer i -> "big";
    ...
};
```

`when` 后跟布尔表达式，叫**守卫**（guard）。分支匹配 = 类型匹配 **并且** 守卫为真；守卫为假则继续试后面的分支（含同类型的下一个）。守卫里可用刚绑定的变量（`i < 0`）。

### 2.4 顺序很重要：支配（dominance）

从上到下第一个匹配生效，所以**范围大的分支不能写在范围小的前面**，否则后者永远走不到。编译器直接拒绝：

```java
case Object x -> "obj";
case String s -> "str";       // error: this case label is dominated by a preceding case label
```

规则：标签 A 能匹配的值**包含**标签 B 的全部（A 是 B 的父类型且 A 无守卫），则 A **支配**（dominates）B，B 必须写在 A 前面：

| 写法 | 结果 |
|---|---|
| `case CharSequence cs` 然后 `case String s` | 后者被支配，编译错误 |
| `case String s when s.length() > 3` 然后 `case String s` | **合法**：带守卫的不支配，因为守卫可能为假 |
| `case String s` 然后 `case String s when ...` | 后者被支配，编译错误 |
| `default` 写在模式分支前面 | 编译错误：`default` 之后的模式分支被支配 |
| `case Object x` 和 `default` 同时有 | 编译错误：`switch has both an unconditional pattern and a default label` |

口诀：**先具体、后一般；带守卫在前、不带在后；`default` 最后。**

### 2.5 穷尽性（exhaustiveness）——这一节最重要

**switch 表达式**（`return switch ...` / `var x = switch ...`）必须**覆盖选择器类型的所有可能值**，否则编译错误：

```
error: the switch expression does not cover all possible input values
```

**用了模式或 `case null` 的 switch 语句**也必须穷尽（`the switch statement does not cover all possible input values`）。只有「老式」switch 语句（`int`/`String`/`enum` 常量分支，无模式无 null）可以不穷尽。

一组 case 对类型 `T` 穷尽，当且仅当满足任一条：

1. 有**无条件**模式（类型是 `T` 或其父类型，无守卫）或有 `default`；
2. `T` 是 **sealed 接口 / 抽象 sealed 类**，且**每个**许可子类型都被覆盖（子类型自己 sealed 就递归展开）；
3. `T` 是 enum 且每个常量都有 `case`；
4. （record 模式的情形见 J04 的嵌套展开。）

带守卫的分支**不算**覆盖：

```java
case String s when s.length() > 3 -> "long";
case Integer i -> "int";
// 对 Object 不穷尽：String 且长度 <= 3 的情形没人处理（实测编译错误）
```

### 2.6 enum 常量作为 case 标签，和 sealed 配合

Java 21 允许用**限定名**写 enum 常量当 case，即使选择器是包含它的 sealed 接口：

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

列全 `LOW/MID/HIGH` 三个常量，`Level` 就算被覆盖（`J03Ex2.java`）。

### 2.7 箭头 `->` vs 冒号 `:`

模式标签最自然的是 `case X x ->`。用经典 `case X x:` 也行，但：
* 不允许 fall-through 进入模式标签（`illegal fall-through to a pattern`），因为绑定变量那时没有值。
* 一个 `case` 里不能放多个会绑定变量的模式（`case String a, Integer b` 报错）。

---

## 3. 编译器和 JVM 到底做了什么

用 `javap -c` 看 `show(Result r)`（两个分支，略有删减）：

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

逐步解释：

1. **`invokedynamic typeSwitch`**：与 record 的 `equals` 同一机制（第一次执行时调用引导方法生成逻辑）。引导方法是 `java.lang.runtime.SwitchBootstraps.typeSwitch`，静态参数是**标签列表**（`Ok.class`、`Err.class`）。调用时传 `(选择器, 起始下标)`，返回「第一个匹配标签的下标」；都不匹配返回标签个数；`null` 返回 `-1`。
2. 返回值上再做普通 `lookupswitch`/`tableswitch` 跳到分支，分支里先 `checkcast`——就是你在 Java 8 手写的强转，现在由编译器生成并保证与判断同一类型。
3. **没写 `case null`** 时编译器在最前插 `Objects.requireNonNull(selector)`；写了则让 `-1` 直接跳到你的分支。
4. **守卫失败怎么「继续往下试」**：看 `case Integer i when i < 0` 的字节码：

   ```
   48: aload_1; checkcast Integer; astore_3
   53: aload_3; invokevirtual Integer.intValue; iflt 65   // 守卫 i < 0 为真，跳到分支体
   60: iconst_1; istore_2                                 // 守卫为假：把「起始下标」改成 1
   62: goto 4                                             // 回到第 4 行，重新调用 typeSwitch，从标签 1 开始再试
   ```

   `typeSwitch` 的第二个参数就是「重启下标」。**类型匹配交给 `typeSwitch`，守卫是普通字节码，二者靠重启下标衔接。**
5. **`default -> throw new MatchException(null, null)`**：sealed 层级的 switch 即使没写 `default`，编译器也生成一个抛 `MatchException` 的 default 目标。正常走不到；只有层级在**编译之后**被改过才会到：

   ```
   先编译 sealed interface S permits X, Y 和 switch (s) { case X x -> 1; case Y y -> 2; }
   再把 S 改成 permits X, Y, Z 并只编译 S 和 Z，不碰 switch 所在的类
   运行 f(new Z())  ->  java.lang.MatchException
   ```

   同理，enum 的 switch 表达式在编译后枚举多出新常量，运行时也是 `MatchException`。**这就是「sealed 的 switch 不要写 `default`」的原因**：写了，新增变体时编译器不再报错，会悄悄落入 default。
6. **性能**：JDK 21 的 `typeSwitch` 按顺序依次 `isInstance` 检查标签，不是哈希表；几个分支毫无问题，热路径上几十个分支要实测（实现细节随版本改进，别当规范依赖）。

### javac 怎么证明「穷尽」

编译器把所有无守卫的 `case` 模式收集起来，对选择器类型做**递归覆盖检查**：`Result`（sealed）展开成 `Ok`、`Err`（读 `PermittedSubclasses`）；每个子类型在 case 里有无守卫的类型模式就算覆盖，子类型自己 sealed 就再展开；全覆盖即穷尽，否则报 `does not cover all possible input values`。

检查全在**编译期**，运行时只多一个永远走不到的 `MatchException` 分支。

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

输入 `{null, 41, 7L, "hello", new int[]{1,2,3}, 3.14}` 的输出：

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

输入 `MID, Tick(1,0), Tick(200000,5), Tick(100,3)` 的输出：

```
mid level
empty tick
expensive tick
tick 100x3
```

最后一个 `case Tick t` **没有守卫**——既是兜底，也是让编译器相信 `Tick` 被完整覆盖的那一行。

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

这是订单簿校验的简化版。好处：校验顺序就是代码顺序（id → price → quantity → 状态）；将来新增 `Modify` 命令，switch 立刻编译失败；没有 `instanceof`/强转/嵌套 `if`。

输出（`knownIds = {1, 2}`）：

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

只在**真想把剩下的都当一类**时才写 `default`；sealed 层级的 switch 一般不写。

### 5.2 守卫里的副作用

守卫在类型匹配之后求值，**每次尝试都求一次**。别在守卫里做副作用（改变量、读流、计数），否则顺序一变行为就变。守卫引用的外部局部变量必须 effectively final，否则报 `local variables referenced from a guard must be final or effectively final`。

### 5.3 `null` 与 `default` 不是一回事

`default` **不处理 `null`**：没写 `case null`，`null` 直接 NPE，不会落进 `default`。要同时处理写 `case null, default`。

### 5.4 绑定变量不能与外层局部变量同名

`String s = ...; switch (o) { case String s -> ... }` 编译错误（变量已定义），换个名字。

### 5.5 选择器必须是引用类型（Java 21）

对 `int` 选择器用 `case Integer i` 在 21 里不可用（`pattern of type Integer is not applicable at int`）。先装箱成 `Integer`/`Object`，或用传统常量标签。

### 5.6 泛型擦除

`case List<String> l` 对 `Object` 选择器因擦除（erasure）无法运行时检查 `<String>`，编译器拒绝。选择器本身是 sealed 泛型类型（如 `Poll<T>`）时 `case Ready<T> r` 可以，因为类型参数能由选择器推出。

### 5.7 新增变体 ≠ 向后兼容

第 3 节第 5 点：不重编译的旧 switch 会抛 `MatchException`。公共库的 sealed 层级加成员是破坏性变更。

### 5.8 不适合的场景

* 变体 > 20 种且在热路径：先实测；虚方法（每个 record 实现 `apply()`）可能更快，也更符合开闭原则。
* 分派逻辑属于对象自己、多处复用：写成接口方法，别在外面反复 switch。
* 只有一个条件：`if (o instanceof Foo f && ...)` 更直接。

---

## 6. 真实代码里的 switch

* **`OrderBook`** —— `when` 守卫写校验顺序（例 3 的原型）：
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
  从上到下第一个匹配生效，所以「更具体的错误」写前面；最后几行无守卫，让编译器验证 sealed 层级被穷尽。`case Cancel _, Modify _` 用了未命名模式 `_`（Java 21 的**预览**特性：不需要变量名时用 `_` 占位）。
* **`JobChains`** —— `render(Outcome)`：
  ```java
  return switch (outcome) {
      case Malformed _ -> List.of("Malformed Input");
      case Ok(var chains) -> { ... yield lines; }
  };
  ```
* **`QueueEvents`** —— `switch (e)` 处理四种事件（作为 switch **语句**，无 `default`，同样要穷尽）；`render(Answer)` 有带守卫的 record 模式：
  ```java
  case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();
  case Value(QueueMean.Mean(var n, var d)) -> n + "/" + d;
  ```
* **`RegisterSim`** —— 对 15 种指令的 switch，无 `default`；**`ConcurrentMerge`** —— `switch (m)` 处理 `Item/End/Failed` 三种消息。

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
2. `switch (o)` 里 `o == null`，分别发生什么？(a) 无 `case null` 无 `default`；(b) 有 `default` 无 `case null`；(c) 有 `case null, default`。
3. 对 `sealed interface Shape permits Circle, Square, Tri`，只写 `case Circle`、`case Square when x > 0`、`case Tri`，switch 表达式能编译吗？
4. 写了 sealed 层级的 switch 后，团队新增了一个 record 实现。如果 switch 末尾有 `default`，会发生什么？如果没有呢？
5. `invokedynamic typeSwitch` 的返回值是什么？守卫失败时字节码怎么「继续往下试」？

<details><summary>答案</summary>

1. `case String s`：`CharSequence` 是 `String` 的父类型且无守卫，支配了后面的 `String`（`this case label is dominated by a preceding case label`）。要先写 `String` 再写 `CharSequence`。
2. (a) NPE；(b) 也是 NPE（`default` 不处理 `null`）；(c) 进入 `case null, default` 分支，不抛异常。
3. 不能。`case Square when x > 0` 带守卫不算覆盖 `Square`，报 `does not cover all possible input values`。再加一行无守卫的 `case Square` 或 `default`。
4. 有 `default`：编译通过，新类型悄悄落入 `default`；没有：编译失败，逼你补分支（若直接跑没重编译的旧 class，则运行时抛 `MatchException`）。
5. 返回第一个匹配标签的下标（不匹配返回标签数、`null` 返回 `-1`），随后 `lookupswitch`/`tableswitch` 跳转。守卫为假时，字节码把「重启下标」设为当前下标 + 1，`goto` 回 `typeSwitch` 调用处，从下一标签重新匹配。

</details>

「延伸」J04 record 模式：在 `case` 里直接拆开 record 的字段。
