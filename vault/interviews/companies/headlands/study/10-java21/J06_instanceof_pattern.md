# J06 · `instanceof` 模式：判断类型和转型合成一步

> 版本：Java 16 正式（JEP 394）。Java 14、15 是预览（JEP 305、JEP 375）。Java 21 起允许「总是匹配」的模式（JEP 440/441 的配套变化）。
> 本课所有可运行代码在 `study/10-java21/examples/J06/`。
> 前置知识：普通的 `instanceof` 与强制类型转换（cast）。
> 官方出处：JEP 394 Pattern Matching for instanceof — https://openjdk.org/jeps/394 ；语言规范 §15.20.2 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.20.2

> 这是所有「模式」里最简单的一种，也是 J03、J04 里 `case String s`、`case Point(var x, var y)` 的原型。理解了它的作用域规则，后面的就都顺了。

---

## 1. 先看痛点：判断一次，转型再写一次

先复习一个概念。**类型转换**（cast）是把一个引用「当作」另一个类型：`(String) o`。如果 `o` 真实类型不是 `String`，运行时抛 `ClassCastException`。
所以转型之前习惯先用 `instanceof` 检查一次。Java 8 里这是固定的两步套路（完整代码：`examples/J06/J06Old.java`）：

```java
@Override public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Price)) return false;       // 第一步：检查类型
    Price other = (Price) o;                        // 第二步：转型，并再声明一个变量
    return ticks == other.ticks && Objects.equals(symbol, other.symbol);
}
```

以及读弱类型配置值（`Map<String, Object>`）：

```java
Object v = cfg.get(key);
if (v instanceof Integer) {
    return ((Integer) v).longValue();               // 又是括号套括号的转型
} else if (v instanceof Long) {
    return (Long) v;
} else if (v instanceof String) {
    return Long.parseLong(((String) v).trim());
}
```

痛点：

