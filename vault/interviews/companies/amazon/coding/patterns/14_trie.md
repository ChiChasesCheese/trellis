# 14 · 字典树（Trie）：前缀的共享与剪枝

> 本讲覆盖：LC 14 Longest Common Prefix · 139 Word Break · 1268 Search Suggestions System · 211 Design Add and Search Words Data Structure · 212 Word Search II（Hard）· 472 Concatenated Words（Hard）
> 前置：第 01 讲（`dict`）、第 06 讲（DFS）、第 10 讲（DP 的"前 i 个字符能否切分"）、第 12 讲（回溯的 choose / un-choose）。第 11 讲的 LC 588 文件系统其实就是一棵"目录名组成的 trie"。
> 读完你应该能：(1) 画出一棵 trie 并说明节点**就是**一个前缀；(2) 手写 `insert / search / starts_with / delete`；(3) 判断什么时候该用 trie、什么时候一个 `set` 或「排序 + 二分」就够了；(4) 把 trie 和回溯（212）、DP（139 / 472）、通配符 DFS（211）组合起来；(5) 回答 trie 的内存代价这个资深追问（Python 里它比你以为的贵得多，3 节有实测）。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

词典里有 N 个单词。操作一：「有没有单词以 `p` 开头？」最笨的做法是扫描所有单词，对每个单词比较前缀：O(N · |p|)，每次查询都要重来一遍。

LC 1268（搜索建议）：用户每敲一个字母，就要给出词典里以当前输入为前缀的、字典序最小的 3 个商品。最笨的做法：每敲一个字母，过滤全部商品再排序，O(|q| · N log N)。

LC 212（Word Search II）：棋盘里同时找 W 个单词。最笨的做法：对每个单词单独跑一遍第 12 讲的 Word Search，总计 O(W · R · C · 3^L)。

### 1.2 慢在哪里 / 错在哪里

`car`、`card`、`care`、`cat` 前两三个字母完全一样，扫描时却把 `c-a` 比较了四遍。词越多、共同前缀越长，重复比较越多。212 里更糟：棋盘上沿着 `c-a-r` 走一遍，本来可以顺带发现 `card`、`care`，却被分成了三次独立的搜索。

> 因果链：很多单词共享前缀 → 把单词存成一棵树，每条边是一个字符，**从根到某个节点的路径就是一个前缀** → 查询前缀只需沿着树走 `|p|` 步，和词典里有多少单词**无关** → 因为节点就是前缀，可以把"这个前缀下最小的 3 个词"（1268）、"这里有个单词结束"（所有题）、"这个前缀下还有没找到的词吗"（212）挂在节点上。

### 1.3 Trie 是什么（从零讲）

- **Trie（字典树 / 前缀树，读作 "try"）**：根节点代表空前缀；每个节点有若干子节点，用字符标记；标记为"单词结尾"的节点表示从根到这里的字符串是词典里的一个词。
- 例子：`car, card, care, cat`

```text
(root)
  c
   a
    r ($)      <- "car" is a word
     d ($)     <- "card"
     e ($)     <- "care"
    t ($)      <- "cat"
```

- **三个基本操作**（长度为 L 的串，都是 O(L)，和词典大小无关）：
  - `insert(w)`：沿着路径走，缺哪个子节点就新建，最后在末节点打上"单词结尾"标记。
  - `search(w)`：沿路径走到末节点，**并且**该节点有结尾标记（只是前缀不算单词）。
  - `starts_with(p)`：沿路径走完就行，不看结尾标记。
- **Python 里的两种常见表示**：
  - `dict` 节点：`node = {}`，子节点是 `node[ch]`，结尾标记放一个特殊键（本讲用 `"$"`）。写起来最短，适合面试。
  - 类节点：`class Node: children = {}; is_end = False`。可读性更好；字母表固定小写时也可以用 `[None] * 26` 的数组，查找更快但每个节点固定占 26 个槽。
- **什么时候用 trie，什么时候不用**：

