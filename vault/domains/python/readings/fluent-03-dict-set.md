---
nodes: [model.dict-set-internals, model.hash-eq]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 3 章 字典与集合
---
# Fluent Python 2e · 第 3 章 字典与集合

这一章解释字典和集合为什么是 O(1) 平均查找：都建立在哈希表之上，键必须可哈希，而可哈希要求 `__hash__` 和 `__eq__` 保持一致。也讲了 3.7+ 字典保序是实现细节变正式语义的过程。

**读时提取：**
- 可哈希对象必须满足 `__eq__` 相等则 `__hash__` 相等
- 字典查找为什么平均是 O(1)，哈希冲突怎么处理
- 字典从 CPython 3.6 起保持插入顺序，3.7 起这是语言保证
- 集合运算（并、交、差）背后仍然是哈希表的操作

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
