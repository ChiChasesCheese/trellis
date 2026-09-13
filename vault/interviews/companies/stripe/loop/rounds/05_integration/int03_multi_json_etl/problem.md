# int03 · Multi-JSON ETL — 三份异构 JSON → 统一客户字典 → 双向转换 → 订单 join → 异常报告
<!-- mockserver: none -->

**Type:** onsite Integration（真实文件系统 I/O，非算法题；无需 mockserver） · **Stage:** 60 min，3 part
**Last asked:** linkjob 2025-12 面经（三份来源不同的 JSON 文件读取、互转字典、双向 ETL） · **Frequency:** linkjob
2025-12（本节主来源）；Exponent 的 Integration 题型清单单独列出"读多个 JSON 文件互转格式"一类 · **Confidence:**
medium-high for 题目形状（"三份 JSON → 字典 → 双向 ETL"这句话是 linkjob 面经原话，独立于 Exponent 的题型分类
交叉印证）；具体文件名、字段名、异常分类、CLI 参数是本仓库复刻（面经原文没有给出 I/O 细节，见 Sources）。

## Context
Stripe 内部经常需要把"当前系统"的数据和"迁移中/遗留系统"的导出文件对账：字段名不一样、有的记录缺字段、
同一个人在两边各有一条记录（谁是"权威"版本？），下游报表还要再 join 一份订单数据。这道题模拟这个场景：三份
独立生成的 JSON 文件（`customers.json` 当前系统导出、`legacy_export.json` 旧系统导出、`orders.json` 订单
数据），字段名故意不一致、故意有缺失和重复，考察的是**防御性解析**（不静默吞掉坏数据，而是分类记录）、
**幂等的双向格式转换**、以及"三份数据里任何一份处理慢了会拖垮下一步"时的模块化设计。不考算法，考数据契约。

## 面试官给的"数据契约"文档（按本仓库 data/ 实现整理）

### `customers.json` — 当前系统导出，扁平记录列表
```
[
  {"id": <int>, "email": <str>, "name": <str>, "created": "<YYYY-MM-DD>"},
  ...
]
```
`email`/`name`/`created` 均可能缺失（键不存在）或为空字符串；`id` 保证总是存在。同一个 `email`（大小写/首尾
空格不敏感）可能出现多次（不同 `id`，代表重复导出或历史更名）。

### `legacy_export.json` — 旧系统导出，嵌套记录字典，字段名不同
```
{
  "records": {
    "<legacy_id>": {"cust": {"mail": <str>, "full_name": <str>, "signup_date": "<YYYY-MM-DD>"}},
    ...
  }
}
```
`legacy_id` 是字符串 key（如 `"L0001"`）。`cust.mail`/`cust.full_name`/`cust.signup_date` 均可能缺失。

### `orders.json` — 订单列表，按 `customer_email` 关联客户
```
[
  {
    "order_id": <str>, "customer_email": <str>,
    "items": [{"sku": <str>, "qty": <int>, "unit_cents": <int>}, ...],
    "status": <str>, "placed_at": "<YYYY-MM-DDTHH:MM:SS>"
  },
  ...
]
```
`customer_email` 可能为空；同一个 `order_id` 可能重复出现（数据管道重跑导致的重复导出，不代表两笔不同订单）。
`items` 为空列表时该订单总额为 0（合法，不是异常）。

## 数据字典（unified `Customer` 字段 ← 各来源字段名映射）

| unified `Customer` 字段 | `customers.json` | `legacy_export.json`（`records.<legacy_id>.cust`） |
|---|---|---|
| `id` | `id`（int，统一转成 `str`） | `records` 的 key，即 `<legacy_id>`（字符串，如 `"L0001"`） |
| `email` | `email`（`normalize_email`：trim + lower；缺失/空 → 该记录整体丢弃并记异常） | `cust.mail`（同样 `normalize_email`；缺失/空 → 丢弃并记异常） |
| `name` | `name`（缺失 → `""`） | `cust.full_name`（缺失 → `""`） |
| `created` | `created`（缺失 → `""`，ISO `YYYY-MM-DD`） | `cust.signup_date`（缺失 → `""`） |

