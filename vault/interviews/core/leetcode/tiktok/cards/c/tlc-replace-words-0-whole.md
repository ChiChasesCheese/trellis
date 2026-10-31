---
id: tlc-replace-words-0-whole
node: c.replace-words
type: qa
---
## Q
**LC 648 单词替换**｜Medium · LC TikTok 全时段热度 38/100

给定由词根组成的词典 `dictionary` 和一个空格分隔的句子 `sentence`。把句子里每个以某个词根为前缀的单词（衍生词）替换成词根；一个衍生词有多个词根可选时，用**最短**的词根。返回替换后的句子。`1 <= dictionary.length <= 1000`，`1 <= dictionary[i].length <= 100`，`1 <= sentence.length <= 10^6`，全部为小写字母，句子里单词数在 `[1, 1000]`，每个单词长度在 `[1, 1000]`，单词间一个空格，无前导和尾随空格。例：`dictionary = ["cat","bat","rat"]`，`sentence = "the cattle was rattled by the battery"` → `"the cat was rat by the bat"`；`dictionary = ["a","b","c"]`，`sentence = "aadsfasf absbs bbab cadsfafs"` → `"a a b c"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把词根建成前缀树（Trie），每个单词沿树往下走，碰到的第一个词根结尾就是最短词根。

**识别。** 「找最短的前缀匹配」：前缀树的第一个结尾节点自动就是最短的。词根最长 100，句子单词最长 1000，不能对每个单词对每个词根都比较。

**推导。** 对每个单词切出 `word[:1]`、`word[:2]`……看是否在词根集合里，第一个命中的就是最短，切片开销随长度累加。把词根建成 Trie，沿单词逐字符往下走：走到词根结尾立刻返回，走不下去说明没有词根，原样返回。

**简单解法。** 词根放进集合，对每个单词的前缀依次查找。

```python
def replace_words_set(dictionary: list[str], sentence: str) -> str:
    roots = set(dictionary)
    longest = max(map(len, dictionary))          # 前缀不必比最长词根更长

    def shorten(word: str) -> str:
        for i in range(1, min(len(word), longest) + 1):
            if word[:i] in roots:                # 从短到长，第一个命中就是最短词根
                return word[:i]
        return word

    return " ".join(map(shorten, sentence.split()))
```

每个单词最多切 `100` 次、每次切片 `O(100)`，总共约 `10^7` 字符操作，足够；Trie 省掉切片和哈希。

最优解：

```python
def replace_words(dictionary: list[str], sentence: str) -> str:
    trie: dict[str, dict] = {}
    for root in dictionary:
        node = trie
        for ch in root:
            node = node.setdefault(ch, {})
        node["$"] = root                         # "$" 记录以此结尾的词根本身

    def shorten(word: str) -> str:
        node = trie
        for ch in word:
            if ch not in node:                   # 前缀走不通：没有词根可替换
                break
            node = node[ch]
            if "$" in node:                      # 第一次碰到词根结尾 = 最短词根
                return node["$"]
        return word

    return " ".join(map(shorten, sentence.split()))
```

运行：示例 1 → `"the cat was rat by the bat"`，示例 2 → `"a a b c"`；`dictionary = ["ab","abc"]`，`sentence = "abcd ab x"` → `"ab ab x"`（取最短词根 `ab`）。

**复杂度。** 建树 `O(Σ|root|)`，每个单词最多走 `min(|word|, 100)` 步，总 `O(Σ min(|word|, 100))`；空间 `O(Σ|root|)`。

**拓展优化。**
- 词根很多时节点用数组 `[None] * 26` 代替字典，内存连续；Python 里字典版更短，面试够用。
- 同一部词典反复处理多个句子：Trie 只建一次，每个句子复用。

**易错点。**
- 命中词根结尾后不返回、继续往下走：会取到更长的词根，示例 `["ab","abc"]` 会错。
- 漏掉循环结束后的 `return word`：单词没有碰到任何词根结尾时必须原样返回。
- 句子用 `split(" ")` 而不是 `split()`：题目保证单空格分隔时两者一致，但习惯用 `split()` 对多空格更安全。

**追问。**
- 句子特别长（`10^6` 字符）：`split` 和 `join` 都是线性，没有问题；流式处理则逐词输出。
- 词根增删频繁：Trie 本身支持增量插入，删除时回溯清理空节点。

**同模式。** LC 208 实现前缀树、LC 1268 搜索推荐系统、LC 677 键值映射、LC 676 实现魔法字典、LC 616 给字符串添加加粗标签。
