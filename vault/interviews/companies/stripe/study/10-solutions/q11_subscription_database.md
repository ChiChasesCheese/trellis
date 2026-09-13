# q11 · 订阅数据库（start / end / check，时长先"替换"后"累加"）

> `problems/q11_subscription_database/` · 3 个 part
> **主题：Part 3 把 Part 2 的规则反过来了 —— 这就是"必须读完全部 part"的教科书例子。**

## 一句话题意

每行 `timestamp,op,user[,duration]`，`op ∈ {start, end, check}`。
只有 `check` 有输出（`active` / `inactive`）。
Part 2 的新 `start` **替换**旧订阅，Part 3 的新 `start` **在当前到期时间上累加**。

## 输入 / 输出

```
PART n
timestamp,op,user[,duration]      timestamp/duration 非负整数；user 大小写敏感
```
**事件按输入顺序处理，不按 timestamp 重排。** 最多 2·10^5 行。
输出：每个 `check` 一行，按输入序。

## 核心考点

**`S01` 读完全部 part（P3 翻转 P2）** · `S02` 可选第 4 字段 · `S03` 每用户状态 ·
**`S05` 闭区间边界** · `S10` 带取消的有序事件流 · `S12` 时长算术 · `S19` 一个 `simulate(mode)`

## 解题思路

**一个函数三种模式**，别写三份：

```python
def simulate(events, mode):        # mode ∈ {1, 2, 3}
    exp = {}      # user → 到期时间；None 表示无限期；不在字典里 = 未订阅
    out = []
    for t, op, user, d in events:
        if op == "start":
            if mode == 1 or d is None:
                exp[user] = None                              # 无限期
            elif mode == 2:
                exp[user] = t + d                             # 替换
            else:  # mode 3，累加
                cur = exp.get(user, "none")
                if cur is None:        pass                   # 无限期不受影响
                elif cur == "none" or t > cur:  exp[user] = t + d      # 没有 / 已过期 → 从 t 起
                else:                  exp[user] = cur + d    # ★ 从**当前到期**累加
        elif op == "end":
            exp.pop(user, None)                               # 未订阅 → no-op
        else:  # check
            e = exp.get(user, "none")
            out.append("active" if e is None or (e != "none" and t <= e) else "inactive")
    return out
```

**闭区间**：`c <= t + d` 是 active。样例：`1,start,Michael,9` → 10 时 active，11 时 inactive。

**Part 3 的累加是从"当前到期"算，不是从新 start 的时间戳算。**
样例：`1,start,M,10`（到期 11）然后 `2,start,M,4` → 到期 `11 + 4 = 15`，不是 `2 + 4`。

Part 3 的四个角落（题面明确）：
- 无限期订阅不被任何后来的 `start` 影响。
- 有限期上来一个**不带 duration** 的 `start` → 变无限期。
- 已过期 / 已 `end` / 从未有过 → 从新 start 的时间戳重新开始：`t + d`。
- "在 t 时仍 active" 用**同样的闭区间判定**（`t <= cur`），所以恰好在到期日 start 会延长。

## 坑

1. **P3 翻转 P2**：replace vs accumulate。读到 P3 才动手，P2 的代码就白写了。
2. **闭区间**：`start + d` 时 active，`+1` 时 inactive。`d = 0` → 只有 `t` 当天 active。
3. **同时间戳按输入序**：`5,start,A` 后 `5,check,A` → active；`5,end,A` 后 `5,check,A` → inactive。
4. `end` 未订阅的用户 / `end` 两次 → no-op。
5. Part 2：无 duration 的 start 在有限期之后 → 变无限期；有限期在无限期之后 → **缩短**（替换）。
6. Part 3：**从当前到期累加**，不是从新 start；已过期则从新 start 重开；无限期永不缩短。
7. 用户之间完全独立；**用户名大小写敏感**（`michael` ≠ `Michael`）。
8. **时间戳倒退也照输入序处理**（不重排）。
9. 只有 `check` 有输出；无 check → 无输出。

## 变体

- 原题返回 `list[str]`（start/end 返回 `""`）；这里只打印 check 的结果。
- q07 用同一套 `start + duration` / `RENEW,+n` 词汇 ——「续期延长结束日」就是这里 Part 3 的规则。

## Code Core 节点

**`round.reading`**（P3 翻转 P2） · `model.entity-state` · `model.event-stream` ·
**`chrono.intervals`**（闭区间） · `chrono.arithmetic` · `output.sentinels`

## 自测清单

- [ ] check 在任何 start 之前 / 未知用户 → inactive
- [ ] `start+d` active、`+1` inactive、`d=0`
- [ ] 同时间戳 start→check、end→check
- [ ] end 未订阅 / end 两次
- [ ] P2：无 duration 覆盖有限期、有限期覆盖无限期
- [ ] P3：从当前到期累加、已过期重开、无限期不变、恰好在到期日 start
- [ ] 大小写敏感的用户名
- [ ] 时间戳倒退
