---
id: craft-composition-of-independent-axes-2-independence-test
node: craft.architecture.composition-of-independent-axes
type: qa
step: 2
---
## Q
**独立变化轴的组合 · 怎么判断两个变化方向真的独立**｜架构

缓存想加一种「淘汰占空间最大的键」的策略。它需要知道值有多大，而值存在存储后端里。最省事的做法是让策略直接拿到存储对象去查大小。这样做之后，「策略」和「存储」还是两条独立的轴吗？有什么办法既要体积又保持独立？

## A
**要点。** 判据：两个接口互不 import 对方，也不需要对方的内部结构。策略一旦持有存储的引用，就依赖了存储的 `get`：换成一个只写不读的远程存储，策略就坏了。保持独立的办法是由第三方（缓存）在写入时把策略需要的元数据传给它（键、体积），策略只记元数据，不碰值。

```python
class SizeAwarePolicy:                         # 耦合：策略依赖存储
    """想淘汰「占空间最大」的键：策略必须知道值有多大。"""
    def __init__(self, store) -> None:
        self.store = store                     # 耦合：策略开始依赖存储
        self.keys: list[str] = []
    def on_insert(self, k): self.keys.append(k)
    def victim(self): return max(self.keys, key=lambda k: len(self.store.get(k)))

class MemoryStore:
    def __init__(self): self.d = {}
    def get(self, k): return self.d[k]
    def put(self, k, v): self.d[k] = v

store = MemoryStore()
pol = SizeAwarePolicy(store)
for k, v in (("a", "x" * 3), ("b", "x" * 50), ("c", "x" * 10)):
    store.put(k, v); pol.on_insert(k)
print("按体积淘汰:", pol.victim())

# 不耦合的做法：由 Cache 在写入时把体积作为元数据交给策略
class SizeAwarePolicy2:                        # 独立：元数据由写入方传入
    def __init__(self) -> None: self.size: dict[str, int] = {}
    def on_insert(self, k, size: int): self.size[k] = size
    def victim(self): return max(self.size, key=self.size.get)

pol2 = SizeAwarePolicy2()
for k, v in (("a", "x" * 3), ("b", "x" * 50), ("c", "x" * 10)):
    pol2.on_insert(k, len(v))
print("元数据由写入方传入:", pol2.victim())
```

写入体积 3、50、10 的值各一个，两种策略选出的牺牲者，实际输出：

```
按体积淘汰: b
元数据由写入方传入: b
```

**为什么。** 两个结果相同，差别在依赖方向：独立版本的策略不知道存储是什么，所以能在任何后端上运行，也能单独测试；代价是策略接口变宽了（`on_insert` 多一个参数），所有策略都要接受这个参数。

**易错。** 看似独立实则耦合的信号：一个类的构造函数收下了另一条轴的对象；或者测试一个轴时必须先造另一个轴的实现。
