# Headland mock coding test（Java 21 + Maven）

这是一套用 **Java 21** 做的 HackerRank 风格模拟题：每题是一个 Maven 小项目里的一个包，有你要写的 `Starter.java`、参考解 `Solution.java` 和 JUnit 5 测试。
同一套测试通过 `impl` 系统属性选择实现，所以既能给参考解判分，也能给你自己的代码判分。
每题配一篇中文讲义，逐题带写，并回顾用到的 Java 21 语法与最佳实践。

| 路径 | 内容 |
|---|---|
| `java/` | 一个 Maven 项目（Java 21、JUnit 5），每题一个包 |
| `study/` | 逐题带写、Java 21 语法与最佳实践回顾 |
| `java/mutation_check.py` | 给 `Solution.java` 注入单个错误的变体，每个变体都必须让某个测试失败（`python3 mutation_check.py q01`） |

| 题 | 包 | 测试 | 讲义 |
|---|---|---|---|
| q01 FizzBuzz | `headland.q01` | `FizzBuzzTest`（12 个测试） | `study/q01_fizzbuzz.md` |
| q02 Job Runner | `headland.q02` (`Solution` imperative, `Functional` streams throughout) | `JobRunnerTest`（42 个测试） | `study/q02_job_runner.md` |

```bash
cd vault/interviews/companies/headlands/mock_maven/java
mvn -q test                                   # reference solutions (default -Dimpl=solution)
mvn -q test -Dimpl=starter                    # your code
mvn -q test -Dimpl=starter -Dtest='headland/q01/**'  # one problem
```

每题 `qNN_name` 对应包 `headland.qNN`：接口、`Starter.java`（你的）和 `Solution.java`（参考解）放在 `src/main/java/headland/qNN/`，测试在 `src/test/java/headland/qNN/`，每个难度层级一个测试类。
