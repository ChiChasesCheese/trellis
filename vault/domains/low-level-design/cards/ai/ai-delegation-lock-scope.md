---
id: ai-delegation-lock-scope
node: ai.delegation
type: qa
step: 3
---
## Q
并发服务里“检查余额，再扣款”，为什么锁的范围要自己定、自己核对，而不是让智能体写完就信？

## A
**锁要罩住“检查加写入”整个动作**

- **检查在锁外**：两个线程都通过检查，各自再进锁写，余额变成负数；
- **公开测试通常看不到**：单线程测试里这两种写法的结果一模一样；
- **测试要自己造**：在检查和写入之间加入延迟（或屏障），让线程交错；
- **核对**：打开代码，看 `with lock` 的缩进范围，包不包括条件判断。

```python
import threading, time

class Wallet:
    def __init__(self): self.balance, self.lock = 100, threading.Lock()
    def spend_bad(self, n):
        if self.balance >= n:                 # 检查在锁外
            time.sleep(0.05)
            with self.lock: self.balance -= n
    def spend_ok(self, n):
        with self.lock:                       # 检查和写入同一把锁
            if self.balance >= n:
                time.sleep(0.05); self.balance -= n

def run(name):
    w = Wallet(); ts = [threading.Thread(target=getattr(w, name), args=(80,)) for _ in range(2)]
    [t.start() for t in ts]; [t.join() for t in ts]; return w.balance
print(run("spend_bad"), run("spend_ok"))      # -60 20
```

**知识点：**该交给 AI 还是自己写（When to Delegate）
