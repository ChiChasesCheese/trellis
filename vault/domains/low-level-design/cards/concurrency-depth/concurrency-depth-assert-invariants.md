---
id: concurrency-depth-assert-invariants
node: concurrency-depth.testing
type: qa
step: 2
---
## Q
“8 个线程同时放同一笔贷款，恰好一个成功”的并发测试，应该断言什么？为什么不断言“哪个线程赢了”或“花了多少毫秒”？

## A
**断言不变量，不断言谁赢、也不断言时序**

- **谁赢是不确定的**：线程调度每次不同。断言线程 3 赢，这个测试自己就是 flaky；
- **要断言的是不论谁赢都成立的事**：每笔贷款恰好一个线程拿到 `True`，其余是 `False`；账户总额不变；放款后状态是 `active`；
- **读线程也断言**：写线程运行期间，读线程反复读，断言读到的 ID 总是从 1 开始的连续前缀，抓“读到中间状态”；
- **每个线程碰很多笔，而不是一笔**：只有一笔时窗口太窄。实测（3.11，8 线程，1e-6 间隔，200 轮）：每线程只放 1 笔，无锁实现 1–2/200 轮抓到；每线程碰 100 笔，27/200 轮抓到；加锁两种都是 0/200。默认间隔下无锁也是 0/200；3.14t 默认间隔 119/200；
- **示例只写了“每笔恰好一个赢家”这一条**，总额不变、读线程的断言写法相同；
- **时序不进断言**：不要断言“耗时小于 X 毫秒”，机器忙一点就红。

```python
import sys, threading
def test_each_loan_disbursed_once(make_loans, n=100, threads=8):
    sys.setswitchinterval(1e-6)
    try:
        for _ in range(200):                       # 每轮全新实例
            loans, barrier, wins = make_loans(n), threading.Barrier(threads), []
            def work():
                barrier.wait()
                wins.append([loans.disburse(i) for i in range(n)])
            ts = [threading.Thread(target=work) for _ in range(threads)]
            [t.start() for t in ts]; [t.join() for t in ts]
            for i in range(n):                     # 不变量：每笔恰好一个赢家
                assert sum(w[i] for w in wins) == 1
    finally:
        sys.setswitchinterval(0.005)
```

**知识点：**测试并发代码（Testing Concurrency）
