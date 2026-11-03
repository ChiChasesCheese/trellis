---
id: craft-id-generation-1-counter-not-len
node: craft.idioms.id-generation
type: qa
step: 1
---
## Q
**ID 生成 · 为什么不能用「现有数量 + 1」当编号**｜写法

一个内存里的订单簿要给每笔订单发 ID。最顺手的写法是 `f"o{len(orders) + 1}"`。取消一单之后会发生什么？换成 `itertools.count` 之后，多个线程同时取号还要注意什么？

## A
**要点。** ID 的唯一性要求是「永远不重复」，而不是「等于现在有几个」。数量会因为删除而变小，所以 `len + 1` 会把已经发出的编号再发一次。发号器应该是一个只增不减的计数器，与容器内容无关；并发时，取号这一步要么在锁里，要么用单个原子操作完成。

```python
import itertools, threading

orders: dict[str, str] = {}
def new_id_naive() -> str:
    return f"o{len(orders) + 1}"

orders[new_id_naive()] = "a"        # o1
orders[new_id_naive()] = "b"        # o2
del orders["o1"]                    # 取消一单
print(new_id_naive(), "已存在?", new_id_naive() in orders)

ids = itertools.count(1)            # 只增不减，与 orders 无关
lock = threading.Lock()
def new_id() -> str:
    with lock:
        return f"o{next(ids)}"

got: list[str] = []
def work() -> None:
    for _ in range(1000):
        got.append(new_id())
ts = [threading.Thread(target=work) for _ in range(8)]
[t.start() for t in ts]; [t.join() for t in ts]
print(len(got), len(set(got)))
```

实际输出：

```
o2 已存在? True
8000 8000
```

**为什么。** 在 CPython（有全局解释器锁）里，`next(itertools.count())` 是一次 C 调用，实际上不会被打断，所以不加锁通常也不重复；但语言规范没有保证这一点，且换成生成器表达式时，多线程同时 `next()` 同一个生成器会抛 `ValueError: generator already executing`。所以取号处加一把小锁，成本可以忽略，正确性不再依赖实现细节。

**代价。** 计数器是进程内存：重启后从 1 开始，会和已落库的编号冲突。要么启动时从库里读最大值接着发，要么改用不依赖本地状态的 ID，例如 UUID 或「时间戳 + 机器号 + 序号」的雪花 ID。
