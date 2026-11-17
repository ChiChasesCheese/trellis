---
id: fsm-persistence-replay-side-effects
node: fsm.persistence
type: qa
step: 4
---
## Q
崩溃重启后，靠事件日志重放恢复状态。重放时，“给用户发通知”这类副作用会再发一遍吗？怎么避免？

## A
**重放要么不执行副作用，要么靠幂等键去重**

- **重放不等于首次执行**：状态可以重算，已经发出去的邮件、已经调过的接口不能再来一次；
- **至少一次投递**：崩溃会让一条事件被处理不止一次，系统设计成“允许重复，接收端去重”，是更常见、也更容易做对的取舍（设计判断）；
- **去重键**：每个事件一个稳定的编号（或“用户加电影编号”这类业务键），已处理的编号和状态一起持久化；
- **处理记录要和状态在同一事务里写**，否则又回到“扣了没标记”的问题。

```python
log = [{"id": "e1", "kind": "disburse"}]
sent, done = [], set()                                 # done 要和状态一起持久化

def deliver(ev):
    if ev["id"] in done: return                        # 幂等键：重放不再发
    sent.append(ev["id"]); done.add(ev["id"])

for _ in range(2):                                     # 崩溃重启，再重放一遍
    for ev in log: deliver(ev)
print(sent)                                            # ['e1']
```

**知识点：**持久化与恢复（Persistence & Resume）