| 需求 | 够用的最简单结构 | 为什么还需要 trie |
|---|---|---|
| 只问"这个完整单词在不在" | `set` | 不需要 trie |
| 前缀查询、静态词典 | 排序 + `bisect` | 词典频繁增删、需要在前缀处聚合数据（top-k、计数）时用 trie |
| 通配符 `.`、同时匹配很多词（211 / 212） | — | 只有树结构能"一起走、一起剪枝" |
| 按字典序遍历某个前缀下的所有词 | 排序数组也行 | trie 的 DFS 天然按字典序 |

- **内存代价**（资深必答）：trie 用"每个节点一个哈希表"换"共享前缀"。CPython 里一个空 `dict` 就是 64 字节，一个只有一个键的 `dict` 是 184 字节。如果词典的前缀共享很少，trie 会比存整串的 `set` 大得多（3 节有实测）。降低内存的办法：**压缩 trie（radix tree / Patricia trie）**把只有一个孩子的链合并成一条边；固定字母表用数组；只读词典用 **DAWG / 最小自动机**；真正大规模的场景用排序数组 + 二分，或 FST（Lucene 的做法）。
- **删除**：沿路径标记取消结尾，然后**自底向上**删掉不再有孩子且不是结尾的节点；否则 trie 只增不减（内存泄漏）。

## 2. 模板与逐行讲解

```python
from random import Random

# Template T1: a dict-based trie with insert / search / prefix queries / ordered listing / delete
class Trie:
    END = "$"                                   # a key that can never be a lowercase letter

    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})      # follow the edge, creating the child on demand
        node[self.END] = True

    def _find(self, prefix):                    # the node reached by `prefix`, or None
        node = self.root
        for ch in prefix:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._find(word)
        return node is not None and self.END in node          # a prefix alone is NOT a word

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def words_with_prefix(self, prefix):        # lexicographic order because children are visited in sorted order
        start = self._find(prefix)
        out = []

        def dfs(node, path):
            if self.END in node:
                out.append("".join(path))
            for ch in sorted(k for k in node if k != self.END):
                path.append(ch)
                dfs(node[ch], path)
                path.pop()                      # same choose / un-choose as backtracking

        if start is not None:
            dfs(start, list(prefix))
        return out

    def delete(self, word):
        path = [self.root]                      # remember the nodes on the way down
        for ch in word:
            nxt = path[-1].get(ch)
            if nxt is None:
                return False                    # not present
            path.append(nxt)
        if self.END not in path[-1]:
            return False
        del path[-1][self.END]
        for i in range(len(word) - 1, -1, -1):  # bottom-up: remove nodes that became useless
            if path[i + 1]:                     # still has children or an END marker
                break
            del path[i][word[i]]
        return True


t = Trie()
for w in ["car", "card", "care", "cat"]:
    t.insert(w)
assert t.search("car") and t.search("card") and not t.search("ca") and not t.search("cars")
assert t.starts_with("ca") and not t.starts_with("cab") and t.starts_with("")
assert t.words_with_prefix("car") == ["car", "card", "care"] and t.words_with_prefix("x") == []
assert t.delete("card") and not t.search("card") and t.search("car") and t.search("care")
assert not t.delete("card") and not t.delete("ca")
assert t.delete("car") and t.delete("care") and t.delete("cat") and t.root == {}   # fully pruned back to empty

rng = Random(3)                                 # cross-check against a plain set
words, ref, trie = [], set(), Trie()
for _ in range(500):
    w = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    if rng.random() < 0.7:
        trie.insert(w); ref.add(w)
    else:
        assert trie.delete(w) == (w in ref); ref.discard(w)
    q = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    assert trie.search(q) == (q in ref)
    assert trie.starts_with(q) == any(x.startswith(q) for x in ref)
    assert trie.words_with_prefix(q) == sorted(x for x in ref if x.startswith(q))
```

逐行讲解：

