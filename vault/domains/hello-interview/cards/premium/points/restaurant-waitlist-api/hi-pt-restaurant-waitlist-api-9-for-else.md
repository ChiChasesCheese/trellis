---
id: hi-pt-restaurant-waitlist-api-9-for-else
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 9
---
## Q
**餐厅候位 API · 循环的 else 子句**｜追问 · 出自：餐厅候位 API › 深入 1

`_drain` 里"找遍整个队伍都没人能坐就结束，否则入座后重新从头找"，用什么 Python 写法最直接？

## A
**写法。** `for ... else`：循环里找到人就入座并 `break`，外层 `while True` 再从头找；循环自然走完（没有 `break`）才进 `else` 返回结果。

```python
else:                      # 整个队伍找遍也没人能坐
    return seated
```
**对比。** 用标志变量要多一个可变状态，每个出口都得记得设置。
