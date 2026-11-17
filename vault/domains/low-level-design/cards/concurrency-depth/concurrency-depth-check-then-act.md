---
id: concurrency-depth-check-then-act
node: concurrency-depth.compound-actions
type: qa
step: 1
---
## Q
`if key not in d: d[key] = factory()` 里，`in` 和赋值各自都是线程安全的操作，为什么合在一起就会重复创建？锁要罩住什么？

## A
**每步原子，组合不原子：锁罩住检查和动作**

- **哪里破**：线程 A 查到没有、还没写入，线程 B 也查到没有，两边都调了 `factory()`，后写的覆盖先写的，先建的对象已经被 A 拿去用了；
- **GIL 管不到**：GIL 只让一次 `in`、一次 `d[k] = v` 各自不被打断，两次操作之间随时可能换线程；
- **实测（CPython 3.11，4 线程抢 300 个 key，100 轮）**：默认切换间隔 0/100 轮出现重复创建，`sys.setswitchinterval(1e-6)` 下 77/100 轮；加锁后两种间隔都是 0/100。默认间隔下测不出，是 GIL 把竞态藏起来了，不是代码对；
- **3.14t（free-threaded，没有 GIL）**：不加锁 66/100 轮，默认间隔就能测到；加锁写法不变；
- **返回值也在锁内取**：锁外再读 `d[key]` 又是一次新的组合。

```python
import threading
class Registry:
    def __init__(self):
        self._items, self._lock = {}, threading.Lock()
    def get_or_create(self, key, factory):
        with self._lock:                    # 检查和写入在同一个临界区
            if key not in self._items:
                self._items[key] = factory()
            return self._items[key]

r, made = Registry(), []
a = r.get_or_create("k", lambda: made.append(1) or object())
b = r.get_or_create("k", lambda: made.append(1) or object())
print(a is b, len(made))                    # True 1
```

<details class="pt"><summary>延伸</summary>

`factory()` 很慢时，上面的写法让所有 key 排队。可以先在锁外建好再放进去（可能白建一份），或者只在锁里登记“这个 key 有人在建”、建的动作放锁外（single-flight），或者每个 key 一把锁。

</details>

**知识点：**复合操作（Compound Actions）
