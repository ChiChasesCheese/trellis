# 子代理指令 · Millennium LEaD 第一轮题集（`loop/rounds/01_first_round/`）

> 你是 `sonnet` 子代理，**不得再派生代理**。你只拥有分配给你的题目目录和对应的题解文章文件，不碰别的文件。
> 面向读者：Chi，1.5 年后端（PayPal Braintree，Snowflake/SQL/Python/Kotlin），自建 66K 行 Python 量化研究平台（pandas/DuckDB/FastAPI/PyTorch）。
> 目标轮次：**Millennium LEaD Program 第一轮 45 min**（Webex + HackerRank 实时编码；一手报道 = 15 min 背景 + 30 min 编码；题目"实用、贴近工作、不是 LeetCode 式"占多数，也有 LC medium 与 Python 内功题）。

## 0. 先读（复用，不重造）

- 布局与契约：`../CONVENTIONS.md`（每题 `problem.md` + `starter_template.py` + `starter.py` + `solution.py` + `test_<id>.py` + `REPORT.md`）。
- 参考实现（同一套 conftest/pytest.ini）：`../../snowflake/loop/rounds/03_phone_coding/pc06_happy_number/`（3-part，含 O(1) 空间的反作弊测试）与 `pc03_recent_event_stream/`（类设计 + 批处理封装）。**照它们的骨架写。**
- 题解模板：`../study/30-articles/_TEMPLATE.md`；参考成品 `../../snowflake/study/30-articles/pc06_happy_number.md`。
- 证据：每题的来源与置信度在 `../catalog/raw/coding_first_round.md`（若该文件尚未出现，用本文件 §2 的来源行；**不要自己编来源**）。

## 1. 硬规则（违反即退回）

1. **语言**：`problem.md`、`REPORT.md`、题解文章全部中文，技术名词英文括注；代码、docstring、API 签名英文。
2. **自包含**：只靠该题目录 + 本 kit 的链接就能做。`problem.md` 必含：背景（来源一句话）· API 契约 · Part 1..N 规则 · **Worked examples（全部由 `solution.py` 实际运行得出，不手算）** · `main()` 命令流 · 边界清单 · 追问 · 来源与置信度。
3. **重建标注**：来源只给了题名或一句话时，你补的 part / 细节一律标 **(reconstructed)**。一手原题与原追问不标。
4. **测试**：≥ 16 个 test，每个恰好一个 `partN` marker，外加 `edge` / `fmt` / `perf` / `io` 之一（按需）。必含：每个 worked example 逐字；空输入；单条；重复；非法输入抛 `ValueError`；一个 `perf`（规模写进 `problem.md`，本机 < 2 s）；至少一个 `io`（`run_script` fixture 跑 `main()`）。
5. **验收口径**：`solution.py` 全绿，**空的 `starter.py`（= `starter_template.py` 的拷贝）必须全红或大面积红**。你自己先跑：
   ```
   cd vault/interviews/companies/millennium
   uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_first_round/<id>_* -q -p no:cacheprovider
   IMPL=starter uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_first_round/<id>_* -q -p no:cacheprovider
   ```
   pandas 题：`--with pytest --with pandas`；测试若 `import pandas` 失败要 `pytest.importorskip("pandas")`，**但 solution 的核心逻辑不能只靠 pandas**（提供纯 Python 路径），因为 HackerRank 的语言环境可能没有它。
6. **数字**：`REPORT.md` 里的复杂度、规模、测试数全部来自你实际跑过的命令；测试数用 `grep -c "def test"`。
7. **不写过程话**（"我先…然后…"、"本次任务"），文件是给读者的成品。
8. **完成后**在你的回复里给出：目录列表、两条 pytest 命令的最后一行输出、`grep -c "def test"`、你认为最弱的两处（会被编排者重点复核）。

## 2. 题目分配与来源（编排者填）

