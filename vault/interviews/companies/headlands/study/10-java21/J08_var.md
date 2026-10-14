# J08 · `var`：局部变量类型推断

> 版本：Java 10（JEP 286）；Java 11 起可用于 lambda 形参（JEP 323）。
> 本课所有可运行代码在 `study/10-java21/examples/J08/`。
> 前置知识：Java 泛型的基本写法（`List<String>`）、增强 `for`、`try-with-resources`。
> 官方出处：JEP 286 Local-Variable Type Inference — https://openjdk.org/jeps/286 ；官方风格指南 — https://openjdk.org/projects/amber/guides/lvti-style-guide

> `var` 是 Java 最容易被误解的特性之一：它**不是**动态类型，**不是** JavaScript 的 `var`，也**不是**「少写点字」的万能药。
> 本课的重点是：它到底做了什么，什么时候用能让代码更好读，什么时候反而更糟。

---

## 1. 先看痛点：类型在左右两边写两遍，复杂类型占满整行

Java 8 里声明局部变量必须写类型（完整代码：`examples/J08/J08Old.java`）：

```java
Map<String, List<Fill>> bySymbol = new HashMap<String, List<Fill>>();    // Java 7 之前
Map<String, List<Fill>> bySymbol = new HashMap<>();                       // Java 7 加了 <>，右边省略一次

for (Map.Entry<String, List<Fill>> e : bySymbol.entrySet()) {            // 遍历时又得完整写一遍
    ...
}
```

痛点：

