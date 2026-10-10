# q02 · Job Runner（Java 21，HackerRank，STDIN → STDOUT）

题面原文：`../catalog/raw/hackerrank_job_runner_photos.md`。代码：`../java/src/main/java/headland/q02/`。

```bash
cd vault/interviews/companies/headland/java
mvn -q test -Dimpl=starter -Dtest='headland/q02/**'   # 你的 Starter.java
mvn -q test -Dtest='headland/q02/**'                  # 参考解：42/42
python3 mutation_check.py q02                          # 17 个错误版本全部被抓到
```

## 1. 规则：题面写明的，和我们推断的

**题面写明（high）**：CSV 从 STDIN 读入，第一行是表头；`next_job_id = 0` 表示链的结尾；输出按链的总时长**降序**排列；
报告以 `-` 开头，每节以 `-` 结尾；时间格式 `HH:MM:SS`；输入有任何问题都要**正常退出**，并且只往 STDOUT 打印 `Malformed Input`。

**从例子推出（high）**：平均时间是**截断**的（35 / 2 = 17.5 → `00:00:17`）；文件里行的顺序不等于链的顺序。

**推断（inferred，真实隐藏测试可能不同）**：

| 情况 | 判定 | 理由 |
|---|---|---|
| 表头必须**逐字**是 `#job_id,runtime_in_seconds,next_job_id`（整行首尾空白可以容忍） | 否则 Malformed | "malformed in any way" |
| 每个字段必须是纯数字 `\d+`：不带符号、空格、小数点，不能为空 | 否则 Malformed | 同上；`Integer.parseInt("+5")` 能成功，所以要先用正则拦一道 |
| id、时长、next 用 `long` 存，超出 long 的范围就判 Malformed | — | 题面说 "integer"，没说范围 |
| id = 0 | Malformed | 0 是链尾标记，用作 id 会混淆 |
| id 重复 | Malformed | 题面说 "unique integer id" |
| next 指向不存在的 job | Malformed | 链断了 |
| 两个 job 的 next 指向同一个 job | Malformed | 一条链是一个**序列**，不会分叉或汇合 |
| 有环（包括自己指向自己） | Malformed | 环永远到不了 0 |
| 只有表头、没有 job | 输出一行 `-` | 一天没跑任何 job 不算格式错误 |
| 总时长相同 | 按 `start_job` **升序** | 题面没说，要保证输出确定 |
| 文件末尾的空行 / CRLF 换行 | 接受 | 真实文件经常这样；但 job 之间的空行判 Malformed |
| 超过 99 小时 | 小时部分照常多写几位（`100:00:00`） | `%02d` 是最少两位，不是只保留两位 |

## 2. 设计：先全部解析、全部校验，最后一次性输出

```
stdin 的每一行 ──parse──▶ Map<Long, Job> ──chains──▶ List<Chain>（已排序） ──render──▶ String ──▶ 只 print 一次
                  │                         │
                  └───── MalformedInputException ───▶ "Malformed Input\n"
```

**最重要的一条**：报告没有全部算完之前，**一个字都不能打印**。如果边读边打印，读到第 100 行才发现格式错误时，前面的内容已经输出了，
这时 STDOUT 里就不只有 `Malformed Input`（错误版本 "partial report before the error" 挂了 6 个测试）。

为什么用一个**受检异常** `MalformedInputException` 来传递"格式错误"：
- 这个错误可能出现在很多层（表头、字段、引用、环），用异常可以一路传到 `main`，中间不用每层都检查返回值；
- 它是受检异常，`parse` 和 `chains` 的签名上写着 `throws`，编译器会逼着调用方处理，不会被漏掉；
- 另一种写法是 Java 21 的 `sealed interface Result permits Ok, Malformed`，再用模式匹配 `switch` 分两种情况处理。
  在这么小的程序里，异常更省代码；如果结果要在很多层之间传来传去，sealed 结果类型会更清楚。

## 2.5 图的形状：不是 DAG（有环）、是 DAG 但不是一条直线，怎么办

把每个 job 看成一个点，`next` 看成一条边。**每一行只能写一个 `next`，所以每个点最多只有一条出边**（出度 ≤ 1）。
这种图叫"函数图"（functional graph），它只可能长成下面几种样子：

| 形状 | 例子 | 是不是合法的链 | 被哪道检查抓到 |
|---|---|---|---|
| 直线，末尾指向 0 | `1→2→0` | 合法 | — |
| 分叉（一个 job 有两个 next） | 只能写成重复的 id：`1,5,2` 加 `1,5,3` | 不合法 | 重复 id |
| 汇合，Y 字形（两个 job 指向同一个 job） | `1→3`、`2→3`、`3→0` | 不合法 | 前驱数 ≤ 1 |
| 纯环 | `1→1`、`1→2→1`、`1→2→3→1` | 不合法 | 计数：环上的 job 不在任何一条链上 |
| 尾巴接环，ρ 字形 | `1→2→3→2` | 不合法 | 前驱数 ≤ 1：环的入口 2 有两个前驱（1 和 3） |
| 指向不存在的 job | `1→9`，但没有 9 | 不合法 | next 是否存在 |