1. `END = "$"`：结尾标记和字符共用同一个 `dict`，所以必须选一个不会出现在输入里的键。输入里有 `$` 时会出错，见 5 节；稳妥的做法是把标记放在节点的单独字段里（类节点的 `is_end`）。
2. `node = node.setdefault(ch, {})`：如果有这个孩子就返回它，没有就新建一个空 `dict` 放进去再返回。这一行同时完成"查"和"建"。
3. `_find` 返回节点而不是布尔值：`search` 和 `starts_with` 唯一的区别就是最后看不看 `END`。把共同部分提出来，两个函数各一行。
4. `search` 里的 `self.END in node`：`"car"` 在 trie 里，`"ca"` 的节点存在，但它不是单词；这是新手最常漏的判断。
5. `words_with_prefix` 的 DFS：和第 12 讲回溯一模一样——`path.append(ch)` / 递归 / `path.pop()`。孩子按字符排序，所以输出自然是字典序。1268 的"最小的 3 个"就是它的剪枝版本。
6. `delete` 先沿路径把节点**存下来**（`path`），因为 `dict` 节点不知道自己的父亲。删掉结尾标记后自底向上，只要某个节点变空（没有孩子、也没有标记）就从父节点里删掉它；遇到仍有用的节点就停。最后的断言证明删除全部单词后 trie 回到 `{}`。
7. 随机对拍：用 `set` 作为参照，同时验证 `search`、`starts_with`、`words_with_prefix`，并让插入和删除交错发生。

## 3. 完整手算（Worked trace）

下面是真实运行结果：把 `car, card, care, cat` 建成 trie 打印出来，做几次前缀走访，最后看内存。

```python
import tracemalloc
from random import Random

def build(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    return root

def show(node, indent=0):
    for key in sorted(node):
        if key == "$":
            print("  " * indent + "$  (a word ends here)")
        else:
            print("  " * indent + key)
            show(node[key], indent + 1)

def count_nodes(node):
    return 1 + sum(count_nodes(child) for key, child in node.items() if key != "$")

words = ["car", "card", "care", "cat"]
root = build(words)
show(root)
print("characters in the words:", sum(map(len, words)), " trie nodes (excluding the root):", count_nodes(root) - 1)

def walk(root, prefix):
    node = root
    for i, ch in enumerate(prefix):
        if ch not in node:
            print(f"prefix {prefix!r}: no child {ch!r} after {prefix[:i]!r} -> stop after {i + 1} steps")
            return None
        node = node[ch]
    print(f"prefix {prefix!r}: reached a node with children {sorted(k for k in node if k != '$')}, word ends here: {'$' in node}")
    return node

walk(root, "car")
walk(root, "ca")
walk(root, "cab")

# memory of a dict-based trie versus a plain set of the same words (deterministic data, CPython)
rng = Random(1)
vocab = ["".join(rng.choice("abcdefghij") for _ in range(rng.randint(4, 9))) for _ in range(20000)]
tracemalloc.start()
s = set(vocab)
mem_set = tracemalloc.get_traced_memory()[0]
t = build(vocab)
mem_both = tracemalloc.get_traced_memory()[0]
tracemalloc.stop()
print(f"{len(s)} distinct words, {sum(map(len, s))} chars: set of strings ~{mem_set // 1024} KiB, dict-trie ~{(mem_both - mem_set) // 1024} KiB (about {(mem_both - mem_set) / mem_set:.1f}x)")
```

```text
c
  a
    r
      $  (a word ends here)
      d
        $  (a word ends here)
      e
        $  (a word ends here)
    t
      $  (a word ends here)
characters in the words: 14  trie nodes (excluding the root): 6
prefix 'car': reached a node with children ['d', 'e'], word ends here: True
prefix 'ca': reached a node with children ['r', 't'], word ends here: False
prefix 'cab': no child 'b' after 'ca' -> stop after 3 steps
19403 distinct words, 127279 chars: set of strings ~512 KiB, dict-trie ~10534 KiB (about 20.6x)
```

怎么读：

- 14 个字符的 4 个单词只用了 6 个节点：`c-a-r` 这段被四个词中的三个共享，`c-a` 被四个词共享。
- 走 `"car"` 到达的节点既有孩子 `d, e`，又有结尾标记——所以 `search("car")` 为真，同时 `starts_with("car")` 也为真；走 `"ca"` 到达的节点有孩子但**没有**结尾标记——`search("ca")` 为假。
- 走 `"cab"`：到了 `ca` 之后发现没有孩子 `b`，3 步就能判定"没有任何词以 `cab` 开头"，和词典有多少个词无关。这正是 212 的剪枝依据：棋盘 DFS 走到一个 trie 里不存在的前缀，整个分支立即放弃。
- 最后一行是资深追问的数据：2 万个几乎没有共享前缀的随机词，`dict` 版 trie 的内存大约是 `set` 的二十倍。**trie 的优势是时间（以及前缀聚合），不是内存。**面试里说"如果内存是瓶颈，我会用压缩 trie 或排序数组 + 二分"就是加分项。

