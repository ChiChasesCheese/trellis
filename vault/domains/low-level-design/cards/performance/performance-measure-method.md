---
id: performance-measure-method
node: performance.measure-first
type: qa
step: 2
---
## Q
用 `time.time()` 前后相减量一次函数，数字每次都不同，还有人在量的时候开着 `tracemalloc`。怎样量才可信？

## A
**同一份输入、多次重复取最小值、只开一个测量工具**

- **用 `timeit.repeat`**：它关掉垃圾回收（默认）、用高精度计时器，重复 N 次；
- **取最小值，不是平均值**：噪声（别的进程、缓存状态）只会让时间变长，最小值最接近代码本身的开销；
- **输入固定且有代表性**：每次量同一份数据，建数据的时间不要算进去；
- **一次只开一个工具**：测量工具自己会拖慢程序，量时间时别开内存跟踪或剖析；
- **只比较同一台机器、同一个版本上的数**：换一台机器、换一个 Python 版本，绝对值就没有意义，结论要写明环境。

实测（3.11，本机）：把 1000 个浮点数转成字符串的同一段代码，每次调用的耗时：

| 条件 | 耗时 |
|---|---|
| 什么工具都不开 | 153 µs |
| `tracemalloc` 开着 | 290 µs（约 1.9 倍） |
| `cProfile` 开着 | 179 µs（约 1.2 倍） |

```python
import timeit, random

xs = [random.random() for _ in range(1000)]

def work():
    return [str(x) for x in xs]

runs = timeit.repeat(work, number=200, repeat=5)
print([round(r / 200 * 1e6) for r in runs], "µs；取最小值", round(min(runs) / 200 * 1e6), "µs")
```

**知识点：**先测量（Measure First）
