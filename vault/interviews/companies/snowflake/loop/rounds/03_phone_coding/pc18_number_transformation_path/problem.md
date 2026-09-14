# pc18 · Number Transformation Path — 任意路径（宇称推理）→ 有界 BFS 求最短

> TrueInterview 87 题清单第 9 题，2026-06 报告。三种操作、`transform` 的签名与"不必最短、不可达返回
> None/抛错"是一手预览原文；split 的定义域（只对偶数生效）是本 kit 的重建选择，用来让"不可达"真正发生。
> Part 2 **(reconstructed)**。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 9 行、§3）列出 Snowflake 一轮 Algorithm 题 "Number Transformation Path"：三种操作
`add(+2)` / `sub(-2)` / `split(floor(/2))`，`transform(a, b)` 返回从 `a` 到 `b`（含首尾）的正整数序列，
**不要求最短**，不可达时返回 `None` 或抛错。预览没有说明 `split` 能否作用于奇数——这直接决定了题目
是否存在真正"不可达"的情况（如果 `split` 对任何正整数都合法，可以证明从任意 `a` 出发总能构造出到达任意
`b` 的路径，见下面"追问 1"；那样"返回 None"这个分支永远不会触发，和题面"return None when impossible"
的措辞矛盾）。为了让不可达真的存在、并对上"宇称"这条提示，本 kit 采用最常见的教学定义：
**`split` 只在当前数是偶数时可用**（结果 `n // 2` 恰好整除，不损失信息）；对奇数调用 `split` 是非法操作。

## 输入

一对正整数 `a, b`。

## API 契约（英文签名）

```python
def transform(a: int, b: int) -> list[int] | None
def shortest_transform(a: int, b: int) -> list[int] | None
```
`a < 1` 或 `b < 1` → `ValueError`。

## 规则

从正整数 `n` 出发，允许的操作：
- `add`：`n → n + 2`（总是合法）
- `sub`：`n → n - 2`（只有结果仍 `≥ 1` 才合法）
- `split`：`n → n // 2`，**仅当 `n` 是偶数时合法** **(reconstructed，声明的选择)**

`add` / `sub` 永远不改变奇偶性；只有 `split` 能改变奇偶性，而且它只能从偶数出发。因此：

- 若 `a` 是**奇数**：永远碰不到任何偶数（想离开奇数集合必须先 `split`，但 `split` 需要偶数输入，
  奇数集合里没有偶数可以 `split`）——只能在奇数集合内用 `add`/`sub` 平移。**结论：`b` 必须也是奇数，
  否则不可达。**
- 若 `a` 是**偶数**：可以先用 `add`/`sub` 平移到偶数 `2b`，再 `split` 一次恰好落到 `b`（如果 `b`
  本身是偶数，直接平移过去，不需要 `split`）。**结论：任意 `b ≥ 1` 都可达。**

### Part 1 — 任意正确路径（一手原题）

`transform(a, b)`：按上面规则构造任意一条合法路径；`a` 奇 `b` 偶时返回 `None`。

### Part 2 — 最短路径，有界 BFS **(reconstructed)**

`shortest_transform(a, b)`：和 `transform` 同样的不可达判定，但要求路径**最短**。数值理论上可以
无限大，BFS 必须设一个"足够大但有限"的搜索上界——Part 1 的构造已经证明，从 `a` 出发只需要平移到
`2b`（至多）就能一步 `split` 命中 `b`，所以最优解不可能需要探索比 `2·max(a,b) + 4` 更远的地方
（预留一点余量给往下 `sub` 的方向）。

## Worked examples（全部由 `solution.py` 实际运行得出）

- `transform(5, 5)` = `[5]`
- `transform(1, 7)` = `[1, 3, 5, 7]`（同奇偶，直接平移）
- `transform(4, 7)` = `[4, 6, 8, 10, 12, 14, 7]`（偶→奇：平移到 `2*7=14` 再 `split`）
- `transform(7, 4)` = `None`（奇 → 偶，不可达）
- `transform(2, 1)` = `[2, 1]`（`split(2) = 1`）
- `shortest_transform(4, 7)` = `[4, 6, 3, 5, 7]`（4 步：`split(6)=3` 比先平移到 14 再切短得多）
- `shortest_transform(1, 7)` = `[1, 3, 5, 7]`（同奇偶时直接平移已经是最短）
- `shortest_transform(100, 1)` = `[100, 50, 48, 24, 12, 6, 3, 1]`（7 步）

## `main()` 命令流

```
PART 1              PART 2
5 5                 1 7
7 4                 → 1 3 5 7
→ 5
  IMPOSSIBLE
```
每行 `a b`；不可达输出字面量 `IMPOSSIBLE`。

## 边界清单

- `a == b`（路径就是 `[a]`，不使用任何操作）
- 奇数 `a` → 偶数 `b`：两个 Part 都必须返回 `None`
- `split` 降到 `1`（`2 → 1`）之后不能再 `split`（`1` 是奇数）也不能再 `sub`（`1 - 2 < 1`），只能 `add`
- `a ≤ 0` 或 `b ≤ 0` → `ValueError`
- Part 2 的搜索上界要覆盖 Part 1 构造用到的最大中间值（`2 * max(a, b)`），否则会漏解

## 追问

1. **如果 `split` 对奇数也合法（`floor` 到底），还会有不可达的情况吗？** 不会——这正是本 kit 选择
   "`split` 仅偶数可用"这条重建规则的原因：如果奇数也能 `split`（比如从奇数 `2k+1` 切到 `k`），可以证明
   任选中间值 `m`（与 `a` 同奇偶）使得 `m // 2 == b`，任意 `a, b` 都能一步连通，"返回 None" 这个分支就
   永远不会触发，和题面"不可达返回 None"的措辞矛盾。面试里如果对方给的是"任意数都能 split"版本，就该
   主动追问"真的存在不可达的情况吗？"
2. **BFS 上界怎么证明足够？** 不严格证明最优性，只需要证明"至少不会漏掉比已知构造更短的解"：Part 1
   的构造给出了一个可行解，其路径上出现的最大值是 `max(a, 2b)`；最优解不会需要探索比这更远、又没有
   任何理由绕远路的状态，`2·max(a,b)+4` 留了余量。
3. **状态空间会不会爆？** 会随 `max(a,b)` 线性增长，对面试规模（几千以内）完全可控；这也是"有界 BFS"
   四个字的重点——无界 BFS 在这道题上是错的（数值可以无限增长）。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，2026-06 报告，"Number Transformation Path"，Algorithm。见
  `../../../catalog/raw/github_repos.md` §2 第 9 行、§3。三种操作与 `transform` 签名、"不必最短 /
  不可达返回 None"均为原文。
- `split` 仅偶数可用是本 kit 对预览未说明部分的重建选择（已声明，理由见"追问 1"）；Part 2 全部为重建。

## 考什么

S05 隐式图上的可达性分析（不建图，靠奇偶推理直接判定）· S08 从"任意路径"压到"最短路径"（有界 BFS）·
识别何时朴素的"无界搜索"是错的、需要主动给出一个可论证的上界。
