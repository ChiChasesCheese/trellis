---
id: concurrency-depth-deterministic-interleaving
node: concurrency-depth.testing
type: qa
step: 4
---
## Q
先检查后创建的竞态靠压测只能碰概率。怎样写一个每次都稳定复现这个竞态的测试？如果被测代码加了锁，同样的手法又该断言什么？

## A
**在缺口里放一个钩子，用 `Event` 把线程停在那里**

- **思路**：把“检查之后、动作之前”这个缺口变成一个可替换的回调（钩子）。测试让第一个线程停在钩子里，让第二个线程完整跑完，再放第一个线程继续，交错顺序被测试写死了；
- **无锁版本（示例就是它）**：`made` 一定是 2，测试每次都红，确定地证明有竞态；
- **有锁版本**（示例没写）：钩子在临界区里，第二个线程会阻塞在锁上。断言应该是“第二个线程在第一个停住时没有完成”（`join(timeout=0.2)` 之后仍然活着），放行第一个后两个都完成且 `made == 1`；
- **代价**：生产代码要留一个测试用的钩子（或者让测试子类覆盖一个方法）。只给最关键的缺口留；
- **用 `Event` 不用 `sleep`**：`sleep(0.1)` 在忙的机器上不够长，在闲的机器上白等。

```python
import threading
class Reg:
    def __init__(self, gap=lambda: None): self.d, self.gap, self.made = {}, gap, 0
    def get(self, k):
        if k not in self.d:
            self.gap()                           # 测试在这里卡住一个线程
            self.made += 1; self.d[k] = object()
        return self.d[k]
in_gap, go = threading.Event(), threading.Event()
r = Reg(gap=lambda: (in_gap.set(), go.wait()))   # 第一个线程停在缺口里
a = threading.Thread(target=r.get, args=("k",)); a.start()
in_gap.wait(); r.gap = lambda: None              # 第二个线程不再停
r.get("k"); go.set(); a.join()
print(r.made)                                    # 2：每次都重复创建
```

**知识点：**测试并发代码（Testing Concurrency）
