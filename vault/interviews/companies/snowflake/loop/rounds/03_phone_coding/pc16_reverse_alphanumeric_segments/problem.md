# pc16 · Reverse Alphanumeric Segments — 双指针分段翻转 → 原地 O(1) 空间

> TrueInterview 87 题清单第 8 题，2026-06 报告。Part 1 是一手预览原题；Part 2 **(reconstructed)**。

## 背景

TrueInterview 聚合站（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 8 行、§3）列出 Snowflake 一轮 Algorithm 题 "Reverse Alphanumeric Segments"，公开预览只给出题干一句话和
`We're → eW'er` 的例子；题面付费，具体的多 Part 结构、边界规则、追问均未知，本 kit 按同类"字符串分段变换"题的常见
追问顺序重建 Part 2。

## 输入

一个字符串（可能包含空格、标点、Unicode 字符、空字符串）。

## API 契约（英文签名）

```python
def reverse_alnum_segments(s: str) -> str
def reverse_alnum_segments_inplace(chars: list) -> None
```

## 规则

把字符串看成"字母数字游程"（`str.isalnum()` 为真的最长连续段）与"边界字符"（其余字符，包括空格、
标点、撇号）交替出现的序列；边界字符原地不动，每一段字母数字游程整体反转。

### Part 1 — 任意正确解法（一手原题）

`reverse_alnum_segments(s)` 返回新字符串。双指针扫描：遇到字母数字就找到这一段的右端，
段内首尾交换直至相遇，再跳过后面的边界字符继续扫描。`We're` 中 `'` 是边界，两段 `We`、`re` 各自反转，
拼回 `eW` + `'` + `er` = `eW'er`。

### Part 2 — 原地、O(1) 额外空间、Unicode-aware **(reconstructed)**

`reverse_alnum_segments_inplace(chars)` 直接修改传入的 `list[str]`（每个元素一个字符），不返回值，
不得新建一个等长的容器（除了输入本身）。因为 Python 的 `str.isalnum()` 本身就是 Unicode-aware
的（`'é'`、`'字'` 都算字母数字），这一版本不需要额外处理 Unicode——它就是把 Part 1 的"新建字符串"
换成"原地双指针交换"。已知局限（不测试）：把组合字符（combining marks）当作独立 code point 处理，
不做字形聚类（grapheme clustering）。

## Worked examples（全部由 `solution.py` 实际运行得出）

- `reverse_alnum_segments("We're")` = `"eW'er"`
- `reverse_alnum_segments("café123!")` = `"321éfac!"`（`é` 算字母数字，`café123` 是一整段）
- `reverse_alnum_segments("")` = `""`
- `reverse_alnum_segments("!!!")` = `"!!!"`
- `reverse_alnum_segments_inplace(list("ab12-cd"))` → `"21ba-dc"`

## `main()` 命令流

```
PART 1              PART 2
We're               We're
abc                 →eW'er
→eW'er
cba
```
每行一个字符串（**空行是合法输入**，代表空字符串，不会被 `main()` 过滤——这与本 kit 其它以数字为输入的题
不同，那些题会跳过空行）。

## 边界清单

- 空字符串、空行（合法输入，不是"跳过"）
- 整串全是字母数字（一整段）/ 整串全是边界字符（不变）
- 首尾就是边界字符
- Unicode 字母（`café`、`漢字`）与数字混合在同一段
- Part 2 必须修改同一个 list 对象（不能返回新 list 换掉引用）

## 追问

1. **为什么不用 `re.split` 建新 list 再拼？** 可以，但那是 O(n) 额外空间；Part 2 的追问就是砍掉这份空间。
2. **如果输入是不可变的 `str`，怎么做到"原地"？** 做不到——这正是 Part 2 的 API 签名从 `str` 换成
   `list[str]` 的原因：`str` 在 Python 里不可变，O(1) 空间原地修改必须换成可变序列。
3. **多字节 Unicode 呢？** 如果按 UTF-8 字节而不是 code point 处理，一个多字节字符的字节可能被单独
   反转导致乱码；本题在 Python 的 `str`/`list[str]` 层面操作，天然按 code point 对齐，不会遇到这个坑。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，2026-06 报告，"Reverse Alphanumeric Segments"，Algorithm。见
  `../../../catalog/raw/github_repos.md` §2 第 8 行、§3。
- Part 2（原地 / O(1) / Unicode-aware 追问）为重建，基于同类"分段变换"题在电面中的常见追问顺序。

## 考什么

S02 双指针（段内反转）· S01 一遍扫描识别边界 · 从"新建容器"压到"原地 O(1) 空间"（与 pc06 Part 2 同一
压缩方向，但这里是字符串题而不是判环）。
