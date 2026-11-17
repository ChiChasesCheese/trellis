---
id: performance-prof-cpu-vs-wait
node: performance.profiling
type: qa
step: 3
---
## Q
一个接口 200 ms 才返回，剖析一看最大的是 `time.sleep`（或者 `socket.recv`、数据库调用），CPU 的占用却很低。这时候优化代码里的计算还有意义吗？怎么区分 CPU 时间和等待时间？

## A
**先分清时间花在“算”还是“等”：等待的时间，靠优化计算是省不下来的**

- **`time.perf_counter()` 量墙钟时间**（含等待）；**`time.process_time()` 只量本进程的 CPU 时间**；两者差得多，说明大部分时间在等；
- **`cProfile` 默认按墙钟时间记账**：函数里睡了多久、等了多久，都算在 `tottime` 里，所以 `time.sleep`、`recv` 会排在最前面；看见这类函数排第一，要认出这是“在等”，不是“在算”；
- **等待的优化手段不同**：减少往返次数（批量取回）、并发地发请求、缓存、让数据离得更近；
- **计算的优化手段**：换算法、换数据结构、把循环交给 C；
- **两者都有时分开处理**：先拿掉等待（它往往占大头），再看剩下的计算。

实测（3.11，本机）：一个函数先 `sleep` 一会儿（模拟等待外部服务），再算 20 万个平方和：墙钟约 0.26 s，进程 CPU 时间约 0.02 s；`cProfile` 里 `time.sleep` 的 `tottime` 是 0.234 s，计算部分共约 0.04 s。

```python
import time

def handler():
    time.sleep(0.1)                              # 等外部服务：不占 CPU
    return sum(i * i for i in range(200_000))   # 真正的计算

w0, c0 = time.perf_counter(), time.process_time()
handler()
print(f"墙钟 {time.perf_counter() - w0:.3f}s  CPU {time.process_time() - c0:.3f}s")
```

**知识点：**读懂剖析结果（Reading Profiles）
