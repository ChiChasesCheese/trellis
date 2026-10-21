# J08 · `var`：局部变量类型推断

> 版本：Java 10；Java 11 起可用于 lambda 形参。可运行代码：`examples/J08/`。
> 前置：泛型基本写法（`List<String>`）、增强 `for`、`try-with-resources`。
> `var` 最容易被误解：它**不是**动态类型，**不是** JavaScript 的 `var`，也不是「少写点字」的万能药。本课讲它到底做了什么，何时让代码更好读，何时更糟。

---

## 1. 先看痛点：类型在左右两边写两遍，复杂类型占满整行

Java 8 声明局部变量必须写类型（`examples/J08/J08Old.java`）：

```java
Map<String, List<Fill>> bySymbol = new HashMap<String, List<Fill>>();    // Java 7 之前
Map<String, List<Fill>> bySymbol = new HashMap<>();                       // Java 7 加了 <>，右边省略一次

for (Map.Entry<String, List<Fill>> e : bySymbol.entrySet()) {            // 遍历时又得完整写一遍
    ...
}
```

痛点：

1. **冗余**：`new HashMap<...>()` 已说明类型，左边再写一遍没有新信息。
2. **泛型越复杂越长**：`Map<String, Map<Side, List<Map.Entry<Long, String>>>>`，写的累，读的更累。
3. **类型名遮挡变量名和意图**：眼睛先扫到一大串类型，有意义的 `bySymbol` 被挤到中间。
4. **有些类型根本写不出来**（匿名类自己的类型、交叉类型），Java 8 只能向上转型，丢掉其中的成员。

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
var fills = new ArrayList<Fill>();       // 推断为 ArrayList<Fill>
var count = 0;                            // int
var name = "AAPL";                        // String
for (var f : fills) { ... }               // f : Fill
```

规则：**编译器看右边初始化表达式的类型，当作变量的类型**，之后与你手写该类型完全一样。

### 2.2 `var` 不是动态类型

最重要的一点：`var` 的类型在**编译期**确定，不可更改：

```java
var x = 1;        // x 是 int
x = "s";          // 编译错误：incompatible types: String cannot be converted to int
```

JavaScript / Python 的变量可先后装不同类型；Java 的 `var` 只是「让编译器替你填类型」。

### 2.3 可以用的地方

| 位置 | 例子 |
|---|---|
| 有初始化器的局部变量 | `var list = new ArrayList<Fill>();` |
| 传统 `for` 的循环变量 | `for (var i = 0; i < n; i++)` |
| 增强 `for` 的循环变量 | `for (var e : map.entrySet())` |
| `try-with-resources` | `try (var in = new BufferedReader(...)) { ... }` |
| lambda 的形参（Java 11） | `(var x, var y) -> x + y`（所有形参要么全 `var`，要么全不 `var`；目的是能加注解） |

### 2.4 不能用的地方（编译器报错）

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

规律：`var` 只用于**局部变量**，且右边必须**自带足够的类型信息**。lambda、方法引用、数组初始化器、`null` 都要靠左边的「目标类型」，而 `var` 没有左边的类型。

### 2.5 `var` 不是关键字

`var` 是**保留类型名**（reserved type name），不是关键字：老代码里变量叫 `var`（`int var = 3;`）依然合法，只是不能把**类**叫 `var`，升级不会弄坏旧代码。

---

## 3. 编译器和 JVM 到底做了什么

**什么都没做**——`var` 纯编译期特性，JVM 看不到。同一逻辑写两个方法：

```java
static int a() { var m = new HashMap<String, List<Integer>>(); m.put("a", new ArrayList<>()); return m.size(); }
static int b() { HashMap<String, List<Integer>> m = new HashMap<String, List<Integer>>(); m.put("a", new ArrayList<>()); return m.size(); }
```

用 `javac -g` 编译后 `javap -c -l` 对比：14 条字节码指令**逐条相同**，`LocalVariableTable` 也相同（`m  Ljava/util/HashMap;`）。`var` 在 class 文件里不留痕迹，性能和调试器所见与手写类型一样；它也不会让代码变快变慢，纯粹是可读性问题。

### 推断规则的几个细节

1. **字面量默认类型**：`var a = 18_950;` 是 `int`，`18_950L` 是 `long`，`1.5` 是 `double`，`'x'` 是 `char`。（`J08Ex2` 用 `getClass()` 看到的是装箱类型 `Integer Long Double Character`。）
2. **推断的是「右边表达式的静态类型」，不是你心里想的类型**：`var list = new ArrayList<Fill>();` 是 `ArrayList<Fill>`，**不是** `List<Fill>`。想限制成接口（限制可调用方法、方便换实现）就显式写 `List<Fill> list = new ArrayList<>();`。
3. **diamond 与 `var` 同用会退化**：`var list = new ArrayList<>();` 右边无类型信息可推 `<>`，结果是 `ArrayList<Object>`（`J08Ex2` 里加 `"a"` 和 `1` 都不报错）。
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

对比 `J08Old`：整个 `Map.Entry<String, List<Fill>> e` 不用写。输出：

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

这是 `var` 最典型的陷阱：**类型不再写在左边，数字字面量悄悄是 `int`，乘法溢出没人发现。** 写成 `long notional = px * qty;` 也是同样的 bug（右边仍是 int 乘法后才转 long），但显式类型更容易让 reviewer 问「为什么右边没转 long」。

另外两个小实验（同一文件）：

```java
var list1 = new ArrayList<>();          // ArrayList<Object>
list1.add("a"); list1.add(1);            // 都能加 -> [a, 1]

