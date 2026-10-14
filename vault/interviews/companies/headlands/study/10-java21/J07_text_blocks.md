# J07 · 文本块 `"""`：多行字符串照着原样写

> 版本：Java 15 正式（JEP 378）。Java 13、14 是预览（JEP 355、JEP 368）。
> 本课所有可运行代码在 `study/10-java21/examples/J07/`。
> 前置知识：字符串、转义序列（`\n`、`\"`）、字符串拼接。
> 官方出处：JEP 378 Text Blocks — https://openjdk.org/jeps/378 ；语言规范 §3.10.6 — https://docs.oracle.com/javase/specs/jls/se21/html/jls-3.html#jls-3.10.6

> 注意：Java 21 里还有一个叫 String Templates 的预览特性（`STR."..."`），它在 JDK 23 被撤回，本 kit **不用**它，也不要和文本块混淆。

---

## 1. 先看痛点：Java 8 的多行字符串被符号淹没

Java 8 里一个字符串字面量**不能跨行**。要写多行内容，只能一段一段拼起来，每段末尾补 `\n`，里面的双引号逐个转义
（完整代码：`examples/J07/J07Old.java`）：

```java
String json = "{\n" +
        "  \"symbol\": \"AAPL\",\n" +
        "  \"side\": \"BUY\",\n" +
        "  \"qty\": 100\n" +
        "}\n";
```

问题有三个：

1. **可读性差**。你想写的是一份 JSON，看到的却是引号、反斜杠、加号。每个 `"` 前面都要多一个 `\`，容易漏；漏了就是编译错误或语法混乱。
2. **复制粘贴困难**。把一段 JSON/SQL/测试样例从别处复制进代码，要手动逐行改写；反过来想把字符串里的内容拿出去也一样。
3. **悄悄出错**。`J07Old` 里的 SQL：

   ```java
   String sql = "SELECT symbol, SUM(qty) " +
           "FROM fills" +                  // ← 少了结尾空格
           "WHERE side = 'BUY' " + ...
   // 结果："SELECT symbol, SUM(qty) FROM fillsWHERE side = 'BUY' GROUP BY symbol"
   ```
   `fillsWHERE` 粘在一起，数据库才会报错，编译器看不出来。

在本 kit 里，**测试的样例输入/期望输出**是大量的多行文本（订单簿的命令序列、CSV 日志）。这类内容用旧写法几乎没法维护。

---

## 2. 语法逐条讲

### 2.1 基本形式

```java
String json = """
        {
          "symbol": "AAPL",
          "qty": 100
        }
        """;
```

规则：

1. 开头是三个双引号 `"""`，**后面必须直接换行**（可以有空格，但不能有别的字符）。实测：`"""abc"""` 在一行里会报 `illegal text block open delimiter sequence, missing line terminator`。
2. 内容从**下一行**开始。
3. 结尾也是 `"""`。它可以单独占一行，也可以紧跟在最后一行内容后面。
4. 里面可以**直接写 `"`**，不用转义。

和旧写法对比：得到的 `String` 完全一样。`J07Ex1` 里：

```java
String old = "{\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n";
json.equals(old)     // true
json == old          // 也是 true！
```

`==` 也是 `true` 说明二者是**同一个对象**：文本块是编译期常量，和普通字符串字面量一样放进常量池（constant pool），内容相同就共用一份（`javap` 看，两次 `ldc` 指向同一个常量池项 `#7`）。
文本块**不是一种新的类型**，就是 `java.lang.String`。

### 2.2 「偶然空白」怎么处理：缩进的去除规则

文本块在源码里需要缩进才好看，但你不希望这些缩进变成字符串内容。规则（叫「去除偶然空白」，stripping incidental whitespace）：

1. 把内容分成行。
2. 找所有**非空白行**的缩进（行首的空白字符数）以及**结束符 `"""` 所在行**的缩进（如果结束符单独占一行），取其中的**最小值**。
3. 每一行去掉这么多字符的缩进。
4. 每一行**行尾的空白**也被去掉。

所以：**结束符 `"""` 的位置决定缩进基准。** 实测（`J07Ex1`、以及我另做的小实验）：

