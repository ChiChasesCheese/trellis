---
id: debugging-reproduce-two-instances
node: debugging.reproduce
type: qa
step: 4
---
## Q
用户说“保存以后，服务重启就丢数据”，但你的单元测试写完数据立刻读，全是绿的。为什么测试没抓到？该怎么写才能复现？

## A
**“重启后丢数据”要用两个实例复现：写完关掉，再开一个新的读**

- **同一个实例读得到自己没提交的数据**：事务内的写入对本连接可见，对别的连接不可见；单实例测试永远看不出问题；
- **新实例才是“重启”的等价物**：新对象、新连接、同一个存储位置（文件路径），什么内存状态都不带；
- **同样的思路用于缓存和内存状态**：缺陷藏在“内存里有、存储里没有”的差距里，测试要把内存清掉再读；
- **提交点放在哪里**：每次写完提交，还是由调用方提交，规格要说清；不说，两种实现各自的测试都能绿。

```python
import os, sqlite3, tempfile

class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS t(x)")

    def add(self, x): self.db.execute("INSERT INTO t VALUES(?)", (x,))  # 缺陷：没有 commit
    def all(self): return [r[0] for r in self.db.execute("SELECT x FROM t")]

path = os.path.join(tempfile.mkdtemp(), "s.db")
a = Store(path); a.add(1)
print(a.all())                 # [1]：同一实例读得到，测试绿
a.db.close()                   # “重启”：连接关闭，未提交的写入被丢弃
print(Store(path).all())       # []：新实例什么也没有
```

**知识点：**稳定复现（Reproduce）
