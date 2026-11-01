---
id: tlc-daily-design-bus-seat-booking-system-0-whole
node: 2026-10.design-bus-seat-booking-system
type: qa
---
## Q
**LC 4080 设计公交车座位预订系统**｜Medium · 2026-10-10 解出

公交车共有 `n` 排座位，每排四个座位 `"A"`、`"B"`、`"C"`、`"D"`。`"A"`、`"D"` 靠窗，`"B"`、`"C"` 在中间；`"A"` 与 `"B"` 相邻，`"D"` 与 `"C"` 相邻。预订耗时规则：预订中间座位始终 1 秒；预订靠窗座位时，若其相邻的中间座位尚未被预订则 1 秒，已被预订则 3 秒。座位用 `"A1"`、`"D20"` 这样的字符串表示（字母 + 排号）。

实现 `BusBooking` 类：
- `BusBooking(int n)`：`n` 排空座位。
- `void toggle(string seat)`：该座位未被预订则预订，已被预订则释放。
- `int getTotalTime()`：当前所有已预订座位按 `toggle` 的调用顺序预订所需的总秒数；没有已预订座位返回 `0`。
- `int getMinTime()`：当前所有已预订座位可以任意调整预订顺序时的最小总秒数；没有已预订座位返回 `0`。

一个座位的耗时在其被预订的那一刻确定，之后预订或释放其他座位都不会改变它。`1 <= n <= 10^5`，`seat[0]` 是 `'A'`、`'B'`、`'C'`、`'D'` 之一，其余字符是整数 `row`，`1 <= row <= n`，`toggle`、`getTotalTime`、`getMinTime` 的调用总次数不超过 `10^5`。

例：`n = 20`，依次 `toggle("B3")`、`toggle("A3")`，`getTotalTime()` → `4`（`B3` 1 秒，`A3` 因 `B3` 已订而 3 秒），`getMinTime()` → `2`（先订 `A3` 再订 `B3`）；再 `toggle("C3")`、`toggle("D3")`，`getTotalTime()` → `8`，`getMinTime()` → `4`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 设计题（Design）：增量维护聚合值 + 「耗时在写入时快照」的状态记账。

**一句话。** 用字典 `cost` 记下每个已订座位**当时**的耗时，再维护一个运行总和 `total`：预订时算出耗时、记入字典并加到总和，释放时从字典取出该座位的耗时并从总和里减去；`getMinTime` 恒等于已订座位数，因为把所有靠窗座位排在中间座位之前订，每个座位都只要 1 秒。

**识别。** 「耗时在被预订时确定，之后不变」说明耗时是一份要**存下来**的快照，不能每次按当前座位集合重算；`10^5` 次调用要求每个操作 `O(1)`，所以总和必须增量维护，不能每次遍历。`getMinTime` 问的是「任意顺序」，要找的是最优顺序下的下界。

**推导。** 直接做：每次 `getTotalTime` 把已订座位按预订顺序重放一遍，`O(座位数)`，调用多了超时，而且释放中间座位后重放会改掉靠窗座位已经固定的 3 秒。改成快照：预订时只看相邻中间座位在不在 `cost` 里，决定 1 秒还是 3 秒；释放时把存下的耗时原样减掉。最小总时间：每个座位至少 1 秒；若让所有靠窗座位先订，那时它们的相邻中间座位都还没被订，耗时全是 1，所以下界 `座位数` 可以达到，答案就是 `len(cost)`。

```python
class BusBooking:
    def __init__(self, n: int):
        # 座位 -> 它被预订那一刻确定的耗时（之后不再变化）
        self.cost: dict[str, int] = {}
        self.total = 0                      # 所有已订座位耗时之和，增量维护

    def toggle(self, seat: str) -> None:
        if seat in self.cost:               # 已订：释放，减去当初存下的耗时（不重算）
            self.total -= self.cost.pop(seat)
            return
        col, row = seat[0], seat[1:]
        if col in "AD":
            # 靠窗座位：A 邻 B，D 邻 C；相邻中间座位已订则 3 秒，否则 1 秒
            mid = ("B" if col == "A" else "C") + row
            c = 3 if mid in self.cost else 1
        else:
            c = 1                           # 中间座位始终 1 秒
        self.cost[seat] = c
        self.total += c

    def getTotalTime(self) -> int:
        return self.total

    def getMinTime(self) -> int:
        # 最优顺序：先订全部靠窗座位，再订中间座位，每个座位都只要 1 秒
        return len(self.cost)
```

运行：示例 1 → `getTotalTime` `4`、`getMinTime` `2`，再订 `C3`、`D3` 后 `8`、`4`；示例 2（`C7`、`D7` 之后）→ `4`；`toggle("D7")`、`toggle("C7")`、`toggle("D7")` 之后 → `getTotalTime` `1`、`getMinTime` `1`。`toggle("B3")`、`toggle("A3")`、`toggle("B3")` 之后 → `getTotalTime` `3`、`getMinTime` `1`。

**复杂度。** 每个操作 `O(1)`；空间 `O(已订座位数)`，不依赖 `n`。

**易错点。**
- 释放后按当前座位集合重算总时间，忽略了耗时是快照：`toggle("B3")`、`toggle("A3")`、`toggle("B3")` 之后重算得到 `1`，正确是 `3`（`A3` 当初已经付了 3 秒）。
- 把相邻关系记错（`A` 邻 `C`、`D` 邻 `B`）：`toggle("C3")`、`toggle("A3")` 会误得 `4`，正确是 `2`。
- `getMinTime` 用「靠窗数 + 中间数 × ……」之类的公式或枚举排列：下界就是座位数，只要承认可以先订靠窗座位。

**同模式。** LC 380 O(1) 时间插入、删除和获取随机元素、LC 1352 最后 K 个数的乘积、LC 2349 设计数字容器系统、LC 1146 快照数组。