```java
String x = """
        a
          b
        c
        """;        // 结束符与内容同缩进 -> "a\n  b\nc\n"  （长度 8）

String y = """
        a
          b
        c""";       // 结束符紧跟最后一行 -> "a\n  b\nc"    （长度 7，末尾没有换行）

String z = """
          a
        b
      """;          // 结束符比内容更靠左 -> 内容保留多出来的缩进："    a\n  b\n"
```

要点：

* **想要结尾有换行**：结束符单独占一行。**不要结尾换行**：结束符紧跟在内容后面（`J07Ex1`：`"hello\n"` 长度 6 vs `"hello"` 长度 5）。
* **想保留一些缩进**：让结束符往左缩出去，内容比它多出的部分被保留。
* 空白行不参与计算最小缩进（所以内容里的空行不会把缩进基准拉到 0）。
* 编辑器的自动缩进变化时，所有行同时移动，**相对缩进不变**，字符串内容也就不变——这是这套规则的设计目的。

### 2.3 换行符

无论源文件用 `\n`、`\r\n` 还是 `\r`，文本块里的换行一律规范化为 `\n`。所以在 Windows 上编辑的文件和在 macOS 上编辑的文件得到相同的字符串（实测 `contains("\r")` 为 `false`）。

### 2.4 转义序列

文本块里照常可以用 `\n`、`\t`、`\\`、`\"`。**在去除缩进和行尾空白之后**，转义才被解释，所以：

| 转义 | 作用 | 例子 |
|---|---|---|
| `\<换行>` | **续行**：这个换行不进入字符串，下一行接在后面 | 把很长的一行拆成多行写 |
| `\s` | 一个空格，且**不会被当作行尾空白删掉** | 保住行尾的空格：`x\s\s\s` |
| `\"""` | 内容里放三个连续引号（一个 `"` 单独出现不需要转义，三个连在一起才需要至少转义一个） | `quotes: \"""three\"""` |
| `\n` | 显式换行 | 在一行里放换行 |

`J07Ex2` 实测：

```java
String longLine = """
        SELECT symbol, SUM(qty) \
        FROM fills \
        WHERE side = 'BUY'""";
// -> "SELECT symbol, SUM(qty) FROM fills WHERE side = 'BUY'"      一行

String keepTrailing = """
        x\s\s\s
        y""";
// -> "x   \ny"
```

无效的转义（例如 `\q`）是编译错误：`illegal escape character`（实测）。

### 2.5 和 String 的方法配合

* `.formatted(args...)`（Java 15 新增）：`"""...%s...""".formatted(x)`，等价于 `String.format(textBlock, x)`。
* `.lines()`（Java 11）：按行拆成 `Stream<String>`，不管换行符是什么；本 kit 的测试常用它，`block.lines().toList()`。
* `.stripIndent()`（Java 15）：对任意字符串执行与文本块相同的「去公共缩进 + 去行尾空白」。
* `.translateEscapes()`（Java 15）：把字符串**内容里**的反斜杠转义序列翻译成真实字符（用于从配置文件读出来的文本，源码里的转义不需要）。

---

## 3. 编译器和 JVM 到底做了什么

**全部在编译期完成，JVM 完全不知道文本块的存在。**

1. 词法分析器（lexer）识别到 `"""` + 换行，开始读取一个文本块；读到结束的 `"""` 为止。
2. 把换行规范化成 `\n`。
3. 执行「去除偶然空白」（等价于对整块内容调用一次 `String.stripIndent()`）。
4. 解释转义序列（等价于 `translateEscapes()`）。
5. 得到一个普通的字符串常量，放进常量池。

`javap` 看 `J07Ex1.main` 的字节码（实测）：

```
 0: ldc  #7   // String {\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n       <- 文本块
10: ldc  #7   // 同一个常量池项（旧写法的拼接字符串，编译期折叠后也是这个常量）
23: ldc  #31  // String hello\n
25: ldc  #33  // String hello
```

