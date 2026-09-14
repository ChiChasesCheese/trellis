---
id: cc-toolbox-prefix-trie-build
node: toolbox.prefix-trees
type: qa
---
## Q
Build a trie over 10^5 words and answer both "is `p` a prefix of some word" and "is `p` itself a word". Structure and cost?

## A
**Nested dicts plus an explicit terminal marker.**

```python
root = {}
for w in words:
    node = root
    for ch in w:
        node = node.setdefault(ch, {})
    node["$"] = True             # marker key that cannot collide with a character
```

- Insert and lookup are O(len(word)) — independent of how many words are stored, which is the property a hash set cannot match for *prefix* questions.
- Walk to the end of `p`: arriving at a node answers "prefix exists"; `"$" in node` answers "is a word". They are different questions and the marker is the only way to tell them apart.
- The marker must be a key no character can produce; if the alphabet is arbitrary, use a sentinel object or a `(children, is_word)` pair instead of `"$"`.
- Memory is the cost — one dict per node ([[cc-toolbox-prefix-when-not-a-trie]]).

## Q zh
在 10^5 个单词上建 trie，并回答「`p` 是不是某个单词的前缀」以及「`p` 本身是不是一个单词」。用什么结构，代价多少？

## A zh
**嵌套 dict 加一个显式的终止标记。**

```python
root = {}
for w in words:
    node = root
    for ch in w:
        node = node.setdefault(ch, {})
    node["$"] = True             # 不会与任何字符冲突的标记 key
```

- 插入和查找都是 O(len(word))，与存了多少单词无关 —— 这正是哈希集合在*前缀*问题上无法企及的性质。
- 沿 `p` 走到底：能走到节点就回答了「前缀存在」；`"$" in node` 回答「是不是单词」。这是两个不同的问题，而标记是区分它们的唯一手段。
- 标记必须是任何字符都产生不了的 key；若字母表任意，就用哨兵对象或 `(children, is_word)` 二元组代替 `"$"`。
- 代价是内存 —— 每个节点一个 dict（[[cc-toolbox-prefix-when-not-a-trie]]）。