## 4. 题目

```python
import bisect
from collections import defaultdict
```

### 4.1 LC 14 · Longest Common Prefix（Easy，频率 75）

```python
# solutions/14_longest_common_prefix.py
def longest_common_prefix(strs):
    if not strs:
        return ""
    first = strs[0]
    for i, ch in enumerate(first):               # vertical scan: column i of every word
        for s in strs[1:]:
            if i == len(s) or s[i] != ch:
                return first[:i]
    return first


class PrefixTrie:                                # the same answer from a trie; worth it when words are added over time
    def __init__(self):
        self.root = {}                           # node = dict char -> child node; "$" marks the end of a word
        self.size = 0

    def add(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
        self.size += 1

    def common_prefix(self):
        node, out = self.root, []
        while len(node) == 1 and "$" not in node:   # exactly one way to continue and no word ends here
            ch = next(iter(node))
            out.append(ch)
            node = node[ch]
        return "".join(out)
```

- **一句话洞见**：纵向扫描——逐列比较所有字符串的第 `i` 个字符，第一次不一致（或某个串到头）就停。Trie 版本：所有单词插入后，从根往下走，**只要当前节点只有一个孩子且不是结尾**，就是公共前缀的一部分。
- **为什么 Easy 题也放进 trie 讲义**：它展示了 trie 的"结构即答案"——公共前缀就是根到第一个分叉点的路径。但对一次性查询，纵向扫描更简单更省内存；trie 只在**词是陆续加进来、公共前缀要反复查询**时才值得。
- **复杂度**：纵向扫描时间 O(S)（S = 所有字符总数的上界；最坏是最短串的长度 × n），空间 O(1)；trie 时间 O(S)，空间 O(S)。

**资深追问**

- **规模 ×1000**：纵向扫描天然可以分块并行（每块算自己的 LCP，再对各块的 LCP 求 LCP——LCP 满足结合律）。
- **流式**：新字符串到来时，`lcp = common_prefix(lcp, new)`，O(L) 更新；不需要保存历史（只能缩短，不会变长）。有删除操作时才需要 trie（或计数）。
- **内存**：纵向扫描 O(1)；trie O(S)。
- **并发**：结合律使得 reduce 可以并行（fork-join）。
- **接口**：空列表返回 `""`；含空串返回 `""`；是否区分大小写；Unicode（按码点还是按字素簇）。
- **测试**：单元素、全相同、没有公共前缀、一个串是另一个的前缀（`["ab","abc"]`）、空串；和暴力枚举所有前缀长度对拍（我们做了，同时检查 trie 版本）。

### 4.2 LC 139 · Word Break（Medium，频率 62）

```python
# solutions/139_word_break.py
def word_break(s, word_dict):
    root = {}
    for w in word_dict:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True                          # a dictionary word ends here
    n = len(s)
    reachable = [False] * (n + 1)                 # reachable[i]: s[:i] can be segmented
    reachable[0] = True
    for i in range(n):
        if not reachable[i]:
            continue
        node = root
        for j in range(i, n):                     # extend one character at a time, stop when no word continues
            node = node.get(s[j])
            if node is None:
                break
            if "$" in node:
                reachable[j + 1] = True
        if reachable[n]:
            return True
    return reachable[n]
```

