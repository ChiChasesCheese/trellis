---
id: hl-mm02-what-asked
node: problems.mm02-job-runner
type: qa
step: 1
---
## Q
Job Runner 题（HackerRank，STDIN → STDOUT）读入什么、输出什么？题面明确了哪些规则？

## A
读入 CSV，每行一个 job：编号、运行秒数、下一个 job 的编号（0 表示链尾）。把 job 串成若干条链，按总时长**降序**打印报告，输入有任何问题就只打印 `Malformed Input`。考点：输入校验覆盖多少种坏数据、图的形状怎么判（环、汇合）、以及「全部算完再一次性输出」。

**题面明确**：
- CSV 从 STDIN 读入，第一行是表头；
- `next_job_id = 0` 表示链的结尾；
- 输出按链的总时长降序；
- 报告以 `-` 开头，每节以 `-` 结尾；
- 时间格式 `HH:MM:SS`；
- 输入有任何问题都要**正常退出**（exit zero），并且只往 STDOUT 打印 `Malformed Input`。

**从例子可得**：平均时间是**截断**的（35 / 2 = 17.5 → `00:00:17`）；文件里行的顺序不等于链的顺序。

**不要调用 `System.exit(1)`**，异常也不要从 `main` 抛出去，否则 JVM 以非零状态退出；在测试环境里调用 `System.exit` 会直接杀掉测试进程。

运行：`mvn -q test -Dimpl=starter -Dtest='headland/q02/**'` 跑你的 Starter；参考解 42/42；`python3 mutation_check.py q02` 17 个错误版本全部被抓到；函数式版本 15 个。
