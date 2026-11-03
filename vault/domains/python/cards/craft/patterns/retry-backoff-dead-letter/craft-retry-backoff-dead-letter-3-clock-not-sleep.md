---
id: craft-retry-backoff-dead-letter-3-clock-not-sleep
node: craft.patterns.retry-backoff-dead-letter
type: qa
step: 3
---
## Q
**重试、退避与死信 · 抖动（jitter）为什么要做成参数，而不是在函数里直接 random**｜写法

指数退避有一个已知问题：1000 个客户端同时遇到故障，按同样的 1、2、4 秒重试，会在同一时刻一起冲向刚恢复的服务（惊群，thundering herd）。解法是给等待时间加随机抖动。随机性应该写在 `delay_for` 内部，还是由调用方传入？

## A
**要点。** 传入。生产环境要抖动（打散重试），测试要可重复（同一个输入永远得到同一个序列）。把随机数发生器 `rng` 当参数：生产传默认的，测试传带种子的 `random.Random(7)`，或者不传（无抖动，纯确定）。时钟同理：「到点了没有」是对注入时钟的一次比较，推进假时钟就能走完整条重试路径。

```python
import random

def delay(attempt, base=1.0, mult=2.0, cap=60.0, rng=None):
    raw = min(base * mult ** (attempt - 1), cap)
    return raw if rng is None else rng.uniform(0, raw)    # 全抖动：在 [0, raw] 里均匀取

# 1000 个客户端同时失败，按各自的退避重试：没有抖动时每轮都是同一刻齐射
no_jitter = {delay(a) for a in range(1, 4)}
print("无抖动: 1000 个客户端第 1..3 次重试的时刻集合 =", sorted(no_jitter), "（所有人踩同一个点）")
rng = random.Random(7)
firsts = [delay(1, rng=rng) for _ in range(1000)]
print("有抖动: 第 1 次重试散布在 [%.2f, %.2f]，平均 %.2f" % (min(firsts), max(firsts), sum(firsts) / len(firsts)))
rng2, rng3 = random.Random(7), random.Random(7)           # 同一个种子
print("同一个种子可复现:", [round(delay(3, rng=rng2), 3) for _ in range(2)] == [round(delay(3, rng=rng3), 3) for _ in range(2)])
```

```
无抖动: 1000 个客户端第 1..3 次重试的时刻集合 = [1.0, 2.0, 4.0] （所有人踩同一个点）
有抖动: 第 1 次重试散布在 [0.00, 1.00]，平均 0.48
同一个种子可复现: True
```

**为什么。** 无抖动时，1000 个客户端只有 3 个不同的重试时刻，每一轮都是一次齐射；全抖动把它们摊平到整个区间。把随机和时间都变成参数，是「依赖注入」在重试里的具体样子：核心逻辑是纯的，不确定性留在边界。

**代价。** 全抖动意味着个别客户端会几乎立刻重试（0.00 附近）。有些系统用「等价抖动」（一半固定、一半随机）保留一个最小间隔，具体取舍看被保护的服务能承受多大的尖峰。

**易错。** 随机数要用独立实例（`random.Random(seed)`），而不是模块级的 `random.seed(...)`：后者是全局状态，会让别的测试顺序相关。
