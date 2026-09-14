# q34 · URL 压缩（分段 numeronym · 尾部折叠 · 歧义检测）

> `problems/q34_compress_url/` · 4 个 part · phone screen（~35 分钟活编码）
> **主题：纯字符串规范化 —— 唯一的难点是"折叠时点算不算字符"。**

## 一句话题意

把 URL 按 `/` 切成**大段**，每段再按 `.` 切成**小段**，每个小段压成 numeronym
`w[0] + str(len(w) - 2) + w[-1]`（`internationalization` → `i18n`）。
Part 2 限制每个大段最多保留 `m` 个小段，多出来的**折叠成一个**。

## 核心考点

`S02` 解析 · `S09` 精确格式 · **`S14` 字符串规范化** · `S19` 增量 · `S20` 自测

## 解题思路

### Part 1

```python
def numeronym(w): return f"{w[0]}{len(w) - 2}{w[-1]}"
def compress(url):
    return "/".join(".".join(numeronym(mn) for mn in mj.split("."))
                    for mj in url.split("/"))
```

短词会得到奇怪但**正确**的结果：`to` → `t0o`，`a` → `a-1a`（这是源 Java 的输出）。

### Part 2 — 尾部折叠

大段的小段数 > `m` 时：前 `m-1` 个照 Part 1 压，
**从第 m 个小段到最后**（**包括中间的点**）折成一个 numeronym：

```
第 m 个小段的首字母 + (它和最后一个小段末字母之间的字符数，点也算) + 最后一个小段的末字母
```

小段数 **≤ `m`** 的大段与 Part 1 完全相同（**不折叠**）。
`m = 1` 因此把整个大段折成一个：`stripe.com` → `s8m`，`customer.maria` → `c12a`（不是 `c6r.m3a`）。

### Part 3 — 最小长度阈值（重构）

小段（或 Part 2 折出来的尾巴）字符数 **< `min_len`** 时**原样输出**（`len == min_len` 仍压缩）。
Part 1–2 的 `min_len = 0`。`min_len = 3` 时：`ab` 保持 `ab`，`abc` → `a1c`。

### Part 4 — 解压歧义（重构）

numeronym 是有损的：`payments` 和 `pastries` 都变成 `p6s`。
给一份 URL 日志，报告每个被 **≥ 2 个不同原串**共享的压缩形式，以及不同原串的个数，
按压缩串排序。**完全相同的重复 URL 只算一次。**

## 坑

1. **小段数恰好等于 `m` 的大段不折叠**（和 Part 1 相同）。
2. **`m = 1` 折叠整个大段，包括它的点**。
3. 3 字母的词 → `x1x`；Part 3 的边界：`len < min_len` 原样，`len == min_len` 压缩；
   无阈值时 `to` → `t0o`、`a` → `a-1a`。
4. 没有任何分隔符的单个词；只有一个大段但小段很多的 URL。
5. Part 4：**完全重复的 URL 只算一次**；只有一个原串的压缩形式**不打印**；按压缩串的普通字符串序排。
6. **Part 3 的阈值也作用在折出来的尾巴上**（`a.b` 是 3 个字符 → `min_len=3` 时压成 `a1b`）。

## 变体

- 先做一个纯 numeronym 热身（`internationalization` → `i18n`，`localization` → `l10n`）再套 URL。
- 用哈希代替 numeronym（题面自己说现实中的修法就是哈希）。

## Code Core 节点

**`algorithms.strings`** · `input.normalization` · `output.formatting` · `correctness.edge-catalog`

## 自测清单

- [ ] 小段数 `== m` / `> m`
- [ ] `m = 1` 的整段折叠（含点）
- [ ] 1 / 2 / 3 字母的词
- [ ] `min_len` 的 `<` / `==` 边界；作用在尾巴上
- [ ] 无分隔符的单词
- [ ] Part 4：重复 URL 只算一次；单原串的不打印；排序
