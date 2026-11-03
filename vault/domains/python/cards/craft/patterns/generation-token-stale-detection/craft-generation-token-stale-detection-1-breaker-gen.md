---
id: craft-generation-token-stale-detection-1-breaker-gen
node: craft.patterns.generation-token-stale-detection
type: qa
step: 1
---
## Q
**代号令牌 · 熔断器为什么要给每次放行带上代号**｜模式

熔断器有 CLOSED、OPEN、HALF_OPEN 三个状态。一个慢请求在 CLOSED 时出发，之后熔断器因为别的请求失败而打开，冷却后进入半开、放出一个探测。这时那个慢请求终于成功返回。如果熔断器只看「这次是成功」，会发生什么？

## A
**要点。** 慢请求的成功被当成了探测成功，熔断器错误地关闭，而真正的探测还没回来（它之后失败了，熔断器也没再打开）。异步系统里「迟到的结果」是常态，要识别它：状态每转换一次，代号（generation）加一；放行时把当前代号交给调用方，回报时带回来；代号对不上，说明这个结果属于上一轮，不能改变状态。

```python
class Breaker:
    """极简熔断器：连续失败 2 次打开；冷却后半开，放 1 个探测；探测成功则关闭。手动推进时间。"""

    def __init__(self, use_gen: bool) -> None:
        self.state, self.gen, self.fails, self.use_gen = "CLOSED", 0, 0, use_gen

    def _move(self, new: str) -> None:
        self.state = new
        self.gen += 1                    # 代号加一：在途的旧许可全部作废
        self.fails = 0

    def acquire(self) -> int:
        if self.state == "OPEN":
            self._move("HALF_OPEN")                # 假设冷却已过
        return self.gen                  # 许可上带着领取时的代号

    def record(self, gen: int, ok: bool) -> None:
        if self.use_gen and gen != self.gen:
            return                       # 迟到的旧结果：不改变状态
        if self.state == "HALF_OPEN":
            self._move("CLOSED" if ok else "OPEN")
        elif self.state == "CLOSED":
            self.fails = 0 if ok else self.fails + 1
            if self.fails >= 2:
                self._move("OPEN")

for use_gen in (False, True):
    b = Breaker(use_gen)
    slow = b.acquire()                             # 一个慢请求在 CLOSED 时出发（代号 0）
    for _ in range(2):
        b.record(b.acquire(), ok=False)            # 另外两个请求失败 -> 打开
    probe = b.acquire()                            # 冷却后，真正的探测出发（HALF_OPEN）
    b.record(slow, ok=True)                        # 此时那个慢请求终于成功返回
    print("有代号" if use_gen else "无代号", "-> 探测还没返回，状态已是", b.state)
    b.record(probe, ok=False)                      # 探测其实失败了
    print("        探测失败后状态:", b.state)
```

慢请求在 CLOSED 出发，两个失败打开，冷却后探测出发，慢请求成功返回，探测失败：

```
无代号 -> 探测还没返回，状态已是 CLOSED
        探测失败后状态: CLOSED
有代号 -> 探测还没返回，状态已是 HALF_OPEN
        探测失败后状态: OPEN
```

**为什么。** 比对一次就够：不需要时间戳，也不需要知道旧结果具体晚了多久。

**易错。** 熔断器里迟到的旧结果仍然计入成功/失败的指标，只是不改变状态：事实要记下，决策只听当前这一轮。
