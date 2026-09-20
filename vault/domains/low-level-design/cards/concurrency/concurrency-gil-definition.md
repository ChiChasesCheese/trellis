---
id: concurrency-gil-definition
node: concurrency.model
type: qa
step: 1
---
## Q
CPython 的全局解释器锁（GIL，Global Interpreter Lock）到底保证了什么，又没保证什么？

## A
GIL 保证任意时刻只有一个线程在执行 Python 字节码（bytecode），而且解释器不会在**一条**字节码指令的中间切换线程——所以单条字节码是原子的，比如 `d[key] = 1` 这种单一 `STORE_SUBSCR` 操作不会被别的线程看到"改了一半"的中间状态。

它没保证的是：由**多条**字节码组成的操作（几乎所有看起来是"一行代码"的复合操作）不是原子的，线程可以在任意两条字节码之间被切换出去。GIL 保护的是解释器自身不崩溃，不是你的业务不变量；需要跨多步操作保持一致，仍然要靠 `threading.Lock` 自己加锁。
