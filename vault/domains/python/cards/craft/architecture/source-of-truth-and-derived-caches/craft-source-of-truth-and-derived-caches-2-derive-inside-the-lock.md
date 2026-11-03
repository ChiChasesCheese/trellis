---
id: craft-source-of-truth-and-derived-caches-2-derive-inside-the-lock
node: craft.architecture.source-of-truth-and-derived-caches
type: qa
step: 2
---
## Q
**真相与派生缓存 · 对账时「先推导、再拿锁覆盖」错在哪**｜架构

对账函数从账本推导出余额，再写回缓存。为了不长时间占着账户锁，有人把推导放在锁外，只在最后写回时拿锁。听上去只是缩小了临界区，会出什么问题？

## A
**要点。** 推导和写回之间如果插进一笔转账（它在持有账户锁时同时改账本和缓存），写回的就是一个过期值，缓存被「纠正」坏。正确做法是推导和覆盖在同一个临界区里：转账也要拿同一把锁，所以锁内读到的账本与缓存一定是同步的。

```python
def run(locked: bool) -> tuple[int, int]:
    lock = threading.Lock()
    ledger = [("A", +100)]
    cache = {"A": 100}
    derived = lambda: sum(d for a, d in ledger if a == "A")

    def transfer_out(n: int) -> None:       # 转账：持账户锁，同时改账本和缓存
        with lock:
            ledger.append(("A", -n))
            cache["A"] -= n

    def reconcile() -> None:
        with (lock if locked else nullcontext()):   # 锁内推导，还是锁外推导
            d = derived()
            t = threading.Thread(target=transfer_out, args=(30,)); t.start()
            t.join(timeout=0.2)                     # 推导完、写回前，一笔转账想插进来
            cache["A"] = d
        t.join()

    reconcile()
    return cache["A"], derived()

for locked in (False, True):
    print("锁内" if locked else "锁外", "推导：缓存 =", run(locked)[0], "账本推导 =", run(locked)[1])
```

账本初始 100，各跑一次，实际输出：

```
锁外 推导：缓存 = 100 账本推导 = 70
锁内 推导：缓存 = 70 账本推导 = 70
```

**为什么。** 锁外推导时，转账成功了，写回却把缓存覆盖成 100：对账把一个原本只是慢一点的缓存变成了错误的缓存，比不对账还糟。锁内则转账要等对账结束，之后在 100 的基础上扣 30，得到 70。

**代价。** 对账持锁期间，这个账户的转账被阻塞；账本很长时这个代价是真的，应该用快照或增量水位线（上次对到哪条）来缩短推导，而不是把推导挪到锁外。
