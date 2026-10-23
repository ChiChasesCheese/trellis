---
id: hl-mm02-functional-parse
node: problems.mm02-job-runner
type: qa
step: 8
---
## Q
全函数式的 `parse` 和 `render` 怎么写？整行正则、`Optional`、`dropWhile`、`Duration` 各有什么要点？

## A
```java
private static final Pattern JOB_LINE = Pattern.compile("(\\d+),(\\d+),(\\d+)");   // 一条正则校验整行

static Map<Long, Job> parse(List<String> lines) throws MalformedInputException {
    List<String> content = lines.reversed().stream().dropWhile(String::isBlank).toList().reversed();
    if (content.isEmpty() || !content.getFirst().strip().equals(Solution.HEADER)) throw ...;
    List<Optional<Job>> rows = content.stream().skip(1).map(Functional::toJob).toList();
    if (rows.stream().anyMatch(Optional::isEmpty)) throw ...;
    List<Job> jobs = rows.stream().map(Optional::orElseThrow).toList();
    if (jobs.stream().anyMatch(job -> job.id() == 0)) throw ...;
    if (jobs.stream().map(Job::id).distinct().count() != jobs.size()) throw ...;
    return jobs.stream().collect(Collectors.toMap(Job::id, Function.identity(), (a, b) -> a, LinkedHashMap::new));
}
private static Optional<Job> toJob(String line) {     // 失败用 Optional.empty()，不在 lambda 里抛
    Matcher fields = JOB_LINE.matcher(line.strip());
    if (!fields.matches()) return Optional.empty();
    try { return Optional.of(new Job(parseLong(g1), parseLong(g2), parseLong(g3))); }
    catch (NumberFormatException beyondLong) { return Optional.empty(); }
}
static String render(List<Chain> chains) {
    return chains.stream().map(Functional::section).collect(Collectors.joining("", "-\n", ""));
}
static String hhmmss(long seconds) {
    Duration d = Duration.ofSeconds(seconds);
    return "%02d:%02d:%02d".formatted(d.toHours(), d.toMinutesPart(), d.toSecondsPart());
}
```
- **去掉末尾空行（Java 21）**：`lines.reversed()` 是 `SequencedCollection` 的**视图**，不复制；`dropWhile(String::isBlank)`（Java 9）丢开头连续满足条件的元素，所以夹在中间的空行保留，随后被正则判格式错误，与命令式一致；
- **整行正则**代替 `split` + 逐字段校验：`(\d+),(\d+),(\d+)` + **`matches()`**（整行匹配），一次挡住字段数不对、末尾多逗号、空字段、正负号、空格和小数；**不能用 `find()`**：`"1,2,3,4"` 里的 `"1,2,3"` 就能匹配（错误版本「find instead of matches」挂 2 个测试）；
- **`Optional` 代替在 lambda 里抛受检异常**：代价是丢掉具体出错原因，这里只要求打印 `Malformed Input` 可接受；要保留原因可用 sealed `Row permits Parsed, Rejected` + 记录模式 `case Rejected(String line) -> ...`；
- **`distinct().count()` 判重复 id**，之后才 `toMap`；`toMap` 第三个参数是 key 冲突时的合并函数，已被排除所以随便返回并写注释；若让 `toMap` 抛 `IllegalStateException` 就得捕获过宽的运行时异常；
- **`joining(分隔符, 前缀, 后缀)` 在流为空时也输出前后缀**，所以只有表头的输入仍输出 `-`；
- **`Duration`**：`toHours()` 返回**总**小时数（100 小时就是 100），`toMinutesPart()`/`toSecondsPart()`（Java 9）返回零头；误用 `toMinutes()` 得总分钟数（错误版本「minutes as a total」挂 3 个测试）。

实测：5 万条短链命令式 566 ms，函数式 641 ms；10 万 job 长链 277 / 310 ms，输出逐字节相同，波动约 ±100 ms，无实质差别。
