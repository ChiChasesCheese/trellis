---
id: pl-conc-structured-pitfall-orphan
node: concurrency.structured-concurrency
type: qa
step: 10
---
## Q
在请求处理函数里用「发射后不管」启动后台任务，失败时会怎样？结构化并发还有哪些做不到的地方？

## A
Python 里这样写：
```python
async def boom():
    await asyncio.sleep(0.05)
    raise RuntimeError("lost in the background")

async def handler():
    asyncio.create_task(boom())      # fire and forget
    return "response sent"
```
运行结果：处理函数照常返回 `response sent`，`main finished normally`，只在垃圾回收时往 stderr 打一行 `Task exception was never retrieved ... RuntimeError: lost in the background`。调用方得到“成功”，真正的失败只出现在日志里（如果有人看日志的话）。生产里这类错误会表现为：邮件没发出、缓存没更新、审计记录丢失，而请求都显示成功。

Go 的 `go func() { ... }()` 同样：panic 会让整个进程崩溃，错误返回值则被默默丢弃；Java 裸线程里的异常只打印栈。

结构化并发**修补不了**的问题：
1. **不可取消的阻塞**：子任务卡在一个不响应取消的同步调用里（无超时的网络读、持锁、死循环），作用域会一直等它，整个请求被拖住。每个阻塞点要有超时或可中断。
2. **作用域太大**：把所有子任务放进一个根作用域，一个失败全体陪葬；要按故障域划分，独立的子系统各用各的作用域。
3. **跨请求的后台工作**：必须异步、可重试的任务（发邮件）不该靠请求内的 fire-and-forget，应该写进队列（消息队列、数据库表）交给独立的 worker，这样才有持久性和重试。
4. **取消不等于回滚**：被取消的任务可能做了一半，需要幂等或补偿。
