---
id: tlc-tt-tool-call-success-rate-0-whole
node: a.tt-tool-call-success-rate
type: qa
---
## Q
**工具调用成功率统计**｜Easy · TikTok 高频

给定一串工具调用日志，每条是一行字符串 `"<timestamp> <tool_name> <status>"`，字段以空白分隔：`timestamp` 是非负整数（秒），`status` 是 `SUCCESS` 或 `FAIL`。日志里可能有空行或格式错误的行（字段数不是 3、`status` 不是这两个值、`timestamp` 不是整数），要跳过。返回两样东西：每个工具的成功率（成功次数 / 总调用次数，保留 4 位小数），以及失败次数最多的工具名（并列取字典序最小；没有任何失败则返回空字符串）。日志行数 `n <= 10^6`，要求一次遍历、`O(n)` 时间。

例：日志 `["100 search SUCCESS", "101 search FAIL", "", "102 calc FAIL", "bad line", "103 calc FAIL", "104 search SUCCESS", "105 db SUCCESS", "106 db FAIL"]` → 成功率 `{"search": 0.6667, "calc": 0.0, "db": 0.5}`，失败最多的是 `"calc"`（2 次）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 一次遍历，用两个 `Counter` 记每个工具的总次数和失败次数；每行先解析，不合法就跳过；最后用 `(总数 - 失败) / 总数` 算成功率，用复合键 `(-失败次数, 工具名)` 取 `min` 得到“失败最多、并列取字典序最小”的工具。

**识别。** 「按名字分组统计 + 比率 + 取最大且并列有规则」是**哈希计数**（frequency counting）；`n` 到 `10^6` 说明只能扫一遍，不能先收集工具名再对每个工具重扫（`O(n · 工具数)`），也不用排序。真正的细节在两处：解析（空行、坏行）和并列规则。

**推导。** 暴力：先扫一遍收集工具名，再对每个工具扫全日志数成功和失败，`O(n · 工具数)`。浪费：每一行只影响一个工具的两个计数。洞察：读一行就更新那个工具的 `total` 和 `fails`，每行 `O(1)`；最后只对工具数量做一次除法。并列取字典序最小：把比较键写成 `(-失败次数, 名字)`，一次 `min` 同时表达“次数大的优先、名字小的优先”。

```python
from collections import Counter
from collections.abc import Iterable


def parse(line: str) -> tuple[int, str, bool] | None:
    """合法行返回 (时间戳, 工具名, 是否成功)，空行和格式错误的行返回 None。"""
    match line.split():
        case [ts, tool, "SUCCESS" | "FAIL" as status] if ts.isdecimal():
            return int(ts), tool, status == "SUCCESS"
        case _:
            return None


def tool_stats(lines: Iterable[str]) -> tuple[dict[str, float], str]:
    total: Counter[str] = Counter()
    fails: Counter[str] = Counter()
    for line in lines:                              # 一次遍历，lines 可以是文件对象或生成器
        if (rec := parse(line)) is None:
            continue
        _, tool, ok = rec
        total[tool] += 1
        if not ok:
            fails[tool] += 1
    rates = {tool: round((n - fails[tool]) / n, 4) for tool, n in total.items()}
    worst = min(fails, key=lambda t: (-fails[t], t), default="")   # 失败最多；并列取字典序最小
    return rates, worst
```

运行：上面的例子 → `({'search': 0.6667, 'calc': 0.0, 'db': 0.5}, 'calc')`；`[]` → `({}, '')`；只有成功的日志 `["1 a SUCCESS", "2 b SUCCESS"]` → `({'a': 1.0, 'b': 1.0}, '')`；`["1 b FAIL", "2 a FAIL", "3 a SUCCESS"]` → `({'b': 0.0, 'a': 0.5}, 'a')`（`a`、`b` 各失败 1 次，取字典序小的 `a`）。

**复杂度。** 时间 `O(n)`，每行 `split` 和计数都是常数；空间 `O(m)`，`m` 是不同工具的个数；输入是迭代器时不需要把日志全读进内存。

**易错点。**
- 空行直接写 `ts, tool, status = line.split()`：`"".split()` 是 `[]`，抛 `ValueError`，整个统计崩溃；要用模式匹配或先判断字段数。
- 并列用 `max(fails, key=fails.get)`：并列时返回先出现的键。`["1 b FAIL", "2 a FAIL", "3 a SUCCESS"]` 得到 `"b"`，正确是 `"a"`。
- 只遍历 `fails` 算成功率会漏掉从未失败的工具：`["1 a SUCCESS", "2 b FAIL"]` 里 `a` 的成功率 `1.0` 必须在结果里。
- `round` 对恰好落在中点的值向偶数舍入：`1` 次成功、`31` 次失败的工具是 `1/32 = 0.03125`，`round(1 / 32, 4)` 得 `0.0312`，而“四舍五入”的习惯结果是 `0.0313`；要严格四舍五入时用 `Decimal(...).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)`，面试时先问清规则。

**追问。**
- 日志流式到达、随时查询：两个 `Counter` 本来就是增量更新，`add` 一行 `O(1)`，查某工具的成功率 `O(1)`，查失败最多的工具扫一遍 `O(m)`（`m` 很大时用带懒删除的堆）。
- 只看最近 1 小时：用 `deque` 保存窗口内的事件，新事件到来先把 `时间戳 <= 现在 - 3600` 的从队首弹出并回退计数，每个事件进出各一次，均摊 `O(1)`。
- 时间戳可能乱序：`deque` 要换成按时间戳排序的结构（堆），弹出条件不变。

**同模式。** LC 692 前 K 个高频单词、LC 811 子域名访问计数、LC 819 最常见的单词、LC 933 最近的请求次数、LC 362 敲击计数器。
