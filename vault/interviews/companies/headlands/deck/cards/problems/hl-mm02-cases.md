---
id: hl-mm02-cases
node: problems.mm02-job-runner
type: qa
step: 10
---
## Q
Job Runner 手算：job 表 `1,60,23` / `23,30,3` / `3,15,0` / `5,200,0`，以及几类非法输入，各应输出什么？

## A
（表头 `#job_id,runtime_in_seconds,next_job_id`）

合法例：链 5（单 job，200 s，`00:03:20`，平均 `00:03:20`）和链 1→23→3（3 个 job，105 s = `00:01:45`，平均 35 s = `00:00:35`）。总时长降序，链 5 在前。每节以 `-` 开头和结尾：
```
-
start_job: 5
last_job: 5
number_of_jobs: 1
job_chain_runtime: 00:03:20
average_job_time: 00:03:20
-
start_job: 1
last_job: 3
number_of_jobs: 3
job_chain_runtime: 00:01:45
average_job_time: 00:00:35
-
```
平均截断：35 / 2 = 17.5 → `00:00:17`。链起点是没有任何 job 指向的那个 job，不是文件第一行。

只输出 `Malformed Input` 的情形：表头不对；字段带 `+`/空格/小数/空；超 long；id=0；id 重复；next 指向不存在的 job；两个 job 指向同一个 job（Y 字形）；任何环（`1→1`、`1→2→1`、`1→2→3→1`、ρ 字形 `1→2→3→2`）；job 之间有空行。接受的：文件末尾空行、CRLF 换行。只有表头没有 job：输出单行 `-`。

用 `long`（id 可超过 21 亿）；递归遍历 10 万 job 长链会栈溢出，用循环；测试有 5 秒超时防死循环；输出一次性 `print`，不要 `System.exit`。

Java 21 特性清单：record（`Job`、`Chain`）、文本块 + `formatted`、`Comparator` 组合子、`Sequenced Collections`（`reversed()`、`getFirst()`）、`Stream.iterate` 带结束条件、`Collectors.teeing`、`Duration.toMinutesPart()`、`Thread.ofPlatform().daemon()`、`join(Duration)`，另可选 sealed `Result permits Ok, Malformed` + 模式匹配 switch。
