---
id: fsm-guards-actions-clock-guard
node: fsm.guards-actions
type: qa
step: 4
---
## Q
有效期这类守卫要读当前时间。直接在函数里调 `time.time()` 有什么问题？怎么写才能测出边界？

## A
**时钟注入进去，边界取三点**

- **直接读系统时钟**：测试没法让时间停在“恰好 30 秒”，只能 `sleep`，又慢又不稳；
- **注入**：构造时传入一个返回当前时间的函数，生产用 `time.time`，测试传假的；
- **一个守卫一种比较写法**：半开区间 `0 <= 年龄 < 30`，写成一个有名字的函数，规则只出现一次；
- **三点**：29.9 秒有效、30 秒无效、负年龄（时钟回拨）无效。

```python
class Reset:
    TTL = 30
    def __init__(self, clock): self.clock, self.made = clock, None
    def issue(self): self.made = self.clock()
    def fresh(self):                                       # 守卫：只读，不改状态
        return self.made is not None and 0 <= self.clock() - self.made < self.TTL

now = [100.0]
r = Reset(lambda: now[0]); r.issue()
for t in (100.0, 129.9, 130.0, 99.0):
    now[0] = t; print(t, r.fresh())
# 100.0 True / 129.9 True / 130.0 False / 99.0 False
```

**知识点：**守卫、动作和进出钩子（Guards, Actions, Hooks）
