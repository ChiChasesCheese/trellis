# J04 · record 模式：在 `case` 里直接把 record 拆开

> 版本：Java 21 正式（19、20 为预览）。可运行代码：`examples/J04/`。
> 前置：J01（`record`）、J03（`switch` 模式匹配）。

---

## 1. 先看痛点：取一个嵌套的值，要走「判断 → 强转 → 取外层 → 取内层」四步

场景：队列均值的答案是个分数，用 `Value(Mean(分子, 分母))` 两层结构表示；渲染成字符串时，分母为 1 只打印分子，否则打印 `分子/分母`，空队列打印 `empty`。

Java 8 写法（`examples/J04/J04Old.java`）：

```java
static String render(Answer a) {
    if (a instanceof Value) {
        Value v = (Value) a;              // ① 判断类型 + ② 强转
        Mean m = v.getMean();             // ③ 取出外层字段
        long n = m.getNumerator();        // ④ 取出内层字段
        long d = m.getDenominator();
        if (d == 1) {
            return Long.toString(n);
        } else {
            return n + "/" + d;
        }
    } else if (a instanceof Empty) {
        return "empty";
    }
    throw new IllegalArgumentException();
}
```

痛点：

1. **「想知道的」被淹没在「怎么取到它」里**：真正的逻辑是「分母为 1 的 `Value` 就打印分子」，却被 6 行取值代码包围。
2. **每层都要手动判断 + 强转 + 调 getter**，嵌套越深越长，强转写错编译器不报。
3. **条件和结构混在一起**：「分母为 1」是条件，「这是 `Value(Mean(…))`」是结构；理想是结构用模式写、条件用 `when` 写。

record 模式把「结构」直接写进 `case`，字段自动取出：

```java
static String render(Answer a) {
    return switch (a) {
        case Value(Mean(var n, var d)) when d == 1 -> Long.toString(n);
        case Value(Mean(var n, var d)) -> n + "/" + d;
        case Empty() -> "empty";
    };
}
```

关键变化：**数据的形状和使用它的代码长得一样**，这叫**解构**（destructuring）。

---

## 2. 语法逐条讲

### 2.1 record 模式的写法

record 模式 = **record 类型名 + 括号 + 与组件一一对应的子模式**：

```java
record Point(long x, long y) {}

if (o instanceof Point(long x, long y)) {      // 子模式：long x, long y
    System.out.println(x * x + y * y);
}
```

读法：「若 `o` 是 `Point`，把第一个组件绑定到 `x`，第二个绑定到 `y`」；`x`、`y` 是新局部变量，仅在匹配成功的范围内可用。

两处可用（`examples/J04/J04Ex1.java`）：

* `instanceof`：`o instanceof Point(var x, var y) && x < y`（可接 `&&`）
* `switch` 的 `case`：`case Point(var x, var y) when x == 0 && y == 0 -> "origin"`

> **Java 21 没有**增强 `for` 里的解构（`for (Point(var x, var y) : points)`）：Java 20 预览过，正式版删除了，在 `--release 21` 下是语法错误。

### 2.2 子模式可以是什么

| 子模式 | 例子 | 含义 |
|---|---|---|
| 类型模式（带显式类型） | `Point(long x, long y)` | 组件的类型必须兼容，绑定到 `x` |
| `var` 模式 | `Point(var x, var y)` | 类型由编译器推导为组件的声明类型 |
| 嵌套的 record 模式 | `Value(Mean(var n, var d))` | 再拆一层 |
| 零组件 record | `Empty()` | 括号里什么都没有 |

* **子模式个数必须等于组件个数**：`P(var x)` 而 `P` 有两个组件 → `incorrect number of nested patterns`。
* **类型必须兼容**：组件是 `long` 却写 `Order(int id, ...)` → `pattern of type int is not applicable at long`。基本类型不会自动拓宽，要么写对，要么用 `var`。
* **`var` 最省心**：编译器知道每个组件的类型，`var` 就是照抄；需要明确意图时才写显式类型。

### 2.3 嵌套

```java
case Value(Mean(var n, var d)) when d == 1 -> Long.toString(n);
```

嵌套的 record 模式从外到内匹配：先查是不是 `Value`，再查 `mean()` 的值是不是 `Mean`（静态类型就是 `Mean`，所以必然是，除非为 null，见 2.5），然后取出 `n`、`d`。不管嵌几层，写法都对称，读起来就是数据的形状。

`J04Ex3.java` 的 `simplify` 一次看两层：

```java
case Add(Const(var a), var r) when a == 0 -> simplify(r);       // 0 + r  ->  r
case Neg(Neg(var x)) -> simplify(x);                            // --x     ->  x
```

