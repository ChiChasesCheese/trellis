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
票价就是两站位置之差的绝对值（每个区间 1）：

```python
def calculate_fare(stations: list[str], start: str, stop: str) -> int:
    pos = {name: i for i, name in enumerate(stations)}
    try:
        return abs(pos[start] - pos[stop])
    except KeyError as err:
        raise LookupError(f"unknown station {err}") from None
```

例：stations=["G","U","H","K","I"]，G 到 I 位置 0 和 4，返回 4；I 到 G 同样 4；同站返回 0。