1. **类型名写两遍**。`instanceof Price` 和 `(Price) o` 必须一致；复制粘贴改了一个忘改另一个，要么编译错误，要么（更糟）逻辑错误。
2. **噪音**。核心意图是「如果是价格就比较字段」，却被检查、转型、命名三件事分散了注意力。
3. **作用域松散**。`other` 在 `if` 之外也存在，但只有那一个分支里它才有意义。

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
if (o instanceof String s) {
    System.out.println(s.length());       // s 的类型是 String，不用再强转
}
```

`o instanceof String s` 一次做三件事：

1. 检查 `o` 是不是 `String`（`null` 永远不匹配，和旧 `instanceof` 一样）；
2. 如果是，把它转成 `String`；
3. 声明新的局部变量 `s` 并绑定到转型后的值。

这里的 `String s` 就是一个**类型模式**（type pattern），`s` 是**绑定变量**（binding variable，也叫模式变量 pattern variable）。

旧写法 vs 新写法：

| | 旧 | 新 |
|---|---|---|
| 写法 | `if (o instanceof String) { String s = (String) o; ... }` | `if (o instanceof String s) { ... }` |
| 类型名次数 | 3 次 | 1 次 |
| 变量的有效范围 | 你手动定的 | 编译器按「什么时候一定匹配」推出 |

### 2.2 与 `&&` 连用

```java
if (o instanceof String s && s.length() > 3) { ... }
```

`&&` 是**短路**的：左边为 `false` 就不算右边。所以到右边时，左边一定为 `true`，`s` 一定有值，可以直接用。
这是旧写法做不到的（旧写法得嵌套 if）。

### 2.3 绑定变量的作用域（flow scoping）——本课最重要的概念

绑定变量**只在编译器能证明「模式一定匹配了」的地方**可用。这叫**流敏感的作用域**（flow scoping）。规则不需要死记，用一个问题推导：

> 「走到这一行时，`o instanceof String s` 是不是**一定**为 `true`？」

一定为 `true` → `s` 可用；不一定 → `s` 不可用（实测错误：`cannot find symbol`）。

常见情形：

| 写法 | `s` 在哪里可用 | 理由 |
|---|---|---|
| `if (o instanceof String s) { A } else { B }` | 只在 `A` | 进入 A 说明匹配了；进入 B 说明没匹配 |
| `o instanceof String s && s.isEmpty()` | `&&` 右边 | 右边只在左边为真时才算 |
| `o instanceof String s \|\| s.isEmpty()` | **哪里都不行**（实测 `cannot find symbol`） | 右边在左边为**假**时才算，此时没匹配 |
| `!(o instanceof String s) \|\| s.isEmpty()` | `\|\|` 右边 | 左边为假 = 匹配成功 |
| `if (!(o instanceof String s)) { return; } use(s);` | `if` 之后的整个剩余部分 | 没匹配的路径已经 `return` 了，能走到后面的一定匹配了 |
| `while (i < n && xs.get(i) instanceof Integer k) { ... k ... }` | 循环体 | 循环体只在条件为真时进入 |
| `cond ? (o instanceof String s ? s : "") : ...` | 三元运算符的对应分支 | 同样按「一定为真」推 |

`J06Ex1.firstChar` 示范了第五种，叫「**卫语句**（guard clause）**写法**」：

```java
static String firstChar(Object o) {
    if (!(o instanceof String s)) {
        return "not a string";
    }
    return "first char of " + s + " is " + s.charAt(0);    // s 在这里可用！
}
```

好处：不用多一层缩进，「出错情况先处理，正常路径往下写」的风格保持一致。

### 2.4 绑定变量的其他规则

* **名字不能与已有局部变量/参数冲突**（实测 `variable s is already defined in method ...`）；同一个条件里重复绑定同名变量也不行（`illegal attempt to redefine an existing match binding`）。
* **绑定变量默认不是 `final`**，可以重新赋值：`if (o instanceof String s) { s = s.trim(); ... }`。想禁止就写 `o instanceof final String s`（实测：之后给它赋值报 `cannot assign a value to final variable`）。
* **类型必须可能成立**：`Integer x; if (x instanceof String s)` 编译错误（`Integer cannot be converted to String`），因为 `Integer` 永远不可能同时是 `String`。
* **泛型**：`o instanceof List<String> l`（`o` 是 `Object`）会被拒绝（运行时擦除，没法检查 `<String>`）。`o instanceof List<?> l` 可以。
  当 `o` 的静态类型已经是 `List<String>` 时，`o instanceof ArrayList<String> al` 是安全的，可以写（`J06Ex2.generic2`）。
* **Java 21 允许总是匹配的模式**：`String s; if (s instanceof String t) {...}`。Java 16–20 里这是编译错误（因为 100% 匹配，除了 null）。
  现在允许，是为了让 `instanceof` 和 `switch` 的模式规则统一（J03 的无条件模式）。语义：`s` 非 `null` 时为 `true`。

### 2.5 和 record 模式（J04）的关系

Java 21 里 `instanceof` 的右边除了类型模式，还可以是 record 模式：

```java
if (e instanceof Trade(var px, var qty) && qty >= minQty) { ... }
```

规则完全一样——只是多了「顺便拆开 record」。

---

## 3. 编译器和 JVM 到底做了什么

JVM 层面**没有新指令**。`instanceof` 模式完全是编译器的语法糖，编译后就是你以前手写的那一套。
`J06Ex1.firstChar` 的字节码（实测）：

```
 0: aload_0
 1: instanceof  java/lang/String        // 旧的 instanceof 指令
 4: ifeq        15                      // 不是 String -> 跳到 15
 7: aload_0
 8: checkcast   java/lang/String        // 转型（编译器自动加的）
11: astore_1                            // 存进局部变量 1 —— 这就是绑定变量 s
12: goto        18
15: ldc "not a string"; areturn         // 卫语句里的 return
18: aload_1  ...  s.charAt(0)           // 后面直接使用局部变量 1
```

* 编译器生成 `instanceof` → `checkcast` → `astore`，和你手写的 `(String) o` 完全相同；性能一样。
* 绑定变量就是一个普通的局部变量槽（slot）。所谓「作用域」只是**编译期的名字可见性检查**，不存在于运行时。
* `checkcast` 前面已有 `instanceof` 保护，所以**永远不会**抛 `ClassCastException`。
* 因为 `||` 右边、`if` 之外等位置「不一定匹配」，编译器在这些位置把名字标成不可见——这就是上面 §2.3 那张表的由来，规则都是在编译期按「definitely matched」流分析推出来的。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——基本形式、`&&`、`null`、卫语句

`examples/J06/J06Ex1.java` 实测输出：

```
5                          <- "hello".length()
long string: hello         <- o instanceof String s && s.length() > 3
false                      <- null instanceof String
null is not a String
first char of abc is a not a string      <- firstChar("abc") + " " + firstChar(42)
```

### 例 2：进阶——作用域、`while`、泛型、`final`、总是匹配

`examples/J06/J06Ex2.java`（节选）：

```java
static String and(Object o) {
    return (o instanceof String s && !s.isEmpty()) ? "nonempty string " + s : "no";
}

