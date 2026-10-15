# J05 · `switch` 表达式与 `yield`：让 switch 直接「产出一个值」

> 版本：Java 14 正式（JEP 361）。Java 12、13 是预览（JEP 325、JEP 354）。
> 本课所有可运行代码在 `study/10-java21/examples/J05/`。
> 前置知识：Java 8 的 `switch ... case ...: break;` 基本用法。
> 官方出处：JEP 361 Switch Expressions — https://openjdk.org/jeps/361 ；语言规范 §15.28 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.28

> 说明：前面 J03、J04 里已经大量用了 `case X -> ...` 和 `yield`，那是因为模式匹配 switch 建立在 switch 表达式之上。
> 本课把这块地基单独讲清楚，包括对**普通常量**（`int`、`String`、`enum`）的 switch。

---

## 1. 先看痛点：老 switch 是「语句」，三个麻烦一起来

Java 8 的 `switch` 是**语句**（statement）：它只做事，不产出值。想用 switch 算出一个值，要先声明临时变量，在每个分支里赋值，最后别忘了 `break`
（完整代码：`examples/J05/J05Old.java`）：

```java
static int sign(Side s) {
    int result;                       // ① 临时变量
    switch (s) {
        case BUY:
            result = 1;
            break;                    // ② 每个分支都要 break
        case SELL:
        case SHORT:                   // ③ 想让两个标签共用一个分支，靠「故意不写 break」
            result = -1;
            break;
        default:
            throw new IllegalArgumentException("unknown " + s);
    }
    return result;
}
```

三个具体的麻烦：

### 麻烦一：fall-through（贯穿）

老 switch 的规则是：匹配到某个 `case` 后，**从这里开始一路往下执行，直到遇到 `break`**。忘记 `break`，就会「掉进」下一个分支：

```java
static String buggy(Side s) {
    String label = "";
    switch (s) {
        case BUY:
            label += "buy";           // 本意只想到这里
        case SELL:
            label += "sell";          // 忘了 break：BUY 也会走到这里
            break;
        default:
            label += "other";
    }
    return label;
}
buggy(Side.BUY)    // 期望 "buy"，实际 "buysell"（J05Old 里实测）
```

编译器不报错，因为 fall-through 是**合法**的语言特性（C 语言传下来的）。这类 bug 在代码评审时很难一眼看出——`break` 少了一行，缩进还是对的。

### 麻烦二：所有 `case` 共享一个作用域

整个 `switch { ... }` 是一个花括号块，不同 `case` 里声明的变量彼此可见：

```java
case 1:
    String a = "one";
    return a;
case 2:
    a = "two";        // 能用，但 a 在这里根本没有被初始化过！
```

### 麻烦三：不强制处理所有情况

老 switch 对 `enum` 不要求列全所有常量。`Side` 以后加了一个常量，所有老 switch 默默地走到 `default`（或者什么都不做），没有人提醒你。

### switch 表达式的做法

```java
static int sign(Side s) {
    return switch (s) {
        case BUY -> 1;
        case SELL, SHORT -> -1;
    };
}
```

* `switch` 现在是**表达式**（expression）：它有值，能 `return`、能赋值、能当方法参数。
* 箭头 `->` 形式：**没有 fall-through**，每个分支只执行箭头右边的内容。
* 多个标签用逗号：`case SELL, SHORT`。
* 对 `enum`：列全了所有常量就**不需要 `default`**；漏了就编译错误。

---

## 2. 语法逐条讲

### 2.1 两种 case 形式：箭头 vs 冒号

| | 箭头形式 `case X -> ...` | 冒号形式 `case X: ...` |
|---|---|---|
| fall-through | **没有** | 有（要 `break`） |
| 多标签 | `case A, B ->` | `case A: case B:` 或 `case A, B:` |
| 分支体 | 一个表达式 / 一个块 `{}` / 一个 `throw` | 一串语句 |
| 作用域 | 每个分支自己一个作用域 | 整个 switch 共享 |
| 推荐 | **是** | 只有需要 fall-through 时 |

**同一个 `switch` 里不能混用两种形式**（实测：`different case kinds used in the switch`）。

### 2.2 箭头形式的三种右边

