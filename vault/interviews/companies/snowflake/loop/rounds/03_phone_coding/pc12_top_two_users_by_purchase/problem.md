# pc12 · Top Two Users by Total Purchase Amount — 分组求和 + 排名

> 电面 Easy 题。Part 1 是一手报道的原题；Part 2（按天分组 top-k）、Part 3（流式更新 + 退款）是同类聚合排名题最常见的两个追问，**(reconstructed)**。

## 背景

fastprep.io 收录：「统计每个用户的总购买金额，返回金额最高的两个用户」，标注 Easy / Array-Hash-Table / Phone Screen，最近一次报告 2026-06。

真正的坑不在"用哈希表求和再排序"，而在：**金额是小数，绝不能用浮点数累加**（累计误差在这类题里是最常见的隐藏测试点）；**打平时怎么排**；以及追问里"退款"意味着某用户的累计金额可以变成负数，但他依然要留在排名里参与比较。

## 输入

- Part 1：`records: list[str]`，每条 `"user,amount"`，`amount` 是恰好两位小数的非负数字符串（如 `"12.34"`）。
- Part 2：`records: list[str]`，每条 `"date,user,amount"`；`amount` 同上，非负。
- Part 3：`events: list[str]`，每条要么是 `"user,amount"`（`amount` 可以带负号，代表退款），要么恰好是字符串 `"QUERY"`（在这个时间点查询当前 top two）。
- **金额一律解析成整数分（cents）**，全程不经过浮点数：`"12.34"` → `1234`；输出也是分，不是重新拼出来的美元字符串。
- 格式不对（字段数不对、金额不是"整数.两位小数"、用户名为空）→ 抛 `ValueError`。

## API 契约（英文签名）

```python
def top_two_users(records: list[str]) -> list[tuple[str, int]]
def top_k_per_day(records: list[str], k: int) -> list[tuple[str, list[tuple[str, int]]]]
def process_stream(events: list[str]) -> list[list[tuple[str, int]]]
```

## 规则

### Part 1 — 全局 top two（原题）

按用户累加金额（分），返回**总额降序、金额相同按用户名升序**排序后的前两名。不足两个用户时返回全部。

### Part 2 — 按天分组 top-k **(reconstructed)**

按日期分组，组内按用户累加金额，组内取 **top-k**（排序规则同 Part 1）。按日期升序输出每一天的结果。`k = 0` 时每天的列表为空但日期仍然出现（说明"这天有数据，只是不要任何名次"）。

### Part 3 — 流式更新 + 退款 + 任意时刻查询 **(reconstructed)**

`events` 是一条随时间发生的事件流：金额更新（可正可负，负数代表退款）会累加进该用户的运行总额；`"QUERY"` 事件在**当前**这个时间点给出 top two 快照。返回值是**按 `QUERY` 出现顺序排列**的快照列表。**退款可以把某用户的总额变成 0 或负数，但他依然留在候选池里参与排名**（如果所有人都更惨，负数也能进 top two）。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（基本求和 + 打平按用户名）
```
records = ["alice,10.00", "bob,25.50", "alice,5.00", "carol,25.50"]
# alice=15.00, bob=25.50, carol=25.50 -> bob 和 carol 打平，按用户名升序 bob < carol
top_two_users -> [("bob", 2550), ("carol", 2550)]
```

**例 2**（只有一个用户）
```
records = ["alice,10.00"]
top_two_users -> [("alice", 1000)]
```

**例 3**（按天分组 top 2）
```
records = [
  "2024-01-01,alice,10.00", "2024-01-01,bob,5.00",
  "2024-01-02,alice,1.00", "2024-01-02,bob,1.00", "2024-01-02,carol,3.00",
]
top_k_per_day(records, 2) -> [
  ("2024-01-01", [("alice", 1000), ("bob", 500)]),
  ("2024-01-02", [("carol", 300), ("alice", 100)]),   # alice 和 bob 都是 1.00，按用户名 alice < bob 进前2
]
```

