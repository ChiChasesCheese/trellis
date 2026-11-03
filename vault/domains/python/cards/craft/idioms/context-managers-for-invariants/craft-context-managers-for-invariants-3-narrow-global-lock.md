---
id: craft-context-managers-for-invariants-3-narrow-global-lock
node: craft.idioms.context-managers-for-invariants
type: qa
step: 3
---
## Q
**上下文管理器守不变量 · 先在全局锁里取对象、立刻放掉，再持有它自己的锁**｜写法

四子棋服务按局号找对局，每局有自己的锁。`_locked(game_id)` 先拿全局锁查字典，查到之后放掉全局锁，再拿这一局的锁并 `yield`。直接在全局锁里一路持有到块结束会怎样？

## A
**要点。** 全局锁保护的是「字典」，局锁保护的是「这一局的状态」，是两件不同的事。全局锁只该覆盖查字典那一瞬间。如果一直持有到 `with` 块结束，一局里的慢操作（等对手、写磁盘）就会让所有其他对局都排队，分锁等于白分。

```python
class Match:
    def __init__(self): self.lock = threading.Lock()

class Games:
    def __init__(self):
        self._mu = threading.Lock()
        self._matches = {"g1": Match(), "g2": Match()}

    @contextmanager
    def locked(self, gid):                 # 全局锁只覆盖查字典的一瞬间
        with self._mu:
            m = self._matches.get(gid)
        with m.lock:
            yield m

    @contextmanager
    def locked_slow(self, gid):            # 反例：全局锁一直持有到块结束
        with self._mu:
            m = self._matches[gid]
            with m.lock:
                yield m

def probe(maker, label):
    g = Games()
    inside = threading.Event(); release = threading.Event(); got = []
    def hold():
        with maker(g, "g1"):
            inside.set(); release.wait()   # 对局 g1 里一个很慢的操作
    t = threading.Thread(target=hold); t.start(); inside.wait()
    def other():
        with maker(g, "g2"):               # 另一局，本该不受影响
            got.append(True)
    o = threading.Thread(target=other); o.start(); o.join(0.3)
    print(f"{label}: g1 操作中, g2 能否进入? {bool(got)}")
    release.set(); t.join(); o.join()

probe(Games.locked, "全局锁只查字典")
probe(Games.locked_slow, "全局锁一直持有")
```

实际输出：

```
全局锁只查字典: g1 操作中, g2 能否进入? True
全局锁一直持有: g1 操作中, g2 能否进入? False
```

**为什么。** 先查再放要成立，需要「对局一旦创建就不会被删」或者别的办法保证拿到引用后它仍然有效；否则放掉全局锁到拿到局锁之间，对局可能已被删除。这里的 `_matches` 只增不减，所以安全。

**易错。** 在 `with` 块里 `yield` 出被锁保护的对象，风险是调用方把它存到块外继续用，那时锁已经放了。约定：块内用完，不带出去。
