# J06 · `instanceof` 模式：判断类型和转型合成一步

> 版本：Java 16 正式（14、15 为预览）；Java 21 起允许「总是匹配」的模式。可运行代码：`examples/J06/`。
> 前置：普通 `instanceof` 与强制类型转换（cast）。
> 这是最简单的一种模式，也是 J03、J04 里 `case String s`、`case Point(var x, var y)` 的原型；理解它的作用域规则，后面就顺了。

---

## 1. 先看痛点：判断一次，转型再写一次

**类型转换**（cast）把引用「当作」另一类型：`(String) o`；真实类型不符则运行时抛 `ClassCastException`，所以转型前习惯先 `instanceof`。Java 8 里这是固定两步套路（`examples/J06/J06Old.java`）：

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

1. **类型名写两遍**：`instanceof Price` 与 `(Price) o` 必须一致，改一个忘另一个就出错。
2. **噪音**：核心意图是「是价格就比较字段」，却被检查、转型、命名分散了注意力。
3. **作用域松散**：`other` 在 `if` 外也存在，却只在那一个分支里有意义。

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
if (o instanceof String s) {
    System.out.println(s.length());       // s 的类型是 String，不用再强转
}
```

`o instanceof String s` 一次做三件事：检查 `o` 是不是 `String`（`null` 永不匹配，同旧 `instanceof`）；是则转成 `String`；声明局部变量 `s` 并绑定。`String s` 叫**类型模式**（type pattern），`s` 叫**绑定变量**（binding variable）。

旧写法要 `if (o instanceof String) { String s = (String) o; ... }`（类型名 3 次、变量范围手动定），新写法 `if (o instanceof String s) { ... }`（1 次、范围由编译器按「何时一定匹配」推出）。
### 2.2 与 `&&` 连用

```java
if (o instanceof String s && s.length() > 3) { ... }
```

`&&` **短路**：左边为 `false` 就不算右边，所以到右边时左边必为 `true`，`s` 一定有值。旧写法得嵌套 if。

### 2.3 绑定变量的作用域（flow scoping）——本课最重要的概念

绑定变量**只在编译器能证明「模式一定匹配了」的地方**可用，叫**流敏感作用域**（flow scoping）。不用死记，问一句：

> 「走到这一行时，`o instanceof String s` 是不是**一定**为 `true`？」

一定 → `s` 可用；不一定 → 不可用（`cannot find symbol`）。

常见情形：

| 写法 | `s` 在哪里可用 | 理由 |
|---|---|---|
| `if (o instanceof String s) { A } else { B }` | 只在 `A` | 进入 A 说明匹配了；进入 B 说明没匹配 |
| `o instanceof String s && s.isEmpty()` | `&&` 右边 | 右边只在左边为真时才算 |
| `o instanceof String s \|\| s.isEmpty()` | **哪里都不行**（`cannot find symbol`） | 右边在左边为**假**时才算，此时没匹配 |
| `!(o instanceof String s) \|\| s.isEmpty()` | `\|\|` 右边 | 左边为假 = 匹配成功 |
| `if (!(o instanceof String s)) { return; } use(s);` | `if` 之后的整个剩余部分 | 没匹配的路径已经 `return` 了，能走到后面的一定匹配了 |
| `while (i < n && xs.get(i) instanceof Integer k) { ... k ... }` | 循环体 | 循环体只在条件为真时进入 |
| `cond ? (o instanceof String s ? s : "") : ...` | 三元运算符的对应分支 | 同样按「一定为真」推 |

`J06Ex1.firstChar` 是第五种，叫**卫语句**（guard clause）写法：

```java
static String firstChar(Object o) {
    if (!(o instanceof String s)) {
        return "not a string";
    }
    return "first char of " + s + " is " + s.charAt(0);    // s 在这里可用！
}
```

好处：少一层缩进，「出错情况先处理，正常路径往下写」。

### 2.4 绑定变量的其他规则

* **名字不能与已有局部变量/参数冲突**（`variable s is already defined`）；同一条件里重复绑定同名也不行。
* **绑定变量默认不是 `final`**，可重新赋值；想禁止写 `o instanceof final String s`。
* **类型必须可能成立**：`Integer x; x instanceof String s` 编译错误，`Integer` 永不可能是 `String`。
* **泛型**：`o`（`Object`）`instanceof List<String> l` 被拒绝（擦除后无法检查 `<String>`），`List<?> l` 可以；`o` 静态类型已是 `List<String>` 时 `o instanceof ArrayList<String> al` 安全（`J06Ex2.generic2`）。
* **Java 21 允许总是匹配的模式**：`String s; s instanceof String t`。Java 16–20 里这是编译错误；放开是为了与 `switch` 的无条件模式规则统一，语义是「`s` 非 `null` 时为 `true`」。

### 2.5 与 record 模式的关系

Java 21 里 `instanceof` 右边还可以是 record 模式（J04），规则完全一样，只是顺便拆开 record：

```java
if (e instanceof Trade(var px, var qty) && qty >= minQty) { ... }
```

---

## 3. 编译器和 JVM 到底做了什么

JVM **没有新指令**，`instanceof` 模式是编译器语法糖，编译后就是你以前手写的那套。`J06Ex1.firstChar` 的字节码：

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

* 生成 `instanceof` → `checkcast` → `astore`，与手写 `(String) o` 完全相同，性能一样；`checkcast` 前有 `instanceof` 保护，**永不**抛 `ClassCastException`。
* 绑定变量就是普通局部变量槽（slot）；「作用域」只是**编译期名字可见性检查**，运行时不存在。
* `||` 右边、`if` 之外等「不一定匹配」的位置，编译器按 definitely matched 流分析把名字标为不可见——这就是 2.3 那张表的由来。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——基本形式、`&&`、`null`、卫语句

`examples/J06/J06Ex1.java` 输出：

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

输出：

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

`equals` 新写法还有个好处：`o instanceof Instrument` 对 `null` 返回 `false`，**不需要单独的 `o == null` 检查**。

> 注意：`Instrument` 若可被继承，`instanceof` 版 `equals` 会让子类与父类实例可能「相等」，破坏对称性，此时改用 `getClass() == o.getClass()`。`final` 类和 record（`equals` 自动生成）没有这个问题。

输出：

```
true  false  false  false          <- 同一对象内容相等 / 交易所不同 / 与字符串比较 / 与 null 比较
1 2 30 -1                          <- readLong 的 Integer / Long / String / 缺省
17                                 <- tradedQty = 5 + 12
[12@101]                           <- bigTrades(minQty=10)
```

---

## 5. 坑与限制

### 5.1 `||` 里用绑定变量

`o instanceof String s || s.isEmpty()` 编译不过。想表达「不是 String 或是空串」写成 `!(o instanceof String s) || s.isEmpty()`。

### 5.2 `if` 之后使用绑定变量，必须保证没匹配的路径已经结束

```java
if (o instanceof String s) { return 1; }
return s.length();          // 编译错误：s 不在作用域
```

反过来写 `if (!(o instanceof String s)) { return/throw/continue; }` 之后就能用 `s`——前提是 `if` 块**不能正常结束**（必须 `return`/`throw`/`break`/`continue`）；只是打印一句话，`s` 仍不可用。

### 5.3 重复名字

同一方法里别放多个 `String s`（含参数）。`if/else if` 链里多个 `instanceof String s` 各自独立，可同名；但 `a instanceof X s && b instanceof Y s` 同条件内同名会报错。

### 5.4 `instanceof` 链依然不会帮你检查「处理全了没有」

`if / else if` 一路 `instanceof` 下去，编译器不检查穷尽性；分派多个类型请用 `switch`。`instanceof` 模式适合**只关心一种类型**，或**一个条件里同时用类型和字段**。

### 5.5 `equals` 的继承问题

见例 3 的注：可继承类用 `getClass() == o.getClass()`。

### 5.6 `instanceof` 太多往往是设计信号

到处 `if (x instanceof A) ... else if (x instanceof B) ...`，通常说明「按类型分派」该用 sealed + switch 或多态方法。

---

## 6. 真实代码里的 instanceof 模式

用得不多——按类型分派的场合都被 `switch` 模式接管了。真实用到的：

* **`BatchMatcher`** —— 对事件流过滤，两种形式都有：
  ```java
  if (e instanceof OrderBook.Rejected(var id, var why)) {         // record 模式
      throw new ArithmeticException("row " + (id - 1) + ": " + why);
  }
  ...
  List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
      if (e instanceof OrderBook.Trade t) sink.accept(t);          // 类型模式
  }).toList();
  ```
  第二处是流水线里「只挑某一种」的惯用写法（`mapMulti` 把每个元素映射成 0..n 个输出，靠 `sink.accept` 发出）。
* **`ConcurrentMerge`** ——
  ```java
  scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
  ```
  三元运算符里的 `instanceof`：`me` 只在「是 `MergeException`」的分支可用。
* **`Main`** —— `if (outcome instanceof JobChains.Malformed) System.exit(1);` 只有类型检查、没有绑定变量（旧式 `instanceof`，依然合法）。

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

1. (a) 能；(b) 不能：`||` 右边在左边为假时才算，`s` 未绑定；(c) 能：if 块 `return` 了，后面一定匹配；(d) 不能：if 块只打印，能正常走完，后面不一定匹配。
2. `false`，`s` 未绑定（不进分支）。
3. 没区别：`instanceof` + `checkcast` + `astore`，绑定变量就是普通局部变量槽。
4. `instanceof` 同时完成「判空、判类型、转型、命名」；`null instanceof Foo` 为 `false`，所以安全。（前提：类是 `final`，或确实想允许子类相等。）
5. 改用 sealed 接口 + `switch` 模式匹配：编译器检查穷尽，字节码走 `typeSwitch`；或把行为放进多态方法。

</details>

「延伸」J07 文本块：把多行字符串写成多行。
