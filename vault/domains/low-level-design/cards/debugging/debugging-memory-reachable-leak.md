---
id: debugging-memory-reachable-leak
node: debugging.memory
type: qa
step: 1
---
## Q
Python 有垃圾回收，为什么服务还是会“内存泄漏”，跑几天后越来越大？Python 里的泄漏长什么样？

## A
**Python 里的泄漏是“还被引用着、但已经没人用”的对象**

- **引用计数加循环回收**：对象没有任何引用时立刻释放，循环引用由 `gc` 定期清理；所以 C 式的“忘了 free”基本不存在；
- **泄漏 = 仍可达**：只要从某个根（模块变量、类属性、全局缓存、线程里的闭包）还能走到它，就不会被回收；
- **常见的根**：模块级的列表/字典越攒越多、没有上限的缓存、注册了不注销的回调和监听器、日志或指标按请求累加的列表；
- **排查方向**：不是问“谁没释放”，而是问“谁还拿着它的引用”；
- **验证手段**：对对象建 `weakref.ref`，丢掉自己的引用后 `gc.collect()`，弱引用还能取到对象，说明有别处在持有它。

```python
import gc, weakref

class Request: ...

seen = []                               # 模块级：这个列表不会被回收

def handle():
    r = Request()
    seen.append(r)                      # 缺陷：为了“以后调试”留着每个请求
    return weakref.ref(r)

ref = handle(); gc.collect()
print(ref() is not None)                # True：处理完了，对象还活着
seen.clear(); gc.collect()
print(ref() is None)                    # True：清掉持有者之后才被回收
```

**知识点：**内存问题（Memory Leaks）
