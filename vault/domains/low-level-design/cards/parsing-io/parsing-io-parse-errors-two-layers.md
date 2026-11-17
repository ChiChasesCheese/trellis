---
id: parsing-io-parse-errors-two-layers
node: parsing-io.parse-errors
type: qa
step: 2
---
## Q
退货服务每行读一个 JSON 请求。一行是 `{"rating": 9, `（既被截断，`rating` 也超范围），另一行是 `{"rating": 9}`。两行应该分别报什么错？为什么要分两个错误类？

## A
**语法错与策略错分两层，语法先于策略**

- **语法层**：文本是不是合法的（子集）JSON；错误固定为 `invalid_json`；
- **策略层**：字段齐不齐、类型和范围对不对；错误是 `invalid_request`；
- **顺序**：先解析再评估；截断的那一行语法就过不了，评估根本没有机会运行，所以报 `invalid_json`；
- **两个类互不继承**：只共享 `ValueError` 这个祖先；调用方按类分流，不会因为 `except InvalidJson` 误抓到策略错；
- **错误码是固定字符串**：不夹带内部细节，也不把库的原始报错抛给调用方。

```python
import json
class InvalidJson(ValueError): pass
class InvalidRequest(ValueError): pass
def parse(line):                                  # 语法层
    try: return json.loads(line)
    except ValueError: raise InvalidJson("invalid_json") from None
def evaluate(obj):                                # 策略层
    r = obj.get("rating") if isinstance(obj, dict) else None
    if type(r) is not int or not 1 <= r <= 5: raise InvalidRequest("invalid_request")
    return "ok"
def process(line):
    try: return evaluate(parse(line))
    except (InvalidJson, InvalidRequest) as e: return str(e)

print(process('{"rating": 9, '), process('{"rating": 9}'), process('{"rating": 4}'))
```

**知识点：**解析错误（Parse Errors）