### 2.4 泛型 record

```java
record Box<T>(T content) {}

static String unbox(Box<String> b) {
    return switch (b) {
        case Box<String>(var s) -> "string box: " + s.toUpperCase();   // s : String
    };
}
static String unboxAny(Box<?> b) {
    return switch (b) {
        case Box<?>(String s)  -> "string " + s;
        case Box<?>(Integer i) -> "int " + (i + 1);
        case Box<?>(var other) -> "other " + other;
    };
}
```

类型参数能由选择器类型推出时可省略（`Box(var s)` 也行）；上面故意写全。

### 2.5 `null` 的规则

record 模式里的 `null` 有三条规则：

1. **外层 record 本身为 `null`**：不匹配任何 record 模式；没有 `case null` 就抛 NPE。
2. **某组件值为 `null`**，且对应子模式是**无条件**的（类型模式的类型正是组件声明类型或其父类型，或 `var`）：**匹配成功，绑定变量为 `null`**。
3. 子模式**不是无条件**的（组件是 `Object`，子模式写 `String s`）：`null` 不是 `String`，**匹配失败**，继续试下一分支。

`J04Ex2.nullRules`：

```java
record Holder(Object value) {}
switch (h) {
    case Holder(String s) -> "string " + s;     // 组件是 Object，String 不是无条件的
    case Holder(Object o) -> "object " + o;     // Object 是无条件的
}
nullRules(new Holder("x"))   // string x
nullRules(new Holder(null))  // object null     <- null 落到第二个分支，没有 NPE
```

### 2.6 穷尽性会「相乘」

record 模式也参与穷尽性检查。record 的**多个组件**都是 sealed 类型时，所有**组合**都要覆盖：

```java
sealed interface Bit permits Zero, One {}
record Pair(Bit a, Bit b) {}

return switch (p) {
    case Pair(Zero a, Zero b) -> "0";
    case Pair(Zero a, One b)  -> "1";
    case Pair(One a, Zero b)  -> "1";
    case Pair(One a, One b)   -> "0";       // 4 = 2 x 2 种组合，缺一个就编译错误
};
```

去掉最后一行就报 `does not cover all possible input values`。「两个状态机组合」「买卖方向 × 订单类型」这类场景，漏组合就是编译错误。

### 2.7 常量不能写在 record 模式里

```java
case Order(var id, Side.BUY, var px, var q) -> ...    // 编译错误！
```

报 `<identifier> expected`。Java 21 的子模式只能是**模式**（类型模式、`var`、嵌套 record 模式），**不能是常量**（enum 常量、字符串、数字字面量都不行）。要匹配具体值，先绑定再用 `when`：

```java
case Order(var id, Side side, var px, var q) when side == Side.BUY -> ...
```

（J03 里的 `case Level.LOW` 是**顶层**标签接受限定名 enum 常量，不是 record 模式的子模式，两回事。）

---

## 3. 编译器和 JVM 到底做了什么

record 模式**没有**新 JVM 指令，也没有 `invokedynamic`：编译器把它**展开成普通类型检查 + 访问器调用**。`case Add(var l, var r) -> eval(l) + eval(r)` 的字节码（略有删减）：

```
 78: aload_1
 79: checkcast  J04Ex3$Add              // 外层的类型判断由 J03 讲的 typeSwitch 完成，这里只是转型
 82: astore     6
 84: aload      6
 86: invokevirtual J04Ex3$Add.left()    // 调用访问器 left()
 89: astore     9                       //   存到临时变量
 91: aload      9
 93: astore     7                       //   再赋给绑定变量 l
 95: aload      6
 97: invokevirtual J04Ex3$Add.right()   // 调用访问器 right()
 ...
106: aload 7; invokestatic eval; aload 8; invokestatic eval; ladd    // 分支体
```

要点：

1. **访问器真的被调用**（`invokevirtual Add.left()`），不是直接读字段。所以 record 重写了访问器的话，模式匹配用的是重写版（这也是不建议重写访问器的原因）。
2. **异常处理表**：所有访问器调用被 `catch (Throwable)` 包住，任何异常被包成 `MatchException`，原异常放 `cause`（`J04Ex2.useBad`）：

   ```
   record Bad(int x) { public int x() { throw new IllegalStateException("accessor failed"); } }
   switch (o) { case Bad(var x) -> ... }
   // MatchException, cause = java.lang.IllegalStateException: accessor failed
   ```

   模式匹配是语言构造，匹配过程中出错应有统一的异常类型，而不是让调用方看到一个看似与 switch 无关的 `IllegalStateException`。
