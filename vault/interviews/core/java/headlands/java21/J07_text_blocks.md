# J07 · 文本块 `"""`：多行字符串照着原样写

> 版本：Java 15 正式（13、14 为预览）。可运行代码：`examples/J07/`。
> 前置：字符串、转义序列（`\n`、`\"`）、字符串拼接。
> 别和 Java 21 的预览特性 String Templates（`STR."..."`，JDK 23 已撤回）混淆；文本块是稳定特性，不依赖它。
---

## 1. 先看痛点：Java 8 的多行字符串被符号淹没

Java 8 的字符串字面量**不能跨行**。多行内容只能一段段拼，每段末尾补 `\n`，双引号逐个转义（`examples/J07/J07Old.java`）：

```java
String json = "{\n" +
        "  \"symbol\": \"AAPL\",\n" +
        "  \"side\": \"BUY\",\n" +
        "  \"qty\": 100\n" +
        "}\n";
```

三个问题：

1. **可读性差**：想写 JSON，看到的却是引号、反斜杠、加号，漏一个 `\` 就是编译错误。
2. **复制粘贴困难**：JSON/SQL/测试样例从别处复制进来要逐行改写，反过来也一样。
3. **悄悄出错**。`J07Old` 里的 SQL：

   ```java
   String sql = "SELECT symbol, SUM(qty) " +
           "FROM fills" +                  // ← 少了结尾空格
           "WHERE side = 'BUY' " + ...
   // 结果："SELECT symbol, SUM(qty) FROM fillsWHERE side = 'BUY' GROUP BY symbol"
   ```
   `fillsWHERE` 粘在一起，数据库才报错，编译器看不出来。

测试里的样例输入/期望输出（命令序列、CSV 日志）几乎全是多行文本，旧写法没法维护。

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

1. 开头三个双引号 `"""`，**后面必须直接换行**（可有空格，不能有别的字符）：`"""abc"""` 报 `illegal text block open delimiter sequence, missing line terminator`。
2. 内容从**下一行**开始。
3. 结尾也是 `"""`，可单独一行，也可紧跟最后一行内容。
4. 里面**直接写 `"`**，不用转义。

得到的 `String` 与旧写法完全一样（`J07Ex1`）：

```java
String old = "{\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n";
json.equals(old)     // true
json == old          // 也是 true！
```

`==` 也是 `true`：文本块是编译期常量，和普通字面量一样进常量池（constant pool），内容相同共用一份（`javap` 看两次 `ldc` 指向同一项）。文本块**不是新类型**，就是 `java.lang.String`。

### 2.2 「偶然空白」怎么处理：缩进的去除规则

文本块需要缩进才好看，但缩进不该进字符串。规则叫「去除偶然空白」（stripping incidental whitespace）：

1. 把内容分成行。
2. 取所有**非空白行**的缩进，以及**结束符 `"""` 所在行**的缩进（结束符单独占一行时），取**最小值**。
3. 每行去掉这么多缩进，并去掉**行尾空白**。

所以：**结束符 `"""` 的位置决定缩进基准**：

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

* **要结尾换行**：结束符单独占一行；**不要**：结束符紧跟内容（`"hello\n"` 长度 6 vs `"hello"` 长度 5）。
* **要保留缩进**：让结束符往左缩，内容比它多出的部分被保留。
* 空白行不参与最小缩进计算。
* 编辑器改自动缩进时所有行同移，**相对缩进不变**，字符串内容不变——这套规则的设计目的。

### 2.3 换行符

源文件用 `\n`、`\r\n` 还是 `\r`，文本块里的换行一律规范化为 `\n`，所以 Windows 和 macOS 编辑的结果相同。

### 2.4 转义序列

文本块里照常可用 `\n`、`\t`、`\\`、`\"`。转义在去除缩进和行尾空白**之后**才被解释：

| 转义 | 作用 | 例子 |
|---|---|---|
| `\<换行>` | **续行**：这个换行不进入字符串，下一行接在后面 | 把很长的一行拆成多行写 |
| `\s` | 一个空格，且**不会被当作行尾空白删掉** | 保住行尾的空格：`x\s\s\s` |
| `\"""` | 内容里放三个连续引号（单个 `"` 无需转义，三个连着至少转义一个） | `quotes: \"""three\"""` |
| `\n` | 显式换行 | 在一行里放换行 |

`J07Ex2`：

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

无效转义（如 `\q`）是编译错误：`illegal escape character`。

### 2.5 和 String 的方法配合

* `.formatted(args...)`（Java 15）：`"""...%s...""".formatted(x)`，等价 `String.format(textBlock, x)`。
* `.lines()`（Java 11）：按行拆成 `Stream<String>`，与换行符种类无关；测试常用 `block.lines().toList()`。
* `.stripIndent()`（Java 15）：对任意字符串做与文本块相同的「去公共缩进 + 去行尾空白」。
* `.translateEscapes()`（Java 15）：把字符串**内容里**的反斜杠转义翻译成真实字符（用于从配置文件读出的文本）。

---

## 3. 编译器和 JVM 到底做了什么

