---
id: amz-dag-runner-parallel-failure-skips-descendants
node: amazon.amz-dag-runner
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon DAG 执行器里，线程池并行执行时一个步骤失败，怎样只取消它的后代？调度状态怎样避免竞态？

## A
调用线程是唯一调度者：wait(FIRST_COMPLETED) 后由它更新入度表和结果，worker 只跑 fn，状态无需加锁。失败时 skipped |= descendants(name)，之后别的分支把后代入度减到 0 也被 skipped 挡住，不提交；无关分支照常完成。

```python
while running:
    done, _ = wait(running, return_when=FIRST_COMPLETED)
    for fut in done:
        name = running.pop(fut)
        if fut.exception() is not None:
            skipped |= graph.descendants(name)
            continue
        results[name] = fut.result()
        for nxt in graph.users(name):
            left[nxt] -= 1
            if left[nxt] == 0 and nxt not in skipped:
                submit(nxt)
```
