---
id: fsm-illegal-transitions-three-policies
node: fsm.illegal-transitions
type: qa
step: 1
---
## Q
订票服务收到“取消”，但这个预订已经是已取消，或者已经完成。该报错、忽略，还是当成成功？按什么标准选？

## A
**重复到同一结果：幂等；自相矛盾：拒绝**

- **幂等**：事件要把状态带到它已经在的状态，返回和第一次相同的结果，副作用不再发生，名额只释放一次；
- **拒绝**：事件和当前状态矛盾（取消一个已完成的预订），抛明确的错，调用方应当知道；
- **忽略**：悄悄不处理，只适合调用方不可能关心的事件（例如重复的心跳）；对会改变业务结果的事件忽略等于吞错；
- **为什么幂等重要**：网络重试会把同一个请求发两次，调用方收到超时后会再发。

```python
class Reservation:
    def __init__(self, state="active"): self.state, self.free_slots = state, 0

    def cancel(self):
        if self.state == "cancelled": return self.state        # 重复：同样的结果
        if self.state != "active": raise ValueError(f"cannot cancel {self.state}")
        self.state = "cancelled"; self.free_slots += 1         # 只释放一次
        return self.state

r = Reservation(); r.cancel(); r.cancel()
print(r.state, r.free_slots)                                   # cancelled 1
try: Reservation("completed").cancel()
except ValueError as e: print(e)                               # cannot cancel completed
```

**知识点：**非法转移与幂等（Illegal Transitions）
