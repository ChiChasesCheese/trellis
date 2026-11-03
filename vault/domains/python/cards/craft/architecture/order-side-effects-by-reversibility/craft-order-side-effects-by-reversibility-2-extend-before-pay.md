---
id: craft-order-side-effects-by-reversibility-2-extend-before-pay
node: craft.architecture.order-side-effects-by-reversibility
type: qa
step: 2
---
## Q
**副作用按可逆性排序 · 订座确认时，为什么先延长持有期、再付款**｜架构

订座有 20 分钟持有期（hold）：座位先占住，付款成功才算订到。付款走外部支付网关，不能握着座位锁去调（网关一慢全场卡死）。付款要几秒，持有期又快到了。确认订座的几步该怎么排？

## A
**要点。** 排序看的是失败的代价和窗口：先做代价小、能撤销的（延长持有期；失败就释放），再做外部的（锁外付款），最后做提交（把座位翻成已订）。付款成功到落单之间有个窗口，所以进窗口前先把持有期延到「支付窗口」那么长，让窗口内座位不会过期；万一还是超了，抛一个明确的错误，说明这笔钱要退，而不会覆盖别人已经买到的座位。

```python
class HoldExpired(Exception): ...

class Show:
    """座位持有（hold）有过期时间；支付可能很慢。"""
    def __init__(self) -> None:
        self.hold_until = 10                   # 持有到 t=10
        self.sold = False
    def extend(self, until: int) -> None:
        self.hold_until = max(self.hold_until, until)
    def commit(self, now: int) -> None:
        if now > self.hold_until:
            raise HoldExpired("座位已被释放")
        self.sold = True

def confirm(show: Show, pay_takes: int, extend_first: bool) -> str:
    t = 8                                       # 当前时刻，持有期到 t=10
    if extend_first:
        show.extend(t + 30)                     # 进入支付窗口前，先把持有期延长
    t += pay_takes                              # 支付耗时（锁外）
    try:
        show.commit(t)                          # 过了持有期就抛 HoldExpired
    except HoldExpired:
        return f"钱已付、座位已丢，需要退款（t={t}）"
    return "订座成功"

print("不延长持有期:", confirm(Show(), pay_takes=5, extend_first=False))
print("先延长持有期:", confirm(Show(), pay_takes=5, extend_first=True))
print("延长了，但支付仍超过窗口:", confirm(Show(), pay_takes=40, extend_first=True))
```

支付耗时 5、不延长；耗时 5、先延长；耗时 40、先延长，实际输出：

```
不延长持有期: 钱已付、座位已丢，需要退款（t=13）
先延长持有期: 订座成功
延长了，但支付仍超过窗口: 钱已付、座位已丢，需要退款（t=48）
```

**为什么。** 第三行说明排序不是万能的：窗口再长也有被超过的时候，所以失败路径要求明确（带「需要退款」的消息），而不是假装不会发生。

**信号。** 一个多步操作里有慢的外部调用，并且有个会过期的资源（持有期、租约、令牌）：先续期，再调用。
