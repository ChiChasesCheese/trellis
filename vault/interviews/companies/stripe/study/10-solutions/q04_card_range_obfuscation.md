# q04 · 卡号区间混淆（补齐 BIN 内的空隙）

> `problems/q04_card_range_obfuscation/` · 4 个 part
> **本题的主题只有一个：闭区间的 off-by-one。**

## 一句话题意

给一个 6 位 BIN 和若干条 `[start, end] → brand` 的区间（10 位偏移量，**闭区间**），
把整个 BIN 范围 `[BIN·10^10, BIN·10^10 + 9999999999]` 补满，再合并同品牌的相邻区间，
按规范顺序输出 16 位补零的完整卡号区间。

## 输入 / 输出

```
PART n          可选，1..4，缺省 = 4
424242          6 位 BIN
N               区间条数（可能是 0）
start,end,brand N 行；start/end 是 BIN 之后的 10 位偏移，闭区间
```

输出：`start,end,brand`，start/end 是 **16 位补零**的完整数字（`%016d`），
按**最终值**的 `(start, end, brand)` 升序。`N = 0` 时什么都不输出。

## 核心考点

`S01` 读全 spec · `S02` 解析 · `S08` 三键排序 · **`S09` 16 位补零** ·
**`S13` 闭区间 / 补空隙 / off-by-one** · `S19` 增量 · `S20` 自测（相邻 vs 空隙）

## 解题思路

`LO = BIN*10**10`，`HI = LO + 9999999999`。**全程整数**（约 10^16，超出 float 精确范围）。

### Part 1 — 补两端

```python
ivs.sort(key=lambda t: (t.start, t.end, t.brand))
ivs[argmin_start].start = LO
ivs[argmax_end].end     = HI
```

只有一条区间时它变成整个 BIN 范围。

### Part 2 — 补内部空隙（向上延伸**下面**那条）

```python
covered_end = -1
owner = None
for iv in sorted(ivs):
    if owner is not None and iv.start > covered_end + 1:     # ← +1 是关键
        owner.end = iv.start - 1                             # ← -1 是关键
    if iv.end > covered_end:
        covered_end, owner = iv.end, iv
```

- `end + 1 == next.start` 是**相邻**，不是空隙，不动它。
- 重叠区间**不裁剪**，原样输出。

### Part 3 — 嵌套区间

被延伸的是**持有当前最大 end** 的那条，**不是**打印顺序上紧挨着空隙的那条。
`owner` 只在 `iv.end > covered_end` 时更新 —— 上面的代码已经是对的。

最大 end 相同时，取 `start` 较小的（即包住另一条的那条）；完全相同则取排序后靠前的。

### Part 4 — 合并同品牌

```python
out = []
for iv in sorted(ivs, key=lambda t: (t.start, t.end, t.brand)):
    if out and out[-1].brand == iv.brand and iv.start <= out[-1].end + 1:   # 相邻或重叠
        out[-1].end = max(out[-1].end, iv.end)
    else:
        out.append(iv)
```

**品牌是精确字符串比较**（`VISA` ≠ `Visa`），不同品牌即使相邻也不合并。

## 坑

1. **闭区间**：空隙填到 `next.start - 1`，永远不是 `next.start`。
2. **相邻不是空隙**：`end + 1 == next.start` 时不动它，也不因为"相邻"就合并不同品牌。
3. **前导零**：`0000000000` 要能 `int()` 解析，输出要 `%016d` 补零。
4. **输入可能无序**：延伸**前**和延伸**后**都排序（按最终值排）。
5. **嵌套区间**：延伸了被包住的那条 = Part 3 的经典失败。
6. **完全重复的区间**：Part 1–3 保留成两行，Part 4 合并成一行。
7. **品牌精确匹配**，原样输出。
8. `N = 0` 输出空；`N = 1` 输出整个 BIN 范围。
9. **整数运算**：`BIN·10^10 + 9999999999 ≈ 10^16`，float 在这个量级已经不能区分相邻整数。

## 变体

- 输入直接给 16 位完整卡号（而不是 10 位偏移）：任何 ≥ 10^10 的 token 当完整号处理。
- 没有 `PART` 行时默认应用全部规则（Part 4）。

## Code Core 节点

**`chrono.intervals`**（区间的合并/补空隙在这个叶子） · `output.formatting`（补零） ·
`output.ordering` · `algorithms.greedy`（扫描线） · `correctness.edge-catalog`

## 自测清单

- [ ] 题面的 worked example
- [ ] `N = 0` / `N = 1`
- [ ] 相邻区间（`end+1 == next.start`）不被当空隙
- [ ] 嵌套区间：延伸的是外层
- [ ] 输入乱序
- [ ] 完全重复的区间在 Part 3 / Part 4 的不同行为
- [ ] `VISA` 和 `Visa` 不合并
- [ ] 前导零的解析与 16 位补零输出
