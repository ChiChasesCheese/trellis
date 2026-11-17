---
id: concurrency-depth-aba
node: concurrency-depth.atomics
type: qa
step: 2
---
## Q
CAS 只比较“值是否还是我读到的那个”。值从 100 被改成 50 又改回 100，CAS 会成功，这为什么可能出问题？怎么挡住？

## A
**值相同不代表没人动过：给值配一个只增不减的版本号**

- **ABA 问题**：线程 1 读到 A（100），期间别的线程把它改成 B（50）再改回 A，线程 1 的 CAS 看到还是 A，成功；但中间发生的事（扣费、审计记录、释放了资源）线程 1 并不知道，它基于旧状态做的决定已经过期；
- **对策**：每次写入版本号加一，CAS 同时比较值和版本。示例里值回到 100，版本已经是 2，带版本的 CAS 失败；
- **什么时候真有害**：基于值做了别的决定（“余额是 100，所以可以放行”）。只是把计数加一的话，ABA 无害，因为结果只依赖当前值；
- **Python 里的另一个形式**：保存 `id(obj)` 当“同一个对象”的凭证。对象被回收后，新对象很容易拿到同一个地址：实测 1000 次 `del` 后新建同类型的列表，`id` 相同 1000/1000 次；要比较身份，把对象本身（或弱引用）留着，别只存 `id`；
- **数据库里**：`ver` 列、更新时间戳、`ETag`，都是同一个想法。

```python
import threading
class Cell:
    def __init__(self, v): self._v, self._ver, self._l = v, 0, threading.Lock()
    def read(self):
        with self._l: return self._v, self._ver
    def cas(self, exp, new, ver=None):          # ver 给了就连版本一起比
        with self._l:
            if self._v != exp or (ver is not None and self._ver != ver): return False
            self._v, self._ver = new, self._ver + 1
            return True
def scenario(use_version):
    c = Cell(100); v, ver = c.read()
    c.cas(100, 50); c.cas(50, 100)               # 期间别人扣了又补回
    return c.cas(v, 130, ver if use_version else None)
print(scenario(False), scenario(True))           # True False
```

**知识点：**原子操作与无锁（Atomics & Lock-Free）
