# qA04 · LC 1169 非法交易（金额上限 + 60 分钟内异地）

> `problems/qA04_lc1169_invalid_transactions/` · 3 个 part · **唯一进入 6 个月榜单的题，频率 100**
> **主题：分组 + 排序 + 窗口 —— Radar 速度规则的骨架。**

## 一句话题意

交易 `name,time,amount,city`。非法 ⟺ `amount > 1000`，**或**存在同名交易，
时间差 ≤ 60 分钟且**城市不同**。

## 解题思路

### Part 1

```python
by_name = defaultdict(list)
for i, t in enumerate(txs): by_name[t.name].append((t.time, i, t))
for name, lst in by_name.items():
    lst.sort()                                  # (time, 输入下标)
    # 滑窗 [t-60, t+60]，窗口内维护 city 的计数
    # 第 i 笔 city-非法 ⟺ window_size - count[city_i] > 0
```

`amount > 1000` 与上面的条件**取或**。输出按**输入顺序**；
**完全相同的重复字符串各自报告一次**（一笔交易不会和自己冲突 —— 城市相同）。

### Part 2 — 理由

`Verdict(index, transaction, reasons)`，按输入序。
`reasons` 里 `"amount>1000"` **在前**（如适用），然后每个冲突的交易一条
`"city:<对方的交易字符串>"`，按对方的 `(time, 输入下标)` 排序。
合法交易不产生 Verdict。

### Part 3 — 流式

交易**按时间非递减**到达（倒退则 `ValueError`）。
`add` 返回**因这次到达而变成非法的**交易，顺序是
[窗口内更早的冲突项按 `(time, 到达序)`，然后这次到达的本身]；
**每笔交易整体只报告一次**。
按 name 淘汰 `now - window` 之前的历史，内存被一个窗口的流量界住。

## 坑

1. **金额恰好 1000 合法，1001 非法。**
2. **时间差恰好 60 → 冲突；61 → 不冲突**；**对称**（更早的那笔也非法）。
3. **同名同城，任何时间差都不冲突。**
4. **完全相同的重复字符串**：各报一次，但**不是因为彼此**。
5. 交易可能**不按时间给出**（先排序）；同一分钟里同名交易很多时，
   **窗口计数不能退化成 O(n²)**（用 city 计数器，不要两两比较）。
6. Part 3 的淘汰边界（`now - 60` **仍在**窗口内）、到达序的平手、**不重复报告**。

## 变体

- q01（MCC / 争议密度）和 q02（小时密度）是这一题的多 part 生长形态。
- 返回下标而不是字符串；返回合法交易的集合。

## Code Core 节点

**`algorithms.sliding-window`** · **`rules.grouping`** · `chrono.windows` ·
`rules.thresholds` · `output.ordering` · `performance.hot-loop`

## 自测清单

- [ ] 金额 1000 / 1001
- [ ] 时间差 60 / 61；对称性
- [ ] 同名同城
- [ ] 完全相同的重复字符串
- [ ] 输入不按时间序
- [ ] 同一分钟大量同名交易的耗时
- [ ] Part 3 的淘汰边界与不重复报告
