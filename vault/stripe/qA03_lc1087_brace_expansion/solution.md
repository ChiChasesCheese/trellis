# qA03 · LC 1087 花括号展开（栈 · 回溯 · 嵌套 · 计数与第 k 个）

> `problems/qA03_lc1087_brace_expansion/` · 4 个 part · LC Stripe tag 频率 82–89
> **主题：栈解析 + 笛卡尔积 + 排序 —— phone screen 的三件套。**

## 一句话题意

`{a,b}c{d,e}` 展开成 `acd ace bcd bce`。返回**排序去重**后的全部结果。

## 解题思路

### Part 1 — 迭代（栈）

先把字符串切成**段**：字面量是只有一个选项的段，`{…}` 是按 `,` 切分的一组 token
（token 可以多字符，也可以是空串）。然后迭代展开：

```python
words = [""]
for seg in segments:                      # seg 是选项列表
    words = [w + opt for w in words for opt in seg]
return sorted(set(words))
```

**`echo_malformed=True`（Stripe 筛选变体）**：模板畸形时（没有 `{`、`{` 没配 `}`、
`}` 在 `{` 之前、**嵌套的 `{`**）**或任何一组 token 少于 2 个** → 原样返回 `[s]`。

### Part 2 — 递归回溯

`dfs(i, prefix)`，结果必须与 Part 1 完全一致。

### Part 3 — 嵌套（LC 1096 语法）

花括号可以嵌套，组内的逗号分隔的**候选**本身可以含组：
`{a,b}{c,{d,e}}` → `ac ad ae bc bd be`；
`{{a,z},a{b,c},{ab,z}}` → `a ab ac z`（**并集去重**）。

**拼接 = 笛卡尔积，逗号 = 集合并。**
用一个 `(alternatives, current)` 的帧栈：遇 `{` 入栈，遇 `}` 出栈。

### Part 4 — 计数与第 k 个

`count_expansions(s)` = 各组**去重后**选项数的乘积（字面量算 1），**不生成任何词**。
`kth_expansion(s, k)`（1-based）= **选择序**下的第 k 个：
每组的去重选项排序，**最左的组是最高位**，对 `k-1` 做混合进制分解。

在 LC 1087 的语法下（单字母选项），**选择序就是词典序**，所以
`kth_expansion(s, k) == brace_expansion(s)[k-1]`。
**多字符 token 时两者可能不同 —— 面试时要说出来。**

## 坑

1. 完全没有花括号 → 返回字符串本身；组在开头 / 结尾；相邻的组 `{a,b}{c,d}`。
2. **空 token `{,.bak}`** 和**重复 token `{a,a,b}`**（去重后排序）。
3. **组内选项无序给出（`{b,a}`）时，输出仍要全局排序**（不是每组内排）。
4. 筛选变体的畸形模板：缺 `{`、反序、嵌套、`{}`、`{x}`（只有一个 token）。
5. Part 3：嵌套并集去重；空候选 `{a,}`。
6. Part 4：模板的展开量可能达到 10^20，**绝不能真的生成**。

## 变体

- 只支持单个组 + 畸形回显（`echo_malformed` 标志）。
- 花括号里有空格（`"abc{xyzzy,zyx}d{aa, bb}a"`）—— 面试官说要 strip 才 strip。
- LC 1096 的嵌套语法 —— Part 3。

## Code Core 节点

**`algorithms.backtracking`**（枚举、计数、第 k 个） · **`input.grammar`**（栈解析） ·
`algorithms.strings` · `toolbox.deque`（栈） · `output.ordering`

## 自测清单

- [ ] 无花括号 / 组在首 / 组在尾 / 相邻组
- [ ] 空 token / 重复 token / 无序 token
- [ ] 五种畸形模板
- [ ] 嵌套 + 并集去重 + `{a,}`
- [ ] `count_expansions` 在 10^20 规模上瞬间返回
- [ ] `kth_expansion(s, k) == brace_expansion(s)[k-1]`（单字母时）