统一后的 `Customer` 就是 `{"id": str, "email": str, "name": str, "created": str}` 这四个键，不多不少
——`to_legacy`/`from_legacy` 的往返等价（见 Part 2）依赖这一点。

## Rules
### Part 1 — 读取与统一
`class EtlError(Exception)`：任何格式错误的输入文件都抛这个异常，消息必须包含**文件路径**，JSON 语法错误时还要
包含 `json.JSONDecodeError` 报出的**行号/列号**（如 `"...: invalid JSON at line 3 column 5: ..."`）。

- `load_json_file(path: str) -> Any`：读文件、`json.loads`；文件不存在、无法解码、JSON 语法错误都统一抛
  `EtlError`（调用方不应该看到裸的 `OSError`/`json.JSONDecodeError`）。
- `normalize_email(raw) -> str`：非字符串或假值（`None`/`""`）返回 `""`；否则 `raw.strip().lower()`。
- `parse_customers(raw: list[dict]) -> tuple[list[dict], list[dict]]`：把 `customers.json` 的原始记录转换成
  `Customer` 列表；`email` 规范化后为空的记录**丢弃**，同时追加一条 `{"type": "missing_email", "source":
  "customers", "ref": <id 或下标>, "detail": ...}` 异常。
- `parse_legacy(raw: dict) -> tuple[list[dict], list[dict]]`：同上，读 `legacy_export.json`，按数据字典做字段
  名映射；`mail` 规范化后为空同样丢弃 + 记 `source="legacy"` 异常。
- `unify_customers(*customer_lists: list[dict]) -> tuple[dict[str, dict], list[dict]]`：把任意多份 `Customer`
  列表按 `email` 合并成 `dict[email, Customer]`。**同一 email 出现多次时，`created` 最早的记录胜出**
  （字符串比较，`YYYY-MM-DD` 格式天然可比较大小）；`created` 缺失/空的记录视为"最晚"（永远不会赢过一条有日期
  的记录）；严格早于才替换（同日期保留先出现的）。每次替换都记一条 `{"type": "duplicate_customer",
  "source": "unify", "ref": <email>, "detail": ...}` 异常。
- `load_all(in_dir: str) -> tuple[dict[str, dict], list[dict], list[dict]]`：从 `in_dir` 读取
  `customers.json` / `legacy_export.json` / `orders.json` 三个文件（固定文件名），返回
  `(统一后的 customers 字典, 原始 orders 列表, 到目前为止的异常列表)`。`orders.json` 在这一步只读取校验、
  不做任何客户关联（关联在 Part 2）。

### Part 2 — 双向转换 + 订单 join
- `to_legacy(customer: dict) -> dict`：`Customer -> {"legacy_id": id, "cust": {"mail": email,
  "full_name": name, "signup_date": created}}`。纯格式转换，不做 I/O、不做校验。
- `from_legacy(record: dict) -> dict`：`to_legacy` 的逆函数。**往返等价**：对任何这个模块产出的 `Customer c`
  （`email` 已经是 `normalize_email` 过的），`from_legacy(to_legacy(c)) == c` 恒成立。
- `join_orders(customers: dict[str, dict], orders: list[dict]) -> tuple[dict[str, dict], list[dict]]`：按
  （规范化后的）`customer_email` 把每笔订单挂到对应客户上，返回一份**新**的 `dict[email, Customer]`，每个值
  多一个 `"orders"` 列表（每笔订单精简成 `{"order_id", "status", "placed_at", "total_cents"}`，
  `total_cents = Σ qty × unit_cents`，整数分）。同时产出异常：
  - `customer_email` 规范化后为空 → `{"type": "missing_email", "source": "orders", ...}`
  - `customer_email` 不在 `customers` 里 → `{"type": "orphan_order", "source": "orders", ...}`
  - 同一个 `order_id` 出现 ≥2 次 → 每个重复的 `order_id` 记一条 `{"type": "duplicate_order", "source":
    "orders", ...}`（不影响 join——重复订单仍然各自计入金额和订单数，这是"数据管道重跑"场景的忠实反映，不是
    去重需求；本题只要求**报告**重复，不要求去重金额）。

