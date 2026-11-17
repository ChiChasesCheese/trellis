---
id: data-optional-missing-is-not-zero
node: data.optional
type: qa
step: 1
---
## Q
活动推荐按“离用户多远”筛选。用户的出发点查不到坐标时，把距离算成 `0` 或者返回一个默认城市，会发生什么？缺失的值该怎么参与判断？

## A
**缺失就是缺失，不能顶替成一个合法的值**

- **缺位置当 0**：距离 0 落在任何半径以内，于是所有活动都“匹配”，而这个用户其实没有出发点；
- **默认值是编造的数据**：悄悄换成默认城市，推荐结果看起来正常，错得没人发现；
- **用 `None` 表示缺失**：参与判断的代码必须显式处理，类型写成 `float | None`，类型检查器会盯着没处理的地方；
- **缺了就按“不匹配”**：合同写明，缺出发点或活动城市没有坐标，这个活动不匹配、不抛异常；
- **来源有优先级时顺序也是合同**：用户分享的位置优先于家所在的城市；前者缺了才用后者。

```python
COORDS = {"sf": (37.8, -122.4), "la": (34.1, -118.2)}

def near(origin: str | None, city: str, radius: float) -> bool:
    if origin not in COORDS or city not in COORDS:       # None 也不在表里
        return False                                      # 缺了就不匹配
    (a, b), (c, d) = COORDS[origin], COORDS[city]
    return ((a - c) ** 2 + (b - d) ** 2) ** 0.5 <= radius

print(near("sf", "la", 10), near(None, "la", 10), near("nowhere", "la", 10))
```

**知识点：**缺失值的表示（Optional & Null）