1. **冗余（redundancy）**。`new HashMap<...>()` 已经明明白白告诉了你变量的类型，左边再写一遍不增加任何信息。
2. **泛型越复杂越长**。`Map<String, Map<Side, List<Map.Entry<Long, String>>>>` 这种类型，写的人累，读的人更累。
3. **类型名遮挡了变量名和意图**。读代码时眼睛先扫到的是一大串类型，真正有意义的名字 `bySymbol` 被挤到中间。
4. **有些类型根本没法写出来**（匿名类自己的类型、`?:` 产生的交叉类型），Java 8 里只能向上转型到能写的类型，丢掉其中的成员。

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
var fills = new ArrayList<Fill>();       // 推断为 ArrayList<Fill>
var count = 0;                            // int
var name = "AAPL";                        // String
for (var f : fills) { ... }               // f : Fill
```

规则：**编译器看右边初始化表达式的类型，把它当作变量的类型。** 之后这个变量就和你手写了那个类型一模一样。

### 2.2 `var` 不是动态类型

最重要的一点。`var` 变量的类型在**编译期**就确定了，并且不可更改：

```java
var x = 1;        // x 是 int
x = "s";          // 编译错误：incompatible types: String cannot be converted to int
```

对比 JavaScript / Python：那里变量可以先后装不同类型的值。Java 的 `var` 只是「让编译器替你填类型」。

### 2.3 可以用的地方

| 位置 | 例子 |
|---|---|
| 有初始化器的局部变量 | `var list = new ArrayList<Fill>();` |
| 传统 `for` 的循环变量 | `for (var i = 0; i < n; i++)` |
| 增强 `for` 的循环变量 | `for (var e : map.entrySet())` |
| `try-with-resources` | `try (var in = new BufferedReader(...)) { ... }` |
| lambda 的形参（Java 11） | `(var x, var y) -> x + y`（所有形参要么全 `var`，要么全不 `var`；目的是能加注解） |

### 2.4 不能用的地方（编译器的原话，全部实测）

| 写法 | 错误 |
|---|---|
| `var u;`（没有初始化器） | `cannot infer type for local variable u (cannot use 'var' on variable without initializer)` |
| `var n = null;` | `... (variable initializer is 'null')` |
| `var arr = {1, 2, 3};` | `... (array initializer needs an explicit target-type)` |
| `var f = () -> 1;` | `... (lambda expression needs an explicit target-type)` |
| `var m = String::length;` | `... (method reference needs an explicit target-type)` |
| `var x = 1, y = 2;` | `'var' is not allowed in a compound declaration` |
| `var z[] = new int[1];` | `'var' is not allowed as an element type of an array` |
| `var self = self + 1;` | `... (cannot use 'var' on self-referencing variable)` |
| 字段：`var field = 1;` | `'var' is not allowed here` |
| 方法返回类型：`static var g()` | `'var' is not allowed here` |
| 方法参数：`void h(var p)` | `'var' is not allowed here` |

规律：`var` 只用于**局部变量**；右边必须**自己带着足够的类型信息**。lambda、方法引用、数组初始化器、`null` 都需要「目标类型」（左边告诉它是什么），而 `var` 偏偏没有左边的类型，所以不行。

### 2.5 `var` 不是关键字

`var` 是「**保留类型名**」（reserved type name），不是普通关键字。老代码里把变量叫 `var` 依然合法（`int var = 3;`），只是不能把**类**叫 `var`。不用担心升级后旧代码突然坏掉。

---

## 3. 编译器和 JVM 到底做了什么

**什么都没做**——`var` 完全是编译期特性，JVM 看不到。

我用同一份逻辑写了两个方法：

```java
static int a() { var m = new HashMap<String, List<Integer>>(); m.put("a", new ArrayList<>()); return m.size(); }
static int b() { HashMap<String, List<Integer>> m = new HashMap<String, List<Integer>>(); m.put("a", new ArrayList<>()); return m.size(); }
```

用 `javac -g` 编译后 `javap -c -l` 对比（实测）：

* 14 条字节码指令**逐条完全相同**；
* `LocalVariableTable`（调试信息）也完全相同：`m  Ljava/util/HashMap;`。

结论：`var` 在 class 文件里不留任何痕迹；运行时性能、调试器看到的类型，都和手写类型一模一样。
反过来，**它也不会让代码变快或变慢**——纯粹是可读性/可写性问题。

### 推断规则的几个细节

1. **字面量的默认类型**：`var a = 18_950;` 是 `int`，`var b = 18_950L;` 是 `long`，`var c = 1.5;` 是 `double`，`var d = 'x';` 是 `char`。（`J08Ex2` 实测输出 `Integer Long Double Character`，因为通过 `getClass()` 看的是装箱后的类型。）
2. **推断的是「右边表达式的静态类型」，不是「你心里想的类型」**。`var list = new ArrayList<Fill>();` 的类型是 `ArrayList<Fill>`，**不是** `List<Fill>`。如果你希望变量类型是接口（想限制能调用的方法，或为了以后换实现），要显式写 `List<Fill> list = new ArrayList<>();`。
3. **diamond 和 `var` 同时用会退化**：`var list = new ArrayList<>();` 右边没有任何类型信息可用来推 `<>`，结果是 `ArrayList<Object>`（`J08Ex2` 里往里面加了 `"a"` 和 `1` 都不报错）。
4. **非可表示类型（non-denotable type）**：匿名类、交叉类型这些**无法在源码里写出名字**的类型，`var` 能保留：

   ```java
   var anon = new Object() { int hits = 0; void hit() { hits++; } };
   anon.hit();                          // 能调用！如果写 Object anon = new Object() {...}，这行编译不过
   ```

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——局部变量与循环

`examples/J08/J08Ex1.java`：

```java
var fills = new ArrayList<Fill>();                     // ArrayList<Fill>
var bySymbol = new HashMap<String, List<Fill>>();
for (var f : fills) {                                  // f : Fill
    bySymbol.computeIfAbsent(f.symbol, k -> new ArrayList<>()).add(f);
}
for (var e : bySymbol.entrySet()) {                    // e : Map.Entry<String, List<Fill>>
    long total = 0;
    for (var f : e.getValue()) total += f.qty;
    System.out.println(e.getKey() + " " + total);
}
try (var in = new BufferedReader(new StringReader("line1\nline2"))) {
    var line = in.readLine();                           // String
    System.out.println(line.toUpperCase());
}
```

对比 `J08Old`：`Map.Entry<String, List<Fill>> e` 整个不用写。实测输出：

```
MSFT 50
AAPL 125
0 1 2
LINE1
```

### 例 2：进阶——推断规则与陷阱

`examples/J08/J08Ex2.java`（节选）：

```java
var px = 3_000_000;            // int
var qty = 3_000;               // int
var wrong = px * qty;          // int * int = int，溢出！
var right = (long) px * qty;
System.out.println(wrong + " vs " + right);       // 410065408 vs 9000000000
```

这是 `var` 最典型的陷阱：**类型不再写在左边，数字字面量悄悄是 `int`，乘法溢出了没人发现。**
如果写成 `long notional = px * qty;` 左边的 `long` 让读者想到「这是 long」，但**右边仍然是 int 乘法后才转成 long**——两种写法都有这个 bug，不过显式写类型更可能让 reviewer 注意到「为什么右边没转 long」。

另外两个小实验（同一文件）：

```java
var list1 = new ArrayList<>();          // ArrayList<Object>
list1.add("a"); list1.add(1);            // 都能加 -> [a, 1]

