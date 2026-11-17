---
id: parsing-io-regex-shape-vs-meaning
node: parsing-io.regex
type: qa
step: 6
---
## Q
到期日要求是真实存在的 `YYYY-MM-DD`。只用正则 `[0-9]{4}-[0-9]{2}-[0-9]{2}` 够不够？什么情况下干脆不该用正则？

## A
**正则卡形状，意义交给专门的解析器**

- **正则管不了日历**：`2023-02-30` 形状完全对，但不是真实的日子；月份天数、闰年写进正则又长又错；
- **3.11 的 `date.fromisoformat`**：能判断真实日历日，但它也接受 `20230115`、`2023-W01-1` 这类别的 ISO 写法，所以要先用正则卡死定宽的 `YYYY-MM-DD`；
- **顺序**：正则判形状，再 `fromisoformat` 判日期，两步的错误归成同一个；
- **不该用正则的情形**：嵌套结构（括号配对、HTML、JSON）正则表示不了；固定分隔的字段用 `split(", ", 2)` 更清楚；有现成解析器的格式（`csv`、`json`、`urllib.parse`）用库；
- **判断标准**：一个模式写完你自己读不懂，就拆成几步。

```python
import re
from datetime import date

SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")

def parse_day(s: str) -> date:
    if not SHAPE.fullmatch(s): raise ValueError("format")
    return date.fromisoformat(s)                     # 真实日历日，否则 ValueError

print(parse_day("2024-02-29"))                       # 2024-02-29
for bad in ("2023-02-30", "20230115", "2023-W01-1"):
    try: parse_day(bad)
    except ValueError as e: print(bad, e)
```

**知识点：**正则表达式（Regular Expressions）