* 文本块 = 一条 `ldc`（加载常量），没有运行时拼接，没有 `StringBuilder`，**零运行时开销**。
* 对比：Java 8 里 `"a" + "b" + "c"` 如果全是字面量，编译器也会做常量折叠，结果也是一条 `ldc`。但只要掺入一个变量，就变成 `StringBuilder`（Java 9 以后是 `invokedynamic makeConcatWithConstants`）。
  文本块里**不能**直接嵌入变量，所以用 `.formatted()` 这是个**运行时**调用（一次 `String.format`），开销与手写 `String.format` 相同。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——JSON、结尾换行、缩进

`examples/J07/J07Ex1.java` 实测输出：

```
{
  "symbol": "AAPL",
  "qty": 100
}
true               <- json.equals(old)
true               <- json == old
6 5                <- """\n hello\n """ 与 """\n hello""" 的长度
[    four more spaces
]                  <- 结束符比内容靠左：多出来的 4 个空格被保留
4 lines            <- json.lines().count()
```

### 例 2：进阶——转义、续行、`\s`、`stripIndent`、`formatted`

`examples/J07/J07Ex2.java` 实测输出：

```
6 3                                            <- "x   \ny" 长 6；文本块里行尾空格被删，只剩 "x\ny" 长 3
[x   |y]                                       <- \s 保住了 3 个行尾空格
SELECT symbol, SUM(qty) FROM fills WHERE side = 'BUY'      <- 3 行拼成 1 行
tab:	here
quotes: """three"""
backslash: \
a|  b|c                                        <- "   a\n     b\n   c".stripIndent()
symbol=AAPL qty=100
true                                           <- "a\\tb".translateEscapes().equals("a\tb")
```

第一行有个值得注意的细节：` `（Unicode 转义的空格）在**编译的最早阶段**，早于词法分析，就被换成一个真实的空格字符。所以它和手敲在行尾的空格没有区别，会被当作行尾空白删掉。
要保住行尾空格，用 `\s`（文本块的转义，在去除空白**之后**才处理）。

### 例 3：贴近真实——测试里的「多行输入 → 多行期望输出」

`examples/J07/J07Ex3.java`：

```java
static List<String> lines(String block) { return block.lines().toList(); }

var input = lines("""
        # 样例
        LIMIT 1 SELL 101 5
        LIMIT 2 BUY 101 3

        """);

var expected = lines("""
        BUY id=2 qty=3
        total=8
        """);

summarize(input).equals(expected)      // PASS
```

这正是本 kit 测试里的惯用法。比如 `OrderBookTest.sampleReplayMatchesProblemStatement`：把 `problem.md` 里的样例**原样粘进**测试，逐字符比较。
样例有任何改动，复制粘贴即可，不用逐行加引号和 `\n`。

后半段是 SQL：

```java
String sql = """
        SELECT symbol, SUM(qty) AS total
        FROM fills
        WHERE side = 'BUY'
        GROUP BY symbol
        """;
```

每行结尾自带换行，不会再出现 `fillsWHERE` 这种粘连。

---

## 5. 坑与限制

### 5.1 开头 `"""` 后面不能有内容

`"""abc"""` 报错。想写单行字符串用普通 `"abc"`。

### 5.2 混用制表符（Tab）和空格

「缩进」按**字符个数**数，一个 Tab 和一个空格都算 1。如果有的行用 Tab、有的行用空格，视觉上对齐的几行实际缩进字符数不同，去除后相对缩进就乱了。
编辑器统一设成「Tab 转空格」。

### 5.3 结尾的换行容易忽略

结束符单独占一行 → 字符串**以 `\n` 结尾**。拿它去和不带结尾换行的字符串比较会失败；`.lines()` 则不受影响（它不产生末尾的空行）。
比较前先想清楚你要不要这个换行，或者统一用 `.strip()`、`.lines()`。

### 5.4 行尾空白被删

如果内容需要行尾空格（比如固定宽度格式），用 `\s`。IDE 有时会自动去掉行尾空格，所以把它们写成 `\s` 也防止被编辑器清理掉。

### 5.5 不能直接嵌入变量

文本块里没有 `${x}`。要插值：`.formatted(x)`，或普通的 `+`，或 `String.format`。`.formatted` 里的 `%` 要写成 `%%`：JSON 里出现百分号时注意。

### 5.6 三个连续的双引号要转义

内容里恰好出现 `"""` 要写成 `\"""`（实测不转义会导致文本块提前结束，后面全是语法错误）。

