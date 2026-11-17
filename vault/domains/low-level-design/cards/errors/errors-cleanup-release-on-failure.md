---
id: errors-cleanup-release-on-failure
node: errors.cleanup
type: qa
step: 3
---
## Q
图片处理流水线用“名额和字节预算”限制并发：开始处理前占用，处理完归还。某张图变换失败时没有归还，会发生什么？应该怎么写？

## A
**占用和归还成对，归还放进 `finally`**

- **只在成功路径归还**：每失败一张图就永久少一份预算，失败多了流水线被饿死，没有报错，只是越来越慢直到卡住；
- **占用写在 `try` 之前**：占用不成功就没有东西可还；
- **归还写在 `finally`**：成功、失败、异常都还同一个数量；
- **还要还“同一份”**：用占用时的 `size` 还，不要在中途改了变量再还；
- **一张图失败不影响别的图**：调用方捕获后接着处理下一张，预算已经回到原样。

```python
free = [10]                                   # 剩余预算

def process(size: int, fail: bool):
    if size > free[0]: raise MemoryError      # 占用成功才进 try
    free[0] -= size
    try:
        if fail: raise ValueError("bad image")
        return size
    finally:
        free[0] += size                       # 成败都还同一个 size

for fail in (True, False, True):
    try: process(6, fail)
    except ValueError: pass
print(free[0])                                # 10：三张图之后预算原样
```

**知识点：**所有路径上的清理（Cleanup on Every Path）
