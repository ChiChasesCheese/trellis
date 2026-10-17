# 连接词的 Trie + DFS 写法（Concatenated Words, Trie + DFS）

给一个单词列表，找出其中所有的「连接词」：能由列表里至少两个较短的单词首尾相接拼成的单词。常见做法是把词放进集合，再对每个单词做动态规划（DP）切分。这一讲换一种写法：把词典建成前缀树（Trie），沿着单词的字符在树上走，走一次就能知道从某个起点出发有哪些词典词可以接上，再用 DFS 加记忆化往后切。

## 题面与约束
给一个不重复的单词列表，返回其中所有「连接词」：能由列表里**至少两个**较短的单词拼成。
约束：`1 <= words.length <= 10^4`，`1 <= words[i].length <= 30`，`words[i]` 只含小写字母，`words` 中字符串互不相同，`1 <= sum(words[i].length) <= 10^5`。

## 开场先问的澄清问题
1. 单词可以重复使用吗？（可以，如 `ratcatdogcat`。）
2. 一个单词能由它自己拼成吗？（不能：至少两段。）
3. 空串是否出现？（约束里最短为 1。）

## 先补一点基础：Trie（前缀树）
- **是什么**：每个节点代表一个前缀，边是字符；某节点标记「这里结束了一个单词」。
- **为什么需要**：切分单词时要反复问「`w[i:j]` 是不是词典里的词」。用集合要切片、哈希，每次 O(L)；Trie 沿着字符一直走，**走一次就能知道 i 开头的所有词典词的结尾位置**。
- **怎么工作**：插入 `cat`：根 → c → a → t(标记)。再插入 `cats`：沿用 c-a-t，再添一个 s(标记)。

## 与词集合 DP 的对比
| | 词集合 + DP | Trie + DFS |
|---|---|---|
| 判断一段是不是词 | 切片后查哈希，O(L) | 沿 Trie 走，每步 O(1) |
| 枚举一个起点的所有切法 | 对每个终点各切一次，O(L²) 字符操作 | 一次走到底，遇到标记就是一个候选终点，O(L) |
| 剪枝 | `dp[i]` 数组 | 记忆「从 i 开始切不通」的集合 |
| 递归深度 | 无递归 | 最多一层一个词，≤ 单词长度 30 |

## 最笨解
对每个单词，枚举所有切分点，每段查集合，递归判断剩余部分，指数级；`_brute` 即此（仅小数据）。

## 逐步改进
1. **问题**：每个起点重复检查大量前缀，每次检查都要切片和哈希。
2. **想法**：把所有单词建一棵 Trie；对单词 w 从下标 i 出发沿 Trie 走，每遇到「单词结尾」标记就在该位置 j+1 递归。沿树走一次就列出了所有候选终点，不用逐个切片。
3. **「至少两段」**：从 0 开始的第一段不能是整个单词本身（否则每个单词都能由自己拼成）。条件写成 `i > 0 or j + 1 < len(w)`。
4. **记忆化**：某个起点 i 失败过，后续从同一个起点也不会成功（剩余部分只关心能否切开，与已经切了几段无关），记入 `dead`，保证每个起点只展开一次，每个单词 O(L²) 最坏（L ≤ 30），总 O(sum(L²)) 量级。
5. **深度**：递归层数 ≤ 单词长度 ≤ 30，没有栈溢出风险。

```python
def find_all_concatenated_words(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def can_split(w, i, dead):                            # can w[i:] be cut into >= 1 dictionary words?
        if i == len(w):
            return True
        if i in dead:
            return False
        node = root
        for j in range(i, len(w)):
            node = node.get(w[j])
            if node is None:
                break
            if "$" in node and (i > 0 or j + 1 < len(w)):   # from 0 the piece must not be the whole word
                if can_split(w, j + 1, dead):
                    return True
        dead.add(i)                                       # memo: failing suffixes are never retried
        return False

    return [w for w in words if w and can_split(w, 0, set())]
```

示例：`cat, cats, catsdogcats, dog, dogcatsdog, hippopotamuses, rat, ratcatdogcat` 返回 `catsdogcats, dogcatsdog, ratcatdogcat`；`[a, b, ab, abc]` 只有 `ab`（`abc` 的 `c` 不在词典里）。

## 复杂度
建 Trie O(S)，S = sum(len)；每个单词 O(L²)（L ≤ 30），总 O(Σ L²)。空间 O(S)。

## senior 追问
1. **与「最短优先」写法的取舍**：最短优先只需要含更短单词的 Trie，建 Trie 时跳过连接词，节点更少；上面的写法对原列表顺序无要求，更直观。
2. **单词很长（1e5）**：Python 递归不行，改自底向上 DP：`reachable[i]`，枚举时在 Trie 上走；`dead` 集合就是这个 DP 的记忆表。
3. **返回具体的拼法**：DFS 记录路径；或者 DP 记前驱。
4. **要求至少三段**：把「段数」放入状态（计数 min(段数, 3)）。
5. **字符集很大或 Unicode**：Trie 子节点用字典而不是长度 26 的数组（上面的代码已是）。
6. **词典在线更新**：Trie 的插入天然支持；删除时只要把结尾标记去掉，必要时清理空分支。

## 自测题
1. 为什么 `i > 0 or j + 1 < len(w)` 不写成 `j + 1 < len(w)`？
<details><summary>答案</summary>`i > 0` 时最后一段到达末尾是合法的结束；只有从 0 开始的第一段不能覆盖整个单词。</details>
2. `dead` 为什么按起点记，而不按 (起点, 段数) 记？
<details><summary>答案</summary>第一段之后「至少两段」已经满足，剩余部分只关心能否切开，与段数无关。</details>
3. 去掉 `dead` 会怎样？
<details><summary>答案</summary>答案仍正确，但同一后缀被重复展开，最坏指数级。</details>