```java
return switch (cmd) {
    case "LIMIT"  -> 1;                          // ① 表达式：它的值就是这个分支的值
    case "CANCEL" -> {                           // ② 块：需要多条语句时用，用 yield 给值
        int x = compute();
        yield x * 2;
    }
    default       -> throw new IllegalArgumentException(cmd);   // ③ throw：这个分支不产出值
};
```

* 箭头右边是表达式时，**不要加 `yield`**，表达式本身就是值。
* 块里必须用 `yield` 给出值，并且**块不能不给值就结束**（实测：`switch rule completes without providing a value`）。
* `throw` 分支合法，不需要值。

### 2.3 `yield`

`yield` 的意思是「这个分支的结果是…，并结束整个 switch 表达式」，类似 `return` 之于方法。它只能在 switch 表达式的块里用：

```java
case MON, TUE, WED, THU, FRI -> {
    int open = 9, close = 16;            // 块内的局部变量，作用域只在这个分支
    yield close - open;
}
```

冒号形式的 switch 表达式也要用 `yield`（`J05Ex2.oldStyleExpr`）：

```java
return switch (n) {
    case 1:
        yield "one";
    case 2:
    case 3:
        yield "two or three";
    default:
        yield "many";
};
```

> `yield` 是**上下文关键字**（contextual keyword），所以老代码里叫 `yield` 的变量名/方法名通常还能用；但调用一个叫 `yield` 的方法要写成 `this.yield(...)` 或 `Thread.yield()`。

### 2.4 switch 表达式里不能「逃出去」

表达式必须产出一个值，所以这些跳转语句在 switch 表达式的分支里**被禁止**：

| 写法 | 实测错误 |
|---|---|
| `break;` 跳出外层循环/switch | `attempt to break out of a switch expression` |
| `return 5;` | `attempt to return out of a switch expression` |
| `continue;` | 同理被禁止 |

允许的出口只有：`yield`、`throw`、正常的箭头表达式。

### 2.5 穷尽性

switch **表达式**必须穷尽（和 J03 讲的一样）。对常量类型：

| 选择器类型 | 怎样才算穷尽 |
|---|---|
| `enum` | 列全所有常量，或写 `default` |
| `int`、`char`、`String` 等 | 必须有 `default`（值域是开放的） |
| sealed / 模式 | J03 的规则 |

实测：枚举漏一个常量，`error: the switch expression does not cover all possible input values`。
**不推荐给 enum 的 switch 表达式加 `default`**：加了之后，将来新增常量时编译器不再提醒。

### 2.6 结果类型怎么确定

switch 表达式的类型取决于所处位置：

* 在**赋值上下文**（`String s = switch ...`）：每个分支都必须能赋给 `String`，否则报 `bad type in switch expression`（实测）。
* 在**独立**位置（`var x = switch ...`）：各分支类型取公共类型；数值分支会做数值提升。`J05Ex2.mixedTypes`：分支分别是 `int`、`double`、`long`，结果是 `double`，所以 `mixedTypes(0)` 是 `1.0`。
  注意这个提升可能让你意外（`long` 变成 `double` 会丢精度），让各分支类型一致最安全。

### 2.7 switch 表达式可以出现在任何表达式能出现的地方

```java
System.out.println("level is " + switch (level) { case 1 -> "low"; case 2 -> "mid"; default -> "high"; });
```

---

## 3. 编译器和 JVM 到底做了什么

箭头和 `yield` 只是**语法糖级别**的变化，没有新的 JVM 指令。编译出来还是 `tableswitch` / `lookupswitch` + `goto`。

### 3.1 箭头形式的编译

`J05Ex1.sign`（`case BUY -> 1; case SELL, SHORT -> -1;`）的字节码（实测）：

```
 0: aload_0
 1: invokevirtual Side.ordinal()
 4: tableswitch { 0: 42   1: 46   2: 46   default: 32 }       // BUY -> 42；SELL、SHORT 都 -> 46
32: new MatchException ... athrow                               // default：不应走到
42: iconst_1;  goto 47
46: iconst_m1
47: ireturn
```

