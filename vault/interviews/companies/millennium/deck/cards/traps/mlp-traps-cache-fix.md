---
id: mlp-traps-cache-fix
node: traps.cache-thread
type: qa
step: 2
---
## Q
**有上限的缓存：输出什么**｜语言陷阱与读代码

下面两段代码输出什么？

```java
Map<Integer, String> cache = new LinkedHashMap<>(16, 0.75f, true) {
    protected boolean removeEldestEntry(Map.Entry<Integer, String> e) {
        return size() > 3;
    }
};
for (int i = 1; i <= 4; i++) cache.put(i, "s" + i);
cache.get(2);
cache.put(5, "s5");
System.out.println(cache.keySet());
```

```python
@lru_cache(maxsize=2)
def f(x): return x * x
f(1); f(2); f(3)
print(f.cache_info())
```

## A
**输出。** Java：`[4, 2, 5]`。Python：`CacheInfo(hits=0, misses=3, maxsize=2, currsize=2)`。

- **Java 逐步追踪：** 第三个构造参数 `true` 表示按访问顺序排列。放入 1、2、3 后超过 3 的那一刻是放入 4，淘汰最旧的 1，剩 `[2, 3, 4]`；`get(2)` 把 2 移到最新，变成 `[3, 4, 2]`；放入 5，淘汰最旧的 3，得 `[4, 2, 5]`。
- **`removeEldestEntry`：** 每次放入后被调用，返回 true 就删掉最旧条目；这是用十行写出 LRU 缓存的标准办法。
- **Python 追踪：** `f(1)`、`f(2)`、`f(3)` 都是首次调用，三次未命中；容量 2，放入 3 时挤掉 1，所以现在只有两条。
- **带过期时间的版本：** 每条存 `(值, 过期时刻)`，读取时先比较当前时间，过期就删并当作未命中；容量超限时 `OrderedDict.popitem(last=False)` 淘汰最旧。
- **记住：** 缓存必须同时有大小上限和过期策略；无界的 `dict` 或 `Map` 只能用在生命周期很短的局部变量里。

**英文答法。**
- "I'd bound it with an **LRU**: evict the least recently used entry once it's over capacity."
- "Entries also carry an **expiry time**, checked lazily on read."