### Part 3 — 报告 + 异常 CSV + CLI
- `build_report(joined: dict[str, dict]) -> dict[str, dict]`：`join_orders` 的输出 → 按 email 排序的
  `dict[email, {"order_count": int, "total_cents": int, "most_recent_order": str | None}]`。
  `most_recent_order` 取 `placed_at` 字典序最大（ISO-8601 格式下等价于时间最晚）的订单的 `order_id`；零订单
  客户是 `None`，不是缺键。
- `write_outputs(out_dir: str, report: dict, anomalies: list[dict]) -> None`：在 `out_dir`（不存在则创建）下
  写 `report.json`（`json.dumps(..., indent=2, sort_keys=True)`）和 `anomalies.csv`（表头固定
  `type,source,ref,detail`，用 `csv.writer`，逐行是异常字典的四个字段，顺序即 `anomalies` 列表顺序）。
- `run_etl(in_dir: str, out_dir: str) -> dict`：编排 `load_all` → `join_orders` → `build_report` →
  `write_outputs`，返回 `{"customers": n, "orders": n, "anomalies": n}` 摘要。
- `main_cli(argv) -> int`：`--in-dir DIR --out-dir DIR`，调用 `run_etl` 并打印
  `f"customers={n} orders={n} anomalies={n}"`。

### `main()` / `PART n` 驱动（供 io 测试）
```
PART 1
<in_dir>
                            输出: "customers=<n> anomalies=<n>"

PART 2
<in_dir>
<email>
                            输出: 该客户 to_legacy() 的单行 JSON（sort_keys），
                            下一行 "ROUNDTRIP_OK" 或 "ROUNDTRIP_FAIL"；
                            email 不存在 → 只输出一行 "NOT_FOUND"

PART 3
<in_dir>
<out_dir>
                            输出: "customers=<n> orders=<n> anomalies=<n>"（同时把
                            report.json / anomalies.csv 写到 out_dir）
```

## Worked examples
最小三文件示例（省略磁盘路径，直接给内容）：
```
customers.json:
[
  {"id": 1, "email": "Alice@Example.com ", "name": "Alice A", "created": "2024-03-01"},
  {"id": 2, "email": "bob@example.com", "created": "2024-01-15"},
  {"id": 3, "email": "alice@example.com", "name": "Alice Dup", "created": "2023-11-20"},
  {"id": 4, "name": "No Email"}
]

legacy_export.json:
{"records": {
  "L001": {"cust": {"mail": "carol@example.com", "full_name": "Carol C", "signup_date": "2022-05-05"}},
  "L002": {"cust": {"mail": "bob@example.com", "full_name": "Bob Legacy"}},
  "L003": {"cust": {}}
}}

orders.json:
[
  {"order_id": "O1", "customer_email": "alice@example.com", "items": [{"sku":"A","qty":2,"unit_cents":500}], "status": "paid", "placed_at": "2024-05-01T10:00:00"},
  {"order_id": "O2", "customer_email": "ALICE@example.com", "items": [{"sku":"B","qty":1,"unit_cents":1200}], "status": "paid", "placed_at": "2024-06-01T10:00:00"},
  {"order_id": "O3", "customer_email": "ghost@example.com", "items": [], "status": "paid", "placed_at": "2024-01-01T00:00:00"},
  {"order_id": "O4", "customer_email": "", "items": [], "status": "paid", "placed_at": "2024-01-01T00:00:00"},
  {"order_id": "O1", "customer_email": "alice@example.com", "items": [{"sku":"A","qty":2,"unit_cents":500}], "status": "paid", "placed_at": "2024-05-01T10:00:00"}
]
```
`load_all(in_dir)`：
```
unified = {
  "alice@example.com": {"id": "3", "email": "alice@example.com", "name": "Alice Dup", "created": "2023-11-20"},
  "bob@example.com":   {"id": "2", "email": "bob@example.com", "name": "", "created": "2024-01-15"},
  "carol@example.com": {"id": "L001", "email": "carol@example.com", "name": "Carol C", "created": "2022-05-05"},
}
anomalies = [
  {"type": "missing_email", "source": "customers", "ref": "4", "detail": "customer record has no usable email"},
  {"type": "missing_email", "source": "legacy", "ref": "L003", "detail": "legacy record has no usable mail"},
  {"type": "duplicate_customer", "source": "unify", "ref": "alice@example.com",
   "detail": "dropped id='1' created='2024-03-01', kept id='3'"},
  {"type": "duplicate_customer", "source": "unify", "ref": "bob@example.com",
   "detail": "dropped id='L002' created='', kept id='2'"},
]
```
（id=1 的 alice 记录 `created=2024-03-01` 晚于 id=3 的 `2023-11-20`，所以 id=3 胜出；bob 的 legacy 版本
`signup_date` 缺失视为最晚，customers.json 版本胜出。）

