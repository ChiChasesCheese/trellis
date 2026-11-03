---
id: craft-idempotency-key-stores-result-1-claim-run-store
node: craft.patterns.idempotency-key-stores-result
type: qa
step: 1
---
## Q
**幂等键存结果 · 为什么「查有没有做过」不是幂等**｜写法

客户端付款超时后会重试同一个请求，三次重试几乎同时到达服务端。服务端写成「`key` 已处理就返回旧结果，否则扣款并记下」。为什么还是可能扣三次？怎样才能保证同一个键只扣一次，而且三个调用方都拿到同一张收据？

## A
**要点。** 幂等（idempotent）的意思是：同一个请求重复提交，效果和提交一次相同，调用方拿到相同的答案。做法是三步：原子占位（第一个到的成为拥有者）→ 只有拥有者执行 → 把结果存下，其余请求等结果。「先查再做」中间有窗口，三个请求都查不到记录。

```python
def pay_naive(key, order):
    if key in done:                 # 三个请求都查不到
        return done[key]
    done[key] = charge(order)       # 三次真的扣款
    return done[key]

def pay(key, order):
    with mu:                        # 原子占位
        slot = slots.get(key)
        owner = slot is None
        if owner:
            slot = slots[key] = Slot()      # Slot: Event + result
    if owner:
        slot.result = charge(order)         # 只有拥有者执行
        slot.event.set()                    # 先存结果，后唤醒
    else:
        slot.event.wait()                   # 等拥有者，不再扣一次
    return slot.result
```

三个线程用同一个键，实际输出：

```
pay_naive 扣款次数 3 返回 ['receipt-1', 'receipt-2', 'receipt-3']
pay 扣款次数 1 返回 ['receipt-1', 'receipt-1', 'receipt-1']
```

**为什么。** 「存结果」不是可选项：重试者需要的是第一次的答案，而不只是「做过了」。

**易错。** 拥有者成功之前，等待者不能直接返回「处理中」当作成功。
