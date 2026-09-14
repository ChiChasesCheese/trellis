# pc27 · Recipe Sequence Matcher：字符串匹配三兄弟——暴力索引 / 严格 O(1) 空间 / 共享前缀 Trie

> [!tldr]
> - 这题考的是：判断 `recipe` 是否作为**连续子序列**出现在 `ingredients` 里，同一个问题在三种
>   不同资源预算下的实现（可以预处理 / 严格 O(1) 额外空间 / many-recipe 共享前缀），不是三道
>   不同的题，是同一个问题换约束
> - 三步套路：先用"位置索引 + 只检查首 token 出现处"写出正确解 → 追问变成"O(1) 额外空间"时把
>   索引整个删掉换成朴素双指针重启扫描 → 追问变成"很多 recipe 共享前缀"时把索引换成一棵 trie
> - 最值得带走的一个模式：**"额外空间"是个可以精确到"随输入规模增长的辅助结构"的硬约束**——
>   面试官说 O(1) 时必须把哈希表、失配表这类结构真的删掉，不能换个名字（比如 `set` 记录已试过
>   的起点）继续偷偷用等价的东西

## 1. 题目在说什么（人话版）

`ingredients` 是一串食材 token（比如 `["egg","flour","sugar","egg","milk"]`），每个 `recipe`
也是一串 token；判断 `recipe` 里的 token 是否**原样连续**地出现在 `ingredients` 的某一段里——
不是"依次出现但可以跳着选"（那是子序列，LC 392 那种），是"连续一段完全匹配"（更像字符串里找子
串）。

三行小例子：
```
ingredients = ["egg","flour","sugar","egg","milk"]
["flour","sugar"]  -> True   (出现在下标 1-2)
["sugar","milk"]   -> False  (中间隔着 egg，不连续)
```

## 2. 读题：把文字变成模型

- **实体**：`ingredients`（一条食材 token 序列）、一个或多个 `recipe`（待匹配的 token 序列）。
- **输入长什么样**：`ingredients: list[str]`；Part 1/3 是 `recipes: list[list[str]]`（批量查
  询），Part 2 是单个 `recipe: list[str]`（追问明确要求严格 O(1) 空间，批量查询会让"额外空间"
  这个约束失去意义）。
- **输出要什么**：`list[bool]`（Part 1/3）或单个 `bool`（Part 2），空 `recipe` 恒为 `True`。
- **状态**：Part 1 是 `token -> [位置]` 的哈希索引；Part 2 只有几个下标变量，不允许任何随输入
  增长的结构；Part 3 是一棵 trie。
- **一句话建模**：这是一道**多模式子串匹配**题，三个 part 分别对应"预处理换时间"、"完全不花额
  外空间"、"多模式共享前缀"三种经典取舍，本质上是同一个问题在不同资源预算下的答案。

> [!note] 为什么选这个数据结构
> Part 1 用位置索引是因为"只检查 recipe 首 token 出现的位置"比暴力枚举每个起点更快（首 token
> 罕见时收益明显，全同一 token 时退化成暴力，但仍然正确）。Part 3 用 trie 是因为多个 recipe 共
> 享前缀时，位置索引法要对每个 recipe 各自扫一遍，公共前缀被重复比较；trie 让每个起点只走一次
> 路径，沿途碰到的"某个 recipe 的终止节点"直接标记，共享前缀天然只比较一次。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`main()` 按 `PART n` 分发；`part1`/`part2`/`part3` 各自解析 `INGREDIENTS` /
   `N` / recipe 行，调用对应函数，格式化成 `"true"`/`"false"`。
2. **Part 1 最小可用**：建 `token -> [位置]` 索引；对每个 recipe，只在其首 token 出现的位置里
   验证后续 token 是否连续匹配。立刻用样例自测。
3. **Part 2 叠加**：这不是在 Part 1 上"加"东西，而是**整个换掉**——不许有索引，写朴素的
   "每个起点从头比较、遇到第一个不匹配就换下一个起点"的双指针重启扫描。
4. **Part 3 叠加**：把 `recipes` 建成一棵 trie（`children: dict[str, Node]` + 记录哪些 recipe
   在这个节点终止），对 `ingredients` 每个起点只走一次 trie。
