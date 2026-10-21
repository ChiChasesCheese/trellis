# Headlands · Software Engineer —— 从这里开始

**下一轮**：技术视频面，**2026-10-26（周一）12:00 PT**，Teams + CoderPad。内容是技术问题、背景问题加现场编码，一般用不满一小时。
**语言**：他们主要用 C++，由面试官决定，所以 **C++ 和 Java 都要能写**。
**禁止 AI 工具**：练习时也要关掉补全，按考场条件练。

## 地图

| 想做什么 | 去哪 |
|---|---|
| 这一场怎么走、看重什么、6 天怎么排 | [loop/LOOP_GUIDE.md](loop/LOOP_GUIDE.md) |
| **背景问题**：怎么问 → 故事 → 题库 → 练习 | [behavioral/00_how_it_works.md](behavioral/00_how_it_works.md) · `behavioral/stories/` · [behavioral/question_bank.md](behavioral/question_bank.md) · [behavioral/drill.md](behavioral/drill.md) |
| **C++ 课本**（16 课，从 Java 讲到 C++） | [study/20-cpp/README.md](study/20-cpp/README.md) |
| **C++ 语言深度题**（44 题 + 速查表） | [kq_cpp_depth/questions.md](loop/rounds/01_video/kq_cpp_depth/questions.md) · [cheatsheet.md](loop/rounds/01_video/kq_cpp_depth/cheatsheet.md) |
| **编码题**（Java 15 题，其中 12 题另有 C++ 版） | `loop/rounds/<轮次>/<题>/`；讲义在 `study/30-articles/`（`_cpp.md` 是 C++ 版） |
| Java 21 课本 / 基础课本 | [study/10-java21/README.md](study/10-java21/README.md) · [study/00-foundations/README.md](study/00-foundations/README.md) |
| Java 语言深度题 | [kq_language_depth/questions.md](loop/rounds/01_video/kq_language_depth/questions.md) |
| 公司是做什么的 / 简历对 JD / 反问 | [01-company-brief.md](01-company-brief.md) · [fit.md](fit.md) · [06-questions-to-ask.md](06-questions-to-ask.md) |
| Onsite：设计题和 LLD | [loop/rounds/04_sd/00_how_to_run.md](loop/rounds/04_sd/00_how_to_run.md) · `loop/rounds/03_lld/` |

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

## 题目一览

| 题 | 内容 | C++ 版 |
|---|---|---|
| oa01 | Job chain 报表（你过了的 OA） | ✅ |
| hc01 | 买卖股票 DP 家族 | ✅ |
| hc02 | 合并 K 路有序流 → 多线程 | ✅ |
| hc03 | 递归求和 → 溢出 / 栈深度 / 并行 | ✅ |
| hc04 | 带快照的 queue mean → 单写多读 | ✅ |
| hc05 | 订单簿 + 撮合 + 零分配 | ✅ |
| hc06 | 32 位寄存器位运算 | ✅ |
| hc07 | ticker 哈希表优化 | ✅ |
| hc08 | 订单序列 API（树状数组） | ✅ |
| hc09 | Top-K 成交额 | ✅ |
| hc11 | 订单区间最大重叠 | ✅ |
| hc13 | 固定大小内存池 | ✅ |
| ld01–ld03 | SPSC 通道 / 交易 OOD / 异步 TCP 通道 | — |
| sd01–sd03 | 无用代码分析 / 定时任务调度 / 低延迟交易系统 | — |
