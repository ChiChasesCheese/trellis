# qA10 · LC 161 一次编辑距离（+ 相邻交换 + 命名编辑 + k 次以内）

> `problems/qA10_lc161_one_edit_distance/` · 4 个 part · LC Stripe tag 频率 61–67
> **主题：五分钟的题，但"完全相同返回 false"是最常见的错。**

## 一句话题意

`s` 和 `t` 是否**恰好相差一次编辑**（插入 / 删除 / 替换）。

## 解题思路

```python
def is_one_edit_distance(s, t) -> bool:
    if len(s) > len(t): s, t = t, s              # 保证 len(s) <= len(t)
    if len(t) - len(s) > 1: return False
    for i, (x, y) in enumerate(zip(s, t)):
        if x != y:
            return s[i+1:] == t[i+1:] if len(s) == len(t) else s[i:] == t[i+1:]
    return len(s) + 1 == len(t)                  # ★ 前缀全同 → 只能是末尾多一个；相同则 False
}
```

单趟 O(n)，O(1) 额外空间（切片在第一个不匹配处就停）。

### Part 2 — 相邻交换也算一次编辑

Part 1，**或者** `len(s) == len(t)` 且恰好在 `i` 和 `i+1` 两处不同，
且 `s[i] == t[i+1]` 且 `s[i+1] == t[i]`（**两个不同字符**的换位；
交换两个相同字符什么都没变，不算编辑）。
这就是 q05 Part 4 的规则（"一位被改 或 相邻两位被交换"）。

### Part 3 — 命名这次编辑

`Edit(kind, index, char)`（`delete` 和 `swap` 的 `char` 是 `""`）。
**确定性**：`index` 是 `s` 和 `t` **第一个不同的下标**
（`s` 是 `t` 的真前缀时是 `len(s)`，所以 `"aa" → "aaa"` 是 `insert 2 a`，**不是** `insert 0 a`）。
四种 kind 不会撞车：`swap` 改两个位置，`replace` 改一个，`insert`/`delete` 改长度。

### Part 4 — k 次以内（带状 DP）

Levenshtein 距离 ≤ k。要求：
- `abs(len(s) - len(t)) > k` → 立刻 false；
- `k = 0` → 相等判断；
- **DP 必须是带状的** —— 只算 `|i − j| <= k` 的格子，O(k·n) 时间、O(k) 内存。
  `n = 10^4, k = 50` 要远低于一秒，而完整的 O(n·m) 表做不到。

`within_k_edits(s, t, 1)` == `s == t or is_one_edit_distance(s, t)`。

## 坑

1. **完全相同 → false**（最常见的错误答案），包括两个空串。
2. 一个空、另一个长度 1 → true；长度 2 → false。
3. 差别在**最后一个**字符；多出的字符在**最开头**或**最末尾**。
4. **"第一个不匹配"必须扫出来**，不能假设多出的字符在末尾。
5. Part 2：**交换两个相同字符不算编辑**；`"ab"/"ba"` 不是 replace。
6. Part 3：插入的下标是第一个不匹配处（`"aa"/"aaa"` → 2）。
7. Part 4：长度差单独就能否决；带的边缘 `|i − j| == k`；`k = 0`。

## 变体

- q05 Part 4：枚举所有相距一次编辑/交换的串，保留合法卡号。
- LC 72（完整 Levenshtein）、LC 583 —— 不带状的 DP。
- 风控里的"`t` 是不是 `s` 的笔误？"：Damerau 距离 ≤ 1 + 大小写折叠（q06 的风格）。

## Code Core 节点

**`algorithms.strings`** · **`algorithms.dp`**（带状 DP） · `correctness.edge-catalog` ·
`performance.budget`

## 自测清单

- [ ] 完全相同 / 两个空串
- [ ] `""` vs `"a"` / `""` vs `"ab"`
- [ ] 差别在末字符 / 多的字符在最前 / 在最后
- [ ] Part 2：相同字符交换 / `"ab"` vs `"ba"`
- [ ] Part 3：`"aa"` → `"aaa"` 的 index
- [ ] Part 4：长度差 > k / `k = 0` / `n=10^4, k=50` 的耗时