* 每个分支后面的 `goto 47` 是编译器自动加的「跳到 switch 末尾」——这就是 `break` 的作用，由编译器写，你不会忘。
* 多标签 `SELL, SHORT` 就是**两个下标指向同一个地址**（46），不是 fall-through。
* **enum 的 `default` 分支抛 `MatchException`**（Java 21。更早版本抛 `IncompatibleClassChangeError`）。正常永远走不到；
  只有枚举在编译之后新增了常量、而这个 switch 没有重新编译时才会触发。我做了实验：先编译一个只有 `RED, GREEN` 的枚举和一个列全这两个的 switch 表达式，
  再把枚举改成 `RED, GREEN, BLUE` 只重编枚举，传入 `BLUE` → `java.lang.MatchException`。

### 3.2 enum switch 的两种实现

* `enum` 和 `switch` 在**同一个顶层类**里（如 `J05Ex1`）：直接用 `ordinal()` 做 `tableswitch`（上面的字节码）。
* `enum` 在**另一个文件**：编译器生成一个合成类 `Use$1`，里面有静态数组 `$SwitchMap$Col`，在类初始化时把「`ordinal()` → 本次编译时的 case 编号」映射好。
  实测：`Use$1.class` 的 `<clinit>` 里依次 `Col.R.ordinal()`、`Col.G.ordinal()` 写进 `int[]`，每次写都包在 `catch NoSuchFieldError` 里。
  为什么这样绕：枚举常量的 `ordinal()` 在后来重排/增删常量后会变，如果 switch 直接把旧的序号写死，就会走错分支；
  先查表（运行时用当前枚举的 `ordinal()` 取映射）就安全了。

### 3.3 字符串 switch 的编译

`J05Ex1.describe(String)` 的字节码（实测，略有删减）：

```
 5: invokevirtual String.hashCode()
 8: lookupswitch { -2027976644: 80   72438683: 52   102976443: 66   1980572282: 94   default: 105 }
52: aload_1; ldc "LIMIT"; invokevirtual String.equals; ifeq 105; iconst_0; istore_2; goto 105
...
105: iload_2
106: tableswitch { 0: 136   1: 136   2: 141   3: 146   default: 151 }
```

这是**两步**：

1. 先算 `hashCode()`，用 `lookupswitch` 找到「可能是哪个字符串」；因为不同字符串可能哈希碰撞，所以分支里还要 `equals` 确认，确认后把「第几个标签」存到临时变量；
2. 再对这个临时变量做一次普通的 `tableswitch`，跳到分支体。

所以字符串 switch 的代价是「一次 `hashCode`（`String` 缓存了哈希，通常是 O(1)）+ 至多一次 `equals`」，不是逐个比较。
对比 Java 8 的 `if (s.equals("A")) ... else if (s.equals("B")) ...`：分支很多时 switch 更快；分支很少时差别可以忽略。
（`switch` 对 `null` 选择器抛 NPE，因为第一步要调 `hashCode()`。）

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——枚举、字符串、多标签

`examples/J05/J05Ex1.java`：

```java
static int sign(Side s) {
    return switch (s) {
        case BUY -> 1;
        case SELL, SHORT -> -1;
    };
}

static String describe(String cmd) {
    return switch (cmd) {
        case "LIMIT", "limit" -> "limit order";
        case "MARKET" -> "market order";
        case "CANCEL" -> "cancel";
        default -> "unknown: " + cmd;       // String 是开放集合，必须有 default
    };
}
```

实测输出：

```
BUY -> 1
SELL -> -1
SHORT -> -1
limit order
cancel
unknown: foo
two                 <- 最后一段：箭头形式当「语句」用（不产出值）
```

### 例 2：进阶——`yield`、`throw` 分支、冒号形式、类型提升

`examples/J05/J05Ex2.java`（节选）：

```java
static int tradingHours(Day d) {
    return switch (d) {
        case MON, TUE, WED, THU, FRI -> {
            int open = 9, close = 16;
            yield close - open;
        }
        case SAT, SUN -> 0;
    };
}

static long parsePositive(String s) {
    return switch (s.isEmpty() ? 0 : 1) {
        case 0 -> throw new IllegalArgumentException("empty");
        default -> {
            long v = Long.parseLong(s);
            if (v <= 0) throw new IllegalArgumentException("not positive: " + v);
            yield v;
        }
    };
}
```

实测输出：

