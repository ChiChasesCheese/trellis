# J13 · 未命名变量与模式 `_`：把「我故意不用它」写进代码

> **版本：Java 21 预览（Preview），JEP 443（"Unnamed Patterns and Variables"）；JDK 22 转正，JEP 456，没有改动。**
> 编译 `javac --release 21 --enable-preview`，运行 `java --enable-preview`。**在 JDK 21 上不带 `--enable-preview` 会直接编译失败**（实测见 3 节）。
> 本课代码在 `study/10-java21/examples/J13/`，输出是本机 JDK 21.0.12 实跑的。
> 前置知识：`try/catch`、`for-each`、lambda、`switch`；第 2.3 节用到 J02（sealed）、J03/J04（模式匹配、record 模式），没读过也能看懂例子，但建议回头补。
> 官方出处：JEP 443 — https://openjdk.org/jeps/443 ；转正 JEP 456 — https://openjdk.org/jeps/456

---

## 1. 先看痛点：不用的变量也得起名字

### 1.1 为什么「必须起名」是个问题

Java 的语法规定：**每个声明出来的变量都要有名字**。可现实里有很多变量是「语法要求我声明，但我根本不会用」：

```java
try {
    return Integer.parseInt(s);
} catch (NumberFormatException e) {   // e 根本没用
    return -1;
}

for (String ignored : names) {        // 只想数个数
    n++;
}

counts.computeIfAbsent("k", k -> 0);  // lambda 的参数 k 没用到

if (ev instanceof Fill f) id = f.orderId();   // 其实只需要知道"是 Fill"
```

（完整的 Java 8 风格代码：`examples/J13/J13Old.java`。）

这带来三个小而持续的痛：

1. **读代码的人要多想一步**：看到 `e`，得扫一遍 `catch` 体确认它真的没被用。命名成 `ignored` 是人肉约定，编译器不知道。
2. **静态检查器和 IDE 报"未使用变量"警告**，团队只能加 `@SuppressWarnings` 或统一约定名字，噪声很大。
3. **模式匹配时更明显**。J04 的 record 模式让你一步解构 `Fill(var id, var qty, var px)`；如果只要 `id`，另外两个也必须起名并带着"未使用"警告，
   或者放弃解构回到 `f.orderId()`。

历史上 `_` 在 Java 1.0 是合法标识符；Java 8 起用它会警告，Java 9 起（JEP 213）直接是错误，**就是为了给这个特性腾位置**。

---

## 2. 语法逐条讲

> 预览特性。以下每处，在 JDK 21 都要带 `--enable-preview`。

### 2.1 未命名变量（unnamed variable）：声明处写 `_`

| 位置 | 例子 |
|---|---|
| `catch` 参数 | `catch (NumberFormatException _) { return -1; }` |
| 增强 `for` 的变量 | `for (String _ : names) n++;` |
| 局部变量声明（必须有初始化） | `var _ = map.put("k", 1);`（明示"我故意丢弃返回值"） |
| `try-with-resources` 的资源 | `try (var _ = new Res()) { ... }` |
| lambda 参数 | `computeIfAbsent("z", _ -> 0)`；`(_, _) -> 42` |
| 传统 `for` 的初始化变量 | `for (int i = 0, _ = sideEffect(); i < n; i++)` |

**含义**：声明了变量，但**不能再引用它**，也**不会产生"未使用"警告**。多个 `_` 在同一作用域里合法（例 1 里 `(_, _) -> 42`），因为它们本来就不是能被引用的名字。

### 2.2 未命名模式变量（unnamed pattern variable）：类型模式里不绑定

```java
case Fill _ -> "FILL";            // 等价于 case Fill f -> ... 但不引入变量 f
if (o instanceof Fill _) { ... }  // 只判断类型
```

### 2.3 未命名模式（unnamed pattern）：record 解构里占位

```java
case Fill(var id, _, _) -> id;        // 只取第一个字段，另外两个"我不关心"
case Reject(var id, _) -> id;
case Placed(Order(_, Side s, _, var q)) when q >= 1000 -> ...   // 可嵌套
```

`_` 单独作为一个"模式"：它匹配任何东西（包括类型不同的子结构，类似 `var _` 的效果），**不绑定变量**。

### 2.4 多个模式共用一个 `case` 分支

```java
case Cancel _, Reject _ -> "TERMINAL";
```

这在以前**做不到**：因为 `case A a, B b ->` 里两个绑定变量 `a`、`b` 在分支体里都要能用，但只有一个匹配成立，另一个未初始化，编译器不允许（`illegal fall-through from a pattern`）。
**当所有模式都不引入变量（全是 `_`）时，就没有这个问题，所以允许写在一起**。实测：

```
Bad2.java:2: error: illegal fall-through from a pattern
 static int f(S s){ return switch(s){ case A(var x), B(var y) -> 1; }; }
```

### 2.5 `_` 不是什么

* 不是变量：不能读、不能赋值。`int x = _ + 1;` 编译失败：

```
error: as of release 21, the underscore keyword '_' is only allowed to declare
  unnamed patterns, local variables, exception parameters or lambda parameters
```