`join_orders(unified, orders_raw)` 的异常：
```
{"type": "orphan_order",   "source": "orders", "ref": "O3", "detail": "no customer for email 'ghost@example.com'"}
{"type": "missing_email",  "source": "orders", "ref": "O4", "detail": "order has no customer_email"}
{"type": "duplicate_order","source": "orders", "ref": "O1", "detail": "order_id appears 2 times"}
```
`build_report(...)`：
```
{
  "alice@example.com": {"order_count": 3, "total_cents": 3200, "most_recent_order": "O2"},
  "bob@example.com":   {"order_count": 0, "total_cents": 0,    "most_recent_order": null},
  "carol@example.com": {"order_count": 0, "total_cents": 0,    "most_recent_order": null},
}
```
（O1 出现两次，每次都计入：`ALICE@example.com` 规范化后也命中同一个客户；3 笔订单共
`2*500 + 1*1200 + 2*500 = 3200` 分；O2 的 `placed_at` 最晚，`most_recent_order = "O2"`。）

`to_legacy`/`from_legacy` 往返：
```
c = unified["carol@example.com"]
to_legacy(c) == {"legacy_id": "L001", "cust": {"mail": "carol@example.com", "full_name": "Carol C", "signup_date": "2022-05-05"}}
from_legacy(to_legacy(c)) == c   # True
```

## Edge cases hidden tests are known to target
- `email`/`mail` 缺失键 vs 空字符串 vs 纯空白字符串，三种都要判定为"无邮箱"并丢弃 + 记异常
- 同一 email 在 `customers.json` **内部**重复、在 `customers.json` 和 `legacy_export.json` **之间**重复，
  两种情况 `unify_customers` 都要生效（它接受任意多个列表，不只是两个固定参数）
- 重复 email 时 `created` 缺失的一方必须输给有日期的一方（不能因为字符串比较 `"" < "2020-01-01"` 就让缺失的
  一方"更早"从而胜出——这是最容易写反的边界）
- `created` 完全相同的两条重复记录，先出现的（`unify_customers` 参数顺序中先被处理的）保留
- `order_id` 重复：两笔订单各自都要计入 `report` 的 `order_count`/`total_cents`（不去重金额），但异常表里
  只记一条 `duplicate_order`（不是每次重复都记一条）
- `items` 为空列表的订单，`total_cents = 0`，不是异常，也不影响 `order_count`
- 空 JSON 文件（`""`）→ `load_json_file` 抛 `EtlError`，消息含文件路径和 `line 1 column 1`
  （`json.JSONDecodeError` 对空字符串的标准报错位置）
- `customers.json` 不是 JSON 列表（比如整个文件是一个对象）→ `load_all` 显式抛 `EtlError`，不是让下游解析
  代码在遍历时抛出一个语义不清的 `TypeError`
- `main()` PART 2 对不存在的 email 输出恰好一行 `"NOT_FOUND"`（不是空字符串、不是抛异常）
- `report.json`/`anomalies.csv` 的输出目录不存在时要能创建（`out_dir` 是多级路径也一样）
- 10^5 量级订单（`join_orders`/`build_report`）在 2 秒内完成——用 dict 查找，不要对 `customers` 做线性扫描
  找归属

## Variants seen in the wild
- linkjob 原文只说"reading three JSON files, converting them into dictionaries, and performing
  bidirectional ETL operations"，没有给出具体字段名、异常分类、CLI 形状；本仓库的三份 schema、"数据字典"
  映射表、`anomalies.csv` 的四类异常（`missing_email`/`duplicate_customer`/`orphan_order`/
  `duplicate_order`）都是本仓库为了让"双向 ETL"可测试而补全的合理复刻，不是题面原文。
  [`loop/raw/en_forums.md` 第 258 行]
