# J05 · `switch` 表达式与 `yield`：让 switch 直接「产出一个值」

> 版本：Java 14 正式（12、13 为预览）。可运行代码：`examples/J05/`。
> 前置：Java 8 的 `switch ... case ...: break;`。J03、J04 已大量用 `case X -> ...` 和 `yield`，本课把这块地基单独讲清，包括对**普通常量**（`int`、`String`、`enum`）的 switch。

---

## 1. 先看痛点：老 switch 是「语句」，三个麻烦一起来

Java 8 的 `switch` 是**语句**（statement）：只做事，不产出值。要用它算值，得先声明临时变量、每个分支赋值、别忘 `break`（`examples/J05/J05Old.java`）：

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

三个麻烦。

### 麻烦一：fall-through（贯穿）

匹配到某个 `case` 后，**从这里一路往下执行，直到遇到 `break`**。忘了 `break` 就掉进下一分支：

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

编译器不报错——fall-through 是**合法**特性（C 语言传下来的）。这类 bug 评审时很难看出：少一行 `break`，缩进依旧是对的。

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

老 switch 对 `enum` 不要求列全。`Side` 以后加了常量，所有老 switch 默默走 `default`（或什么都不做），没人提醒。

### switch 表达式的做法

```java
static int sign(Side s) {
    return switch (s) {
        case BUY -> 1;
        case SELL, SHORT -> -1;
    };
}
```

* `switch` 现在是**表达式**（expression）：有值，能 `return`、赋值、当参数。
* 箭头 `->`：**没有 fall-through**，只执行箭头右边的内容。
* 多标签用逗号：`case SELL, SHORT`。
* `enum` 列全常量就**不需要 `default`**，漏了编译错误。

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

**同一个 `switch` 里不能混用两种形式**（`different case kinds used in the switch`）。

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

* 右边是表达式时**不要加 `yield`**，表达式本身就是值。
* 块里必须用 `yield` 给值，**块不能不给值就结束**（`switch rule completes without providing a value`）。
* `throw` 分支合法，不需要值。

### 2.3 `yield`

`yield` 意为「这个分支的结果是…，并结束整个 switch 表达式」，类似方法里的 `return`，只能用在 switch 表达式的块里：

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

> `yield` 是**上下文关键字**：老代码里叫 `yield` 的变量/方法名通常还能用，但调用叫 `yield` 的方法要写 `this.yield(...)` 或 `Thread.yield()`。

### 2.4 switch 表达式里不能「逃出去」

表达式必须产出值，所以这些跳转在 switch 表达式分支里**被禁止**：

| 写法 | 报错 |
|---|---|
| `break;` 跳出外层循环/switch | `attempt to break out of a switch expression` |
| `return 5;` | `attempt to return out of a switch expression` |
| `continue;` | 同理 |

允许的出口只有 `yield`、`throw`、箭头表达式。

### 2.5 穷尽性

switch **表达式**必须穷尽（同 J03）。对常量类型：

| 选择器类型 | 怎样才算穷尽 |
|---|---|
| `enum` | 列全所有常量，或写 `default` |
| `int`、`char`、`String` 等 | 必须有 `default`（值域是开放的） |
| sealed / 模式 | 见 J03：覆盖所有许可子类型 |

漏一个枚举常量报 `the switch expression does not cover all possible input values`。**enum 的 switch 表达式别加 `default`**：加了之后新增常量编译器不再提醒。

### 2.6 结果类型怎么确定

结果类型取决于位置：

* **赋值上下文**（`String s = switch ...`）：每个分支都得能赋给 `String`，否则 `bad type in switch expression`。
* **独立**位置（`var x = switch ...`）：取各分支公共类型，数值分支做数值提升。`J05Ex2.mixedTypes` 的分支是 `int`、`double`、`long`，结果是 `double`，`mixedTypes(0)` 为 `1.0`。`long` 变 `double` 会丢精度，各分支类型一致最安全。

### 2.7 switch 表达式可以出现在任何表达式能出现的地方

```java
System.out.println("level is " + switch (level) { case 1 -> "low"; case 2 -> "mid"; default -> "high"; });
```

---

## 3. 编译器和 JVM 到底做了什么

箭头和 `yield` 只是**语法糖**，没有新 JVM 指令，编译出来还是 `tableswitch` / `lookupswitch` + `goto`。

### 3.1 箭头形式的编译

`J05Ex1.sign` 的字节码：

```
 0: aload_0
 1: invokevirtual Side.ordinal()
 4: tableswitch { 0: 42   1: 46   2: 46   default: 32 }       // BUY -> 42；SELL、SHORT 都 -> 46
32: new MatchException ... athrow                               // default：不应走到
42: iconst_1;  goto 47
46: iconst_m1
47: ireturn
```

* 每个分支后的 `goto 47` 是编译器加的「跳到 switch 末尾」——就是 `break`，由编译器写，你不会忘。
* 多标签 `SELL, SHORT` 是**两个下标指向同一地址**（46），不是 fall-through。
* **enum 的 `default` 抛 `MatchException`**（更早版本抛 `IncompatibleClassChangeError`）。正常走不到；仅当枚举在编译后新增常量而 switch 没重编译才触发：先编译 `RED, GREEN` 的枚举和列全它们的 switch 表达式，再把枚举改成 `RED, GREEN, BLUE` 只重编枚举，传入 `BLUE` → `MatchException`。

### 3.2 enum switch 的两种实现

* `enum` 与 `switch` 在**同一个顶层类**：直接 `ordinal()` + `tableswitch`（如上）。
* `enum` 在**另一文件**：编译器生成合成类 `Use$1`，含静态数组 `$SwitchMap$Col`，类初始化时把「`ordinal()` → 本次编译的 case 编号」映射好（每次写入包在 `catch NoSuchFieldError` 里）。原因：枚举被增删/重排后 `ordinal()` 会变，写死旧序号会走错分支；运行时查表就安全。

