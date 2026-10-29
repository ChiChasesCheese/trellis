---
id: tlc-tt-tool-call-success-rate-3-why
node: a.tt-tool-call-success-rate
type: qa
step: 3
---
## Q
**工具调用成功率统计**｜正确性

“失败最多、并列取字典序最小”为什么写成 `min(fails, key=lambda t: (-fails[t], t))`？格式错误的行为什么要整行丢弃，只取前三个字段会错在哪里？

## A
**不变量。** 处理完前 `i` 行后：`total[t]` 等于前 `i` 行中工具 `t` 的**合法**行数，`fails[t]` 等于其中状态为 `FAIL` 的行数；`fails` 的键一定是 `total` 的键的子集，所以成功率的分母不会是 `0`。

**复合键。** 元组按字典序比较：先比 `-fails[t]`，次数大的（负数更小）排前；次数相同再比名字，字典序小的排前。`min` 取最前面的那个，一次表达两条规则。

**反例一：用 `max(fails, key=fails.get)`。** 并列时 `max` 返回遍历顺序里先出现的键。日志 `["1 b FAIL", "2 a FAIL", "3 a SUCCESS"]` 里 `b`、`a` 各失败 1 次，`fails` 的插入顺序是 `b`、`a`，`max` 得到 `"b"`；复合键得到 `"a"`，符合“字典序最小”。

**反例二：坏行只取前三个字段。** 日志 `["105 db SUCCESS", "106 db FAIL", "107 db FAIL x"]` 的第三行有 4 个字段，是格式错误的行。写成 `ts, tool, status = line.split()[:3]` 会把它当作一次失败，`db` 的成功率变成 `1/3 = 0.3333`；整行丢弃得到 `1/2 = 0.5`。同理，字段数不足的行（如 `"108 search"`）如果补默认值也会污染计数。

**为什么用 `fails` 里的键取最大。** `fails` 只含失败过的工具，所以没有任何失败时 `fails` 为空，`min` 靠 `default=""` 返回空字符串；从未失败的工具即使在 `total` 里也不可能被选中。
