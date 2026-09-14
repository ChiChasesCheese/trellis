---
id: cc-toolbox-prefix-sorted-bisect
node: toolbox.prefix-trees
type: cloze
---
In a **sorted** word list every word starting with `p` occupies one contiguous block, so a trie is unnecessary: the block runs from {{c1::`bisect_left(words, p)`}} to {{c2::the first index whose word does not start with `p`}}, which `bisect_left(words, p + "￿")` finds. That is {{c3::O(log n)}} per query with no build cost beyond the sort, and it is the right choice whenever the word set is {{c4::static}} — a trie earns its memory only when words arrive incrementally or you need an aggregate at every prefix.

## zh
在**有序**单词表里，所有以 `p` 开头的单词占据一段连续区间，所以并不需要 trie：这段从 {{c1::`bisect_left(words, p)`}} 到 {{c2::第一个不以 `p` 开头的单词的下标}}，后者用 `bisect_left(words, p + "￿")` 求得。每次查询 {{c3::O(log n)}}，除排序外没有构建成本，只要单词集合是 {{c4::静态的}} 就该这么选 —— trie 只有在单词增量到达、或需要每个前缀上的聚合量时才配得上它的内存。