5. **收尾**：跑一遍边界清单——空 recipe、recipe 比 ingredients 长、全同一 token 的最坏情况、多
   个相同 recipe 落在同一个 trie 终止节点。

## 4. 代码怎么组织

```
find_recipes(ingredients, recipes) -> list[bool]          # Part1：位置索引
find_recipes_o1_space(ingredients, recipe) -> bool        # Part2：双指针重启扫描，O(1) 辅助空间
_TrieNode / find_recipes_trie(ingredients, recipes)        # Part3：共享前缀 trie，一次扫描
_read_n_lines / _tok                                       # 命令流解析 helper，三个 part 共用
part1/part2/part3(lines) -> list[str]  /  main()           # 分发 + 格式化
```
三个函数彼此独立（不是互相调用的关系），因为它们代表三种**互斥的资源约束**，不是同一套逻辑的
增量叠加——这一点在面试里要主动说清楚，避免面试官以为你把 Part 2 写成了"Part 1 去掉索引"的退
化版本（顺序其实是反过来的：Part 2 从来没有索引可去）。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
class _TrieNode:
    __slots__ = ("children",)
    def __init__(self):
        self.children = {}

def find_recipes_trie(ingredients, recipes):
    root = _TrieNode()
    end_indices = defaultdict(list)          # id(node) -> 在这个节点终止的 recipe 下标
    for idx, recipe in enumerate(recipes):
        if not recipe:
            continue                          # 空 recipe 天然匹配，不进 trie
        node = root
        for tok in recipe:
            node = node.children.setdefault(tok, _TrieNode())
        end_indices[id(node)].append(idx)

    found = [not r for r in recipes]          # 空 recipe 预先标记为 True
    n = len(ingredients)
    for start in range(n):                    # 每个起点只走一次 trie，共享前缀天然只比较一次
        node = root
        pos = start
        while pos < n and ingredients[pos] in node.children:
            node = node.children[ingredients[pos]]
            pos += 1
            for idx in end_indices.get(id(node), ()):
                found[idx] = True
    return found
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「我确认一下：'连续子序列'是指原样连续的一段，不是可以跳着选的子序列；空 recipe 应
  该天然算匹配吧？」
- 写 Part 2 时：「面试官说 O(1) 额外空间，我把 Part 1 的位置索引整个删掉，换成朴素的重启扫
  描——最坏 O(n·m)，但辅助空间只有几个下标变量。」
- 写 Part 3 时：「很多 recipe 共享前缀，我建一棵 trie，对 `ingredients` 每个起点只走一次，共享
  前缀天然只被比较一次，而不是对每个 recipe 各自扫一遍。」
- 交付时：「样例过了；如果时间允许，我可以讨论 KMP/Rabin-Karp 把 Part 1 做到 O(n+m)，或者用
  Aho-Corasick 把 Part 3 的'每个起点重新走一遍 trie'这一层浪费也消掉。」

## 7. 常见跑偏（方法层面，3 条）

- Part 2 里"忍不住"用一个 `set` 记录已经尝试过的起点做剪枝——这仍然是一个随输入增长的辅助结
  构，本质上违反了"严格 O(1) 额外空间"这条约束，只是换了个名字。
- Part 3 里多个完全相同的 recipe 落在同一个 trie 终止节点，只标记了其中一个下标，漏掉了"同一个
  节点可能对应多个 recipe"这件事。
- 把 Part 1 的"只检查首 token 出现的位置"错写成"扫描全部起点再判断首 token"，退化成和 Part 2
  一样的复杂度，却还占用着索引的空间——两头不讨好。

## 8. 同族题 / 延伸

- 与 `od13_dictionary_trie_codec` 共用"trie"这个工具，但目的完全不同：那题是拿 trie 做无歧义
  序列化，这题是拿 trie 做共享前缀的多模式匹配——同一种数据结构服务于不同的问题。
- 与 `pc21_accumulator_interpreter` 同族的地方在于：本 kit 的 Part 3 都标注了
  **(reconstructed)**，是围绕"这套机制最常见的效率类追问"重建出来的，而不是原题原文。
- 练习命令：`python3 loop/mock.py start pc27`
