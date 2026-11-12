---
slug: replace-words
---
## Q
**LC 648 单词替换**｜Medium

给词根词典 `dictionary` 和句子 `sentence`，把句中每个单词替换成它最短的词根前缀，没有词根就保持不变。

## A
**一句话。** 词根建前缀树（Trie），单词沿树往下走，第一个遇到的词根结尾就是最短词根。

```python
def replace_words(dictionary, sentence):
    trie = {}
    for root in dictionary:
        node = trie
        for ch in root:
            node = node.setdefault(ch, {})
        node["$"] = root           # 记录以此结尾的词根

    def shorten(word):
        node = trie
        for ch in word:
            if ch not in node:
                break
            node = node[ch]
            if "$" in node:
                return node["$"]   # 第一个词根结尾最短
        return word

    return " ".join(map(shorten, sentence.split()))
```

**复杂度。** 时间 `O(Σ|root| + Σ|word|)`，空间 `O(Σ|root|)`。

**易错点。**
- 命中词根后不返回、继续往下走：会取到更长的词根，`["ab","abc"]` 就错。
- 漏掉最后的 `return word`：没命中任何词根的单词必须原样返回。

**追问。**
- 词根频繁增删？：Trie 支持增量插入，删除时回溯清掉空节点。
- 不用 Trie 怎么做？：把词根放进集合，对每个单词枚举前缀查表，`O(L^2)`。

**同模式。** LC 208 实现前缀树、LC 1268 搜索推荐系统、LC 677 键值映射、LC 676 实现魔法字典
