---
id: hl-loop-mock-maven
node: company.loop
type: qa
step: 17
---
## Q
Java 21 + Maven 的 HackerRank 风格模拟题怎么组织、怎么跑？`-Dimpl` 起什么作用？

## A
每题是一个 Maven 项目里的一个包：你写的 `Starter.java`、参考解 `Solution.java`、JUnit 5 测试。**同一套测试**通过 `impl` 系统属性选择实现，所以既能给参考解判分，也能给你自己的代码判分。

```
mvn -q test                         # 参考解（默认 -Dimpl=solution）
mvn -q test -Dimpl=starter          # 你的代码
mvn -q test -Dimpl=starter -Dtest='headland/q01/**'   # 只跑一题
```
- 题：q01 FizzBuzz（12 个测试）、q02 Job Runner（42 个测试，`Solution` 命令式，`Functional` 全程 streams）。
- `mutation_check.py`：给参考解注入单个错误的变体，每个变体都必须让某个测试失败，用来验证测试够强。
