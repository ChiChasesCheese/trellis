---
id: errors-unrecoverable-unknown-outcome
node: errors.unrecoverable
type: qa
step: 4
---
## Q
智能体调用一个不可撤销的工具（比如发邮件），调用发出去以后进程崩了。重启后日志里这次调用是 `pending`，该直接再调一次吗？

## A
**结果未知时先问下游，问不到就停下交给人**

- **顺序**：先写 `pending`，再带幂等键调用，最后写 `done`；崩溃只可能落在三步之间；
- **`pending` 的意思是“不知道做没做”**：可能已经发出去了，只是没来得及记；
- **直接重跑**：邮件发两封，款扣两次；不可撤销的操作最怕这个；
- **恢复的第一步是查询**：向下游或按幂等键问一句结果，再把记录改成 `done` 或 `failed`；
- **查不到就是不可恢复**：抛错、报警、等人处理，不猜。

```python
log = {"call-1": "pending"}                       # 崩溃前留下的

def recover(call_id: str, ask_downstream) -> str:
    if log[call_id] == "pending":
        outcome = ask_downstream(call_id)         # 先问：下游到底做了没有
        if outcome is None:
            raise RuntimeError("outcome unknown: needs a human")
        log[call_id] = "done" if outcome else "failed"
    return log[call_id]

print(recover("call-1", lambda cid: True))        # done
```

**知识点：**不可恢复错误与顶层处理（Crash vs Recover）
