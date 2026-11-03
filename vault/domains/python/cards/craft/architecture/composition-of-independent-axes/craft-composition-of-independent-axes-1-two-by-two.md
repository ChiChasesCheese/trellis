---
id: craft-composition-of-independent-axes-1-two-by-two
node: craft.architecture.composition-of-independent-axes
type: qa
step: 1
---
## Q
**独立变化轴的组合 · 缓存有 2 种淘汰策略、2 种存储后端，要写几个类**｜架构

可配置缓存要支持 LRU 和 LFU 两种淘汰策略，以及内存和文件两种存储后端。最直接的写法是每种组合一个类：`LruMemoryCache`、`LfuFileCache`……再来第三种策略就变成 6 个类。怎样让类的数量随轴相加而不是相乘？

## A
**要点。** 把变化的两个方向拆成两条互不引用的轴。淘汰策略只记元数据（使用顺序或次数），不存值；存储后端只存值，不懂顺序。缓存本身只管流程、容量、过期、统计，不知道谁被淘汰、数据放哪。2 种策略加 2 种后端只写 4 个小类，再加第三种策略只多写 1 个。

```python
class LruPolicy:                            # 只记「用的顺序」，不存值
    def __init__(self): self.order = OrderedDict()
    def __contains__(self, k): return k in self.order
    def on_insert(self, k): self.order[k] = None
    def on_access(self, k): self.order.move_to_end(k)
    def on_remove(self, k): self.order.pop(k, None)
    def victim(self): return next(iter(self.order))

class LfuPolicy:                            # 只记「用的次数」，不存值
    def __init__(self): self.freq = {}
    def __contains__(self, k): return k in self.freq
    def on_insert(self, k): self.freq[k] = 1
    def on_access(self, k): self.freq[k] += 1
    def on_remove(self, k): del self.freq[k]
    def victim(self): return min(self.freq, key=self.freq.get)   # 次数相同取最早插入的

class MemoryStore:                          # 只存值，不懂顺序
    def __init__(self): self.d = {}
    def get(self, k): return self.d[k]
    def put(self, k, v): self.d[k] = v
    def delete(self, k): self.d.pop(k, None)

class ReprStore(MemoryStore):               # 先序列化再存，像文件或网络
    def put(self, k, v): self.d[k] = repr(v)
    def get(self, k): return eval(self.d[k])

class Cache:                                # 只管流程和容量
    def __init__(self, cap, policy, store):
        self.cap, self.policy, self.store = cap, policy, store
    def put(self, k, v):
        self.store.put(k, v)                # 会失败的一步在前
        if k in self.policy:
            self.policy.on_access(k)
        else:
            if len(self.store.d) > self.cap:
                victim = self.policy.victim()
                self.store.delete(victim); self.policy.on_remove(victim)
            self.policy.on_insert(k)
    def get(self, k):
        self.policy.on_access(k); return self.store.get(k)

for P in (LruPolicy, LfuPolicy):
    for S in (MemoryStore, ReprStore):
        c = Cache(2, P(), S())
        c.put("a", 1); c.put("b", 2)
        c.get("a"); c.get("a"); c.get("b")  # 访问次数 a=3、b=2，最近用的是 b
        c.put("c", 3)
        print(f"{P.__name__} + {S.__name__}: 留下", sorted(c.store.d))
```

容量 2；放入 a、b，读 a 两次、b 一次，再放 c，四种组合留下的键，实际输出：

```
LruPolicy + MemoryStore: 留下 ['b', 'c']
LruPolicy + ReprStore: 留下 ['b', 'c']
LfuPolicy + MemoryStore: 留下 ['a', 'c']
LfuPolicy + ReprStore: 留下 ['a', 'c']
```

**为什么。** 结果由策略决定（LRU 淘汰最近最少用的 a，LFU 淘汰次数最少的 b），与存储后端无关：换后端不影响淘汰结果，两条轴确实是独立的。

**代价。** 拆开后「放入」要跨两个对象，一致性靠顺序保证（先写存储，成功后才动策略）；一个类里全做完的写法没有这个问题，但组合类会爆炸。
