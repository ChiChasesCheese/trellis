---
slug: tt-tool-call-success-rate
---
## Q
**工具调用成功率统计**｜Easy

日志每行 `"<timestamp> <tool_name> <status>"`，`status` 为 `SUCCESS` 或 `FAIL`，空行和格式错误的行跳过。一次遍历，返回每个工具的成功率（保留 4 位小数）和失败次数最多的工具名（并列取字典序最小，无失败返回 `""`）。

## A
**一句话。** 两个 `Counter` 记总次数和失败次数，行先解析再计数，失败最多用复合键 `(-失败次数, 工具名)` 取 `min`。

```python
def parse(line):
    match line.split():
        case [ts, tool, "SUCCESS" | "FAIL" as s]:
            if ts.isdecimal():
                return int(ts), tool, s == "SUCCESS"
    return None

def tool_stats(lines):
    total, fails = Counter(), Counter()
    for line in lines:       # 一次遍历
        if (rec := parse(line)) is None:
            continue
        _, tool, ok = rec
        total[tool] += 1
        if not ok:
            fails[tool] += 1
    rates = {t: round((n - fails[t]) / n, 4)
             for t, n in total.items()}
    worst = min(fails, key=lambda t: (-fails[t], t),
                default="")
    return rates, worst
```

**复杂度。** 时间 `O(n)`，空间 `O(m)`（`m` 为工具数）。

**易错点。**
- 空行直接 `ts, tool, status = line.split()`：`"".split()` 是 `[]`，抛 `ValueError`。
- 并列用 `max(fails, key=fails.get)`：返回先出现的键，`["1 b FAIL", "2 a FAIL", "3 a SUCCESS"]` 得 `"b"`，应为 `"a"`。
- 只遍历 `fails` 算成功率：从未失败的工具漏掉。

**追问。**
- 只看最近 1 小时？：`deque` 存窗口内事件，新事件到来先弹出过期的并回退计数，均摊 `O(1)`。
- 时间戳乱序？：`deque` 换成按时间戳排序的堆，弹出条件不变。

**同模式。** LC 692 前 K 个高频单词、LC 811 子域名访问计数、LC 933 最近的请求次数、LC 362 敲击计数器
