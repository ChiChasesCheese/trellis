---
id: tlc-tt-tool-call-success-rate-2-code
node: b.tt-tool-call-success-rate
type: qa
step: 2
---
## Q
**工具调用成功率统计**｜写出 Python 实现

`tool_stats(lines)`：`lines` 是日志行的可迭代对象（至多 `10^6` 行），每行 `"<timestamp> <tool_name> <status>"`，`status` 是 `SUCCESS` 或 `FAIL`，空行和格式错误的行跳过。返回每个工具的成功率（保留 4 位小数）和失败最多的工具名（并列取字典序最小，无失败返回 `""`），一次遍历。

## A
**思路。** `parse` 用结构化模式匹配一次校验“恰好三个字段、状态是两个字面量之一、时间戳是整数”；主循环用两个 `Counter` 累计；最后统一算比率，并用复合键取失败最多的工具。

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

运行：`["100 search SUCCESS", "101 search FAIL", "", "102 calc FAIL", "bad line", "103 calc FAIL", "104 search SUCCESS", "105 db SUCCESS", "106 db FAIL"]` → `({'search': 0.6667, 'calc': 0.0, 'db': 0.5}, 'calc')`；`[]` → `({}, '')`；`["1 a SUCCESS", "2 b SUCCESS"]` → `({'a': 1.0, 'b': 1.0}, '')`；`["1 b FAIL", "2 a FAIL", "3 a SUCCESS"]` → `({'b': 0.0, 'a': 0.5}, 'a')`；`parse("100 a success")`（小写状态）、`parse("-5 a FAIL")`、`parse("1.5 a FAIL")` 都是 `None`。

**复杂度。** 时间 `O(n)`，每行一次 `split` 加常数次计数；空间 `O(m)`，`m` 为不同工具的个数。

**写法要点。** `match line.split()` 的序列模式同时检查字段数，`"SUCCESS" | "FAIL" as status` 检查取值并绑定，`if ts.isdecimal()` 是守卫，比手写 `len` 加多个 `if` 清楚；`split()` 不带参数，能容忍多余空白；`(rec := parse(line)) is None` 用海象避免先赋值再判断；`Counter` 对不存在的键读出 `0`，所以 `fails[tool]` 可以直接读；`min(..., default="")` 处理空 `fails`；参数类型写 `Iterable[str]`，文件对象和生成器都能直接传入，不必先 `readlines()`。
