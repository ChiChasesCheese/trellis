---
id: concurrency-depth-free-threaded-exposes
node: concurrency-depth.memory-model
type: qa
step: 4
---
## Q
同一份多线程代码在 3.11 上稳定通过，换到 free-threaded 构建（3.13t、3.14t，没有 GIL）会坏哪些地方？哪些不会坏？

## A
**没有 GIL，被它藏起来的竞态都会暴露；加了锁的代码不受影响**

- **仍然安全**：内置容器的单次操作（`list.append`、`dict.setdefault` 等），free-threaded 构建给每个对象加了内部锁。实测 8 线程各 20000 次，`append` 后长度恰好 160000，`setdefault` 后恰好 20000 个键，3.14t 上一样；
- **会坏的**：靠 GIL 巧合安全的读改写。同一段代码（8 线程各 `n += 1` 20000 次）3.11 上总是 160000，3.14t 上三次试验都不是；先检查后创建、遍历时修改、限流器的判定加计数，在 3.14t 上默认间隔下 21–99/100 轮出错；
- **不变的**：显式的 `Lock`、`Queue`、`Event` 在两个构建上语义相同；所以“复合操作全部放进锁里”这条规则，是同时对两种构建都正确的写法；
- **查看当前构建**：`sys._is_gil_enabled()`（3.13 起才有，没有就当作有 GIL）；
- **C 扩展**：调用 C 扩展的线程安全，要看扩展是否声明支持无 GIL；不支持的扩展会让解释器重新打开 GIL；
- **测试策略**：并发测试在 3.11 上通过说明不了什么，CI 里加一个 free-threaded 的作业，能把靠运气的代码抓出来。

```python
import sys, threading

print(getattr(sys, "_is_gil_enabled", lambda: True)())   # 3.14t：False
n, box = 0, []
def work():
    global n
    for _ in range(20_000):
        box.append(1)            # 内置容器的单个方法：两个构建上都安全
        n += 1                   # 读改写：只有 GIL 的巧合在保护它
ts = [threading.Thread(target=work) for _ in range(8)]
[t.start() for t in ts]; [t.join() for t in ts]
print(len(box) == 160_000, n == 160_000)   # 3.11：True True；3.14t：True False
```

**知识点：**内存模型与可见性（Memory Model）