| ID | 题 | 来源与置信度 | Part 设计要点 |
|---|---|---|---|
| pc01 | **Grouped aggregation over millions of rows**（CSV/DataFrame 按 id 分组求和；分块 + 多线程/多进程） | **HIGH（一手）** LeetCode Discuss 7423863（2025-12，Quant Dev-Python，Round 3）："given a dataframe or csv with millions of records, group by a common identifier and find aggregated sums… solved by chunking and re-aggregating"；面试官允许查语法 | Part 1 单遍纯 Python 流式 group-sum（`csv` 模块，dict 累加，Decimal 或整数分）· Part 2 分块 → 每块聚合 → 合并（`chunk_size`，可用 `concurrent.futures`，测试用 `multiprocessing` 或线程均可但结果必须确定）· Part 3 **(reconstructed)** 多键分组 + 多聚合（sum/count/max）+ 输出按 key 排序；追问：内存上限、GIL、为什么多进程而不是多线程、pandas `read_csv(chunksize)` |
| pc02 | **Async paginated API ingestion**（`asyncio` 拉取分页 API 直到 next 为空；并发上限；重试） | **HIGH** PracHub Millennium 页 "Implement paginated API ingestion"（Technical Screen，2025-09-06）+ "Debug missing output in Python async HTTP flow"（2025-10-24）；LeetCode Discuss 7423863 Round 2 "Asyncio — write working code and explain how coroutines work"；1p3a thread-1124751（异步编程追问） | 不能真联网：把"HTTP 客户端"抽象成 `fetch_page(cursor) -> dict` 的可注入 async 函数（测试注入假客户端，可设延迟/抛错）。Part 1 顺序翻页收集所有 items · Part 2 并发（`asyncio.Semaphore` 限并发，`gather`），保持输出顺序稳定 · Part 3 **(reconstructed)** 指数退避重试 + 幂等去重；追问：coroutine vs thread、event loop 在哪、`await` 漏写的典型 bug（对应"missing output"题）、超时 |
| pc03 | **Decorators**（retry / memoize / timing / rate-limit 装饰器，含参数化装饰器与 `functools.wraps`） | **HIGH** LeetCode Discuss 7423863 Round 5 "decorator code writing"；1p3a thread-1079245（Developer OA：Python decorator）；1p3a 1143768；aggregator（TechPrep/InterviewQuery）"decorators, generators, context managers" | Part 1 `@timed` + `@memoize`（保留 `__name__`/docstring）· Part 2 参数化 `@retry(times, exceptions, backoff)`，计数可测 · Part 3 **(reconstructed)** 类装饰器/带状态的 `@rate_limited(n, per_seconds)`（注入时钟）；追问：装饰器执行时机、栈叠顺序、`wraps` 为什么必要、方法上的装饰器与 `self` |
| pc04 | **Big-integer string arithmetic**（两个十进制字符串相加 → 减法/乘法/任意进制） | **HIGH（一手）** 1p3a thread-1090775（C++ Developer 电面 45 min：15 min 背景 + 30 min "large integer addition as strings"，面试官反馈很少） | Part 1 加法（含前导零、空串非法）· Part 2 带符号加减 · Part 3 **(reconstructed)** 乘法 O(n·m) + 任意进制 2–36；追问：为什么不用 `int()`（面试要看手写进位）、时间复杂度、负数处理 |
| pc05 | **Subarray sums divisible by K**（前缀和取模计数；扩展到"和恰为 K"、"最长子数组"） | **HIGH（一手）** LeetCode Discuss 7423863 Round 2（LC 974）；TechPrep 2026 列表 | Part 1 LC 974 计数 · Part 2 LC 560 和为 K 的计数 · Part 3 **(reconstructed)** 最长和为 K 子数组的长度 + 返回一段区间（tie: 最左）；追问：负数取模、O(n) vs O(n²)、流式版本 |
| pc06 | **Water problems**（Trapping Rain Water + Container With Most Water，双指针） | **HIGH（一手）** LeetCode Discuss 7423863 Round 1（LC 42 + LC 11 同一轮两题）；TechPrep 2026 | Part 1 LC 11 双指针 · Part 2 LC 42（先 O(n) 前后缀，再双指针 O(1) 空间；测试禁用 O(n) 辅助数组的一个用例可选）· Part 3 **(reconstructed)** 2D 版（LC 407，堆）或"有 k 次加高柱子"择一；追问：为什么双指针正确（交换论证） |
| pc07 | **Anagram store**（设计一个数据结构存字符串、按 anagram 组查询/计数/删除；Valid Parentheses 热身） | **HIGH** PracHub "Design a data structure to store anagrams"（Technical Screen，2026-02-12）；StealthCoder：Valid Parentheses、Palindromic Substrings 在 Millennium 报道列表 | Part 1 `AnagramStore.add/group_of/count`（键 = 排序串 或 26 计数元组，两者比较）· Part 2 `remove` + `most_common_group`（tie 字典序）· Part 3 **(reconstructed)** 支持 Unicode/大小写策略 + 流式 top-k；热身函数 `is_valid_parentheses`；追问：sorted key O(L log L) vs count key O(L)、哈希元组、内存 |
| pc08 | **LRU cache with TTL + median from stream**（两个经典设计题打包成一题两部分） | **MED** QuantVault Millennium 题单（LRU Cache · Median from a Data Stream，未标轮次）；Stripe/Snowflake 题库同族高频 | Part 1 `LRUCache(capacity)` O(1) get/put（`OrderedDict` 与手写双链表两种，测试只看行为）· Part 2 加 TTL（注入时钟）· Part 3 `MedianStream.add/median`（两个堆）；追问：线程安全、LRU vs LFU、为什么两个堆 |
| pc09 | **Price data store**（时间序列价格：写入、最新价、as-of 查询、区间聚合） | **HIGH** LeetCode Discuss 7423863 Round 5 "price data design problem"（Quant Dev-Python）；PracHub "How would you model stock price prediction?"（2026-02，口头） | Part 1 `PriceStore.upsert(symbol, ts, price)` / `latest(symbol)` / `as_of(symbol, ts)`（二分，乱序写入、同 ts 覆盖）· Part 2 区间 `ohlc(symbol, t0, t1)` + `vwap`（带 volume）· Part 3 **(reconstructed)** 多币种：用 FX 表把价格换算成基础货币（对应 QuantVault OA "multi-currency PnL"）；追问：为什么不用 dict-of-list 直接 append、内存、迟到数据、持久化 |
| pc10 | **SQL drill in Python**（用 `sqlite3` 内存库：分组、窗口、join、去重，五道小题） | **MED-HIGH** 1p3a thread-1079245（OA：SQL basics）、thread-855488（SQL 挂）、thread-939377（DS/DE OA 1 SQL）；InterviewQuery "possibly SQL queries" 在 45-min 技术筛 | 题目给三张表（trades / instruments / fx_rates）的 DDL + 种子数据；`part1..part5` 各返回一个 SQL 字符串，测试用 sqlite3 执行后与期望比对（期望由 solution 生成并写死）。Part 1 每 symbol 当日成交额 · Part 2 每 trader 最新一笔（窗口 `ROW_NUMBER`）· Part 3 join fx 换算基础货币并按 desk 汇总 · Part 4 连续交易日 streak（gaps-and-islands）· Part 5 去重与 NULL 陷阱（`NOT IN` vs `NOT EXISTS`）。`starter_template.py` 里每个 part 返回 `""`。 |

## 3. 每题必须写的题解文章

路径 `study/30-articles/<id>_<slug>.md`（与目录名一致），按 `_TEMPLATE.md` 的 8 节，中文，≤ 200 行；"§6 面试里怎么说"用英文句子（Chi 面试说英文）；"§8 同族题"链到本 kit 其它题或 `../../snowflake/` / `../../stripe/` 的同族题（只写相对路径，不编 ID）。

## 4. 完成定义

- `verify_suites.py` 口径通过（reference 绿、空 starter 红）。
- `problem.md` 的每个 worked example 在测试里逐字出现。
- `REPORT.md` 六节：Summary · Sources & confidence · Approach by part · Pitfalls hidden tests target · Complexity & measured cost · Test inventory · Skills exercised（照 `pc06` 的 REPORT）。
- 题解文章存在且 §5 的代码骨架能和 `solution.py` 对上。
