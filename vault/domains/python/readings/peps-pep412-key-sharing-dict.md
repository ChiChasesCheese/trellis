---
nodes:
- memory.object-size
title: PEP 412：键共享字典（Key-Sharing Dictionary）
corpus: peps
section: 24-pep-0412
url: https://peps.python.org/pep-0412/
tags:
- canonical
---

# PEP 412：键共享字典（Key-Sharing Dictionary）

解释同一个类的多个实例，它们的 __dict__ 为什么能共享内存而不是各自复制一份键。核心机制是把字典拆成“键表”和“值数组”两部分（split-table）：实例属性字典默认以 split 形式创建，键表缓存在类型对象上，只要各实例没有动态增删不同的属性，键表就能被同一个类的所有实例共享，值数组各自独立。一旦某个实例的键开始分化（比如动态加了别的没有的属性），该字典会惰性转换回普通的合并表（combined-table）形式，保证正确性优先于内存优化。实测收益是面向对象程序内存降低 10%-20%，字典本身可以缩小近一半。也说明了代价：改变了内部数据结构，直接操作字典内部的第三方代码会失效；split 字典的迭代顺序可能和以前不同。这是回答“为什么该用 __slots__ 而不是普通属性字典”时的背景知识。
