# pc10 · SQL Drill — 分组聚合 → 窗口函数 → join+FX → gaps-and-islands → NOT IN 的 NULL 陷阱

> 45 分钟第一轮里常见的"混合 Python + SQL"环节；五道小题全部 **(reconstructed)**——多个独立来源都确认"有 SQL 环节、强调速度"，但均未留下具体题面，题目按这类岗位典型 SQL 考点重建。

## 背景

三条独立报道指向同一件事：Millennium 的技术筛不是纯 LeetCode，还混了 SQL。1point3acres thread-1079245（Developer OA，2 h/5 题）报道"SQL 基础、Python decorator"；thread-855488（Quant/FE OA，3 h/4 题）"3 道 Python 直白、SQL 一题挂"；thread-939377（DS/DE OA，120 min/8 题）"3 概率选择 + 3 算法选择 + 1 SQL + 1 coding"；Blind 摘要独立确认"HackerRank-style screen leaning heavily on coding, mix of Python and SQL, main thing is speed"。这五道题把"SQL 基础"具体化成一套用 `sqlite3` 内存库跑的小题：分组聚合 → 窗口函数 → 多表 join 换算货币 → gaps-and-islands 连续区间 → `NOT IN` 的经典 NULL 陷阱。

## 数据模型

三张表，定义在同目录 `schema.sql`（DDL）+ `seed.sql`（种子数据，可直接读，本文档所有例子都来自它）：

```sql
CREATE TABLE instruments (
    symbol   TEXT PRIMARY KEY,
    desk     TEXT NOT NULL,     -- 'EQUITY' | 'RATES' | 'FX'
    currency TEXT NOT NULL      -- 该 instrument 的计价货币
);

CREATE TABLE trades (
    trade_id   INTEGER PRIMARY KEY,
    symbol     TEXT,            -- NULL = 现金调整类分录，不挂靠任何 instrument
    trader     TEXT NOT NULL,
    trade_date TEXT NOT NULL,   -- 'YYYY-MM-DD'
    ts         TEXT NOT NULL,   -- 'YYYY-MM-DD HH:MM:SS'
    qty        INTEGER NOT NULL,  -- 正=买，负=卖
    price      REAL NOT NULL
);

CREATE TABLE fx_rates (
    currency     TEXT NOT NULL,
    rate_date    TEXT NOT NULL,
    rate_to_usd  REAL NOT NULL   -- 1 单位 currency = rate_to_usd USD
);
```

`instruments` 里有 7 个 symbol，其中 `ORPHAN` **从未出现在 `trades` 里**（Part 5 会用到）；`trades` 里有一条 `symbol IS NULL` 的现金分录（trader `garcia`，Part 2/4/5 都会碰到它）。完整种子数据见 `seed.sql`。

## API 契约（英文签名）

```python
def part1() -> str: ...   # 每 symbol 每日成交额
def part2() -> str: ...   # 每 trader 最新一笔交易
def part3() -> str: ...   # join FX 换算成 USD，按 desk 汇总
def part4() -> str: ...   # 每 trader 最长连续交易日
def part5() -> str: ...   # garcia 从未交易过的 instrument
```

每个函数返回一段 SQL 字符串，不接收参数；测试把它拿去对内存 sqlite3 库（用同一份 `schema.sql` + `seed.sql` 建的）执行，逐行比对结果。**sqlite3 语法**；Part 4 用了窗口函数 `ROW_NUMBER()`，需要 `sqlite3.sqlite_version_info >= (3, 25, 0)`（2018-09 起支持）——本机 `import sqlite3; sqlite3.sqlite_version` 先确认一遍。

## 规则

### Part 1 — 每 symbol 每日成交额

按 `(symbol, trade_date)` 分组，`SUM(ABS(qty) * price)` 作为当日成交额（不区分买卖方向，`qty` 取绝对值）。**`JOIN instruments`**（而不是直接 `GROUP BY trades.symbol`）：现金分录没有 `symbol`，不属于任何一个 symbol 的"当日成交额"，用 join 顺带把它排除，不需要额外写 `WHERE symbol IS NOT NULL`。金额 `ROUND(..., 2)`，避免浮点噪声。按 `symbol, trade_date` 升序输出。

### Part 2 — 每 trader 最新一笔交易

`ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC)`，取每个 trader 排名第一的那行，输出 `(trader, symbol, trade_date, ts, qty, price)`，按 `trader` 排序。**和 Part 1 相反**：这里**不**过滤 `symbol IS NULL`——如果一个 trader 最近一次真的就是那笔现金分录，它就是这题问的答案（种子数据里 `garcia` 正是这种情况）。

