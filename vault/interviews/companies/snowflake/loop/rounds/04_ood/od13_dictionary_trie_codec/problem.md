# od13 · Dictionary Trie Codec — 紧凑编码 + 不重建整棵树的前缀流式查询

> TrueInterview 同步清单第 63 题 "Serialize and Deserialize Dictionary Trie"（Algo，2025-12
> 报告）。题面付费，预览只给出最小骨架："不同的小写单词建 trie；`serialize` 成字符串，
> `deserialize` 重建并按字典序返回全部单词；编码方式自选"。具体编码格式、压缩率下界、非法输入
> 校验、以及"不重建整棵树的前缀查询"全部 **(reconstructed)**。

## 背景

把一组互不相同的小写单词压成一棵字典树，再把这棵树序列化成一个字符串（用于落盘或网络传
输），反过来也要能从这个字符串精确重建出全部单词。这是"设计一种自定义、无歧义、可流式解析
的编码格式"这类题的标准考法（同族：od14 的长度前缀编码、od15 的 JSON 解析），本题额外要求
"不反序列化整棵树就能回答前缀查询"，逼你把编码格式设计得**本身就可以被结构化地跳过**。

## API 契约（英文签名）

```python
def serialize(words: list[str]) -> str: ...
def deserialize(data: str) -> list[str]: ...          # all words, lexicographic order
def starts_with(data: str, prefix: str) -> bool: ...   # Part 3, does NOT rebuild the trie
```

## 编码格式（本题自选，逐条说明）

语法（每个字符只可能是 `'0'`、`'1'`、`'#'`，或一个小写字母——单词本身不含数字或 `#`，因此
**不需要任何转义**）：

```
node ::= flag (letter node)*  '#'
flag ::= '0' | '1'      -- '1' 表示"走到这个节点为止的路径本身是一个完整单词"
```

- 每个节点贡献恰好 2 个非字母字符（自己的 `flag` + 收尾的 `#`）；每条边贡献恰好 1 个字母字符。
- 例：`words = ["a", "ab", "b"]` → `serialize(words) == "0a1b1##b1##"`（根节点 `flag=0`，先走
  边 `a` 进入单词 "a" 的节点 `flag=1`，其下再走边 `b` 进入单词 "ab" 的节点 `flag=1`（无子节点，
  直接 `#` 收尾），回到 "a" 节点收尾 `#`；再走根的下一条边 `b` 进入单词 "b" 的节点 `flag=1`，
  `#` 收尾；根节点自己收尾 `#`）。

### Part 2 — 压缩率下界 **(reconstructed)**

设 trie 总节点数（含根）为 N：本编码长度恒等于 `2N + (N-1) = 3N-1`（`N-1` 是边数，等于字母字
符数）。由于"所有单词长度之和"必然 ≥ 边数（每条边至少被一个单词走过），所以：

```
len(serialize(words)) <= sum(len(w) for w in words) + 2 * N
```

`N` 可以直接从编码本身数出来——编码里 `'0'`/`'1'` 字符的个数恰好就是节点数（不需要重建树）。
测试用这个不等式直接校验压缩率，不依赖内部实现细节。

### Part 3 — 非法输入 + 不重建整棵树的前缀查询 **(reconstructed)**

- `deserialize(data)` 必须对任何不符合上述语法的 `data` 抛 `ValueError`：非法 `flag` 字符、
  字母后面没有紧跟合法 `flag`（悬空边）、`#` 数量与已打开的节点数不匹配、根节点收尾后还有多
  余字符（trailing garbage）、空字符串。
- `starts_with(data, prefix)` **不能反序列化整棵树**——它逐字符扫描 `data`，只走 `prefix` 指
  定的那条路径；遇到"当前节点的孩子字母不是我要的那个"，用一个**只占 O(1) 额外空间的括号计
  数器**跳过那整棵不匹配的子树（本编码里 `flag` 相当于开括号、`#` 相当于闭括号，字母不影响嵌
  套深度，是标准的括号匹配跳过）——不需要建立任何 trie 节点对象，只需要移动扫描指针。

### 命令流

