---
id: tlc-tt-tool-call-success-rate-4-followup
node: b.tt-tool-call-success-rate
type: qa
step: 4
---
## Q
**工具调用成功率统计**｜追问

批量版写完后，面试官接着问：（1）日志是流式到达的，要能随时查某个工具的成功率和当前失败最多的工具，怎么设计？（2）只统计最近 1 小时（时间戳单位秒）的调用，怎么办？（3）工具种类非常多时，查“失败最多”还是 `O(m)` 吗？

## A
1. **流式。** 两个 `Counter` 本来就是增量更新：循环体变成 `add(line)` 方法，每行 `O(1)`；查某工具的成功率 `O(1)`；查失败最多的工具扫一遍 `O(m)`。
2. **最近 1 小时。** 窗口是 `(现在 - 3600, 现在]`。用 `deque` 按到达顺序保存窗口内的事件（时间戳递增），每来一个新事件，先把队首 `时间戳 <= 现在 - 3600` 的事件弹出并回退计数，每个事件进出各一次，均摊 `O(1)`；回退到 `0` 的键要删掉，内存才只跟窗口内的工具数有关。
3. **工具很多。** 失败计数每次变化（增加，或窗口回退）都往堆里推一条 `(-失败数, 名字)`；查询时若堆顶的失败数和当前计数对不上就弹掉，直到堆顶有效，这是**懒删除**，均摊 `O(log m)`。

```python
# parse 同批量版：合法行返回 (时间戳, 工具名, 是否成功)，坏行返回 None
class ToolStats:
    """add 一行，随时查询；window 不为 None 时只统计最近 window 秒。"""

    def __init__(self, window: int | None = None) -> None:
        self.window = window
        self.total: Counter[str] = Counter()
        self.fails: Counter[str] = Counter()
        self.events: deque[tuple[int, str, bool]] = deque()    # 窗口内的事件，按时间戳递增

    def add(self, line: str) -> bool:
        if (rec := parse(line)) is None:
            return False
        ts, tool, ok = rec
        self.total[tool] += 1
        self.fails[tool] += not ok
        if self.window is not None:
            self.events.append(rec)
            self.evict(ts)
        return True

    def evict(self, now: int) -> None:
        assert self.window is not None
        while self.events and self.events[0][0] <= now - self.window:
            _, tool, ok = self.events.popleft()
            self.total[tool] -= 1
            self.fails[tool] -= not ok
            if self.total[tool] == 0:               # 清掉计数为 0 的键
                del self.total[tool], self.fails[tool]

    def rate(self, tool: str) -> float | None:
        n = self.total.get(tool, 0)
        return round((n - self.fails[tool]) / n, 4) if n else None

    def worst(self) -> str:
        bad = {t: f for t, f in self.fails.items() if f}
        return min(bad, key=lambda t: (-bad[t], t), default="")
```

   运行（`window = 3600`）：依次加入 `"0 a FAIL"`、`"10 a SUCCESS"`、`"3599 b FAIL"` 后 `rate("a")` → `0.5`，`worst()` → `"a"`；再加入 `"3600 b SUCCESS"`，`"0 a FAIL"` 过期，`rate("a")` → `1.0`，`worst()` → `"b"`。

**Python 提醒**：`Counter` 减到 `0` 的键不会自动删除，`len(counter)` 和遍历里还会看到它，窗口版必须手动 `del`；`list.pop(0)` 是 `O(n)`，队首弹出要用 `deque.popleft()`。