### Part 3 — join FX 换算成 USD，按 desk 汇总

`trades JOIN instruments`（拿到 `desk`、`currency`）再 `LEFT JOIN fx_rates ON (currency, trade_date)` 拿到当日汇率；`USD` 计价的 instrument 用 `CASE WHEN currency = 'USD' THEN 1.0 ELSE rate_to_usd END` 短路，不需要 `fx_rates` 里有一条 `USD` 自身的记录（种子数据里也确实没有）。按 `desk` 汇总 `ROUND(SUM(ABS(qty) * price * rate), 2)`，按 `desk` 排序。

### Part 4 — 每 trader 最长连续交易日（gaps-and-islands）

先 `SELECT DISTINCT trader, trade_date FROM trades WHERE symbol IS NOT NULL`（和 Part 1 一样的理由：现金分录那天不算"有交易"）。再用经典技巧：`julianday(trade_date)`（把日期转成一个整数）减去"按 `trader` 分组、按 `trade_date` 排序的 `ROW_NUMBER()`"，同一段连续日期内这个差值恒定，一旦断档差值就变——按这个差值分组就切出了每一段连续区间（"island"）。每个 trader 取**最长**的一段；并列时取**起始日期最早**的那一段。

### Part 5 — `garcia` 从未交易过的 instrument **(NOT IN 的 NULL 陷阱)**

从 `instruments`（已经是主键去重过的全集，包含从未被任何人交易过的 `ORPHAN`）出发，用 `NOT EXISTS` 相关子查询排除 `garcia` 交易过的 symbol：

```sql
SELECT i.symbol FROM instruments AS i
WHERE NOT EXISTS (
    SELECT 1 FROM trades AS t WHERE t.trader = 'garcia' AND t.symbol = i.symbol
)
ORDER BY i.symbol
```

**为什么不能写成 `NOT IN`**：`garcia` 有一条 `symbol IS NULL` 的现金分录，如果写 `symbol NOT IN (SELECT symbol FROM trades WHERE trader = 'garcia')`，子查询结果集里混进一个 `NULL`；SQL 里 `x NOT IN (a, b, NULL)` 只要 `x` 不等于 `a`、`b`，比较到 `NULL` 时结果是 `UNKNOWN` 而不是 `TRUE`，整个 `NOT IN` 表达式对**任何** `x` 都变成 `UNKNOWN`（不满足 `WHERE`），于是查询**静默返回 0 行**——不报错，只是错得很安静。`NOT EXISTS` 是逐行相关子查询，`t.symbol = i.symbol` 遇到 `t.symbol IS NULL` 只是"不匹配"，不会污染其它候选行。

## Worked examples（全部由 `solution.py` 对 `schema.sql` + `seed.sql` 实际执行得出）

**Part 1**（12 行，节选）
```
AAPL   2026-01-05   52650.0
AAPL   2026-01-06   15200.0
...
EURUSD 2026-01-06   110000.0
VOD    2026-01-05   50000.0
```

**Part 2**（4 行，一个 trader 一行）
```
alice   AAPL     2026-01-10  2026-01-10 09:00:00  10      155.0
bob     MSFT     2026-01-09  2026-01-09 09:00:00  20      311.0
dan     EURUSD   2026-01-06  2026-01-06 10:00:00  100000  1.1
garcia  NULL     2026-01-08  2026-01-08 12:00:00  1       500.0
```
（`garcia` 那行 `symbol` 是 `NULL`——它的现金分录就是它目前为止最新的一笔交易。）

**Part 3**
```
EQUITY   249640.0
FX       110000.0
RATES    131526.0
```

**Part 4**
```
alice   2026-01-08  2026-01-10  3
bob     2026-01-05  2026-01-06  2
dan     2026-01-06  2026-01-06  1
garcia  2026-01-05  2026-01-05  1
```
（`garcia` 的交易日是 `01-05`、`01-07`，中间断档，两段都只有 1 天，并列取更早的 `01-05`；那条 `01-08` 的现金分录不算交易日。）

**Part 5**
```
AAPL
BUND
EURUSD
MSFT
ORPHAN
```
（`garcia` 交易过 `VOD`、`GILT`，所以它俩不在结果里；`ORPHAN` 从没被任何人交易过，也出现在结果里——如果驱动表用 `SELECT DISTINCT symbol FROM trades` 而不是 `instruments`，会漏掉它。）

## `main()` 命令流

`main()` 只接一行 `PART <n>`（1–5），执行对应 SQL，逐行输出，列用制表符分隔，`NULL` 输出成空字符串：