static String or(Object o) {
    if (!(o instanceof String s) || s.isEmpty()) {
        return "not a nonempty string";      // 这里 s 不可用（可能没匹配）
    }
    return "string " + s;                     // 这里 s 可用
}

static int sumUntilNonInt(List<Object> xs) {
    int sum = 0, i = 0;
    while (i < xs.size() && xs.get(i) instanceof Integer n) { sum += n; i++; }
    return sum;
}
```

实测输出：

```
nonempty string x | no | no
string x | not a nonempty string | not a nonempty string
6                           <- sumUntilNonInt(List.of(1, 2, 3, "stop", 4)) = 1+2+3
list of 2 | not a list
arraylist 1 | other list    <- generic2(new ArrayList<>(...)) / generic2(List.of("a"))
ABC
string a | null!            <- Java 21 允许 s instanceof String t；null 时为 false
```

### 例 3：贴近真实——`equals`、弱类型配置、事件过滤

`examples/J06/J06Ex3.java`：

```java
// 1. equals：判断 + 转型 + 命名，一行
@Override public boolean equals(Object o) {
    return o instanceof Instrument other
            && ticker.equals(other.ticker)
            && exchange.equals(other.exchange);
}

// 2. 配置值
static long readLong(Map<String, Object> cfg, String key, long dflt) {
    Object v = cfg.get(key);
    if (v instanceof Integer i) return i;
    if (v instanceof Long l) return l;
    if (v instanceof String s && !s.isBlank()) return Long.parseLong(s.trim());
    return dflt;
}

