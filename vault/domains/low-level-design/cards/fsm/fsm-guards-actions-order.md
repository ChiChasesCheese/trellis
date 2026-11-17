---
id: fsm-guards-actions-order
node: fsm.guards-actions
type: qa
step: 2
---
## Q
转移的动作会调用外部支付接口，可能失败。先把状态改成“已支付”再调接口，还是先调接口再改状态？

## A
**动作成功之后再提交状态**

- **先改状态**：接口调用失败时，状态已经是“已支付”，实际没有支付；之后没有任何事件会再去支付；
- **先动作后状态**：接口失败，状态保持原样，调用方可以重试同一个事件；
- **仍然有缝**：动作成功、写状态之前崩溃，重试会把动作再做一次，所以动作本身要幂等（用幂等键），或者和状态写入放在同一个事务里；
- **纯内存的动作**：算出新状态，执行动作，最后一次性赋值，中间任何一步失败，对象都没变。

```python
class Order:
    def __init__(self): self.state = "pending"
    def pay_bad(self, charge):
        self.state = "paid"; charge()                  # 先改状态
    def pay_ok(self, charge):
        charge(); self.state = "paid"                  # 动作成功再提交

def down(): raise RuntimeError("gateway down")
for method in ("pay_bad", "pay_ok"):
    o = Order()
    try: getattr(o, method)(down)
    except RuntimeError: pass
    print(method, o.state)                             # pay_bad paid / pay_ok pending
```

**知识点：**守卫、动作和进出钩子（Guards, Actions, Hooks）