```
MON 7
SAT 0
42
rejected: empty
rejected: not positive: -3
one | two or three | many         <- 冒号形式 + yield
1.0 2.5 3.0                       <- int / double / long 分支混合，结果提升为 double
level is high                     <- switch 表达式拼进字符串
```

### 例 3：贴近真实——命令解析、枚举方法、手续费

`examples/J05/J05Ex3.java`（节选）：

```java
static Command parse(String line) {
    String[] t = line.strip().split("\\s+");
    return switch (t[0].toUpperCase(Locale.ROOT)) {
        case "LIMIT" -> {
            need(t, 5);
            yield new Limit(Long.parseLong(t[1]), Side.valueOf(t[2].toUpperCase(Locale.ROOT)),
                    Long.parseLong(t[3]), Long.parseLong(t[4]));
        }
        case "CANCEL" -> {
            need(t, 2);
            yield new Cancel(Long.parseLong(t[1]));
        }
        default -> throw new IllegalArgumentException("unknown command: " + t[0]);
    };
}
```

这是 `OrderBook.parse` / `OrderSequence.parse` 的简化版：一个 `switch` 把「命令名」映射成「一个 sealed 类型的值」，每个分支先检查参数个数（块里的 `need(...)`），再 `yield new ...`。
对比老写法：要先声明 `Command result = null;`，每个分支赋值并 `break`，最后 `return result;`——并且可能忘记某个分支没赋值，得到 `null`。

```java
enum Side {
    BUY, SELL;
    Side opposite() { return switch (this) { case BUY -> SELL; case SELL -> BUY; }; }   // 枚举方法里 switch (this)
}

static int feeBps(Liquidity liq, long notional) {
    return switch (liq) {
        case MAKER -> -2;               // 做市方返佣
        case TAKER -> {
            int base = 3;
            int surcharge = notional < 10_000 ? 2 : 0;
            yield base + surcharge;
        }
    };
}
```

实测输出：

```
Limit[id=7, side=BUY, px=18950, qty=100]
Cancel[id=7]
error: limit needs 4 args
error: unknown command: modify
SELL BUY
-2 5 3          <- feeBps(MAKER,5000)、feeBps(TAKER,5000)、feeBps(TAKER,2_000_000)
```

---

## 5. 坑与限制

### 5.1 别混用箭头和冒号

同一个 switch 里 `case 1 -> ...; case 2: ...` 编译错误。需要 fall-through 的少数场景才用冒号，并写注释。

### 5.2 `case` 的表达式必须是编译期常量

`case x ->`（`x` 是普通变量）不行；`case MAX ->` 要求 `MAX` 是 `static final` 且在编译期可知的常量。重复的常量报 `duplicate case label`（实测）。

### 5.3 枚举的 `switch` 表达式不要写 `default`

见 2.5。但**例外**：枚举来自外部库、你控制不了它何时新增常量时，加 `default -> throw ...` 是合理的，因为那时你本来就没有「新增了就编译失败」这个保护。

### 5.4 结果类型提升会悄悄改变类型

`int`/`long`/`double` 分支混用会提升（见 2.6）；`Integer` 和 `int` 混用会拆箱，其中一个是 `null` 时会 NPE。让所有分支类型一致。

### 5.5 `default` 的位置与顺序

老 switch 里 `default` 放在中间有 fall-through 含义。箭头形式没有这个问题，但仍建议 `default` 放最后。

### 5.6 `switch` 语句和表达式的区别要记住

* 语句：`switch (x) { case 1 -> foo(); }` —— 不要求穷尽（对常量），不产出值。
* 表达式：`var y = switch (x) {...};` —— 必须穷尽，每个分支必须产出值或 throw。
* 一个语句如果用了模式或 `case null`，它也必须穷尽（J03）。

### 5.7 `null` 选择器

字符串、枚举、包装类型作选择器，值为 `null` 就抛 `NullPointerException`，除非写了 `case null`（J03，Java 21）。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。