### 3.3 字符串 switch 的编译

`J05Ex1.describe(String)` 的字节码（略有删减）：

```
 5: invokevirtual String.hashCode()
 8: lookupswitch { -2027976644: 80   72438683: 52   102976443: 66   1980572282: 94   default: 105 }
52: aload_1; ldc "LIMIT"; invokevirtual String.equals; ifeq 105; iconst_0; istore_2; goto 105
...
105: iload_2
106: tableswitch { 0: 136   1: 136   2: 141   3: 146   default: 151 }
```

**两步**：

1. 算 `hashCode()`，`lookupswitch` 找到「可能是哪个字符串」；哈希可能碰撞，所以分支里还要 `equals` 确认，并把「第几个标签」存入临时变量；
2. 对该变量做普通 `tableswitch` 跳到分支体。

代价是「一次 `hashCode`（`String` 缓存哈希，通常 O(1)）+ 至多一次 `equals`」，不是逐个比较。分支多时比 `if (s.equals("A")) ... else if ...` 快，少时差别可忽略。`null` 选择器抛 NPE，因为第一步要调 `hashCode()`。

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

输出：

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

输出：

```
MON 7
SAT 0
42
rejected: empty
rejected: not positive: -3
one | two or three | many
1.0 2.5 3.0
level is high
```

* `one | two or three | many`：冒号形式 + yield。
* `1.0 2.5 3.0`：int / double / long 分支混合，结果提升为 double。
* `level is high`：switch 表达式拼进字符串。

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

这是命令解析的简化版：一个 `switch` 把「命令名」映射成 sealed 类型的值，每个分支先检查参数个数（`need(...)`）再 `yield new ...`。老写法要先 `Command result = null;`，每分支赋值并 `break`，还可能漏赋值得到 `null`。

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

输出：

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

同一个 switch 里 `case 1 -> ...; case 2: ...` 编译错误。只有需要 fall-through 时才用冒号，并写注释。

### 5.2 `case` 的表达式必须是编译期常量

`case x ->`（`x` 是普通变量）不行；`case MAX ->` 要求 `MAX` 是 `static final` 的编译期常量。重复常量报 `duplicate case label`。

### 5.3 枚举的 `switch` 表达式不要写 `default`

见 2.5。**例外**：枚举来自外部库、你控制不了它何时加常量时，`default -> throw ...` 合理，因为本来就没有「新增即编译失败」的保护。

### 5.4 结果类型提升会悄悄改变类型

`int`/`long`/`double` 分支混用会提升（2.6）；`Integer` 与 `int` 混用会拆箱，其中一个为 `null` 时 NPE。让所有分支类型一致。

### 5.5 `default` 的位置与顺序

老 switch 里 `default` 放中间有 fall-through 含义；箭头形式没这问题，但仍建议放最后。

### 5.6 `switch` 语句和表达式的区别要记住

* 语句：`switch (x) { case 1 -> foo(); }` —— 对常量不要求穷尽，不产出值。
* 表达式：`var y = switch (x) {...};` —— 必须穷尽，每个分支产出值或 throw。
* 语句若用了模式或 `case null`，也必须穷尽。

### 5.7 `null` 选择器

字符串、枚举、包装类型作选择器，为 `null` 就抛 `NullPointerException`，除非写了 `case null`（Java 21）。

---

## 6. 真实代码里的 switch 表达式

* **`OrderBook`** —— `parse` 把一行文本变成 sealed `Command`，每分支一个块 + `yield`：
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
  `execute(Command)` 的块里有**多处 `yield`**（`if` 提前给值，末尾再给一次）。
* **`OrderSequence`** —— `parse` 同样用字符串 switch + `yield` 产出 `Put/Delete/CountUpTo/QtyUpTo/IdAt`。
* **`QueueEvents`** —— `parse`：
  ```java
  case "push" -> { ...; yield new Push(Long.parseLong(t[1])); }
  case "pop" -> { ...; yield new Pop(); }
  ```
* **`JobChains`** —— `render` 的 `case Ok(var chains) -> { ... yield lines; }`（模式匹配 + 块 + `yield`）。
* **`RecursiveSum`** —— 枚举 `Width { INT, LONG; ... }` 的 `add`：
  ```java
  return switch (this) {
      case INT -> Math.toIntExact(s);
      case LONG -> s;
  };
  ```
  枚举方法里的 `switch (this)`，无 `default`，靠穷尽性保证。

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

1. 输出 `buysell`（`BUY` 后没 `break`，贯穿到 `SELL`）。修：在 `case BUY:` 后加 `break;`，或改箭头形式。
2. ```java
   int s = switch (side) { case BUY -> 1; case SELL, SHORT -> -1; };
   ```
   枚举列全了，编译器认为穷尽，不需要 `default`。
3. 都不能。表达式必须产出值，`return`/`break`/`continue` 会让控制流跳出而没有值（`attempt to return out of a switch expression`）。结束分支并给值用 `yield`，中止用 `throw`。
4. 块执行完既没 `yield` 也没 `throw`，表达式没有值。改成 `case 1 -> { System.out.println("x"); yield 0; }`。
5. 第一步：`lookupswitch` 对 `hashCode()` 跳转得到候选标签，用 `equals` 确认并把序号存入临时 int；第二步：对序号 `tableswitch` 跳到分支体。要 `equals` 是因为不同字符串可能哈希碰撞。

</details>

---

「延伸」J06 `instanceof` 模式：最简单的一种模式，也是前面所有模式的起点。
