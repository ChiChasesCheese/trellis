---
id: fsm-illegal-transitions-no-trace
node: fsm.illegal-transitions
type: qa
step: 4
---
## Q
重置码校验失败（错码、已过期）时，服务该不该清掉记录、让码作废？过期这件事要不要存成一个状态？

## A
**失败不改任何东西，过期用时间算出来**

- **失败不留痕**：错码不消耗有效的码，否则别人猜一次就能让你的码失效；
- **过期现算**：库里只存创建时间，校验时用当前时间减去它；存一个 `expired` 标志，要有人在到点时去改，漏改就是缺陷；
- **半开区间**：年龄满足 `0 <= 年龄 < 30` 才有效，恰好 30 秒已过期，所有比较写成同一种形式；
- **成功才清**：校验成功后再清记录，同一个码重放得到 `False`。

```python
class Reset:
    def __init__(self): self.rec = None
    def request(self, code, now): self.rec = (code, now)
    def redeem(self, code, now):
        if self.rec is None: return False
        c, made = self.rec
        if code != c or not 0 <= now - made < 30: return False   # 失败：不动 rec
        self.rec = None; return True                             # 成功：清掉

r = Reset(); r.request("123456", 0)
print(r.redeem("000000", 5), r.redeem("123456", 29), r.redeem("123456", 29))
# False True False：错码不消耗；29 秒成功；重放失败
r.request("777777", 100); print(r.redeem("777777", 130), r.rec)
# False ('777777', 100)：恰好 30 秒已过期，记录还留在库里
```

<details class="pt"><summary>延伸</summary>

过期的记录留在库里，直到被新请求替换，这符合“过期是算出来的，不是改写出来的”：没有任何地方需要在到点时去改它。

</details>

**知识点：**非法转移与幂等（Illegal Transitions）
