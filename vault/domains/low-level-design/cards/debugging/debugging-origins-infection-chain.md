---
id: debugging-origins-infection-chain
node: debugging.failure-origins
type: qa
step: 1
---
## Q
“即将开演”列表里出现了一周前就演完的场次。你应该盯着哪一行？为什么报错（或错误结果）出现的地方，往往不是缺陷所在的地方？

## A
**缺陷 → 感染 → 失败：从错的结果往回找第一个出错的状态**

- **缺陷（defect）**：代码里写错的那一处；
- **感染（infection）**：缺陷执行后，程序状态第一次不对（某个变量的值错了）；
- **失败（failure）**：错误状态一路传播，到你看得见的地方才表现出来（列表里多了不该有的项）；
- **所以追踪的方向是倒着走**：从失败处的错值出发，问“这个值从哪来”，每走一步检查“这里的值对不对”，第一个不对的状态就紧挨着缺陷；
- **失败处的代码经常是对的**：过滤逻辑没有错，只是收到了错的输入；在失败处打补丁，缺陷还在，别的调用者还会中招。

```python
from datetime import date

def days_until(show, today):
    return abs((show - today).days)             # 缺陷：abs 把 -7（已过去）变成 7

def upcoming(shows, today, horizon=7):
    return [s for s in shows if days_until(s, today) <= horizon]

today = date(2026, 11, 17)
shows = [date(2026, 11, 10), date(2026, 11, 20)]
print(upcoming(shows, today))                   # 失败：包含 11 月 10 日
print([days_until(s, today) for s in shows])    # [7, 3]：感染：第一个应是 -7
```

追到的第一个错值是 `days_until` 的返回值；缺陷就在产生它的那一行，`upcoming` 本身没有错。

**知识点：**追踪失败源头（Tracking Failure Origins）