* **`01_video/hc05_market_order_book/reference/OrderBook.java`** —— `parse` 把一行文本变成 sealed `Command`，每个分支一个块 + `yield`：
  ```java
  return switch (t[0].toUpperCase(Locale.ROOT)) {
      case "LIMIT" -> {
          needArgs(t, 5);
          yield new Limit(Long.parseLong(t[1]), side(t[2]), Long.parseLong(t[3]), Long.parseLong(t[4]));
      }
      case "MARKET" -> { needArgs(t, 4); yield new Market(...); }
      ...
      default -> throw new IllegalArgumentException("unknown command: " + t[0]);
  };
  ```
  `execute(Command)` 里的 `case Limit(...) -> { ... yield List.of(new Rejected(id, OVERFLOW)); ... yield events; }` 是在 switch 表达式的块里**多处 `yield`**（`if` 提前给值，末尾再给一次）。
* **`01_video/hc08_order_sequence_api/reference/OrderSequence.java`** —— `parse` 同样用字符串 switch + `yield` 产出 `Put/Delete/CountUpTo/QtyUpTo/IdAt`。
* **`01_video/hc04_queue_mean_snapshot/reference/QueueEvents.java`** —— `parse` 里：
  ```java
  case "push" -> { ...; yield new Push(Long.parseLong(t[1])); }
  case "pop" -> { ...; yield new Pop(); }
  ```
* **`00_oa/oa01_job_chain/reference/JobChains.java`** —— `render` 的 `case Ok(var chains) -> { ... yield lines; }`（模式匹配 + 块 + `yield`）。
* **`01_video/hc03_recursive_sum/reference/RecursiveSum.java`** —— 枚举 `Width { INT, LONG; ... }` 的 `add` 里：
  ```java
  return switch (this) {
      case INT -> Math.toIntExact(s);
      case LONG -> s;
  };
  ```
  这是 `switch (this)` 在枚举方法里的用法，没有 `default`，靠穷尽性保证。

---

## 7. 自测题

1. 下面的代码输出什么？怎么修好它，使 `BUY` 只输出 `buy`？
   ```java
   switch (Side.BUY) {
       case BUY:  System.out.print("buy");
       case SELL: System.out.print("sell"); break;
       default:   System.out.print("other");
   }
   ```
2. 写出等价的 switch 表达式版本：`SELL`/`SHORT` 返回 `-1`，`BUY` 返回 `1`，要求没有 `default` 也能编译。
3. 在 switch 表达式的块里能不能写 `return`？能不能写 `break`？为什么？
4. `case 1 -> { System.out.println("x"); }` 出现在 switch 表达式里为什么编译失败？如何修改？
5. 字符串 switch 编译后是怎样分两步完成的？为什么第一步之后还要 `equals`？

<details><summary>答案</summary>

1. 输出 `buysell`（`BUY` 后面没有 `break`，贯穿到 `SELL`）。修：在 `case BUY:` 的语句后加 `break;`，或改成箭头形式：`case BUY -> System.out.print("buy"); case SELL -> ...`。
2. ```java
   int s = switch (side) { case BUY -> 1; case SELL, SHORT -> -1; };
   ```
   枚举列全了所有常量，编译器认为穷尽，不需要 `default`。
3. 都不能。表达式必须产出一个值，`return`/`break`/`continue` 会让控制流跳出表达式而没有值，编译错误（`attempt to return out of a switch expression` / `attempt to break out of a switch expression`）。要结束分支并给值用 `yield`，要中止用 `throw`。
4. 该块执行完既没有 `yield` 也没有 `throw`，表达式没有值：`switch rule completes without providing a value`。改成 `case 1 -> { System.out.println("x"); yield 0; }`。
5. 第一步：`lookupswitch` 对 `hashCode()` 跳转，找到「候选标签」，在候选里用 `equals` 确认并把标签序号存进临时 int；第二步：对这个序号做 `tableswitch` 跳到分支体。需要 `equals` 是因为不同字符串可能有相同的哈希（碰撞），只靠哈希会误判。

</details>

---

## 8. 延伸阅读

* JEP 361 Switch Expressions — https://openjdk.org/jeps/361 —— 读 Motivation 和 "Description"，里面有 fall-through 和作用域问题的原话和更多例子。
* JLS §15.28 switch Expressions — https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.28 —— 结果类型的确定规则（§15.28.1）。
* JLS §14.11 switch statements — https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.11 —— 语句与表达式的穷尽性差异。
* 下一课：J06 `instanceof` 模式——最简单的一种模式，也是前面所有模式的起点。
