---
id: storage-inverted-index
node: storage.search
type: qa
---
## Q
What is an inverted index, and why can't a B-tree index on a text column do the same job?

## A
A map from **term → posting list of documents containing it** (plus positions/frequencies), built after analysis (tokenizing, lowercasing, stemming). A query intersects/unions the posting lists of its terms, then ranks by relevance (TF-IDF/BM25).

A B-tree indexes the **whole column value** in sort order: it can answer prefix matches (`LIKE 'foo%'`) but not "documents containing this word anywhere", relevance ranking, or fuzzy/multi-term queries — those need per-term postings.

## Q zh
什么是倒排索引，为什么 B-tree 在文本列上的索引无法做同样的工作？

## A zh
一个从**词项 → 包含它的文档的 posting list**（加上位置/频率）的映射，在分析后构建（tokenization、小写、词根还原）。查询相交/并合并其词项的 posting list，然后按相关性排序（TF-IDF/BM25）。

B-tree 在排序顺序中索引**整个列值**：它可以回答前缀匹配（`LIKE 'foo%'`）但不能"包含此词的文档"、相关性排序或模糊/多词查询——那些需要每词 posting。