var anon = new Object() { int hits = 0; void hit() { hits++; } };
anon.hit(); anon.hit();
System.out.println(anon.hits);           // 2
```

lambda 形参：`BiFunction<Long, Long, Long> add = (var x, var y) -> x + y;`（`var` 在这里唯一的用处是能写 `(@NonNull var x, ...)` 带注解的形参）。

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

输出：

```
{AAPL=180, MSFT=10}
{AAPL={BUY=150, SELL=30}, MSFT={BUY=10}}
AAPL BUY 150
AAPL SELL 30
MSFT BUY 10
1895000 2
```

最后一段是**不该用 `var`** 的情形：

```java
long notional = compute(fills.get(0));            // 显式写 long：读者一眼知道是 long
Map<String, Long> declared = qtyBySymbol;         // 想把变量类型限制成接口时，显式写接口
```

---

## 5. 坑与限制：什么时候用，什么时候别用

OpenJDK 风格指南的核心原则：**「读代码的人能不能只看这一行就知道类型？」** 能就用，不能就写出来。

### 5.1 适合用

* 右边**明确出现类型名**：`var list = new ArrayList<Fill>();`、`var in = new BufferedReader(...)`、`var m = pattern.matcher(s)`。
* 类型很长且没信息量：嵌套泛型、`Map.Entry<K, List<V>>`。
* `for` / `try-with-resources` 的变量。
* 变量名本身说明用途：`var matcher`、`var results`。

### 5.2 不适合用

* **右边是方法调用，看不出返回类型**：
  ```java
  var x = foo.process(input);     // x 是什么？得翻 foo 的定义
  ```
  写出类型是对读者的善意。
* **字面量参与运算**（例 2）：`var total = 0;` 之后 `total += qty`（`qty` 是 `long`）能编译（复合赋值隐式窄化），但结果被悄悄截成 `int`。数字类型是业务语义，应显式写。
* **希望变量类型是接口/父类**：`List<Fill> list = new ArrayList<>();` 表达了「只依赖 `List`」。

### 5.3 diamond 退化

`var list = new ArrayList<>();` 得到 `ArrayList<Object>`，几乎总是 bug。写 `var list = new ArrayList<Fill>();` 或 `List<Fill> list = new ArrayList<>();`。

### 5.4 命名要补偿类型信息

用了 `var`，变量名要多承担「这是什么」：`var results`、`var idToOrder` 比 `var r`、`var m` 好得多。

### 5.5 不要为「少打几个字」破坏可读性

IDE 能显示推断类型，但**代码评审、GitHub diff、日志片段**没有 IDE。代码是写给人读的。

### 5.6 `var` 不提供目标类型

`var x = someMethod();` 与 `Type x = someMethod();` 行为无差异，但 `var` **不会**像显式类型那样提供目标类型帮助推断：`List<String> l = Collections.emptyList();` 推出 `List<String>`，`var l = Collections.emptyList();` 得到 `List<Object>`。

## 6. 真实代码里的 var

风格：右边有类型名或类型一眼可知时用 `var`，**数值变量显式写类型**。

* **`JobChains`**：
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
* **`Main`**：`var in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));`、`var outcome = JobChains.analyze(in.lines().toList());`。
* **`OrderBook`**：
  ```java
  var e = book.firstEntry();                  // best()：e 是 Map.Entry<Long, PriceLevel>，类型很长
  var top = opp.firstEntry();
  var bad = validate(cmd);                    // String —— 这个读者要翻 validate 才知道，稍微勉强
  long px = top.getKey();                     // 数值：显式写 long
  long left = sweep(...);                     // 数值：显式写 long
  ```
  分寸：**引用类型用 `var`，需要「这是 long」信息的数值用显式类型**。
* **`MergeK`**：
  ```java
  var out = new ArrayList<T>((int) Math.min(total, Integer.MAX_VALUE - 8));
  var its = new ArrayList<Iterator<? extends T>>(lists.size());   // 泛型很长，var 省掉重复
  var snapshot = List.copyOf(sources);
  ```
* record 模式里的 `case Ok(var chains)`、`case Push(var v)`：同一套推断机制，类型取自组件声明。

---

## 7. 自测题

1. 下列哪些能编译？(a) `var x;` (b) `var y = null;` (c) `var z = new ArrayList<String>();` (d) `var f = () -> 42;` (e) `var a = 1, b = 2;`
2. `var count = 0; long big = 5L; count = big;` 会发生什么？为什么？
3. `var list = new ArrayList<>();` 的类型是什么？之后能不能 `list.add(1); list.add("x");`？
4. `var` 会不会影响运行时性能？怎么验证？
5. 举一个「用 `var` 反而更糟」的例子，并给出改法。

<details><summary>答案</summary>

1. 只有 (c) 能编译。(a) 没有初始化器；(b) `null` 没有类型；(d) lambda 没有目标类型；(e) 复合声明不允许。
2. 编译错误 `incompatible types: possible lossy conversion from long to int`：`0` 是 `int` 字面量，`count` 就是 `int`。想要 `long` 写 `var count = 0L;` 或 `long count = 0;`。
3. `ArrayList<Object>`，两个 `add` 都合法。通常不是想要的，应写 `new ArrayList<String>()` 或显式类型加 diamond。
4. 不影响。`javap -c -l` 对比 `var` 与显式类型的两个方法：字节码和 `LocalVariableTable` 完全一致（§3）。
5. `var total = 0; ... total += qty;`（`qty` 是 `long`）：`total` 是 `int`，溢出风险被推断悄悄隐藏，改 `long total = 0;`。再如 `var result = repo.find(id);` 读者看不出是 `Optional<Order>` 还是 `Order`——显式写类型，或把方法名改明确（`findOrder`）。

</details>

---

「延伸」J09 Sequenced Collections：给有顺序的集合统一的「两端」操作。