3. **嵌套模式**展开成多层「取组件 → 查类型 → 再取」，没有额外对象分配。
4. **规范不承诺访问器被调用的次数和顺序**，所以**让访问器无副作用**。
5. 守卫失败同 J03：回到 `typeSwitch` 的重启下标继续试后面的 `case`。

编译出的字节码**基本等价于手写的 instanceof + 强转 + getter**，没有额外开销。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——`instanceof` 与 `switch` 里拆 `Point`

`examples/J04/J04Ex1.java`：

```java
record Point(long x, long y) {}
Object o = new Point(3, 4);

if (o instanceof Point(long x, long y)) {
    System.out.println("distance^2 = " + (x * x + y * y));      // 25
}
if (o instanceof Point(var x, var y) && x < y) { ... }           // 可以接 &&

String s = switch (o) {
    case Point(var x, var y) when x == 0 && y == 0 -> "origin";
    case Point(var x, var y) -> "point " + x + "," + y;
    default -> "not a point";
};
```

输出：

```
distance^2 = 25
x < y
point 3,4
false           <- "hello" instanceof Point(var x, var y)：类型不对，整个条件为 false
```

### 例 2：进阶——嵌套、泛型、null、组合穷尽

`examples/J04/J04Ex2.java` 前半的输出：

```
7                     render(new Value(new Mean(7, 1)))
-7/2                  render(new Value(new Mean(-7, 2)))
empty                 render(new Empty())
string box: ABC       unbox(new Box<>("abc"))
int 42                unboxAny(new Box<>(41))
other 2.5             unboxAny(new Box<>(2.5))
string x
object null           <- Holder(null) 落到 Holder(Object o)，不抛 NPE
Holder 本身为 null -> NPE
10                    xor(Zero,One) + xor(One,One) = "1" + "0"
MatchException, cause = java.lang.IllegalStateException: accessor failed
```

### 例 3：贴近真实——表达式树的求值与化简；订单事件格式化

`examples/J04/J04Ex3.java`：

```java
sealed interface Expr permits Const, Add, Mul, Neg {}
record Const(long value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}
record Neg(Expr inner) implements Expr {}

static long eval(Expr e) {
    return switch (e) {
        case Const(var v) -> v;
        case Add(var l, var r) -> eval(l) + eval(r);
        case Mul(var l, var r) -> eval(l) * eval(r);
        case Neg(var x) -> -eval(x);
    };
}

static Expr simplify(Expr e) {
    return switch (e) {
        case Add(Const(var a), var r) when a == 0 -> simplify(r);
        case Add(var l, Const(var b)) when b == 0 -> simplify(l);
        case Mul(var l, Const(var b)) when b == 1 -> simplify(l);
        case Mul(Const(var a), var r) when a == 1 -> simplify(r);
        case Neg(Neg(var x)) -> simplify(x);
        case Add(var l, var r) -> new Add(simplify(l), simplify(r));
        ...
    };
}
```

经典用法：**一个 sealed 层级 + 每种操作一个 switch**（编译器保证每个 switch 处理全）。量化/交易系统里，定价公式、风控规则、订单路由条件、查询过滤器都是这种树。

同一个文件里的第二段是订单事件的格式化：

```java
case Trade(var taker, var maker, Side side, var px, var qty) when side == Side.BUY ->
        "BOUGHT %d@%d (taker %d <- maker %d)".formatted(qty, px, taker, maker);
case Trade(var taker, var maker, var side, var px, var qty) -> "SOLD ...";
```

第一个 `case` 把 `side` 写成显式类型 `Side side`，第二个写 `var side`，两者等价；要匹配具体的 `Side.BUY` 就用 `when side == Side.BUY`。

输出：

```
(0 + (2 + 3) * --1) = 5
(2 + 3) * 1 = 5                         <- 0 + ... 和 --1 被化简掉
BOUGHT 5@101 (taker 4 <- maker 1)
SOLD 4@103 (taker 6 -> maker 5)
REST 5 BUY 4@103
```

---

## 5. 坑与限制

### 5.1 子模式写常量 —— 不行

想匹配具体值，绑定后加 `when`（2.7）。

### 5.2 基本类型不会自动拓宽

组件是 `long` 不能写 `int id`，是 `int` 不能写 `long id`（均报 `not applicable`）。不确定就用 `var`。

### 5.3 变量名不能重复

同一个 `case` 里所有绑定变量名必须不同（`Add(var l, var l)` 编译错误），也不能与外层局部变量重名。

### 5.4 只能拆 record