### 5.7 过长的文本块不是好主意

文本块适合几行到几十行的内容。几百行的 SQL 或 HTML 模板放资源文件（`.sql`、`.html`）里，用类加载器读，更容易编辑、高亮、复用。

### 5.8 不要和 String Templates 混淆

String Templates（`STR."Hello \{name}"`）是 Java 21 的预览特性，已在 JDK 23 撤回。文本块是稳定特性，不依赖它。

---

## 6. 在本 kit 哪里用到

**`reference/` 目录里没有文本块**——参考实现是纯逻辑，不含多行样例。文本块全部出现在 `test/` 里，按 CONVENTIONS 的要求「problem.md 里每个样例（逐字）」进测试：

* **`loop/rounds/01_video/hc05_market_order_book/test/OrderBookTest.java`**（第 175–200 行）：
  ```java
  var out = OrderBook.replay(lines("""
          # 样例
          LIMIT 1 SELL 101 5
          LIMIT 2 SELL 101 3
          ...
          MODIFY 9 1
          """));
  assertEquals(lines("""
          REST id=1 side=SELL px=101 qty=5
          ...
          REJECT id=9 reason=unknown id
          """), out);
  ```
  辅助方法：`private static List<String> lines(String block) { return block.lines().toList(); }`（第 21 行）。
* **`loop/rounds/00_oa/oa01_job_chain/test/JobChainsTest.java`**：`parsesHeaderBlankLinesAndSpaces`、`buildsChainsSortedByRuntimeDesc`、`rendersReportExactly` 等，输入的 CSV 日志用文本块。
* **`loop/rounds/01_video/hc06_cpu_register_bitwise/test/RegisterSimTest.java`**（第 68、135 行等）：寄存器程序用文本块。
* 另外 `hc04_queue_mean_snapshot/test/QueueMeanTest.java`、`hc08_order_sequence_api/test/OrderSequenceTest.java` 同样使用。

（可用 `grep -rln '"""' loop/rounds` 复现。）

---

## 7. 自测题

1. 下面这个文本块的内容（精确的字符串）是什么？
   ```java
   String s = """
           a
             b
           """;
   ```
2. 如果把结束符的 `"""` 紧跟在 `b` 后面（`  b"""`），字符串变成什么？
3. 如何在文本块里保留行尾的两个空格？
4. 文本块在运行时比字符串拼接慢吗？
5. 写一个文本块，内容是三行：`a`、`b`、`c`，但在字符串里它们是**同一行**（没有换行），中间不留空格。

<details><summary>答案</summary>

1. `"a\n  b\n"`。内容缩进 8 个空格，`b` 行 10 个空格，结束符 8 个空格；最小缩进 8，去掉后 `a` 零缩进、`b` 保留 2 个空格；结束符单独一行 → 末尾带换行。
2. `"a\n  b"`，没有结尾换行。
3. 用 `\s`：`x\s\s`（或最后一个空格后面跟 `\s`）。直接敲空格会被当作行尾空白删掉。
4. 不慢。文本块在编译期就变成一个常量字符串，运行时就是一条 `ldc`。与字面量拼接常量折叠的结果相同。（只有 `.formatted()` 这类运行时调用才有开销。）
5. ```java
   String s = """
           a\
           b\
           c""";    // "abc"
   ```
   `\` + 换行是续行转义，不产生换行；结束符紧跟在 `c` 后面。

</details>

---

## 8. 延伸阅读

* JEP 378 Text Blocks — https://openjdk.org/jeps/378 —— Description 里有缩进去除的完整算法和各种边界情形的例子；还有一节 "Alternatives" 解释为什么不是 Python 那样的原始字符串。
* Programmer's Guide to Text Blocks — https://docs.oracle.com/en/java/javase/21/text-blocks/index.html —— Oracle 官方教程，有一节专门讲「选择结束符位置」和 `\s`。
* JLS §3.10.6 Text Blocks — https://docs.oracle.com/javase/specs/jls/se21/html/jls-3.html#jls-3.10.6 —— 精确规则。
* `String.stripIndent()` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html#stripIndent() —— 编译器用的就是这个算法。
* 下一课：J08 `var`——局部变量类型推断。
