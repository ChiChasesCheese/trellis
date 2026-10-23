---
id: hl-mm02-all-or-nothing
node: problems.mm02-job-runner
type: qa
step: 3
---
## Q
Job Runner 的整体设计为什么是「先全部解析、全部校验，最后一次性输出」？用受检异常还是 sealed 结果类型传递格式错误？

## A
流程：stdin 每一行 → `parse` → `Map<Long, Job>` → `chains` → 已排序的 `List<Chain>` → `render` → `String` → **只 print 一次**；`parse` 和 `chains` 任何一步抛 `MalformedInputException`，直接输出 `"Malformed Input\n"`。

**最重要的一条**：报告没有全部算完之前，**一个字都不能打印**。若边读边打印，读到第 100 行才发现格式错误时前面的内容已经输出，STDOUT 里就不只有 `Malformed Input`（错误版本「partial report before the error」挂了 6 个测试）。

**为什么用受检异常 `MalformedInputException`**：
- 错误可能出现在很多层（表头、字段、引用、环），异常一路传到 `main`，中间不用每层检查返回值；
- 受检异常，`parse` 和 `chains` 的签名上写着 `throws`，编译器逼调用方处理，不会漏；
- 另一种写法是 Java 21 的 `sealed interface Result permits Ok, Malformed` + 模式匹配 `switch`。在这么小的程序里异常更省代码；结果要在很多层之间传来传去时 sealed 结果类型更清楚。

`main` 的写法：
```java
var reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
List<String> lines = reader.lines().toList();
```
**不要**对 `System.in` 用 try-with-resources：关掉这个 reader 会把 `System.in` 一起关掉，同一个 JVM 里多次调用 `main`（测试就是这样）后面会出问题；`BufferedReader.lines()` 能识别 `\n`、`\r\n`、`\r`，CRLF 文件不用特殊处理。