**为什么三道检查（next 存在、前驱 ≤ 1、计数）加起来就够了**：在出度 ≤ 1 的图里，如果再要求入度 ≤ 1，
那么每个连通块只可能是一条简单路径，或者一个简单环。路径的头是唯一一个入度为 0 的点，也就是起点，从它走一定能走到 0；
环上没有入度为 0 的点，所以永远不会被当成起点，这样遍历时少数的那些 job 就是环。ρ 字形不可能通过"入度 ≤ 1"这一关：
环要有入口，入口那个 job 一定同时有环内和环外两个前驱。

**"前驱 ≤ 1"这道检查还保证了循环一定会结束**。把它去掉以后，ρ 字形 `1→2→3→2` 里，1 没有前驱，会被当成起点，
然后 `while (job.next() != 0)` 就沿着 2→3→2→3… **永远走下去**。这不是理论推演，是实际发生的：加上 ρ 字形测试后，
第一次跑变异检查时整个构建卡死了，因为测试本身没有时间限制。现在测试工具 `Impl.stdoutOf` 把每次调用放到一个守护线程（daemon thread）里，
最多只等 5 秒（`Thread.ofPlatform().daemon().unstarted(...)` 加上 `join(Duration)`，都是 Java 21 的 API），超时就判失败，
报错信息是 "did not finish within 5 s: an infinite loop?"。
**教训：只要测试可能触发死循环，就必须给测试加时间限制，否则一个错误版本会把整个流程卡住，而不是让一个测试失败。**

**为什么不能只靠计数**：如果去掉"前驱 ≤ 1"这道检查，Y 字形会让共享的 job 被走两遍（多数），纯环会让环上的 job 一次都没走到（少数），
两者正好抵消时总数还是对的。测试 "shared job balanced by a self loop" 构造的就是这种情况。

**汇合判成 Malformed 是推断**：题面说一条链是"一个 job 序列"，next 是"在它之后运行的那个 job"。
一次运行的 job 3 不可能同时排在两条不同的链之后，所以我们判为格式错误。另一种可能的解读是"输出两条共享尾部的链"，
这种解读不太自然，我们没有采用。

## 3. 代码分块讲解

**块 A：数据类型都是 record**

```java
record Job(long id, long runtime, long next) {}

record Chain(long start, long last, int jobs, long runtime) {
    long averageRuntime() { return runtime / jobs; }   // long 整数除法本身就是截断
}
```
- record 可以有自己的方法。`averageRuntime()` 放在 `Chain` 里面，因为平均值是由链的数据算出来的。
- 用 `long`：id 可能超过 21 亿（有测试 `idsLargerThanInt`），一天的总秒数累加起来也可能很大。

**块 B：解析。三个容易踩的坑**

```java
String[] fields = line.strip().split(",", -1);      // 坑 1：-1
if (!NON_NEGATIVE_INTEGER.matcher(field).matches()) // 坑 2：先用正则检查，再 parseLong
if (jobs.putIfAbsent(job.id(), job) != null)        // 坑 3：用 putIfAbsent 一步判断重复
```
1. **`split(",")` 会丢掉末尾的空字段**：`"1,60,0,".split(",")` 得到的是 3 个字段，看起来格式正确。
   加上 `-1` 后得到 4 个字段，才会被判为格式错误。这个错误版本一开始**没被抓到**，后来补了测试 "trailing comma after three fields"。
2. **`Long.parseLong` 接受 `"+5"`**，还会对超出 long 范围的数字抛 `NumberFormatException`。先用正则 `\d+` 把关，
   再把 `NumberFormatException` 转换成我们自己的异常。
3. **`Map.putIfAbsent`** 在 key 已经存在时返回旧值，而且不覆盖。先 `containsKey` 再 `put` 也能实现，但要查两次表。
- 用 `LinkedHashMap` 保持输入顺序：结果本身不依赖顺序（最后会排序），但调试时更好对照。

**块 C：建链和校验**