**例 4**（流式更新 + 退款，四次查询）
```
events = ["alice,10.00", "QUERY", "bob,50.00", "QUERY", "alice,-3.00", "QUERY", "bob,-60.00", "QUERY"]
process_stream(events) -> [
  [("alice", 1000)],
  [("bob", 5000), ("alice", 1000)],
  [("bob", 5000), ("alice", 700)],
  [("alice", 700), ("bob", -1000)],     # bob 退款超过累计购买，总额变负，但仍在 top two 里
]
```

## `main()` 命令流

```
PART 1                          PART 3
N 2                             N 8
alice,10.00                     alice,10.00
bob,5.00                        QUERY
→ alice 1000                    bob,50.00
  bob 500                       QUERY
                                 alice,-3.00
                                 QUERY
                                 bob,-60.00
                                 QUERY
                                 → Q 1
                                   alice 1000
                                   Q 2
                                   bob 5000
                                   alice 1000
                                   Q 2
                                   bob 5000
                                   alice 700
                                   Q 2
                                   alice 700
                                   bob -1000
```

Part 1/2/3 都在没有任何结果时输出一行 `-`。

## 边界清单

- 打平：总额相同按用户名升序（例 1、例 3 都覆盖）
- 只有 0 个或 1 个用户
- 金额格式必须是"整数.两位小数"：`"5"`、`"5.001"`、`"5.1"` 都不合法 → `ValueError`
- Part 1/2 里出现负数金额 → `ValueError`（这两个 part 没有退款概念）
- 记录字段数不对（缺逗号或多逗号）、用户名为空 → `ValueError`
- Part 2 的 `k = 0`
- Part 3 退款可以让总额变成 0 或负数，该用户依然参与排名（例 4 最后一步）
- Part 3 没有任何 `QUERY` 事件 → 输出 `-`（空列表）
- Part 3 在第一次 `QUERY` 之前就查询、或从未有任何购买记录就查询 → 空快照 `[]`
- 全程整数分运算，不能出现浮点数误差（比如很多笔 `0.10` 相加不能因为浮点误差偏出 1 分）

## 追问

1. **为什么不能用 `float(amount)` 再乘 100？** 浮点数不能精确表示大多数十进制小数（`0.1 + 0.2 != 0.3`），大量交易累加后误差会放大到能改变排名。本题直接按字符串位置切分整数部分和两位小数部分，全程整数运算。
2. **金额位数不固定（比如日元没有小数）怎么办？** 把"两位小数"抽成一个参数化的最小货币单位换算规则，本题按 fastprep 原题的美元场景固定两位小数。
3. **Part 3 要不要支持撤销某一次具体的购买（不是净额退款）？** 那需要按事件 id 索引原始金额再做反向操作，本题的退款是"净额调整"，不追溯具体哪一笔。
4. **Top two 换成 top-k？** Part 1 的排序逻辑不变，只是切片长度从 2 换成 k；如果还要求"打平的都算"，参考 pc11 的 top-k 打平规则。
5. **数据量很大，Part 3 每次 QUERY 都要 O(用户数 log 用户数) 排序，能不能优化？** 维护一个大小为 2 的"候选集"或一个按总额排序的堆，更新时只有当受影响用户的名次可能进入/离开 top two 时才重新比较，摊还成本远低于每次全量排序；本题量级不需要这个优化，追问里口头说明思路即可。

## 来源与置信度

- **MED**：https://www.fastprep.io/problems/snowflake-top-two-users-by-total-purchase，Easy，Array/Hash-Table，Phone Screen，最近报告 2026-06。见 `../../../../catalog/raw/coding_phone_onsite.md` #7。
- Part 2（按天分组）、Part 3（流式 + 退款）未见一手报道，按聚合排名类暖场题最常见的追问方向重建，已在题面标注 **(reconstructed)**。

## 考什么

S06（计数/聚合哈希 + 确定性排序 tie-break，与 pc11、pc03 同一类考法）· 货币的整数化处理（绝不能过浮点数）· 流式状态维护与"任意时刻查询"的接口设计。
