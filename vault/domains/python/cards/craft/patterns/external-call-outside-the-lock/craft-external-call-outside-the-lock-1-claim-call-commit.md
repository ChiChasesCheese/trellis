---
id: craft-external-call-outside-the-lock-1-claim-call-commit
node: craft.patterns.external-call-outside-the-lock
type: qa
step: 1
---
## Q
**外部调用不持锁 · 为什么付款不能放在库存锁里**｜模式

下单要扣库存、再调支付网关。最直白的写法：拿库存锁，调网关，成功就扣库存，放锁。网关某次要 300 毫秒，会对其它只想读库存的请求造成什么影响？怎么拆？

## A
**要点。** 锁保护的是内存里的一致性，应该只持有微秒级；网络调用的耗时由别人决定。三段式：锁内占位（先把东西预留下来）→ 锁外调用外部 → 锁内提交结果。

```python
import threading, time

lock = threading.Lock()
stock = {"sku": 5}

def slow_gateway() -> None:
    time.sleep(0.3)                       # 支付网关这次很慢

def buy_call_in_lock() -> None:
    with lock:
        slow_gateway()                    # 持锁调外部
        stock["sku"] -= 1

def buy_claim_call_commit() -> None:
    with lock:
        if stock["sku"] <= 0:             # 占位
            return
        stock["sku"] -= 1
    slow_gateway()                        # 锁外调用

def peek() -> float:
    t0 = time.perf_counter()
    with lock:
        _ = stock["sku"]                  # 一次读库存，本来应该微秒级
    return time.perf_counter() - t0

for fn in (buy_call_in_lock, buy_claim_call_commit):
    stock["sku"] = 5
    t = threading.Thread(target=fn)
    t.start(); time.sleep(0.05)           # 让它先拿到锁
    print(f"{fn.__name__}: 另一个线程读库存等了 {peek():.1f}s")
    t.join()
```

一个线程在调网关（0.3 秒）时，另一个线程读库存等待了多久，实际输出（等待时间随机器略有浮动）：

```
buy_call_in_lock: 另一个线程读库存等了 0.2s
buy_claim_call_commit: 另一个线程读库存等了 0.0s
```

**为什么。** 持锁调外部会把一个慢依赖变成全系统的停摆（排队的线程、持有连接、级联超时）。

**代价。** 占位之后到提交之前有窗口：占位必须可恢复（有过期、能撤销），否则支付失败或进程挂了，东西就永远被占着（见下一张卡）。
