---
id: craft-validate-then-commit-4-same-lock
node: craft.patterns.validate-then-commit
type: qa
step: 4
---
## Q
**先校验后提交 · 多线程下校验和提交为什么必须在同一把锁里**｜模式

`withdraw` 先检查余额够不够，通过后再扣钱。单线程下它满足「先校验后提交」。两个线程各取 80，余额 100，会发生什么？校验写得再严格也救不了吗？

## A
**要点。** 救不了。「先校验后提交」只保证单个调用内部不留半截状态；多线程下，两个调用都通过校验，再各自提交，校验结果在提交前已经过期。要让校验和提交之间插不进别的线程，二者必须在同一个临界区（critical section）。

```python
bal = {"a": 100}

def withdraw(amount: int, locked: bool, lock=threading.Lock()) -> str:
    def body() -> str:
        if bal["a"] < amount:        # 校验
            return "拒绝"
        time.sleep(0.01)             # 模拟被调度走
        bal["a"] -= amount           # 提交
        return "成功"
    if locked:
        with lock:                   # 同一把锁包住校验+提交
            return body()
    return body()

for locked in (False, True):
    bal["a"] = 100
    out: list[str] = []
    ts = [threading.Thread(target=lambda: out.append(withdraw(80, locked))) for _ in range(2)]
    [t.start() for t in ts]; [t.join() for t in ts]
    print("同一把锁包住校验+提交:" , locked, out, "余额", bal["a"])
```

两个线程各取 80，余额 100，实际输出：

```
同一把锁包住校验+提交: False ['成功', '成功'] 余额 -60
同一把锁包住校验+提交: True ['成功', '拒绝'] 余额 20
```

**易错。** 只给提交段加锁、校验放在锁外，等于没锁。需要同时改多个账户时，还要按固定顺序加多把锁（见有序加锁）。
