# qA07 · LC 56 合并区间 + LC 1288 移除被覆盖区间

> `problems/qA07_intervals_merge_covered/` · 4 个 part · LC Stripe tag 频率 62
> **主题：一次排序 + 一次线性扫描，难点全在端点语义。**

## 一句话题意

P1 合并重叠区间；P2 数出被完全覆盖的区间；P3 是 q04 的品牌补空隙；P4 是**整数闭区间**版的合并。

## 解题思路

### Part 1 — LC 56（实数语义）

```python
def merge(intervals):
    out = []
    for lo, hi in sorted(intervals):            # 按 (start, end)
        if out and lo <= out[-1][1]:            # ★ 端点相接也合并
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return out
```

### Part 2 — LC 1288（排序方向是全部）

```python
count, max_end = 0, float("-inf")
for lo, hi in sorted(intervals, key=lambda t: (t[0], -t[1])):   # ★ start 升、end 降
    if hi > max_end: max_end = hi                                # 存活
    else:            count += 1                                  # 被覆盖
```

**`end` 降序是关键**：否则 `[1,10]` 排在 `[1,4]` 之后时，`[1,10]` 会被误判为被覆盖。
LC 保证区间唯一；这里**重复区间互相覆盖，只有一份存活**。

### Part 3 — 品牌补空隙（与 q04 打通）

`Labeled(start, end, label)`，**整数闭区间**，全部在 `[lo, hi]` 内。按 q04 的三步：
1. 最小 start 的那条延到 `lo`，最大 end 的那条延到 `hi`
   （最大 end 平手时取 start 较小的，即**包住别人的那条**）；
2. 按 `(start, end, label)` 扫，跟踪 `covered_end` 及其**持有者**（最大 end；平手取 start 小的、再取靠前的）；
   `next.start > covered_end + 1` 时把**持有者**延到 `next.start - 1`；
   **嵌套的区间保持自己的边界**（只有持有者会长）；
3. 合并排序后**相邻**且 label 相同且相接/重叠（`next.start <= cur.end + 1`）的项。

### Part 4 — 整数闭区间的合并

```python
if lo <= out[-1][1] + 1:      # ★ +1：[1,2] 与 [3,4] 相邻，要合并成 [1,4]
```
`[1,2]` 与 `[4,5]` **不合并**（3 没被覆盖）。

**Part 1 和 Part 4 的唯一差别就是那个 `+ 1`** —— 这就是"实数语义"和"整数语义"的区别。

## 坑

1. 输入未排序；**端点相接（`[1,4],[4,5]`）在 P1 合并**；
   **相邻整数只在 P4 合并**。
2. 单个区间；空列表；**零长度区间 `[5,5]`**；重复区间。
3. P2：相同 start 不同 end（**end 必须降序**）；覆盖一切的区间；
   链式 `[1,10],[2,9],[3,8]` → 1 个存活；相同区间只活一份。
4. P3：**嵌套区间不能被延伸**；最大 end 平手取包住别人的那条；
   同 label 中间隔着别的 label 时**不合并**；单个区间变成整个范围。
5. 坐标到 10^5、n 到 10^4 / 10^5 —— O(n log n)。

## 变体

- q04 卡号区间混淆（16 位补零输出、BIN 前缀）。
- q29 部署窗口（allowed 减 freeze，半开分钟）。
- LC 435 最少移除数 / LC 986 区间交集（不在 Stripe tag 里）。

## Code Core 节点

**`chrono.intervals`** · **`output.ordering`**（`(start, -end)` 的排序方向） ·
`algorithms.greedy`（扫描线） · `algorithms.recognition`

## 自测清单

- [ ] 未排序输入 / 端点相接 / 相邻整数（P1 vs P4）
- [ ] 单区间 / 空列表 / `[5,5]` / 重复
- [ ] P2 的 end 降序（把它改成升序，确认 `[1,10],[1,4]` 变错）
- [ ] 链式覆盖 `[1,10],[2,9],[3,8]`
- [ ] P3 的嵌套区间、平手持有者、隔断的同 label
- [ ] 10^5 规模的耗时