// 3. 事件过滤（带 record 模式）
if (e instanceof Trade(var px, var qty) && qty >= minQty) out.add(qty + "@" + px);
```

`equals` 的新写法比 Java 8 还有一个好处：`o instanceof Instrument` 对 `null` 返回 `false`，所以**不需要单独写 `o == null` 的检查**（旧写法里 `getClass() != o.getClass()` 那一套才需要）。

> 注意：如果 `Instrument` 可以被继承，`instanceof` 版的 `equals` 会让子类实例与父类实例可能「相等」，破坏对称性；这时用 `getClass() == o.getClass()`。
> 对 `final` 类（或 record——record 的 `equals` 是自动生成的）没有这个问题。

实测输出：

```
true  false  false  false          <- 同一对象内容相等 / 交易所不同 / 与字符串比较 / 与 null 比较
1 2 30 -1                          <- readLong 的 Integer / Long / String / 缺省
17                                 <- tradedQty = 5 + 12
[12@101]                           <- bigTrades(minQty=10)
```

---

## 5. 坑与限制

### 5.1 `||` 里用绑定变量

`o instanceof String s || s.isEmpty()` 编译不过（实测 `cannot find symbol`）。想表达「不是 String 或者是空串」写成 `!(o instanceof String s) || s.isEmpty()`。

### 5.2 `if` 之后使用绑定变量，必须保证没匹配的路径已经结束

```java
if (o instanceof String s) { return 1; }
return s.length();          // 编译错误：s 不在作用域
```

反过来写 `if (!(o instanceof String s)) { return/throw/continue; }` 之后就能用 `s`——前提是 `if` 块**不能正常结束**（必须 `return`/`throw`/`break`/`continue`）。如果 if 块里只是打印一句话，`s` 仍然不可用。

### 5.3 重复名字

同一个方法里不要多个 `String s`（包括参数）。`if/else if` 链里的多个 `instanceof String s` 是各自独立的作用域，可以同名；但 `a instanceof X s && b instanceof Y s` 同一个条件里同名会报错。

### 5.4 `instanceof` 链依然不会帮你检查「处理全了没有」

`if / else if` 一路 `instanceof` 下去，编译器不检查穷尽性。分派多个类型请用 `switch`（J03）。`instanceof` 模式适合：**只关心一种类型**，或者**一个条件里要同时用类型和字段**。

### 5.5 `equals` 的继承问题

见 §4 例 3 的注。

### 5.6 `instanceof` 太多往往是设计信号

代码里到处 `if (x instanceof A) ... else if (x instanceof B) ...`，通常说明「按类型分派」应该用 sealed + switch（J02、J03）或多态方法。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。`instanceof` 模式在本 kit 里用得不多——因为按类型分派的场合都被 `switch` 模式接管了。真实用到的：

* **`01_video/hc05_market_order_book/reference/BatchMatcher.java`** —— 对事件流做过滤，两种形式都有：
  ```java
  if (e instanceof OrderBook.Rejected(var id, var why)) {         // record 模式
      throw new ArithmeticException("row " + (id - 1) + ": " + why);
  }
  ...
  List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
      if (e instanceof OrderBook.Trade t) sink.accept(t);          // 类型模式
  }).toList();
  ```
  第二处是流水线里「只挑某一种」的惯用写法（`mapMulti` 见 J14）。
* **`01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java`** —— 
  ```java
  scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
  ```
  三元运算符里的 `instanceof`：`me` 只在「是 `MergeException`」的分支可用。
* **`00_oa/oa01_job_chain/reference/Main.java`** —— `if (outcome instanceof JobChains.Malformed) System.exit(1);` 只有类型检查，没有绑定变量（这种就是旧式 `instanceof`，依然合法）。

---

## 7. 自测题

1. 下面哪些能编译？
   ```java
   // (a)
   if (o instanceof String s && s.length() > 2) { }
   // (b)
   if (o instanceof String s || s.length() > 2) { }
   // (c)
   if (!(o instanceof String s)) return;  System.out.println(s);
   // (d)
   if (!(o instanceof String s)) { System.out.println("no"); }  System.out.println(s);
   ```
2. `o` 为 `null` 时 `o instanceof String s` 的结果是什么？`s` 有值吗？
3. `instanceof` 模式编译后和手写 `instanceof` + 强转有什么区别（字节码层面）？
4. 为什么说「Java 16 之后手写 `equals` 的第一步可以直接写成 `return o instanceof Foo other && ...`」？这样写对 `null` 是否安全？
5. 有人写了十几个 `else if (x instanceof Foo f)`，你应该怎么建议？

<details><summary>答案</summary>

1. (a) 能；(b) 不能：`||` 右边在左边为假时才算，此时 `s` 未绑定；(c) 能：if 块 `return` 了，后面一定匹配；(d) 不能：if 块里只是打印，能正常走完，后面不一定匹配。
2. 结果 `false`，`s` 没有被绑定（不会进入分支）。
3. 没有区别：`instanceof` + `checkcast` + `astore`。绑定变量就是一个普通局部变量槽。
4. 因为 `instanceof` 同时完成「判空、判类型、转型、命名」。`null instanceof Foo` 为 `false`，所以不需要单独的 `o == null` 检查，安全。（前提：类是 `final` 或确实想允许子类相等。）
5. 用 sealed 接口 + `switch` 模式匹配（J02、J03）：编译器会检查是否穷尽，且字节码用 `typeSwitch`；或者把行为放进多态方法。

</details>

---

## 8. 延伸阅读

* JEP 394 Pattern Matching for instanceof — https://openjdk.org/jeps/394 —— Description 里 "Scope of pattern variables" 一节用一张表格列出了所有作用域规则。
* JEP 305 Pattern Matching for instanceof (Preview) — https://openjdk.org/jeps/305 —— 第一版，对比能看到哪些设计后来被收紧。
* JLS §6.3.1 Scope for Pattern Variables — https://docs.oracle.com/javase/specs/jls/se21/html/jls-6.html#jls-6.3.1 —— flow scoping 的精确规则（"introduced by"）。
* 《Effective Java》第 3 版 Item 10（Obey the general contract when overriding equals）—— `equals` 的契约与继承问题，用来理解 §4 的注。
* 下一课：J07 文本块——把多行字符串写成多行。
