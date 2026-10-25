# 最后一天：照着做就行

明天只做一件事：跟着答案把原理弄懂，能讲出来。不写全量代码、不做选择题，按下面的顺序往下走；每一块写了要打开什么、做什么、做到什么程度就停。时间不够就从后往前砍，前三块保住。周一 12:00 PT 面试（Teams + CoderPad，语言由面试官定，Java 或 C++）。

## 总览

| 块   | 时长     | 做什么                      | 打开                                                     |        |
| --- | ------ | ------------------------ | ------------------------------------------------------ | ------ |
| 1   | 2.5 h  | 编码题前 9 道：读速读，再看参考解       | [[interviews/companies/headlands/08-solutions-digest]] | 18 题速读 |
| 2   | 1 h    | C++ 现场生存：语法、容器、常见坑       | C16 · 速查表                                              |        |
| 3   | 1 h    | Java 深度题：快在哪、JIT / GC、并发 | Java 题库 A、E、F                                          |        |
| 4   | 1.5 h  | 编码题后 9 道：只读速读            | [[interviews/companies/headlands/08-solutions-digest]] | 18 题速读 |
| 5   | 1 h    | 背景问题：填空、口述两个故事           | 题库 · 故事                                                |        |
| 6   | 30 min | 晚上：公司一页纸、反问、周一清单         | 简报 · 反问                                                |        |

中间每块之间休息 10 分钟。Anki 只在零碎时间刷：`Headlands::03 Java 技术面试题库`、`::08 C++ 技术面试题库`。

## 块 1 · 编码题前 9 道（2.5 h）

打开 [[interviews/companies/headlands/08-solutions-digest|18 题速读]]，按顺序读：hc05 订单簿 → hc14 VWAP → hc15 流式中位数 → hc16 树形 DP → hc07 哈希表 →
hc02 合并 K 路流 → hc04 队列均值快照 → hc09 成交额 Top-K → oa01 任务链。

每道题约 15 分钟：

1. 读速读那一节（5 分钟）：题意、核心思路、数据结构为什么这样选。
2. 打开该题的 Java 参考解 `loop/rounds/<轮次>/<题>/reference/`，对着「核心思路」找到对应的几行（5 分钟）。
3. 合上，口头说一遍：「这题我先……因为……复杂度……追问时……」（5 分钟）。说不顺就回到讲义里那一段。

想动手时只写 Part 1：`python3 tools/jtest.py start <题目目录>` 然后 `python3 tools/jtest.py run <题目目录> --tag part1`。

## 块 2 · C++ 现场生存（1 h）

万一面试官要 C++，目标是「能写对、不出低级错」，不是精通。

1. [[interviews/core/cpp/headlands/lessons/C16_coderpad_survival|C16 CoderPad 现场生存]]：现场写 C++ 的模板、输入输出、编译错误怎么读（20 分钟）。
2. [[interviews/core/cpp/headlands/interview_questions/cheatsheet|C++ 速查表]]：20 条速查（15 分钟），重点是容器对应关系：`HashMap` → `unordered_map`，`TreeMap` → `map`，
   `PriorityQueue` → `priority_queue`（默认是大顶堆），`ArrayDeque` → `deque`。
3. 速读里每题的「C++ 要点」再扫一遍（15 分钟）：溢出用 `long long`，引用传参用 `const&`，边遍历边删要用返回的迭代器。
4. 开场话术（10 分钟）：「我平时主要写 Java；C++ 我写过……如果您不介意，我用 Java；要 C++ 也可以。」

## 块 3 · Java 深度题（1 h）

打开 [[interviews/core/java/headlands/interview_questions/questions|Java 题库]]，只看三节，每题只读「一句话答案」和「60 秒口述」：

- **A 速度与延迟**（Q01–Q04）：为什么带 GC 的 Java 也能快、预热、什么时候不够快。
- **E JIT 与 GC**（Q18–Q24）：分层编译、内联、逃逸分析、去优化、G1 与 ZGC 怎么选。
- **F 并发与内存模型**（Q25 起）：`volatile`、happens-before、`synchronized` 与锁、线程池、并发容器。

每节读完，挑一题大声说一遍英文 60 秒版本。

## 块 4 · 编码题后 9 道（1.5 h）

继续 [[interviews/companies/headlands/08-solutions-digest|18 题速读]]：hc01 股票交易 DP → hc03 递归求和 → hc08 订单序列 API → hc11 区间重叠 → hc06 寄存器位运算 →
hc13 定长内存池 → ld01 SPSC 通道 → ld02 交易系统 OOD → ld03 异步 TCP 通道。

这一块只读速读，每题 10 分钟；LLD 三题重点看「数据结构」和「追问」，它们最可能以聊天的形式出现。

## 块 5 · 背景问题（1 h）

1. 填空（20 分钟）：打开 [[interviews/companies/headlands/behavioral/question_bank|背景问题题库]]，把【待补】填上：写过多少 C++（一句诚实的话）、为什么想做交易、为什么离开 PayPal、愿意去哪个办公室和工作许可、面试时间线。
2. 口述两个故事（30 分钟）：S1 结算管线、S3 静默空值的根因。每个先讲 60 秒版，再讲 2 分钟版，用手机录一遍听。
3. 准备一个性能排查的故事（10 分钟）：测量 → 找到瓶颈 → 改快了多少。没有完整的就用 S6「单行成本 × 峰值行数」。

## 块 6 · 晚上（30 min）

- [[interviews/companies/headlands/01-company-brief|公司简报]] 第 0 节「一页结论」（5 分钟）。
- [[interviews/companies/headlands/06-questions-to-ask|反问清单]] 挑 3 个问题记在纸上（10 分钟）。
- 周一清单（5 分钟）：Teams 和 CoderPad 链接能打开；耳机和网络；水；提前 10 分钟进会议；纸笔。
- 早点睡。

## 周一上午（面试前 2 小时）

- 速读的目录表从头扫一遍，每题只看「核心思路」那一句（30 分钟）。
- 口述一遍自我介绍（60 秒）和「为什么交易 / 为什么 Headlands」。
- 不学新东西。
