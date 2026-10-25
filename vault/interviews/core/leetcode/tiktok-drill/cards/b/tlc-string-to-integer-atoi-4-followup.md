---
id: tlc-string-to-integer-atoi-4-followup
node: b.string-to-integer-atoi
type: qa
step: 4
---
## Q
**LC 8 字符串转换整数 (atoi)**｜追问

面试官接着问：（1）用 C++ / Java 的 32 位 `int` 怎样避免累加时溢出？（2）能不能用正则写得更短，代价是什么？（3）要支持小数、指数（LC 65 有效数字）怎么扩展？

## A
1. **固定位宽**：不能先乘 `10` 再判断，那一步已经溢出。要在乘之前判断：正数 `num > (INT_MAX - d) // 10`，负数 `num > (INT_MAX + 1 - d) // 10`，成立就直接返回边界。卡片里的 `limit` 写法在 64 位整数里等价。
2. **正则版**：`re.match` 一次匹配前导空格、可选符号、至少一位数字，再截断。

```python
import re

def my_atoi_regex(s: str) -> int:
    m = re.match(r" *([+-]?\d+)", s)           # 前导空格、可选符号、至少一位数字
    if m is None:
        return 0
    return max(-(2**31), min(2**31 - 1, int(m.group(1))))
```

对 `"42"`、`" -042"`、`"4193 with words"`、`"0-1"`、`"+-12"`、`"-91283472332"` 与手写版结果一致。代价：把规则藏进了正则，面试官看不到你对边界的掌控；`\d` 在 Python 的 `str` 模式里默认匹配所有 Unicode 十进制数字，要严格 ASCII 需写 `[0-9]` 或加 `re.ASCII`。
3. **有效数字（LC 65）**：同样是状态机，状态变多（符号、整数部分、小数点、小数部分、指数符号、指数部分），用转移表 `状态 -> {字符类别: 下一个状态}`，逐字符查表，最终状态属于接受集合才算合法。

**Python 提醒**：`str.isdigit()` 对 `"²"`、`"١٢"` 都返回 `True`，`int("١٢")` 还会得到 `12`；解析外部输入时用 `"0" <= ch <= "9"` 或 `ch in string.digits`，不要用 `isdigit()`。
