---
id: fluency-strings-ascii-digits
node: fluency.strings-bytes
type: qa
step: 5
---
## Q
信用卡有效期、金额、日期要求“只收 ASCII 数字”。`"٥٥".isdigit()`、`re.match(r"\d+$", "12\n")`、`int("１２")`、`date.fromisoformat("20261117")` 分别会放过什么？该怎么写校验？

## A
**数字校验：先 isascii，正则用 [0-9] 和 fullmatch**

- **`isdigit()` 认各种语言的数字**：阿拉伯文数字、全角数字、上标数字都返回 `True`；`isdecimal()` 只认十进制数字，上标数字就不算；`isnumeric()` 连分数 `½` 也认；三个方法都不等于“只有 ASCII 数字”；
- **加上 `isascii()` 才是 0 到 9**：写成 `s.isascii() and s.isdigit()`；空串的 `isdigit()` 本来就是 `False`，不用另外再挡；
- **正则里的 `\d` 同样会匹配各种语言的数字**：要么写成 `[0-9]`，要么给正则加上 `re.ASCII` 标志；
- **`$` 匹配在结尾换行之前**：`re.match(r"\d+$", "12\n")` 通过；用 `re.fullmatch` 或 `\Z`；
- **`int()` 也宽**：它会接受全角数字、下划线分隔的 `"1_000"`、前后的空白和 `"+5"` 这样的正号，所以转换之前要先把格式卡住；
- **标准库的解析器同样宽松**：3.11 的 `date.fromisoformat` 还接受 `20261117` 这类紧凑写法；要定宽的 `YYYY-MM-DD`，就先用 `[0-9]` 的正则卡住格式，再让它判断这一天是否真的存在，`2026-02-30` 会抛出 `ValueError`。

```python
import re
from datetime import date

DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")

def parse_date(s: str) -> date:
    if not DATE.fullmatch(s):                  # 定宽、ASCII、不容许结尾换行
        raise ValueError("invalid_date")
    return date.fromisoformat(s)               # 再判断这一天是否存在

print("٥٥".isdigit(), ("٥٥".isascii() and "٥٥".isdigit()), int("１２"))   # True False 12
print(bool(re.match(r"\d+$", "12\n")), bool(re.fullmatch(r"[0-9]+", "12\n")))   # True False
print(date.fromisoformat("20261117"))          # 3.11 也收：2026-11-17
for s in ("2026-11-17", "20261117", "2026-02-30"):
    try: print(parse_date(s))
    except ValueError as e: print(s, e)
```

**知识点：**字符串与字节（Strings & Bytes）
