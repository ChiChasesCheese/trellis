---
id: craft-lock-as-transaction-boundary-3-external-calls
node: craft.architecture.lock-as-transaction-boundary
type: qa
step: 3
---
## Q
**锁即事务边界 · 慢的外部调用放在事务里还是外面**｜架构

幂等转账在占键之后、动钱之前，会调一个外部步骤（风控），它可能很慢；ATM 的取款则在持有机器锁时直接调银行网络。两种写法的区别是什么？各自在什么条件下是对的？

## A
**要点。** 事务越短越好，外部调用（网络、磁盘、第三方）的耗时不受你控制，放进事务就等于让所有等锁的人陪它等。转账把风控放在锁外，只在最后提交时短暂进入临界区。ATM 故意把调用放在锁里，因为一台机器同一时刻只有一个会话和一个出钞口，没有别的操作需要并行，持锁调用换来的是状态机不会被穿插。

```python
lock = threading.Lock()
in_call = threading.Event()
release = threading.Event()

def slow_bank() -> None:                      # 外部调用：网络慢
    in_call.set()
    release.wait()

def withdraw(call_inside_lock: bool) -> None:
    if call_inside_lock:
        with lock:
            slow_bank()               # ATM 的写法：持锁调网络
    else:
        slow_bank()                           # 转账 on_execute 的写法：锁外
        with lock:
            pass                      # 然后短暂进临界区提交

for inside in (True, False):
    in_call.clear(); release.clear()
    t = threading.Thread(target=withdraw, args=(inside,)); t.start()
    in_call.wait()                            # 外部调用正在进行
    got = lock.acquire(timeout=0.2)           # 另一个线程想读余额
    if got: lock.release()
    print("持锁调用" if inside else "锁外调用", "-> 读余额的人能拿到锁:", got)
    release.set(); t.join()
```

实际输出：

```
持锁调用 -> 读余额的人能拿到锁: False
锁外调用 -> 读余额的人能拿到锁: True
```

**易错。** 把外部调用挪到锁外有代价：调用到提交之间状态可能变了，所以提交时要重新检查（转账里 `rec.result is None`、键是否仍属于自己）。

**信号。** 看到临界区里有 `requests.`、`await`、`sleep` 或回调，先问：这里有没有别的线程需要并行？没有，是有意的粗锁；有，就是缺陷。
