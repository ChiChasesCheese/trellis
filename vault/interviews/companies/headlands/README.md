# Headlands · Software Engineer —— 从这里开始

这是 Headlands Technologies 软件工程师岗位的备考入口。下一轮是一场技术视频面：现场用 CoderPad 写代码，穿插技术问题和背景问题，面试官由将来的同事担任。公司日常主要写 C++，用哪种语言由面试官决定，所以 C++ 和 Java 都要练。下面先是这一轮的基本信息，然后是各类材料的地图和面试前必须处理的事项。

**下一轮**：技术视频面，**2026-10-26（周一）12:00 PT**，Teams + CoderPad。内容是技术问题、背景问题加现场编码，一般用不满一小时。
**语言**：他们主要用 C++，由面试官决定，所以 **C++ 和 Java 都要能写**。
**禁止 AI 工具**：练习时也要关掉补全，按考场条件练。

**最后一天**：照着 [[interviews/companies/headlands/00-last-day-roadmap|最后一天路线图]] 做，不用再做决定。

## 地图

| 想做什么 | 去哪 |
|---|---|
| 这一场怎么走、看重什么、6 天怎么排 | [loop/LOOP_GUIDE.md](loop/LOOP_GUIDE.md) |
| **背景问题**：怎么问 → 故事 → 题库 → 练习 | [behavioral/00_how_it_works.md](behavioral/00_how_it_works.md) · `behavioral/stories/` · [behavioral/question_bank.md](behavioral/question_bank.md) · [behavioral/drill.md](behavioral/drill.md) |
| **C++ 课本**（16 课，从 Java 讲到 C++） | [core/cpp/headlands/lessons](../../core/cpp/headlands/lessons/README.md) |
| **C++ 语言深度题**（44 题 + 速查表） | [questions.md](../../core/cpp/headlands/interview_questions/questions.md) · [cheatsheet.md](../../core/cpp/headlands/interview_questions/cheatsheet.md) |
| **编码题**（24 题，每题 40 分钟，Java 和 C++ 各写一遍） | 练习清单 [[07-practice-java-cpp]]：按频率排好，每题一个 `problem.md`（动手）和一个 `solution.md`（下手的第一步、原理、两种语言的代码、追问答案）；一页速览 [[08-solutions-digest]] |
| Java 21 课本 / 基础课本 | [core/java/headlands/java21](../../core/java/headlands/java21/README.md) · [core/foundations/headlands](../../core/foundations/headlands/README.md) |
| Java 语言深度题 | [questions.md](../../core/java/headlands/interview_questions/questions.md) |
| 公司是做什么的 / 简历对 JD / 反问 | [01-company-brief.md](01-company-brief.md) · [fit.md](fit.md) · [06-questions-to-ask.md](06-questions-to-ask.md) |
| Onsite：设计题和 LLD | [core/system-design/headlands](../../core/system-design/headlands/00_how_to_run.md) · `loop/rounds/03_lld/` |

## 面试前必须处理

1. **背景问题里只有你能填的空**（`behavioral/question_bank.md`）：
   - 写过多少 C++，用一句话说清，诚实；
   - 为什么想做交易；
   - 为什么离开 PayPal；
   - 愿意去哪个办公室、工作许可的状态；
   - 面试时间线怎么回答。
2. **一个真实的性能排查故事**：你测量过一个运行中的系统、找到瓶颈、并且改快了。这类题交易公司必问，现在故事库里还没有。有的话填进 `behavioral/stories/templates.md`。
3. **两个数字别说错**：
   - S2 坏商户的比例是约 **0.14%**（35,000 个里有 50 个），不是 4%；
   - S10 前后两次估算，行数差约 **9 倍**、金额差约 **1.9 倍**、商户数差约 **2 倍**，不是「10 倍」。

## 做题命令（在本目录下运行）

```bash
# Java
python3 tools/jtest.py start loop/rounds/01_video/hc03_recursive_sum
python3 tools/jtest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1
# C++
python3 tools/cpptest.py start loop/rounds/01_video/hc03_recursive_sum
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1
```

`start` 把空壳复制成你的工作副本（Java 是 `work/`，C++ 是 `cpp/work.hpp`）。写完用 `run` 跑测试，加 `--impl reference` 跑参考解。

每道题的 `problem.md` 同时给出 Java 和 C++ 的签名，`solution.md` 里两种语言的代码都有。在 Cursor 里写之前先跑 `python3 tools/ide.py <题目目录>`，再 Reload Window，Java 和 C++ 就都能补全、报错和保存时格式化。

## 题目一览

| 题 | 内容 | 轮次 |
|---|---|---|
| hc03 | 递归求和 → 溢出 / 栈深 / 公式 | 电面（高频） |
| hc07 | 股票代码打包成整数 → 开放寻址哈希表 | 电面（高频） |
| hc01 | 买卖股票：一次 / 不限次数 / 最多 k 次 | 电面（高频） |
| hc04 | 队列均值 → 快照修正 | 电面（高频） |
| hc05 | 订单簿 → 限价撮合 | 电面（高频） |
| hc02 | 合并 K 个有序序列 → 惰性迭代器 | 电面（高频） |
| hc10 | 出现次数最多的 k 个数 | 电面（高频） |
| hc06 | 32 位寄存器位运算 | 电面（高频） |
| hc08 | 订单序列前缀查询 → 树状数组 | 电面 |
| hc09 | 按成交额取 Top-K | 电面 |
| hc13 | 定长内存池 → 带代数的句柄 | 电面 |
| hc11 | 订单区间最大重叠 → 分买卖 + 撤单 | 电面 |
| hc14 | 成交日志 → VWAP → 滑动时间窗口 | 电面（交易场景） |
| hc15 | 流式中位数 → 滑动窗口中位数 | 电面（交易场景） |
| hc16 | 交易台层级上的树形 DP | 电面（交易场景） |
| hc22 | 带批量加法的栈 → 懒标记 | 电面 |
| hc23 | 游程编码解码 → 分块流式 | 电面 |
| hc17 | 带 `*` 的模式匹配 | 电面 |
| hc21 | 平方根：牛顿法 → 整数平方根 | 电面（申请时的 √42 题） |
| hc19 · hc20 | 不相邻取数 · 合并区间 | onsite |
| hc12 · hc18 | 触发订单过滤 · 由快照算净持仓 | onsite |
| oa01 · oa03 | Job chain 报表（你过了的 OA） · as-of join | OA |
| ld01–ld03 | SPSC 通道 / 交易 OOD / 异步 TCP 通道 | onsite 设计轮 |
| sd01–sd03 | 无用代码分析 / 定时任务调度 / 低延迟交易系统 | onsite 设计轮 |