```java
for (Job job : jobs.values()) {                      // 第一遍：检查每条指向
    if (job.next() == 0) continue;
    if (!jobs.containsKey(job.next())) throw ...;    // 指向不存在的 job
    if (!hasPredecessor.add(job.next())) throw ...;  // Set.add 返回 false，说明已经有别的 job 指向它了
}
for (Job first : jobs.values()) {                    // 第二遍：从每个起点出发，沿着 next 走到 0
    if (hasPredecessor.contains(first.id())) continue;
    ... while (job.next() != 0) { job = jobs.get(job.next()); ... }
}
if (jobsOnChains != jobs.size()) throw ...;          // 有 job 不在任何一条链上 → 说明有环
```
- **起点**就是没有任何 job 指向的那个 job，不是文件里的第一行（测试 `chainStartIsTheJobNobodyPointsToNotTheFirstLine`）。
- **为什么 `while` 循环不会死循环**：每个 job 最多只有一个前驱，而起点没有前驱，所以从起点出发不可能走进环；
  环只能单独存在，它上面的每个 job 都有前驱，于是不会被当成起点，也就走不到。最后数一下"在链上的 job 数"是否等于总数，就能发现环。
- **两个检查缺一不可**：去掉"两个 job 指向同一个 job"这个检查后，测试 "two jobs before the same job" 依然通过，
  因为 job 3 被走了两遍，计数对不上，被环检测顺带抓到了。但如果再加一个自己指向自己的 job 4，两边的误差正好抵消（4 == 4），
  错误就漏过去了。测试 "shared job balanced by a self loop" 专门针对这种情况。**两个错误互相抵消，是"只靠计数"这种校验最典型的盲点。**
- 用循环，不要用递归：一条 10 万个 job 的链如果递归遍历，会栈溢出（`StackOverflowError`），测试 `longChainListedBackwards` 专门覆盖这个。

**块 D：排序**

```java
chains.sort(Comparator.comparingLong(Chain::runtime).reversed().thenComparingLong(Chain::start));
```
- `reversed()` 只作用在它**前面**已经组好的比较器上，所以这里是"时长降序，然后 start 升序"。
  如果写成 `comparingLong(runtime).thenComparingLong(start).reversed()`，两个字段就都变成降序了。
- 用 `comparingLong` 而不是 `comparing`：前者直接比较基本类型 long，不用装箱。

**块 E：输出**

```java
"""
start_job: %d
...
-
""".formatted(chain.start(), ...)          // 文本块（Java 15）+ String.formatted（Java 15）
"%02d:%02d:%02d".formatted(s / 3600, s % 3600 / 60, s % 60)
```
- 文本块里每一行末尾都带 `\n`，结尾的 `"""` 单独放一行，表示最后一行也以换行结束。缩进按结尾 `"""` 所在的列来去掉。
- **性能取舍（实测）**：5 万个链的报告，`formatted` 要 357 ms（JVM 冷启动），全部改用 `StringBuilder.append` 只要 22 ms。
  整个程序在 10 万个 job 的输入上总共约 0.75 s，所以参考解保留了可读性更好的 `formatted`。人工审代码时，可读性更重要。

**块 F：`main`**

```java
var reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
List<String> lines = reader.lines().toList();
```
- **不要**对 `System.in` 用 try-with-resources：关掉这个 reader 会把 `System.in` 一起关掉。在同一个 JVM 里多次调用 `main`（我们的测试就是这样）时，后面的调用就会出问题。
- `BufferedReader.lines()` 能识别 `\n`、`\r\n` 和 `\r` 三种换行，所以 CRLF 的文件不用特殊处理。
- 题目要求"exit zero"：**不要调用 `System.exit(1)`**。异常也不要从 `main` 抛出去，否则 JVM 会以非零状态退出。
  另外，在我们的测试环境里调用 `System.exit` 会直接杀掉测试进程。

## 4. 测试抓的错（`mutation_check.py q02`，全部实际跑过）

| 错误版本 | 挂几个测试 |
|---|---|
| 平均值四舍五入 | 2 |
| 按时长升序排 | 2 |
| 时长相同时按 start 降序 | 1 |
| 不检查表头 | 4 |
| `split(",")` 不带 `-1` | 1（补测试之前：0） |
| 接受 `+5` 这样带符号的数 | 2 |
| 字段里的空格被 trim 掉后接受 | 1 |
| 接受 id 为 0 | 1 |
| 重复 id 直接覆盖 | 1 |
| 不检查 next 是否存在 | 1 |
| 允许两个 job 指向同一个 job | 2，其中 ρ 字形那个是 5 秒超时（补测试之前：0；加上 ρ 字形、还没加超时之前：构建卡死） |
| 不检测环 | 3 |
| 分钟数没有对 60 取模 | 3 |
| 小时数对 24 取模 | 2 |
| 报告开头少了 `-` | 13 |
| 末尾空行也判 Malformed | 1 |
| 先打印了一部分报告，再发现格式错误 | 6 |

顺带一个 Java 细节：写这些错误版本时，`while (false) { ... }` **编译不过**（unreachable statement），而 `if (false) { ... }` 可以。
Java 语言规范专门为 `if` 留了这个口子，用来做条件编译。
