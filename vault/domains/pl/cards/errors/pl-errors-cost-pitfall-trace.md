---
id: pl-errors-cost-pitfall-trace
node: errors.cost
type: qa
step: 8
---
## Q
Java 里把异常当作「找不到」的信号，在高并发下会怎样？为什么栈越深越糟？

## A
典型反模式：一个方法在没有匹配时抛出异常，调用者捕获后走回退逻辑。

```java
static int viaThrow(int i, int depth) {
    if (depth > 0) return viaThrow(i, depth - 1);
    if ((i & 1) == 0) throw new RuntimeException();   // half of the calls "fail"
    return i;
}
```

对比两种做法（本机一次实测，200 万次调用，其中一半失败，平均每次调用耗时）：

```console
返回错误码         约 0.2 到 0.6 ns
抛异常，栈深 5      约 143 ns
抛异常，栈深 20     约 413 ns
抛异常，栈深 200    约 3754 ns
不填栈追踪的异常     约 1.5 ns
```

成本来自 `new RuntimeException()`：构造函数调用 `fillInStackTrace`，遍历整个调用栈，把每一帧复制成 `StackTraceElement`。栈越深，复制越多：200 层的栈要付出 20 层的约 9 倍。在典型的 Web 应用里，调用栈经常有几十到几百层（框架、拦截器、代理），所以一次异常的实际成本是微秒级，同时产生大量需要回收的垃圾。

后果：
- 这类代码在低并发下看不出问题，压测时 CPU 被栈追踪吃掉，尾延迟出现尖峰；
- profiler 的火焰图里 `fillInStackTrace` 异常突出；
- 如果每次失败还往日志里写完整栈追踪，I/O 又放大一次。

修复：用返回值表达「找不到」（`Optional`、`null` 加约定、状态枚举）；或对必须使用异常的热路径，用不填栈追踪的预分配异常；或者在入口处先做检查，避免走到失败路径。

C++ 里同一反模式更贵：本机实测，用异常表示一半调用失败，栈深 20 时平均每次调用约 5 µs，比返回 `std::expected`（C++23，装着值或错误的结果类型）的 0.4 ns 慢约四个数量级；而且 C++ 没有「不填栈追踪」这个开关可关，因为它本来就没有栈追踪，贵的是展开。
Python 中类似的情形：`raise`/`except` 约 79 ns，对比返回 `None` 的约 15 ns，在 Python 里属于可接受，所以 Python 社区并不忌讳这种用法。