- **一句话洞见**：`reachable[i]` 表示 `s[:i]` 能被切分。对每个可达的 `i`，沿着 trie 逐字符往后走，**遇到结尾标记就标记 `reachable[j + 1]`**，走不下去（没有对应的孩子）就停。trie 把"枚举所有切点并查词典"变成"一次沿路径扫描"，并且天然限制在最长单词的长度内。
- **复杂度**：时间 O(n · L)（n = `len(s)`，L = 最长单词长度），空间 O(词典总字符数)。不用 trie 的写法是 `for j: if s[i:j] in word_set`，每次切片 + 哈希是 O(L)，总计 O(n · L²)。
- 朴素递归（不记忆化）在 `"aaaa…ab"` 这种输入上是指数级，`solutions/139_word_break.py` 的测试里放了一个 41 个字符的例子。

**资深追问**

- **规模 ×1000**：词典 100 万词：trie 构建一次、多个查询复用；单个超长字符串：DP 是线性的，但 `reachable` 数组是 O(n)，可以只保留最近 L 个位置的滑动窗口。
- **流式**：字符流边来边判断"到目前为止的前缀能否被切分"：维护"当前所有活跃的 trie 节点"集合（类似 Aho–Corasick 的思想），每来一个字符推进所有节点。
- **内存**：trie 的内存见 3 节；也可以用 `set` + 最长词长度限制（O(词典总字符数)，常数更小）。
- **并发**：词典（只读）可以被多个线程共享，trie 无需加锁；切分本身是顺序依赖，不拆。
- **接口**：只返回布尔值（139）还是所有切分方案（LC 140，输出可能指数级，需要记忆化 + 生成器）；空串返回 `True`；词典含空串会导致死循环风险——要么过滤掉，要么只在 `j >= i` 之后才标记。
- **测试**：空串、词典为空、重叠词（`["a","aa","aaa"]` 对 `"aaaaaab"`）、必须选较短的词才能成功（`"cars"`, `["car","ca","rs"]`）；与"朴素递归"对拍（小输入）。

### 4.3 LC 1268 · Search Suggestions System（Medium，频率 50）

```python
# solutions/1268_search_suggestions_system.py
def suggested_products(products, search_word):
    root = {}
    for word in sorted(products):                      # sorted insertion => each node's list is already sorted
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
            top = node.setdefault("#", [])             # "#" holds up to 3 best words through this node
            if len(top) < 3:
                top.append(word)
    out, node = [], root
    for ch in search_word:
        node = node.get(ch) if node is not None else None
        out.append(node["#"][:] if node is not None else [])   # once the prefix falls off the trie, all later answers are []
    return out


def suggested_products_bisect(products, search_word):          # no trie: sort once, binary-search each prefix
    products = sorted(products)
    out, prefix = [], ""
    for ch in search_word:
        prefix += ch
        i = bisect.bisect_left(products, prefix)
        out.append([p for p in products[i:i + 3] if p.startswith(prefix)])
    return out
```

- **一句话洞见**：把商品**排序后**依次插入 trie，并在经过的**每个节点**上记录"经过这里的前 3 个商品"——因为插入顺序是字典序，先到的就是最小的，列表满 3 个就不再加。用户每敲一个字母，沿 trie 前进一步，直接读当前节点的列表。一旦走出 trie，后面所有结果都是 `[]`。
- **替代解法**（也写在代码里）：排序一次，每个前缀用 `bisect_left` 找到起点再取 3 个——不需要 trie、代码更短、内存小。两种都要会：面试官可能会追问"词典频繁更新怎么办"，此时 trie 能增量更新，排序数组要 O(N) 插入。
- **复杂度**：trie 版——建立 O(S log N)（排序）+ O(S)（插入），每次查询 O(|q|)；bisect 版——每次击键 O(|q| log N)。

**资深追问**

- **规模 ×1000**：商品 10⁹ 种：单机放不下，按**前缀分片**（比如前两个字符的哈希）到多台机器；顶层路由由前缀决定；热门前缀的结果（比如前 3 个字符）预计算并缓存。
- **流式**：商品增删：trie 版本插入时只更新路径上节点的 top-3（需要保留每个节点更多候选，删除时才能补位）；真实系统是离线重建 + 增量合并，并且结果按**热度**而不是字典序排序（节点里存 top-k 热度，不是字典序）。
- **内存**：每个节点存 3 个字符串引用（不是副本）；可以只存商品下标。
- **并发**：只读查询无需锁；更新用"写时复制 + 原子切换根指针"（copy-on-write / RCU）。
- **接口**：大小写、前导 / 尾随空格、重复商品（本实现不去重：`["a","a","a","a"]` 会返回重复项，LeetCode 保证商品互不相同，要先问）；`searchWord` 为空；返回的是新列表还是节点里列表的引用（我们 `[:]` 拷贝，避免调用方修改污染 trie）。
- **测试**：和"每个前缀过滤再排序取前 3"的暴力解对拍；查询词完全不在词典里（全 `[]`）；前缀走出 trie 之后再也回不来；恰好 3 个 / 少于 3 个。

