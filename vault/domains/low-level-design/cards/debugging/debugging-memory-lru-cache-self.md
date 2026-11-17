---
id: debugging-memory-lru-cache-self
node: debugging.memory
type: qa
step: 3
---
## Q
给服务类的方法加了 `@functools.lru_cache`，对象用完删掉，内存却没降。为什么？怎么改？

## A
**`lru_cache` 装饰方法时，`self` 也是缓存的键：缓存活多久，对象就活多久**

- **缓存放在函数对象上**（类级别，整个进程共享一份）；
- **键里包含参数，参数里有 `self`**：缓存持有对每个调用过的实例的强引用，实例不会被回收；
- **`maxsize=None` 时无上限**：每个实例、每组参数都永远留着；
- **改法一**：把需要缓存的纯计算提到模块级函数，键里只有值，没有 `self`；
- **改法二**：需要按实例缓存时，在 `__init__` 里为每个实例创建自己的缓存（对象被回收时缓存一起走），或者缓存数据放到实例自己的字典里；
- **要给任何缓存设上限**：`maxsize` 要有具体的数字，并想一想过期条件。

```python
import functools, gc, weakref

class Leaky:
    @functools.lru_cache(maxsize=None)
    def load(self, k): return k * 2
@functools.lru_cache(maxsize=128)
def _load(k): return k * 2                 # 模块级：键里没有 self
class Fine:
    def load(self, k): return _load(k)

for cls in (Leaky, Fine):
    obj = cls(); obj.load(1); ref = weakref.ref(obj)
    del obj; gc.collect()
    print(cls.__name__, "对象还活着 =", ref() is not None)   # Leaky True / Fine False
```

**知识点：**内存问题（Memory Leaks）