```
SERIALIZE <n> <word1> ... <wordn>     输出编码后的字符串
DESERIALIZE <data>                     输出空格分隔的字典序单词列表，空 → -；Part 3 非法输入 → ERROR
STARTSWITH <data> <prefix>             Part 3：true/false；扫描到非法字符 → ERROR
```

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
SERIALIZE 3 a ab b        → 0a1b1##b1##
DESERIALIZE 0a1b1##b1##   → a ab b
```

```
空单词表：
serialize([])   → '0#'
deserialize('0#') → []
```

```
空字符串本身作为一个单词（根节点 flag=1）：
serialize(['']) → '1#'
deserialize('1#') → ['']
```

```
PART 2（压缩率下界，words = ["a", "ab", "b"]）
len(data) = 11
sum(len(w) for w in words) = 4
节点数 N = data 中 '0'/'1' 字符个数 = 4
下界 = 4 + 2*4 = 12  ->  11 <= 12  成立
```

```
PART 3
SERIALIZE 3 a ab b            → 0a1b1##b1##
STARTSWITH 0a1b1##b1## a      → true
STARTSWITH 0a1b1##b1## c      → false
DESERIALIZE bad                → ERROR         (不是合法 flag 字符)
```

```
深链健壮性（word 长度 10**4，临时调低 sys.setrecursionlimit()）：
serialize(["a"*10000]) 再 deserialize 往返一致，starts_with 对 9999/10001 长度前缀分别给出
true/false，全程不触发 RecursionError（证明是显式栈迭代而非 Python 递归）。
```

## 边界清单

- 空单词表：`serialize([]) == '0#'`，`deserialize('0#') == []`
- 空字符串作为单词：根节点 `flag='1'`；`deserialize` 结果里包含 `''`
- 单词只含小写字母 a-z；出现其它字符（大写、数字、符号）→ `serialize` 抛 `ValueError`
- 压缩率下界对任意单词集合成立，包括共享前缀很多（压缩率高）和完全不共享前缀（退化到
  `3N-1` 的上界）两种极端
- `deserialize` 的每一类非法输入都要单独覆盖：空串、非法 flag 字符、悬空边（字母后没有 flag）、
  未闭合的节点（`#` 数量不够）、根节点收尾后的多余字符
- `starts_with`：空前缀恒为 `True`；前缀等于某个完整单词、前缀是某个单词的真前缀、前缀在树
  里完全不存在（含"存在同名字母但走到一半分叉"）三种情况都要覆盖
- `starts_with` 遇到非法字符（在它实际扫描到的范围内）同样要抛 `ValueError`
- 性能与实现约束：单词长度 10**4 的单链（一个词或多个共享极长前缀的词），`serialize` /
  `deserialize` / `starts_with` 在 `sys.setrecursionlimit()` 调得很低时依然不抛
  `RecursionError`，且在 3 秒预算内完成

## 追问

1. **为什么这个编码不需要转义？** 因为字母表设计成"控制字符"（`0`/`1`/`#`）与"数据字符"（小写
   字母）互不相交——这是设计自定义序列化格式最容易忽视也最重要的一条：先固定一个字符集划分，
   再证明数据永远不会产生歧义，而不是事后再打补丁转义。
2. **`starts_with` 的跳过为什么可以用一个整数深度计数器而不是显式栈？** 因为本编码里"开括号"
   （`flag`）和"闭括号"（`#`）的嵌套结构和字母无关——字母永远出现在"父节点的 flag 之后、子节
   点的 flag 之前"这个固定位置，不引入新的嵌套层，所以只需要跟踪"还有多少个未闭合的节点"这一
   个数字，而不需要保存每一层的具体内容（不像 od15 JSON 解析那样，容器类型不同、需要真正的栈
   来记录"现在在数组里还是对象里"）。
3. **如果要支持"流式增量写入"（边生成单词边追加到编码里，而不是一次性 build 完整棵树再序列
   化）呢？** 需要按插入顺序维护一个"当前路径"的显式栈，每插入一个新单词，先找到它和上一个单
   词的最长公共前缀，把栈弹出到那个深度（这一步就是提前关闭那些不再需要保持"打开"的节点，输
   出它们的 `#`），再把新单词剩余的字符依次入栈——这要求输入单词本身是**排好序**的，否则没法
   保证"公共前缀之后就再也不会有新单词回来复用这段前缀"，是这题一个合理但需要改变输入契约的
   延伸。

## 来源与置信度

- **MED**：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步清单）第 63 题
  "Serialize and Deserialize Dictionary Trie"，Algo，2025-12 报告；正文付费，只见标题、格式标
  签与"不同小写单词建 trie；serialize 成字符串，deserialize 重建并按字典序返回全部单词；编码
  自选"这句预览摘要。见 `../../../catalog/raw/github_repos.md` §2 第 63 行、§3 "od13" 一条。
- 具体编码格式、压缩率不等式、非法输入分类、流式 `starts_with` 全部 **(reconstructed)**。

## 考什么

S09 类设计先定契约（先固定字符集划分再证明无歧义，而不是事后转义）· 自定义序列化格式的设计
（与 od14 的长度前缀编码、od15 的 JSON 语法同族）· 树遍历/构造用显式栈迭代应对深链输入 ·
"不重建整个数据结构就能回答局部查询"这一常见的流式/惰性解析模式。
