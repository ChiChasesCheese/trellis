---
id: api-parameters-batch
node: api.parameters
type: qa
step: 4
---
## Q
给模型用的 `get_weather(city)` 一次只查一个城市，模型要比较五个城市，就要连续调用五轮，每轮都付一次模型往返的延迟和费用。参数应该怎么设计？

## A
**让一次调用能表达调用方的完整意图**

- **接受列表**：`cities: list[str]`，一次请求全部，服务端并发或批量查询，调用方只付一次往返；
- **返回与输入对应**：结果按输入顺序，每项独立成败，一个城市失败不拖垮其他四个；
- **上限写进合同**：批次最多 N 项，超过就 400，空批次返回 `[]` 而不是报错；
- **不要为了批量牺牲单个调用**：单个调用也能用，只是列表长度为 1；
- **工具要考虑调用者是谁**：给模型的工具，参数描述就是它的说明书，名字和含义要写得清楚；总预算（轮数、调用数）要有上限，到了上限给出明确的错误，而不是无限循环。

```python
def get_weather(cities: list[str]) -> list[dict]:
    if not 0 <= len(cities) <= 20:
        raise ValueError("invalid_batch")
    table = {"sf": 18, "la": 24}
    return [{"city": c, "temp": table[c]} if c in table else {"city": c, "error": "not_found"}
            for c in cities]                         # 按输入顺序，单项失败不影响其他

print(get_weather(["sf", "la", "xx"]))
```

**知识点：**参数设计（Parameters）
