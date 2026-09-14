# pc27 · Recipe Sequence Matcher — 连续子序列匹配：预处理 vs O(1) 空间 vs 共享前缀 Trie

> Part 1、Part 2 是一手报道的原题与原追问；Part 3 **(reconstructed)**。

## 背景

TrueInterview 题单预览：`ingredients` 是一串食材 token，每个 `recipe` 也是一串 token，判断
recipe 是否作为**连续子序列**（不是子序列，是子串式的"连续一段"）出现在 `ingredients` 里。原追
问明确要求："**O(1) 额外内存**"——不能建位置索引、不能建自动机，逼着候选人写朴素的双指针重启
扫描。这题的考点其实是"字符串匹配三兄弟"（暴力/预处理索引/多模式 Trie）在同一个问题上的取舍。

## 输入

- Part 1：`ingredients: list[str]`、`recipes: list[list[str]]`；允许对 `ingredients` 做预处理。
- Part 2：`ingredients: list[str]`、单个 `recipe: list[str]`；**不允许**任何随输入增长的额外
  数据结构（哈希表存位置、KMP 失配表都不行）。
- Part 3：与 Part 1 相同的输入，但许多 `recipe` 共享公共前缀（例如很多菜谱都以
  `["boil", "water"]` 开头）。

## API 契约（英文签名）

```python
def find_recipes(ingredients: list[str], recipes: list[list[str]]) -> list[bool]
def find_recipes_o1_space(ingredients: list[str], recipe: list[str]) -> bool
def find_recipes_trie(ingredients: list[str], recipes: list[list[str]]) -> list[bool]
```

空 `recipe`（`[]`）**天然算作"出现"**（空序列是任何序列的连续子序列），三个函数在这一点上行为
一致。

## 规则

### Part 1 — 预处理位置索引（原题）

对 `ingredients` 建一个 `token -> [出现位置]` 的哈希索引；对每个 recipe，只需要检查它**第一个
token**在 `ingredients` 里出现的那些位置，逐一验证后续 token 是否连续匹配。比朴素暴力快在"第一
个 token 很少见"的情况下，最坏情况（比如所有 token 都相同）仍是 `O(n*m)`（KMP/滚动哈希能把最坏
情况降到 `O(n+m)`，但面试预算内先给出这个正确解法通常已经够，追问里再讨论 KMP）。

### Part 2 — O(1) 额外空间（一手原追问）

**不许建位置索引、不许建 KMP 失配表、不许任何随 `ingredients` 或 `recipe` 长度增长的辅助结
构。** 只能用朴素的双指针"重启扫描"：从 `ingredients` 每个起点开始逐 token 比较，遇到第一个不
匹配就换下一个起点。最坏情况时间是 `O(n*m)`，但辅助空间只有几个下标变量，是这题追问真正想考察
的取舍——"用空间换时间 vs 完全不花空间"。

### Part 3 — 多个 recipe 共享前缀 **(reconstructed)**

当 `recipes` 很多且互相共享前缀时（例如 100 个菜谱都以同样的 5 个食材开头），Part 1 的做法要对
每个 recipe 各自扫描一遍，公共前缀被重复比较很多次。把所有 recipe 建成一棵 **trie**，对
`ingredients` 的每个起点只走一次 trie（沿途经过的每个"是某个 recipe 结尾"的节点就把对应的
recipe 标记为命中），共享前缀天然只被比较一次。**测试只要求正确性和"不比 Part 1 明显慢"的性能，
不要求实现 Aho-Corasick 的失配跳转优化**（那是更进一步的多模式匹配算法，能把总时间做到
`O(n + 所有 recipe 长度之和)`，不依赖起点数量，属于追问范畴）。

## Worked examples（全部由 `solution.py` 实际运行得出，三个函数结果一致）