### 4.4 LC 211 · Design Add and Search Words Data Structure（Medium，频率 38）

```python
# solutions/211_add_and_search_words.py
class WordDictionary:
    def __init__(self):
        self.root = {}

    def add_word(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, pattern):
        def dfs(node, i):
            if i == len(pattern):
                return "$" in node
            ch = pattern[i]
            if ch == ".":                              # wildcard: try every real child (skip the "$" marker)
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
```

- **一句话洞见**：普通字符走一条边；通配符 `.` 对所有孩子都试一遍（DFS 分叉）。注意遍历孩子时要**跳过结尾标记键 `"$"`**——它不是一个真实的字符。
- **复杂度**：`add_word` O(L)；`search` 最坏 O(节点总数)（模式全是 `.`，要遍历所有 L 层的所有节点），没有通配符时 O(L)。
- 这是一道**设计题**：契约（空串是不是单词？重复添加怎么办？）和测试比算法更重要。

**资深追问**

- **规模 ×1000**：通配符很多时每次查询接近全树扫描。优化：按**单词长度**分桶（`.` 不改变长度，所以只在同长度的 trie 里搜）；或对"只有末尾几位是 `.`"的常见模式预先建索引；真实系统用倒排索引 / 正则引擎。
- **流式**：`add_word` 与 `search` 交错发生：单线程没问题；多线程见并发。
- **内存**：同 3 节：dict 节点昂贵；固定字母表用数组 / 压缩 trie。
- **并发**：读多写少：读写锁，或写时复制；`add_word` 只会增加节点，不会删除，所以"读线程看到半建好的路径"最多是看不到刚加入的词，不会崩溃——但要在 Python 以外的语言里仔细处理内存可见性。
- **接口**：模式里只有 `.` 一种通配符；是否支持 `*`（任意长度）——那就是正则匹配，需要 DP / 回溯（第 10 讲 LC 10）；模式含非小写字母时怎么办。
- **测试**：和 `re.fullmatch` 对拍（我们做了）；空串模式；全是 `.`；长度不匹配（`"b."` 对 `"bad"`）。

### 4.5 LC 212 · Word Search II（Hard，频率 54）

```python
# solutions/212_word_search_ii.py
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                                   # store the whole word at its end node: no path rebuilding
    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        if "$" in node:
            found.append(node.pop("$"))                 # pop => each word is reported exactly once
        board[r][c] = None                              # mark visited
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch                                # un-choose
        if not node:
            del parent[ch]                              # prune: this branch has no unfound words left

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found
```

- **一句话洞见**：第 12 讲的 Word Search 是"棋盘上 DFS，匹配**一个**词"；这里把所有词建成 trie，DFS 的过程中**同时**沿着 trie 走：棋盘上的下一个字母必须是当前 trie 节点的孩子，否则整条分支剪掉。每个词只搜一次，共享前缀只匹配一次。
- **三个剪枝/技巧**：(1) 在末节点直接存**整个单词**（`node["$"] = w`），不用重建路径；(2) 找到之后 `pop` 掉标记，同一个词不会重复报告；(3) DFS 返回后如果子节点已经没有孩子了就从父节点里**删除**它——找完的分支越来越少，后面的搜索越来越快。
- **复杂度**：最坏仍是 O(R · C · 3^(L−1))（L = 最长单词长度），但实际上被 trie 的前缀存在性剪掉了绝大部分；空间 O(词典总字符数 + L)。
- 与「W 次 Word Search」相比：词多且共享前缀时，快一到两个数量级。

