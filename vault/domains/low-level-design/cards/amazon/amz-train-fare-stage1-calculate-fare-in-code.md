---
id: amz-train-fare-stage1-calculate-fare-in-code
node: amazon.amz-train-fare
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 火车票价设计的第 1 关，线路固定为 G→U→H→K→I、相邻站费用 1，用 Python 写出 `calculate_fare(stations, start, stop)`。

## A
**票价是两站位置之差的绝对值**

- **先建位置表**：站名到下标的字典，查一次 O(1)，不用每次在列表里找；
- **方向无关**：上行下行价格一样，所以取绝对值；同站为 0；
- **未知站要报错**：字典查不到抛 `KeyError`，转成语义明确的 `LookupError`，`from None` 去掉内部的异常链；
- **第 1 关只到这里**：每段费用固定为 1，后面几关会加不同票价和换乘，位置表这一步还能复用。

```python
def calculate_fare(stations: list[str], start: str, stop: str) -> int:
    pos = {name: i for i, name in enumerate(stations)}
    try:
        return abs(pos[start] - pos[stop])
    except KeyError as err:
        raise LookupError(f"unknown station {err}") from None
```

例：线路 `["G","U","H","K","I"]` 上，G 到 I 是位置 0 和 4，返回 4；I 到 G 同样是 4；同站返回 0。