var anon = new Object() { int hits = 0; void hit() { hits++; } };
anon.hit(); anon.hit();
System.out.println(anon.hits);           // 2
```

以及 lambda 形参：`BiFunction<Long, Long, Long> add = (var x, var y) -> x + y;`（这里 `var` 唯一的用处是可以写 `(@NonNull var x, ...)` 这类带注解的形参）。

### 例 3：贴近真实——流水线的中间结果

`examples/J08/J08Ex3.java`（节选）：

```java
var qtyBySymbol = fills.stream().collect(
        Collectors.groupingBy(Fill::symbol, TreeMap::new, Collectors.summingLong(Fill::qty)));
// 类型是 TreeMap<String, Long>；不用在左边写

var nested = fills.stream().collect(Collectors.groupingBy(Fill::symbol, TreeMap::new,
        Collectors.groupingBy(Fill::side, () -> new TreeMap<>(Comparator.naturalOrder()),
                Collectors.summingLong(Fill::qty))));
// 类型是 TreeMap<String, TreeMap<Side, Long>>

for (var e : nested.entrySet()) {
    for (var inner : e.getValue().entrySet()) {
        System.out.println(e.getKey() + " " + inner.getKey() + " " + inner.getValue());
    }
}
```

实测输出：

```
{AAPL=180, MSFT=10}
{AAPL={BUY=150, SELL=30}, MSFT={BUY=10}}
AAPL BUY 150
AAPL SELL 30
MSFT BUY 10
1895000 2
```

最后一段示范**不该用 `var`** 的情形：

```java
long notional = compute(fills.get(0));            // 显式写 long：读者一眼知道是 long
Map<String, Long> declared = qtyBySymbol;         // 想把变量类型限制成接口时，显式写接口
```

---

## 5. 坑与限制：什么时候用，什么时候别用

OpenJDK 官方风格指南的核心原则：**「读代码的人能不能只看这一行就知道类型？」**能就用，不能就写出来。

### 5.1 适合用

* 右边**明确出现了类型名**：`var list = new ArrayList<Fill>();`、`var in = new BufferedReader(...)`、`var m = pattern.matcher(s)`。
* 类型很长且无信息量：嵌套泛型、`Map.Entry<K, List<V>>`。
* `for` / `try-with-resources` 的循环变量。
* 变量名本身说明了用途：`var matcher`、`var results`。

### 5.2 不适合用

* **右边是一个方法调用，读者看不出返回类型**：
  ```java
  var x = foo.process(input);     // x 是什么？得翻 foo 的定义
  ```
  这时写出类型是对读者的善意。
* **字面量参与运算**（见例 2）：`var total = 0;` 之后 `total += qty`（`qty` 是 `long`）能通过编译（复合赋值带隐式窄化），但结果被悄悄截成 `int`。数字类型选择是业务语义（`long` 表示金额最小单位），应该显式写出来。
* **希望变量类型是接口/父类**：`List<Fill> list = new ArrayList<>();` 比 `var list = new ArrayList<Fill>();` 表达了「我只依赖 `List` 接口」。
* **public API 的签名**：`var` 本来就不允许（字段、返回值、参数）。

### 5.3 diamond 退化

`var list = new ArrayList<>();` 得到 `ArrayList<Object>`，几乎总是 bug。要么 `var list = new ArrayList<Fill>();`，要么 `List<Fill> list = new ArrayList<>();`。

### 5.4 命名要补偿类型信息

用了 `var`，变量名就得多承担一些「这是什么」的责任：`var results`、`var idToOrder` 比 `var r`、`var m` 好得多。

### 5.5 不要为了「少打几个字」而破坏可读性

IDE 里可以随时看到推断出的类型，但**代码评审、GitHub diff、日志里的代码片段**没有 IDE。写代码是为了被别人（和未来的自己）读。

### 5.6 `var` 不会影响重载解析或泛型推断以外的行为

`var x = someMethod();` 和 `Type x = someMethod();` 之间没有行为差异，只是变量类型来自表达式本身，**不会**像显式类型那样提供目标类型来帮助推断：
`List<String> l = Collections.emptyList();` 能推出 `List<String>`；`var l = Collections.emptyList();` 得到 `List<Object>`。

---

## 6. 在本 kit 哪里用到

所有路径相对 `loop/rounds/`。kit 的约定与风格指南一致：右边有类型名或类型一眼可知时用 `var`，**数值变量显式写类型**。

* **`00_oa/oa01_job_chain/reference/JobChains.java`**：
  ```java
  var jobs = new ArrayList<Job>();
  for (var raw : lines) {
      var m = LINE.matcher(raw);
      ...
  var byId = new LinkedHashMap<Integer, Job>();
  var hasPredecessor = new HashSet<Integer>();
  var out = new ArrayList<Chain>();
  for (var head : byId.values()) { ... }
  ```
  右边都带 `new X<...>()`，类型一目了然。
* **`00_oa/oa01_job_chain/reference/Main.java`**：`var in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));`、`var outcome = JobChains.analyze(in.lines().toList());`。
* **`01_video/hc05_market_order_book/reference/OrderBook.java`**：
  ```java
  var e = book.firstEntry();                  // best()：e 是 Map.Entry<Long, PriceLevel>，类型很长
  var top = opp.firstEntry();
  var bad = validate(cmd);                    // String —— 这个读者要翻 validate 才知道，稍微勉强
  long px = top.getKey();                     // 数值：显式写 long
  long left = sweep(...);                     // 数值：显式写 long
  ```
  同一个文件里能看出分寸：**引用类型用 `var`，需要「这是 long」这类信息的数值用显式类型**。
* **`01_video/hc02_merge_k_streams/reference/MergeK.java`**：
  ```java
  var out = new ArrayList<T>((int) Math.min(total, Integer.MAX_VALUE - 8));
  var its = new ArrayList<Iterator<? extends T>>(lists.size());   // 泛型很长，var 省掉重复
  var snapshot = List.copyOf(sources);
  ```
* **`case Ok(var chains)`、`case Push(var v)`** 等 record 模式里的 `var`：同样的推断机制，见 J04。

---

## 7. 自测题

1. 下列哪些能编译？(a) `var x;` (b) `var y = null;` (c) `var z = new ArrayList<String>();` (d) `var f = () -> 42;` (e) `var a = 1, b = 2;`
2. `var count = 0; long big = 5L; count = big;` 会发生什么？为什么？
3. `var list = new ArrayList<>();` 的类型是什么？之后能不能 `list.add(1); list.add("x");`？
4. `var` 会不会影响运行时性能？怎么验证？
5. 举一个「用 `var` 反而更糟」的例子，并给出改法。

<details><summary>答案</summary>

1. 只有 (c) 能编译。(a) 没有初始化器；(b) `null` 没有类型；(d) lambda 没有目标类型；(e) 复合声明不允许。
2. 编译错误 `incompatible types: possible lossy conversion from long to int`。`var count = 0;` 里 `0` 是 `int` 字面量，`count` 就是 `int`，不能装 `long`。想要 `long` 就写 `var count = 0L;` 或者 `long count = 0;`（显式写更清晰）。
3. `ArrayList<Object>`。两个 `add` 都合法，因为元素类型是 `Object`。通常这不是想要的，应该写 `new ArrayList<String>()` 或显式类型加 diamond。
4. 不影响。用 `javap -c -l` 对比同一逻辑用 `var` 和显式类型写的两个方法：字节码和 `LocalVariableTable` 完全一致（本课 §3 的实验）。
5. 例如 `var total = 0; ... total += qty;`，`qty` 是 `long`：`total` 是 `int`，溢出风险被类型推断悄悄隐藏。改法：`long total = 0;`。另一例：`var result = repo.find(id);` 读者看不出返回的是 `Optional<Order>` 还是 `Order`——显式写出类型，或者把方法名改得更明确（`findOrder`）。

</details>

---

## 8. 延伸阅读

* JEP 286 Local-Variable Type Inference — https://openjdk.org/jeps/286 —— 读 Motivation 里关于「样板代码」的论述，和 Description 里推断规则的完整清单。
* Local Variable Type Inference: Style Guidelines — https://openjdk.org/projects/amber/guides/lvti-style-guide —— 语言设计者写的 `var` 使用准则，列出原则（Principles）和准则（Guidelines），每条有正反例，**强烈建议读完**。
* JEP 323 Local-Variable Syntax for Lambda Parameters — https://openjdk.org/jeps/323 —— 为什么 lambda 形参要允许 `var`。
* JLS §14.4 Local Variable Declarations — https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.4 —— `var` 的精确规则。
* 下一课：J09 Sequenced Collections——给有顺序的集合加上统一的「两端」操作。
