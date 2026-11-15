---
slug: print-in-order
---
## Q
**LC 1114 按序打印**｜Easy

三个线程分别调用同一个 `Foo` 对象的 `first()`、`second()`、`third()`（启动顺序不定），设计同步机制，使输出总是 "firstsecondthird"。

## A
**一句话。** 两个事件（Event）串起顺序：`first` 完成后置位 `e1`，`second` 等 `e1` 再运行并置位 `e2`，`third` 等 `e2`。

```python
class Foo:
    def __init__(self):
        self.e1 = threading.Event()
        self.e2 = threading.Event()

    def first(self, printFirst):
        printFirst()
        self.e1.set()                # 通知 second 可以开始

    def second(self, printSecond):
        self.e1.wait()               # 等 first 完成
        printSecond()
        self.e2.set()

    def third(self, printThird):
        self.e2.wait()
        printThird()
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 用 `sleep` 排序：靠时间不保证先后，线程调度一抖就乱，必须用同步原语。
- `second` 里不等 `e1`：线程可能先于 `first` 启动，直接打印就乱序。
- 事件被复用：`Event` 一旦 `set` 不会自动清除，这里每个事件只用一次，不用清。

**追问。**
- 换成信号量怎么写？：两个初值为 0 的 `Semaphore`，`release` 代替 `set`，`acquire` 代替 `wait`。
- 要重复多轮怎么办？：每轮结束要 `clear()` 复位，或改用屏障 / 条件变量带轮次编号。

**同模式。** LC 1188 设计有限阻塞队列、LC 1226 哲学家进餐