- Exponent 收录的相近题型清单里，"读多个 JSON 文件互转格式"和"从本地文件抽字段 → 调外部 API"是两道分开的
  题目（后者需要网络调用，属于 int01 那一类）；本题只对应前者，刻意不引入网络依赖。
  [`loop/raw/en_forums.md` 第 269 行]

## What this tests
skills: S02 防御性 JSON 解析（区分"结构错误"与"业务缺失"）· S04 多源数据按 key 合并去重 · S06 整数分金额 ·
S08 确定性排序（`most_recent_order`/report 按 email） · S18 自定义异常归一化（`EtlError`，含文件名+位置） ·
S19 增量设计（Part 2/3 复用 Part 1 的 `Customer` 形状）· S24 领域知识（ETL 幂等性、双向格式转换的往返测试）

## 面试官追问（不少于 6 个）
1. "如果 `legacy_export.json` 有 10 万条记录，`unify_customers` 现在的实现复杂度是多少？" —— 期待：
   O(N)，因为是单次遍历 + dict 查找，不是对已有结果做线性扫描找同 email 记录。
2. "`to_legacy`/`from_legacy` 的往返等价测试，你会怎么用 `hypothesis` 或者手写随机数据来自动生成更多用例？"
   —— 期待：讨论 property-based testing 的思路（任意合法 Customer 都应该往返相等），即使当前只写了几个
   手工用例。
3. "如果 `orders.json` 里同一个 `order_id` 的两条记录金额不一样（不是完全重复，是冲突），现在的实现会怎么
   处理？该怎么处理？" —— 期待：识别当前实现"各自计入、只报告不去重"对冲突场景是不够的，讨论按
   `placed_at` 取最新版本 vs 报错 vs 人工介入三种策略的权衡。
4. "`unify_customers` 接受 `*customer_lists` 而不是固定两个参数，这个设计决定是为了什么？" —— 期待：
   未来如果再接入第三、第四份客户数据源（比如另一次系统迁移），不需要改函数签名。
5. "`created` 字段用字符串比较大小，如果哪天格式变成 `MM/DD/YYYY` 会发生什么？" —— 期待：字符串比较依赖
   ISO-8601 的可排序特性，格式一变就会静默产生错误结果；应该在 `parse_customers`/`parse_legacy` 里显式解析
   成 `date` 对象并校验格式，而不是假设字符串比较永远正确。
6. "`anomalies.csv` 要交给非工程师同事看，还能怎么改进可读性？" —— 期待：讨论按 `type` 分组、加一个汇总
   统计行、或者用更友好的自然语言 `detail` 文案；工程实现和"给谁看"的报告格式是两个不同的关注点。
7. "如果两次运行 `run_etl` 之间某个客户的 email 改了（同一个 `id`，新旧两个 email 都出现在不同批次的
   `customers.json` 里），`unify_customers` 现在能正确处理吗？" —— 期待：现在按 email 做 key，同一个 id
   换 email 会被当成两个不同客户，讨论要不要额外按 `id` 做二次校验/合并（当前实现的已知局限，写清楚而不是
   假装没有）。

## Sources
- `loop/raw/en_forums.md` 第 258 行（linkjob 2025-12 面经："BikeMap task requiring..." 段落前一句提到的另一
  个 2025 年版本："reading three JSON files, converting them into dictionaries, and performing
  bidirectional ETL operations"）
- `loop/raw/en_forums.md` 第 269 行（Exponent 收录的 Integration 题型清单："读多个 JSON 文件互转格式"作为
  独立一类，与"clone repo 调 API"、"本地文件抽字段调外部 API"并列）

## Clarifications（本仓库自定，非题面原文）
- linkjob 原文没有给出具体文件名/字段名/异常分类/CLI 参数，本仓库按"三份异构 JSON、字段名不一致、双向转换
  往返等价"这几个关键词自行设计了一套可测试、可复现（`random.Random(0)` 生成 `data/` 下的三份文件）的完整
  契约。异常分类（`missing_email`/`duplicate_customer`/`orphan_order`/`duplicate_order`）、`created` 最早
  胜出的去重规则、`most_recent_order` 用字符串比较 `placed_at` 都是本仓库补全，不是面经原文细节。
