---
id: hl-mm02-sort-format
node: problems.mm02-job-runner
type: qa
step: 6
---
## Q
Job Runner 的排序比较器、文本块输出和时间格式怎么写？`formatted` 与 `StringBuilder` 的性能取舍是什么？

## A
**排序**：
```java
chains.sort(Comparator.comparingLong(Chain::runtime).reversed().thenComparingLong(Chain::start));
```
`reversed()` 只作用在它**前面**已经组好的比较器上，所以这里是「时长降序，然后 start 升序」；写成 `comparingLong(runtime).thenComparingLong(start).reversed()` 两个字段都降序了。用 `comparingLong` 不用 `comparing`：直接比较基本类型 long，不装箱。

**输出**（文本块 Java 15 + `String.formatted` Java 15）：
```java
"""
start_job: %d
...
-
""".formatted(chain.start(), ...)
"%02d:%02d:%02d".formatted(s / 3600, s % 3600 / 60, s % 60)
```
文本块每一行末尾带 `\n`，结尾的 `"""` 单独放一行表示最后一行也以换行结束；缩进按结尾 `"""` 所在列去掉。`%02d` 是最少两位，不是只保留两位，所以超过 99 小时输出 `100:00:00`。

**性能取舍（实测）**：5 万个链的报告，`formatted` 要 357 ms（JVM 冷启动），全部改用 `StringBuilder.append` 只要 22 ms；整个程序在 10 万个 job 输入上总共约 0.75 s，所以参考解保留可读性更好的 `formatted`。人工审代码时可读性更重要。

测试抓的相关错：平均值四舍五入（2 个测试挂）；按时长升序排（2）；时长相同时按 start 降序（1）；分钟数没对 60 取模（3）；小时数对 24 取模（2）；报告开头少了 `-`（13）；末尾空行也判 Malformed（1）；先打印了一部分报告再发现格式错误（6）。

旁注：写错误版本时 `while (false) { ... }` 编译不过（unreachable statement），而 `if (false) { ... }` 可以——Java 语言规范专门为 `if` 留了口子用来做条件编译。