```
PART 5
→ AAPL
  BUND
  EURUSD
  MSFT
  ORPHAN
```

## 边界清单

- `trades` 为空（`instruments` 非空）→ Part 1–4 均无输出；Part 5 输出全部 instrument（`garcia` 什么都没交易过）
- Part 1：现金分录（`symbol IS NULL`）不出现在任何一行
- Part 2：一个 trader 恰好一行；`garcia` 那行 `symbol` 字段是 `NULL`（不是空字符串，`main()` 展示层才转成空字符串）
- Part 3：全 `USD` 计价的 desk（`FX`，只有 `EURUSD`）不需要 `fx_rates` 里有任何一条 `USD` 记录也能算对
- Part 4：`sqlite3.sqlite_version_info >= (3, 25, 0)`（`ROW_NUMBER()` 依赖）；现金分录当天不计入"交易日"；并列最长时取起始日期最早的一段（`garcia` 的例子）
- Part 5：驱动表必须是 `instruments`（覆盖零交易的 `ORPHAN`），不能是 `SELECT DISTINCT symbol FROM trades`；`NOT IN` 版本在这份种子数据上会**静默返回空结果**（隐藏测试专门验证这一点：直接跑一遍写死的 `NOT IN` 版本，断言它是空的，对照正确版本非空）
- 大规模：5 万条合成交易，Part 4 的窗口函数 + gaps-and-islands 在本机 < 2 s（见 `test_perf_part4_streaks_over_50k_synthetic_trades`）

## 追问

1. **`NOT IN` 还能怎么救？** 给子查询加 `WHERE symbol IS NOT NULL`，或者用 `COALESCE`/`IS DISTINCT FROM`；但语义上 `NOT EXISTS`（或 `LEFT JOIN ... WHERE right.key IS NULL`）更直接，不用记着"每次都要防 NULL"。
2. **Part 3 如果某天某币种没有 `fx_rates` 记录会怎样？** `LEFT JOIN` 会把那一行的汇率留成 `NULL`，`price * NULL = NULL`；SQL 的聚合函数（`SUM`）会**跳过** `NULL`，所以那一行的成交额会被"安静地漏掉"而不是报错或让整组变 `NULL`（除非那一组只有这一行）——这是另一个"沉默而不是报错"的陷阱，值得在面试里主动提出来。
3. **Part 4 换成"最长连续交易日 >= 2 的所有区间"而不是"每个 trader 一段最长的"要怎么改？** 去掉最外层按 `trader` 取 `rn = 1` 的窗口，直接在 `islands` CTE 上过滤 `streak_len >= 2`。
4. **索引会怎么设？** `trades(symbol, trade_date)` 支撑 Part 1，`trades(trader, ts)` 支撑 Part 2，`fx_rates(currency, rate_date)` 已经是复合主键天然支撑 Part 3 的 join。

## 来源与置信度

- **MED-HIGH**：1point3acres thread-1079245（Developer OA，2 h/5 题，"SQL 基础、Python decorator"）、thread-855488（Quant/FE OA，3 h/4 题，"SQL 一题挂"）、thread-939377（DS/DE OA，120 min/8 题，"3 概率选择 + 3 算法选择 + 1 SQL + 1 coding"）三条独立报道都确认 SQL 环节存在；Blind 摘要（"mix of Python and SQL, main thing is speed"）独立佐证"混合 Python/SQL、强调速度"这一形态。
- 均**未给出具体题面**，本题的五个小题、schema、种子数据、全部 worked examples均为按"SQL 基础"这一考纲重建 **(reconstructed)**：分组聚合（最基础）→窗口函数（`ROW_NUMBER`，OA 报道里常见）→多表 join（业务场景里必然出现）→ gaps-and-islands（SQL 面试经典难题）→ `NOT IN`/`NOT EXISTS` 的 NULL 陷阱（`INTERVIEWQUERY`/`TechPrep` 泛泛提及"SQL optimization"时最常考的一个概念）。

## 考什么

分组聚合是 SQL 的地基 · 窗口函数做"每组取一行"（`ROW_NUMBER` + `PARTITION BY`）比自连接/子查询更直接 · 多表 join 里"要不要过滤 NULL 挂靠"的业务判断（Part 1 vs Part 2 的对比就是同一份数据、不同语义下 NULL 处理正好相反）· gaps-and-islands 是连续区间类题目的通用解法 · `NOT IN` 遇到 NULL 会静默返回空结果，这是 SQL 面试里最容易被问到、也最容易在生产环境里悄悄写错的一个坑。
