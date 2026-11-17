---
id: concurrency-depth-prove-concurrency-bounds
node: concurrency-depth.testing
type: qa
step: 6
---
## Q
“线程池最多同时跑 `max_workers` 个任务”和“真的有这么多个同时在跑”怎么分别测？为什么这个测试里池的大小必须恰好等于屏障的人数？

## A
**屏障证明“至少”，计数峰值量出“至多”**

- **至少**：让每个任务到屏障等待，凑不齐 k 个线程屏障就不放行。串行执行的实现会等到超时抛 `BrokenBarrierError`，测试红。屏障必须带 `timeout`，否则一个错误让测试永远挂住；
- **至多**：任务进入时在锁里 `now += 1` 并更新 `peak = max(peak, now)`，离开时 `now -= 1`，最后断言 `peak == k`；
- **池大小要等于屏障人数**：池比 k 小（实测池 2、屏障 3），任务凑不齐，等到超时抛 `BrokenBarrierError`；池比 k 大（池 6、屏障 3，40 轮里 17 轮峰值是 4，其余碰巧等于 3），超出的线程会让峰值超过 k，但不稳定，所以这个断言是在量，上限本身靠 `max_workers` 保证；
- **任务数取 2k**：屏障可重复使用，第二批任务再凑齐一次，证明池在任务完成后重新补上了；
- **不要用 `sleep` 估计重叠**：屏障才是“同时在跑”的证据。

```python
import threading
from concurrent.futures import ThreadPoolExecutor
def test_runs_exactly_k_at_once(k=3):
    barrier = threading.Barrier(k, timeout=2)   # 凑不齐 k 个就 BrokenBarrierError
    lock, now, peak = threading.Lock(), [0], [0]
    def task(_):
        with lock:
            now[0] += 1; peak[0] = max(peak[0], now[0])
        barrier.wait()                          # 至少 k 个同时在跑
        with lock: now[0] -= 1
    with ThreadPoolExecutor(max_workers=k) as ex:
        list(ex.map(task, range(2 * k)))
    assert peak[0] == k                         # 至多 k：量出来的
```

**知识点：**测试并发代码（Testing Concurrency）