record 模式只能用在 **record 类型**上，Java 21 对普通类没有解构方式。想用就改成 record，或用类型模式 + 手动调 getter。

### 5.5 `null` 和 `MatchException` 容易混淆

* 外层 record 为 `null` → NPE（无 `case null` 时）；
* 访问器抛异常 → `MatchException`；
* 模式没覆盖的值 → 仅当 sealed 层级被编译后偷偷改过时才抛 `MatchException`。

### 5.6 别让 record 模式变得过深

`case A(B(C(D(var x))))` 能编译，但读起来像剥洋葱。三层以上就拆成辅助方法，或在 record 上加便利访问方法。

### 5.7 绑定变量是 record 组件值的**拷贝**

绑定变量是组件值的拷贝：基本类型修改它不影响 record；引用类型拿到同一引用，所以浅不可变问题依然存在。

---

## 6. 真实代码里的 record 模式

* **`QueueEvents`** —— 嵌套 record 模式 + 守卫（即本课开头的例子）：
  ```java
  public static String render(Answer a) {
      return switch (a) {
          case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();
          case Value(QueueMean.Mean(var n, var d)) -> n + "/" + d;
          case Empty _ -> "empty";
      };
  }
  ```
  `run(...)` 里还有 `case Push(var v) -> q.push(v);`、`case Correct(var contents) -> {...}`。
* **`OrderBook`** —— `execute` 里对命令解构：
  ```java
  case Limit(var id, var side, var px, var q) -> { ... }
  case Market(var id, var side, var q) -> { ... }
  case Cancel(var id) -> { ... }
  case Modify(var id, var newQty) -> { ... }
  ```
  `BatchMatcher` 用 `instanceof` 版：`if (e instanceof OrderBook.Rejected(var id, var why)) { ... }`。
* **`JobChains`** —— `case Ok(var chains) -> { ... }`。
* **`RegisterSim`** —— 15 个分支都是 `case And(var m) -> reg & m;` 这种单组件解构；零组件的写成 `_`（未命名模式，Java 21 预览）。
* **`ConcurrentMerge`** —— 泛型 record 模式：`case Failed<T>(var cause) -> throw new MergeException(i, cause);`
* **`RecursiveSum`** —— `case Done<T>(var v) -> { return v; }`、`case More<T>(var next) -> cur = next.get();`（trampoline 循环）。

---

## 7. 自测题

1. 下面哪一行不能编译？为什么？
   ```java
   record Order(long id, Side side, long qty) {}
   // (a)
   case Order(var id, Side side, var qty) when side == Side.BUY -> ...
   // (b)
   case Order(var id, Side.BUY, var qty) -> ...
   // (c)
   case Order(int id, Side side, var qty) -> ...
   ```
2. `record Holder(Object value)`，`new Holder(null)` 分别会匹配 `case Holder(String s)` 和 `case Holder(Object o)` 吗？`switch (null)` 呢？
3. `Pair(Bit a, Bit b)`，`Bit` 是 sealed 且有 `Zero`、`One` 两个实现。穷尽的 switch 至少要几个 `case`？
4. record 的访问器抛了异常，在 `case Bad(var x)` 里会看到什么异常？为什么这样设计？
5. 把本课开头的 Java 8 `render` 改成用 `instanceof` 的 record 模式写法（不用 switch）。

<details><summary>答案</summary>

1. (b) 和 (c)。(b)：子模式不能是常量，报 `<identifier> expected`；(c)：组件是 `long`，`int id` 不适用。(a) 合法。
2. `Holder(String s)` 不匹配：`String` 对 `Object` 组件不是无条件模式，`null` 不是 `String`。`Holder(Object o)` 匹配，`o` 为 `null`。选择器本身为 `null` 且无 `case null` 时抛 NPE，不会进入任何 record 模式。
3. 4 个（2 x 2）：`(Zero,Zero)`、`(Zero,One)`、`(One,Zero)`、`(One,One)`；除非用无条件子模式 `Pair(Bit a, Bit b)` 合并。
4. `MatchException`，原异常在 `getCause()`。模式匹配是语言构造，用统一异常类型表示「匹配过程中出错」，避免访问器的异常被误当成 switch 周围代码的问题。
5. ```java
   static String render(Answer a) {
       if (a instanceof Value(Mean(var n, var d))) return d == 1 ? Long.toString(n) : n + "/" + d;
       if (a instanceof Empty) return "empty";
       throw new IllegalArgumentException();
   }
   ```

</details>

「延伸」J05 `switch` 表达式：一直在用的 `->` 和 `yield` 到底怎么回事。