**全在编译期完成，JVM 不知道文本块的存在。** 词法分析器（lexer）读到 `"""` + 换行后读到结束 `"""`；换行规范化为 `\n`；执行「去除偶然空白」（等价于 `String.stripIndent()`）；解释转义（等价于 `translateEscapes()`）；得到普通字符串常量放进常量池。

`J07Ex1.main` 的字节码：

```
 0: ldc  #7   // String {\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n       <- 文本块
10: ldc  #7   // 同一个常量池项（旧写法的拼接字符串，编译期折叠后也是这个常量）
23: ldc  #31  // String hello\n
25: ldc  #33  // String hello
```

* 文本块 = 一条 `ldc`，没有运行时拼接、没有 `StringBuilder`，**零运行时开销**。
* 对比：全是字面量的 `"a" + "b" + "c"` 也会被常量折叠成一条 `ldc`；一旦掺入变量就变 `StringBuilder`（Java 9 起是 `invokedynamic makeConcatWithConstants`）。文本块里**不能**直接嵌变量，用 `.formatted()` 是**运行时**调用（一次 `String.format`），开销与手写 `String.format` 相同。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——JSON、结尾换行、缩进

`examples/J07/J07Ex1.java` 输出：

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

`examples/J07/J07Ex2.java` 输出：

```console
6 3
[x   |y]
SELECT symbol, SUM(qty) FROM fills WHERE side = 'BUY'
tab:	here
quotes: """three"""
backslash: \
a|  b|c
symbol=AAPL qty=100
true
```

* `6 3`：`"x   \ny"` 长 6；文本块里行尾空格被删，只剩 `"x\ny"` 长 3。
* `[x   |y]`：`\s` 保住了 3 个行尾空格。
* `SELECT ...`：3 行拼成 1 行。
* `a|  b|c`：`"   a\n     b\n   c".stripIndent()` 的结果。
* `true`：`"a\\tb".translateEscapes().equals("a\tb")`。

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

这是测试里的惯用法：把题面样例**原样粘进**测试，逐字符比较，不用逐行加引号和 `\n`。

后半段是 SQL：

```java
String sql = """
        SELECT symbol, SUM(qty) AS total
        FROM fills
        WHERE side = 'BUY'
        GROUP BY symbol
        """;
```

每行自带换行，不会再出现 `fillsWHERE` 这种粘连。

---

## 5. 坑与限制

### 5.1 开头 `"""` 后面不能有内容

`"""abc"""` 报错；单行字符串用普通 `"abc"`。

### 5.2 混用制表符（Tab）和空格

「缩进」按**字符个数**数，Tab 和空格各算 1。有的行用 Tab、有的用空格，视觉对齐的行实际缩进不同，去除后相对缩进就乱。编辑器统一「Tab 转空格」。

### 5.3 结尾的换行容易忽略

结束符单独占一行 → 字符串**以 `\n` 结尾**，和不带结尾换行的字符串比较会失败；`.lines()` 不受影响（不产生末尾空行）。比较前想清楚是否要这个换行，或统一用 `.strip()`、`.lines()`。

### 5.4 行尾空白被删

内容需要行尾空格（如固定宽度格式）就用 `\s`；IDE 有时自动清掉行尾空格，写成 `\s` 也能防清理。

### 5.5 不能直接嵌入变量

文本块没有 `${x}`。插值用 `.formatted(x)`、`+` 或 `String.format`；`.formatted` 里的 `%` 要写成 `%%`（JSON 里的百分号注意）。

### 5.6 三个连续的双引号要转义

内容里恰好出现 `"""` 要写成 `\"""`，不转义会让文本块提前结束，后面全是语法错误。

### 5.7 过长的文本块不是好主意

文本块适合几行到几十行。几百行的 SQL/HTML 模板放资源文件（`.sql`、`.html`）用类加载器读，更易编辑、高亮、复用。

---

## 6. 真实代码里的文本块

参考实现是纯逻辑，没有文本块；文本块全在测试里，题面每个样例逐字进测试（`OrderBookTest`）：
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
  辅助方法：`private static List<String> lines(String block) { return block.lines().toList(); }`
* `JobChainsTest`：输入的 CSV 日志用文本块；`RegisterSimTest`：寄存器程序用文本块；`QueueMeanTest`、`OrderSequenceTest` 同样。

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

1. `"a\n  b\n"`。内容缩进 8，`b` 行 10，结束符 8；最小缩进 8，去掉后 `a` 零缩进、`b` 留 2 个空格；结束符单独一行 → 末尾换行。
2. `"a\n  b"`，没有结尾换行。
3. 用 `\s`：`x\s\s`。直接敲空格会被当行尾空白删掉。
4. 不慢。文本块编译期就是一个常量，运行时一条 `ldc`，与字面量常量折叠相同（只有 `.formatted()` 这类运行时调用才有开销）。
5. ```java
   String s = """
           a\
           b\
           c""";    // "abc"
   ```
   `\` + 换行是续行转义，不产生换行；结束符紧跟在 `c` 后面。

</details>

---

「延伸」J08 `var`：局部变量类型推断。
