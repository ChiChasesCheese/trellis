---
id: concurrency-asyncio-await-yield-points
node: concurrency.asyncio
type: qa
step: 2
---
## Q
"协程只在 `await` 处让出控制权"——这句话对写并发安全的协程代码有什么实际好处？

## A
一个协程函数里，两个 `await` 之间的代码是**原子**的：事件循环不会在这段代码执行到一半时切换去跑别的协程，因为压根没有让出点。这意味着只要一段逻辑不跨 `await`，就不需要担心别的协程会在中间插进来修改共享状态——`threading` 下需要用锁保护的很多"读-改-写"，在纯协程、不跨 `await` 的写法下自动就是安全的。

```python
counter = 0
async def incr():
    global counter
    counter += 1  # 不含 await，这一行相对其他协程是原子的
```

但一旦这段逻辑中间插入了一次 `await`（比如先读一个值、`await` 一次网络调用、再写回去），中间点就变成了让出点——另一个协程完全可能在这次 `await` 期间跑进来，把共享状态改成你没预料到的样子，这时候又需要显式同步了。
