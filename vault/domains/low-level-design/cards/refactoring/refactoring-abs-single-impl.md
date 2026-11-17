---
id: refactoring-abs-single-impl
node: refactoring.over-abstraction
type: qa
step: 2
---
## Q
片单服务只用 SQLite。评审时有人建议“加一个 `WatchlistRepository` 接口，再包一层缓存，以后换库方便”。为什么现在不该加？什么时候才该加？

## A
**只有一个实现、一个用法时，接口和缓存是没有顾客的东西**

- **接口的价值在于有两个以上的实现或替身**：现在只有 SQLite；多出来的 `Protocol` 只是多一个要同步修改的文件；
- **测试不需要它**：SQLite 可以用 `:memory:` 在毫秒内建好真库，直接测真实逻辑，比假的内存实现更接近线上；
- **缓存带来新问题**：失效时机、并发、过期数据；没测出它真的慢，就不加；
- **什么时候加接口**：第二个实现真的出现了（换成别的库、或者调用一个慢的外部服务需要替身），那时边界在哪里，已经看得清；
- **改起来不贵**：Python 的 `Protocol` 是结构化的，调用方不用改，之后补上接口很便宜。

```python
import sqlite3

class Watchlists:                                  # 直接用 SQLite，没有仓储接口
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS w(owner, movie)")

    def add(self, owner, movie):
        self.db.execute("INSERT INTO w VALUES(?, ?)", (owner, movie))

    def movies(self, owner):
        return [m for (m,) in self.db.execute("SELECT movie FROM w WHERE owner=?", (owner,))]

w = Watchlists()                                   # 测试里就是真库，没有 mock
w.add("ann", "m1"); print(w.movies("ann"))         # ['m1']
```

**知识点：**过度抽象（Over-Abstraction）