* 不是"忽略编译检查"：`sealed` 穷尽性检查照常（`case Cancel _, Reject _` 仍然算覆盖这两个子类型）。
* 不能用在方法参数、字段、`for` 以外的普通局部变量声明**不带初始化**的情形（局部变量 `var _` 必须有初始化）。

---

## 3. 编译器和 JVM 到底做了什么

* **编译器**：把 `_` 当成一个特殊的"不引入名字"的声明：不在作用域里登记，所以没法被引用，也不产生未使用警告。对于模式 `Fill(var id, _, _)`，
  生成的字节码仍然只调用你**需要**的访问器（`id()`），不会为 `_` 的位置调用访问器——这是比"起个名字再不用"略好的一点（访问器通常很便宜，但副作用/成本由你的 record 决定）。
  （这一条是从 JEP 443 描述的语义推出，没有单独反汇编验证。）
* **没有运行时变化**。`_` 不会出现在 class 文件里的局部变量表中。
* **预览标记**：用了 `_` 的类，class 文件被打上预览依赖，必须 `--enable-preview` 运行。实测不带标志编译：

```
J13Ex2.java:11: error: unnamed variables are a preview feature and are disabled by default.
            case Fill _ -> "FILL";
  (use --enable-preview to enable unnamed variables)
```

* **模式的穷尽性**：`case Cancel _, Reject _` 在穷尽性分析里分别算作覆盖 `Cancel` 和 `Reject`，所以 `sealed` 层级少一个子类仍会编译错误（J03）。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——六个位置的 `_`（`J13Ex1.java`）

```java
try { return Integer.parseInt(s); } catch (NumberFormatException _) { return -1; }
for (String _ : names) n++;
var _ = map.put("k", 1);
map.computeIfAbsent("z", _ -> 0);
try (var _ = new Res()) { ... }
BiFunctionLike f = (_, _) -> 42;
```

实测输出：

```
n = 3
map = {k=1, z=0}
  in try
  Res closed
f = 42, parse("x") = -1, parse("12") = 12
evens = 5
```

`try (var _ = new Res())` 的用途：只需要资源的"打开→自动关闭"生命周期（锁、计时器、测试里的 fixture），不需要调用它的方法。

### 例 2：进阶——sealed 层级分类，record 解构跳字段（`J13Ex2.java`）

```java
static String label(Event e) {
    return switch (e) {
        case Fill _ -> "FILL";
        case Cancel _, Reject _ -> "TERMINAL";     // 两个类型共用一个分支
        case Heartbeat _ -> "HB";
    };
}
static long idOf(Event e) {
    return switch (e) {
        case Fill(var id, _, _) -> id;
        case Cancel(var id) -> id;
        case Reject(var id, _) -> id;
        case Heartbeat() -> -1;
    };
}
```

实测输出：

```
Fill[orderId=1, qty=100, px=18950] -> FILL, id=1
Cancel[orderId=2] -> TERMINAL, id=2
Reject[orderId=3, reason=price] -> TERMINAL, id=3
Heartbeat[] -> HB, id=-1
```

### 例 3：贴近真实——嵌套解构 + `when` 守卫（`J13Ex3.java`）

```java
static String classify(Msg m) {
    return switch (m) {
        case Placed(Order(_, Side s, _, var q)) when q >= 1000 -> "BIG " + s;   // 跳过 id 和 px
        case Placed(Order(_, Side s, _, _)) -> "SMALL " + s;
        case Cancelled _ -> "CANCEL";
    };
}
```

对 4 条消息分类计数，实测输出：

```
{BIG BUY=1, BIG SELL=1, CANCEL=1, SMALL BUY=1}
```

四个字段的 `Order` 只取 `side` 和 `qty`：旧写法要么 `case Placed p -> { Order o = p.order(); if (o.qty() >= 1000) ... }`，
要么给 `id`、`px` 起 `var unusedId, var unusedPx`。新写法一行说清"我关心哪两个字段"。

---

## 5. 坑与限制

### 5.1 预览特性（务必说清楚）

* JDK 21（JEP 443）：预览，要 `--enable-preview`。
* **JDK 22（JEP 456）：转正，"没有改动"地定稿**（据 JEP 456 页面："finalize this feature without change"）。所以本课语法在 JDK 22 及以后**不再需要** `--enable-preview`，可以直接用。
* 迁移成本几乎为零：升级后去掉编译/运行参数即可。
* 代价：团队/CI 工具链（旧版 IDE、Checkstyle、SpotBugs、ErrorProne）可能还不认识 `_`，要先确认。
* 本 kit 的 `jtest.py` 固定 `--release 21 --enable-preview`，所以参考解里能直接用 `_`。

### 5.2 `_` 不要用来"藏"重要的结果

`var _ = queue.offer(x);` 明示丢弃返回值，但 `offer` 返回 `false` 意味着队列满了，丢弃它就是在**吞错误**。`_` 表达"我知道有这个值，但确实不重要"；
如果不确定，别用它，写成 `if (!queue.offer(x)) ...`。

### 5.3 `catch (Exception _)` 太宽