**资深追问**

- **规模 ×1000**：棋盘 ×1000：分块 + 重叠边界（每块向外多取 `L − 1` 格，保证跨块的词不会漏）；词典 ×1000：trie 内存是瓶颈（3 节），改成压缩 trie 或按首字母分片、多趟扫描。
- **流式**：新词陆续加入：每个新词单独跑一次 79 的 DFS（棋盘不变），或增量加入 trie 后再跑一遍受影响的分支。
- **内存**：本实现**在搜索过程中修改了棋盘**（标记 `None`）并在返回时还原；也**消耗了 trie**（删节点、`pop` 标记）。如果 trie 要复用于下一次查询，必须在每次搜索前拷贝，或者不要做这两个优化——这是个契约问题，要说出来。
- **并发**：不同起点格子可以并行，但每个线程需要自己的棋盘副本（原地标记不是线程安全的）和自己的 trie 副本（或者放弃"消耗式"优化，改成结果集合去重）。
- **接口**：返回顺序不保证；`words` 中有重复词（报告一次）；单词长度超过棋盘格数（直接不可能）。
- **测试**：必须有"调用前后棋盘不变"的断言；`words` 里的词互为前缀（`["a","ab","abc"]`）；同一个词出现多次；与"对每个词跑 79"的暴力解对拍（我们做了）。

### 4.6 LC 472 · Concatenated Words（Hard，频率 53）

```python
# solutions/472_concatenated_words.py
def find_all_concatenated_words(words):
    root = {}
    out = []

    def segmentable(w):                              # forward DP, trie walk from every reachable position
        n = len(w)
        reachable = [False] * (n + 1)
        reachable[0] = True
        for i in range(n):
            if not reachable[i]:
                continue
            node = root
            for j in range(i, n):
                node = node.get(w[j])
                if node is None:
                    break
                if "$" in node:
                    reachable[j + 1] = True
            if reachable[n]:
                return True
        return False

    for w in sorted({w for w in words if w}, key=len):   # drop "" and duplicates; shortest first
        if segmentable(w):                                # the trie holds only shorter words: >= 2 pieces
            out.append(w)
        else:
            node = root                                   # a concatenated word adds nothing to the trie, so skip it
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = True
    return out
```

- **一句话洞见**：把 139 的"能否切分"套在每个词上，但切分用的词典就是**其他词**。技巧：按长度从短到大处理——处理到某个词时 trie 里只有比它短（或等长且不同）的词，所以"能被切分"就一定意味着由**至少两个**词拼成（它自己还没有被插进去）。如果某个词本身能被切分，它是冗余的，不需要再插入 trie。
- **复杂度**：排序 O(N log N)；每个词的切分 DP 是 O(L · maxLen)；总计 O(S · maxLen)，S 是总字符数。
- 与 139 的区别：139 的词典是给定的；472 的词典随着处理逐步增长。

**资深追问**

- **规模 ×1000**：N = 10⁶ 个词：排序 + trie 的内存是瓶颈；分层处理——同一长度的词互不依赖，可以并行判断（它们只依赖更短的词）。
- **流式**：新词加入时只需判断这个新词本身是否是拼接词（用现有 trie）；但**它也可能让已有的词变成拼接词**（新词作为一个组件）——要么重新判断较长的词，要么维护"反向索引"。
- **内存**：冗余词不入 trie 节省了空间；dict 节点的内存代价见 3 节。
- **并发**：按长度分层，层内并行，层间串行。
- **接口**：空串要先过滤（否则 `"" + "" + …` 会让一切变成拼接词）；重复词（先去重）；一个词不能由**它自己**拼接而成（去重 + 严格短于）；返回顺序不保证。
- **测试**：`["a","a"]` 不应报告 `a`；`["a","aa","aaa"]` 报告 `aa` 和 `aaa`；空串；与"集合 + 递归拆分，至少两段"的暴力解对拍（我们做了）。

## 5. 常见 bug

