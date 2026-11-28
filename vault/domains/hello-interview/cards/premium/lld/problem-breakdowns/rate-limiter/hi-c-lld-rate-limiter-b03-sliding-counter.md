---
id: hi-c-lld-rate-limiter-b03-sliding-counter
node: lld.problem-breakdowns.rate-limiter.beyond
type: qa
step: 4
---
## Q
**限流器 · 拓展：滑动窗口计数器的加权近似**｜拓展 · 加分

滑动窗口日志精确但耗内存，固定窗口省内存但有边界突发。滑动窗口计数器怎么折中？

## A
**模式。** 用两个相邻固定窗口的计数，按重叠比例加权，近似一个滑动窗口。

```python
class SlidingWindowCounter:
    """每键只存 (当前窗口起点, 当前计数, 上一窗口计数)，用加权近似滑动窗口。"""

    def __init__(self, max_requests: int, window_ms: int, clock) -> None:
        self._max, self._win, self._clock = max_requests, window_ms, clock
        self._s: dict[str, list[float]] = {}     # key -> [start, curr, prev]

    def allow(self, key: str) -> bool:
        now = self._clock()
        start = now - now % self._win            # 当前固定窗口的起点
        s = self._s.setdefault(key, [start, 0, 0])
        if start != s[0]:                        # 窗口翻页
            s[2] = s[1] if start - s[0] == self._win else 0   # 隔了不止一窗，上一窗视为空
            s[0], s[1] = start, 0
        # 假设上一窗口的请求均匀分布：只数还落在"滑动窗口"内的那一部分
        est = s[2] * (1 - (now - start) / self._win) + s[1]
        if est >= self._max:
            return False
        s[1] += 1
        return True


t = [0.0]
c = SlidingWindowCounter(10, 1000, lambda: t[0])
t[0] = 900
assert sum(c.allow("k") for _ in range(10)) == 10    # 上一窗口末尾打满 10 个
t[0] = 1100                                          # 新窗口 100ms：上一窗口还剩 90% 的权重
print([c.allow("k") for _ in range(3)])              # 估计值 = 10*0.9 = 9 -> 只再放行 1 个
# 固定窗口计数器在这里会放行 10 个：窗口边界处 200ms 内共 20 个，两倍于限额
```
- **估计公式：** 估计 = 上一窗口计数 × (1 − 当前窗口已过去的比例) + 当前窗口计数。当前窗口刚开始时上一窗口占几乎全部权重，窗口末尾时几乎为零。
- **假设：** 上一窗口内的请求均匀分布。如果它们集中在窗口末尾，估计会偏低、可能放过略多；如果集中在窗口开头则偏高、会略多拒绝。所以它是近似，不是精确。
- **内存：** 每键三个数字（窗口起点、当前计数、上一计数），与请求量无关。
- **窗口翻页要处理"隔了不止一个窗口"：** 此时上一窗口应视为空，否则会把很久以前的计数带进来。
- **何时选：** 键数很多、每键请求量大、可以接受小误差；需要精确（如登录失败次数）就用日志。
