---
id: errors-retry-budget
node: errors.retry
type: qa
step: 3
---
## Q
重试循环只写“最多 3 次”够吗？三层服务各自重试 3 次，最底下的服务最多会收到多少个请求？

## A
**限次数，也限总时间，只在一层重试**

- **层层放大**：A 调 B、B 调 C，每层最多 3 次，C 最坏收到 3×3×3 = 27 次，而 C 正是因为过载才出错的；
- **限总时间**：整个操作要有截止时间（deadline），只数次数的话，5 次 × 30 秒超时就是两分半；
- **只在一层重试**：选最靠近调用方、清楚操作是否幂等的那一层，其余层快速失败，直接上抛；
- **重试预算**：重试请求不超过正常请求的一成左右，超出就不再重试，避免故障时流量翻倍；
- **用完以后抛原异常**：不要吞掉，也不要换成一个没有信息的 `RuntimeError`。

```python
import time

def retry(fn, attempts=3, deadline=2.0, sleep=time.sleep, now=time.monotonic):
    start = now()
    for n in range(attempts):
        try:
            return fn()
        except TimeoutError:
            if n == attempts - 1 or now() - start >= deadline:
                raise                          # 次数或总时间用完：原异常上抛
            sleep(0.1 * 2 ** n)
calls = []
def down(): calls.append(1); raise TimeoutError
try: retry(down, sleep=lambda s: None)
except TimeoutError: print("放弃，共调用", len(calls), "次")   # 3
```

<details class="pt"><summary>延伸</summary>

远程调用还要有单次超时（timeout），否则一次卡住就把整个 deadline 吃光。单次超时、总 deadline、次数上限是三个独立的旋钮，缺一个都会出事。

</details>

**知识点：**重试与退避（Retry & Backoff）