1. **`search` 忘了检查结尾标记**：`"ca"` 的路径存在但不是词，写成"路径存在就返回真"会把前缀当成单词。
2. **结尾标记键和真实字符冲突**：用 `"$"` 做标记，输入里恰好有 `$`（或用 `None` / 空串）就出错。需要通配符的题（211）遍历孩子时，**忘了跳过标记键**会把 `"$"` 当成一个字符去递归。
3. **Python 浅拷贝与共享**：`[{}] * 26` 创建了 26 个指向**同一个**字典的引用；节点数组要用列表推导式。
4. **`delete` 只删标记不剪枝**：trie 只增不减；剪枝要自底向上，并且遇到仍有孩子或结尾标记的节点就停。
5. **212 里重复报告同一个词**：找到词之后没有 `pop` 掉标记（或没有用集合去重）。
6. **212 里忘了还原棋盘**：标记 `None` 后在 DFS 返回时必须还原（第 12 讲 un-choose），尤其不能在"找到词"的 `return` 路径上漏掉。
7. **472 没有过滤空串 / 没有按长度排序**：空串让所有词都"可切分"；不排序则 trie 里可能已经有更长的词，导致误判。
8. **1268 返回了 trie 内部列表的引用**：调用方一改就污染词典；返回拷贝。
9. **139 的 trie 走完整个后缀**：不在"没有对应孩子"时 `break` 就退化成 O(n²) 甚至更差。

## 6. 自测题

1. Trie 查询前缀的复杂度是多少？为什么和词典大小无关？
   <details><summary>答案</summary>O(|p|)。每个字符对应树上的一步（`dict` 查找 O(1)），走完前缀就知道答案；其他单词只通过共享前缀间接参与，不需要逐个比较。</details>
2. `search("ca")` 与 `starts_with("ca")` 在 `car, cat` 的 trie 上分别返回什么？差别在哪？
   <details><summary>答案</summary>`search` 返回假，`starts_with` 返回真。路径 `c-a` 都存在，但 `ca` 节点没有结尾标记，所以它不是一个完整的单词；`starts_with` 只关心路径是否存在。</details>
3. 什么时候不应该用 trie？
   <details><summary>答案</summary>只需要完整单词的成员判断时（`set` 更简单更省内存）；静态词典的前缀查询（排序 + `bisect` 通常内存更小、代码更短）；前缀共享很少且内存敏感时（Python 里 dict 节点很贵）。需要在前缀上聚合信息、通配符、与回溯 / DP 结合、或需要字典序遍历时才首选 trie。</details>
4. 小编程：在 trie 上实现 `count_prefix(p)`：有多少个单词以 `p` 开头。
   <details><summary>答案</summary>在每个节点维护计数 `cnt`：`insert` 时沿路径每个节点 `cnt += 1`（重复插入同一词要先判断是否已存在）；`count_prefix` 走到前缀末节点，返回它的 `cnt`，走不到返回 0。O(|p|)。删除时沿路径 `cnt -= 1`。</details>
5. 212 Word Search II 为什么比"对每个词跑一遍 79"快？
   <details><summary>答案</summary>棋盘上的一次 DFS 同时服务所有词：沿路径走时 trie 节点告诉我们有没有任何词以当前路径为前缀，没有就剪枝；共享前缀只匹配一次；找到的词的分支会被删掉，搜索空间逐渐缩小。</details>
6. 472 里为什么按长度从短到大处理，而且"拼接词"不需要插入 trie？
   <details><summary>答案</summary>按长度升序时，trie 里只有更短（或等长的其他）的词，所以判断"能被切分"自动意味着由至少两个更短的词拼成，不会用自己去匹配自己。拼接词能被更短的词拼出来，今后它能参与的任何拼接都可以直接用它的组成部分完成，所以插入它是冗余的。</details>
7. 资深追问：搜索建议要按"热度"而不是字典序返回 top-3，并且热度实时变化。你怎么设计？
   <details><summary>答案</summary>节点上存 top-k（比如 k = 10，留余量）的 `(热度, 词)` 小根堆 / 有序列表；热度更新时沿词的路径更新每个节点的 top-k（O(L · k)），异步批量化；查询只读节点列表 O(|q|)。规模大时按前缀分片，写入走队列合并，读走缓存；允许最终一致，热度变化延迟几秒通常可接受。</details>