```python
ingredients = ["egg","flour","sugar","egg","milk","sugar","butter"]
recipes = [
  ["flour","sugar"],                    # True: 位置 1-2
  ["sugar","egg"],                      # True: 位置 2-3
  ["egg","milk","sugar"],               # True: 位置 3-5
  ["egg","flour","sugar","egg"],        # True: 位置 0-3
  ["nope"],                             # False
]
find_recipes(ingredients, recipes)      -> [True, True, True, True, False]
find_recipes_trie(ingredients, recipes) -> [True, True, True, True, False]
[find_recipes_o1_space(ingredients, r) for r in recipes] -> [True, True, True, True, False]

find_recipes(ingredients, [[]])      -> [True]   # 空 recipe 天然匹配
find_recipes_o1_space(ingredients, []) -> True
```

500 组随机 `ingredients`/`recipes`（词表 4 个 token）交叉验证三个函数结果完全一致，见
`test_pc27.py`。

## `main()` 命令流

```
PART 1                                          PART 2
INGREDIENTS egg flour sugar egg milk sugar butter    INGREDIENTS egg flour sugar egg milk sugar butter
N 2                                              RECIPE egg milk sugar
flour sugar                                      → true
nope
→ true
  false

PART 3
INGREDIENTS egg flour sugar egg milk sugar butter
N 2
flour sugar
nope
→ true
  false
```

## 边界清单

- 空 `recipe`（`[]`）→ 三个函数都返回 `True`
- 空 `ingredients`，非空 `recipe` → `False`
- 空 `ingredients`，空 `recipe` → `True`
- `recipe` 比 `ingredients` 长 → `False`
- `recipe` 恰好等于整个 `ingredients` → `True`
- `ingredients` 里全是同一个 token（Part 1/2 的最坏情况 `O(n*m)` 场景，必须仍然给出正确答案，
  只是不追求更快）
- 多个 recipe 共享前缀（Part 3 的主要场景）
- 多个 recipe 完全相同（trie 里落在同一个终止节点，必须都标记为命中）
- recipe 在 `ingredients` 里出现多次（只需要判断"是否出现"，不需要计数或定位）

## 追问

1. **Part 1 能不能做到 `O(n+m)`（而不是 `O(n*m)`）？** 可以，把每个 recipe 拼接
   `recipe + [哨兵] + ingredients` 跑 KMP 的失配表，或者用 Rabin-Karp 滚动哈希比较整段哈希值再
   逐一验证碰撞；本题给出的位置索引解法是"预处理换时间"里最直接的一种，面试里通常先给这个再讨
   论 KMP。
2. **Part 2 如果允许 `O(len(recipe))` 空间（而不是严格 O(1)）呢？** 那就是标准 KMP：用
   `len(recipe)` 大小的失配表把最坏情况降到 `O(n+m)`，用一次遍历不回退 `ingredients` 指针；
   "严格 O(1) 额外空间"专门排除了这个选项，逼着写朴素扫描。
3. **Part 3 换成 Aho-Corasick 呢？** 在 trie 基础上加失配指针（类似 KMP 失配表的多模式版本），
   使总时间不再是"起点数 × trie 深度"而是 `O(len(ingredients) + 所有 recipe 长度之和)`，本题
   trie 版本已经消除了"重复比较公共前缀"的浪费，Aho-Corasick 进一步消除"每个起点都要重新走一遍
   trie"的浪费。
4. **食材可以重复利用吗（比如两个 recipe 的匹配区间重叠）？** 本题只判断"是否出现"，不消耗
   `ingredients`，重叠是允许的（每个 recipe 独立判断）。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 27 项「Recipe Sequence Matcher」，
  经 `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览的"连续子序列 + O(1)
  空间追问"可见），见 `../../../catalog/raw/github_repos.md` §2 第 27 行、§3 "pc27"。
- Part 3（trie 处理共享前缀）为重建，已标注 **(reconstructed)**，是多模式字符串匹配场景最常见
  的追问方向。

## 考什么

S04（字符串/序列匹配：暴力 vs 预处理索引 vs Trie/自动机的取舍）· 对"额外空间"约束的严格遵守
（不能偷偷用一个会随输入增长的结构）· 多模式匹配的共享前缀优化直觉。
