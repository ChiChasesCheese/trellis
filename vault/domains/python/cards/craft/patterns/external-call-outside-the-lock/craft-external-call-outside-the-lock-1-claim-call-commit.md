---
id: craft-external-call-outside-the-lock-1-claim-call-commit
node: craft.patterns.external-call-outside-the-lock
type: qa
step: 1
---
## Q
**外部调用不持锁 · 为什么付款不能放在库存锁里**｜写法

下单要扣库存、再调支付网关。最直白的写法：拿库存锁，调网关，成功就扣库存，放锁。网关某次要 300 毫秒，会对其它只想读库存的请求造成什么影响？怎么拆？

## A
**要点。** 锁保护的是内存里的一致性，应该只持有微秒级；网络调用的耗时由别人决定。三段式：锁内占位（先把东西预留下来）→ 锁外调用外部 → 锁内提交结果。

```python
def buy_call_in_lock():
    with lock:
        slow_gateway()                # 持锁调外部：别人全在排队
        stock["sku"] -= 1

def buy_claim_call_commit():
    with lock:
        if stock["sku"] <= 0:         # 占位
            return
        stock["sku"] -= 1
    slow_gateway()                    # 锁外调用
```

一个线程在调网关时，另一个线程读库存等待了多久，实际输出：

```
buy_call_in_lock: 另一个线程读库存等了 0.2s
buy_claim_call_commit: 另一个线程读库存等了 0.0s
```

**为什么。** 持锁调外部会把一个慢依赖变成全系统的停摆（排队的线程、持有连接、级联超时）。

**代价。** 占位之后到提交之前有窗口：占位必须可恢复（有过期、能撤销），否则支付失败或进程挂了，东西就永远被占着（见下一张卡）。
