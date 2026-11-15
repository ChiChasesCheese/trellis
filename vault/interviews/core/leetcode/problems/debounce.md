---
slug: debounce
---
## Q
**LC 2627 函数防抖**｜Medium

（原题为 JavaScript，这里用 Python。）实现防抖 `debounce(fn, t)`：返回一个新函数；每次调用都会延迟 `t` 毫秒后才真正执行 `fn`，若在延迟期间再次被调用，则取消上一次，只执行最新一次（使用最新一次的参数）。

## A
**一句话。** 闭包里存一个定时器：每次调用先取消旧定时器，再用最新参数开一个新的 `t` 毫秒定时器。

```python
def debounce(fn, t):
    timer = None

    def wrapper(*args):
        nonlocal timer
        if timer:
            timer.cancel()               # 取消上一次待执行的调用
        timer = threading.Timer(t / 1000, fn, args)
        timer.start()
    return wrapper
```

**复杂度。** 每次调用 `O(1)`。

**易错点。**
- 没取消旧定时器：多次调用都会执行，防抖失效。
- 用第一次的参数：执行的应是最后一次调用的参数，每次都重新建定时器就保证了这点。
- 把 `t` 当秒用：`Timer` 的单位是秒，要 `t / 1000`。

**追问。**
- 节流（throttle）区别在哪？：节流是固定时间内最多执行一次且立即执行，防抖是静默 `t` 毫秒后才执行。

**同模式。** LC 2694 事件发射器、LC 2636 Promise 对象池、LC 2695 包装数组