`catch (Exception _) { }` 把所有异常（包括 bug）吞掉，而且不留任何痕迹（连变量名都没有，调试时无法加一行日志去看它）。只在**特定的、预期的**异常上用，
并在注释里说明为什么安全（见第 6 节 `InterruptedException` 的例子）。

### 5.4 共用分支只能全是 `_`

`case A a, B b ->` 编译失败，因为 `a`、`b` 不可能同时存在。改成 `case A _, B _ ->`，或者用共同父接口的变量。

### 5.5 方法参数不能写 `_`

`void f(int _)` 不合法。只有 JEP 列出的位置可以用（2.1 的表）。

---

## 6. 在本 kit 哪里用到

`_` 在 kit 里到处是——因为 `jtest.py` 固定 `--enable-preview`。每处都对应 2.x 的一个位置：

| 文件与行 | 片段 | 对应 |
|---|---|---|
| `loop/rounds/00_oa/oa01_job_chain/reference/JobChains.java:106` | `case Malformed _ -> List.of("Malformed Input");` | 2.2 未命名模式变量 |
| `loop/rounds/01_video/hc05_market_order_book/reference/OrderBook.java:245-246` | `case Limit _, Market _ -> byId.containsKey(cmd.id()) ? DUPLICATE_ID : null;` / `case Cancel _, Modify _ -> ...` | 2.4 共用分支 |
| `loop/rounds/01_video/hc06_cpu_register_bitwise/reference/RegisterSim.java:191, 201-211` | `case Not _ -> ~reg;` `case Popcount _ -> Integer.bitCount(reg);` | 2.2 |
| `loop/rounds/01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java:211` | `case Ready<T>(var v, _) -> out.add(v);` | 2.3 record 解构里跳过字段 `stream` |
| `loop/rounds/01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java:123, 128, 172` | `} catch (InterruptedException _) {` | 2.1 catch 参数 |
| `loop/rounds/01_video/hc03_recursive_sum/reference/RecursiveSum.java:85` | `} catch (StackOverflowError _) { // 预期：深度就记在 probe.depth 里 }` | 2.1 catch 参数 |

两个值得细看的：

**`ConcurrentMerge.java:211`**：`Ready<T>` 是 `record Ready<T>(T value, int stream)`；合并输出时只要值：

```java
case Ready<T>(var v, _) -> out.add(v);
case Done<T> _ -> { return out; }
case Pending<T> _ -> throw new AssertionError("blocking poll never returns Pending");
```

**`RecursiveSum.java:85`**：`catch (StackOverflowError _)` 是一个**有意**吞掉的异常——整段代码就是为了测量递归能到多深，栈溢出是预期事件，数据存在 `probe.depth` 字段里。注释写明了为什么吞掉，符合 5.3 的要求。

---

## 7. 自测题

1. 为什么 Java 9 把 `_` 作为标识符变成错误？这跟 JEP 443 有什么关系？
2. 写出下列旧代码的新写法：
   ```java
   try { risky(); } catch (IOException e) { retries++; }
   for (Order o : orders) { count++; }
   ```
3. `case A a, B b -> ...` 为什么非法，`case A _, B _ -> ...` 为什么合法？
4. 下面哪些在 JDK 21 里是合法的？(a) `int _ = 5;` (b) `System.out.println(_);` (c) `void f(int _) {}` (d) `list.forEach(_ -> n++);`（`n` 是数组元素）
5. 这个特性在哪个 JDK 转正？为什么 `RecursiveSum.java:85` 的 `catch (StackOverflowError _)` 可以接受而 `catch (Exception _) {}` 通常不行？

<details><summary>答案</summary>

1. 给 `_` 腾出"未命名"的语义。先让它在旧代码里变成错误（Java 8 警告、Java 9 错误），防止有人把它当普通变量名用，后面才能安全地赋予新含义。
2. `catch (IOException _) { retries++; }`；`for (Order _ : orders) { count++; }`。
3. `a`、`b` 都要在分支体里可用，但每次只有一个模式匹配，另一个没赋值，编译器无法保证安全。`_` 不引入变量，所以没有这个冲突。
4. (a) 合法（有初始化的局部变量，JDK 21 预览）；(b) 非法，`_` 不能读；(c) 非法，方法参数不在允许位置；(d) 合法（lambda 参数）。
5. JDK 22（JEP 456）。`StackOverflowError` 是特定的、预期的事件，并且在注释里说明了为什么吞掉；`catch (Exception _) {}` 会连 bug 一起吞掉，且不留调试线索。

</details>

---

## 8. 延伸阅读

* JEP 443 Unnamed Patterns and Variables (Preview) — https://openjdk.org/jeps/443 —— JDK 21 版，读 Motivation 里"多个 case 共用分支"的那一节。
* JEP 456 Unnamed Variables & Patterns — https://openjdk.org/jeps/456 —— JDK 22 转正。
* JEP 213 Milling Project Coin — https://openjdk.org/jeps/213 —— Java 9 把 `_` 变成错误的那条（该 JEP 的其中一项）。
* JLS 21（预览特性章节）— https://docs.oracle.com/javase/specs/jls/se21/preview/specs/unnamed-jls.html —— 规范文本。
