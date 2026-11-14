# 07 · 技术面练习：五组可运行的 Python 题

技术面的编码轮常常不是 LeetCode，而是和工作相关的小任务：解析测试结果、并行跑测试、面试官自己出的系统小题，以及带回家题里的评测集剪枝和性能表判读。下面五组题各有题面、空白的 `starter.py`、参考解和一套 pytest 测试。做法是：计时，在 `starter.py` 里写，用测试检查，最后对着题面里的"面试官会追问"把答案说出声。每组的 `problem.md` 把用到的 AI 词都用白话解释了，不需要先学 AI。

## 做的顺序和限时

| 顺序 | 练习 | 限时 | 练什么 | 对应哪一轮 |
|---|---|---:|---|---|
| 1 | [03 · 失败签名](practice/03_failure_signatures/problem.md) | 30 分钟 | XML 解析、正则去噪、按过挂序列归类 | 编码轮的工作题 |
| 2 | [04 · 并行测试执行器](practice/04_parallel_test_runner/problem.md) | 30 分钟 | `subprocess`、进程组、超时、重试语义、线程池 | 编码轮的工作题 |
| 3 | [05 · 多频道消息队列](practice/05_multi_channel_queue/problem.md) | 30 分钟 | 位集合、反向索引、并查集、复杂度 | 编码轮的自出题 |
| 4 | [02 · 性能扫描表 → 放行结论](practice/02_perf_sweep_verdict/problem.md) | 45 分钟 | 列名契约、单位换算、红黄绿规则、异常检查 | 允许用 AI 的轮次、带回家题 |
| 5 | [01 · 评测集剪枝](practice/01_eval_pruning/problem.md) | 45 分钟 | 分层抽样、Kendall τ、放行结论、留一法 | 允许用 AI 的轮次、带回家题 |

- 先做 03、04：离你的测试背景最近，也是编码轮最可能出的形状，先把"30 分钟写完 + 自测"的节奏练熟。
- 05 是面试官自己出过的题，重点在问清规则和说出复杂度。
- 02、01 带 AI 概念，放在最后；先读题面的"背景"表，再开始计时。
- 每组第一遍超时也写完，记下卡在哪；隔两三天不看参考解再做一遍，要在限时内全绿。

## 怎么跑

所有命令都在 kit 目录下执行（`vault/interviews/companies/cerebras/`），仓库根目录是 `../../../..`：

```bash
cd vault/interviews/companies/cerebras

# 参考解：应该全绿
uv run --project ../../../.. pytest practice/03_failure_signatures -q

# 你的 starter.py：把 IMPL 设成 starter，同一套测试就改测你的代码
IMPL=starter uv run --project ../../../.. pytest practice/03_failure_signatures -q

# 只跑某一部分、只跑边界用例
IMPL=starter uv run --project ../../../.. pytest practice/03_failure_signatures -q -m part1
IMPL=starter uv run --project ../../../.. pytest practice/03_failure_signatures -q -m edge

# 五组一起
uv run --project ../../../.. pytest practice -q
```

- 切换原理：kit 根目录的 `conftest.py` 提供 `impl` 夹具，按环境变量 `IMPL` 加载同目录下的 `solution.py`（默认）或 `starter.py`。
- 测试按部分打了标记：`part1` 到 `part4`、`edge`（边界）、`fmt`（输出格式）、`perf`（性能）。
- 数据是生成的，固定随机种子：01、02 跑 `make_data.py`，03 跑 `make_runs.py`，04 跑 `make_commands.py`（生成一个手动试用的 `commands.txt`），05 的数据直接在 `data/` 里。重新生成得到同样的文件。
- 04 的测试会真的起子进程、睡眠，一次约 8 秒；其他几组都在 1 秒内。

## 每一组怎么练

1. **读题 3 分钟**：说出输入、输出、两个澄清问题（比如"error 算不算失败""订阅前的消息要不要"）。
2. **先写 Part 1 就跑 `-m part1`**，绿了再往下，不要一次写完再调。
3. **剩 5 分钟时停**：跑 `-m edge`，挑一个失败的边界说清楚原因。
4. **追问说出声**：题面"面试官会追问"表，每条 30 秒内答完；答不上来的记下，下次先看。
5. **对照参考解**：只看自己卡住的那部分，再关掉重写一遍。

## 做完的标准

| 练习 | 限时内全绿 | 还要能说出 |
|---|---|---|
| 03 | 是 | 签名太粗和太细各会怎样；10 GB 的文件怎么流式读 |
| 04 | 是 | 为什么要杀进程组；重试怎样掩盖缺陷 |
| 05 | Part 1–3（Part 4 是加分） | 位集合求交的代价；退订后并查集怎么办；两种"最少频道"的区别 |
| 02 | 是 | 为什么取不低于客户并发的那一档；从单用户速度猜模型大小 |
| 01 | 是 | 为什么不能直接挑区分度最高的题；3 到 4 个模型时 τ = 1 为什么证据弱 |

相关页面：[06-technical-rounds.md](06-technical-rounds.md) 第 1.3 节和第 4.2 节讲这些题在面试里的形式。
