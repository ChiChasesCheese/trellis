---
id: parsing-io-parse-errors-position
node: parsing-io.parse-errors
type: qa
step: 5
---
## Q
一份多行配置解析失败时，只报「格式错误」，使用者要在几百行里自己找。错误里应该带什么信息？行号和列号怎么算？

## A
**错误带位置：行、列、原因，三样都要**

- **原因用一句话**：写成「期望什么、看到什么」（`Expecting value`），比 `bad syntax` 有用；
- **位置**：解析器内部记的是字符偏移（`pos`）；报错时再换算成「第几行第几列」，不要在每个字符上都维护行列；
- **换算**：行号是偏移之前的换行数加 1；列号是偏移减去最近一个换行之后的位置，也从 1 起；
- **标准库已经做了**：`json.JSONDecodeError` 带 `msg`、`pos`、`lineno`、`colno`；自己写的解析器照这个形状抛，调用方换解析器时不用改错误处理；
- **别泄露**：位置和原因可以展示，被拒绝的原始内容（可能含密钥）不要整段放进错误信息。

```python
import json

def locate(text: str, pos: int) -> tuple[int, int]:
    line = text.count("\n", 0, pos) + 1
    col = pos - (text.rfind("\n", 0, pos) + 1) + 1
    return line, col

text = '{"a": 1,\n "b": }'
try: json.loads(text)
except json.JSONDecodeError as e:
    print(e.lineno, e.colno, e.msg)                       # 2 7 Expecting value
    print(locate(text, e.pos) == (e.lineno, e.colno))     # True
```

**知识点：**解析错误（Parse Errors）
