---
nodes:
- model.numbers
- model.sequences
- model.text-bytes
- model.dict-set-internals
- types.basics
title: 内建类型（Built-in Types）完整参考
corpus: python-docs
section: 60-stdtypes
url: https://docs.python.org/3/library/stdtypes.html
tags:
- canonical
---

# 内建类型（Built-in Types）完整参考

这是查内建类型方法签名和行为细节时最该回来的一份文档，覆盖了数值类型（int/float/complex 及各自的位运算、哈希规则）、序列类型（list/tuple/range 的通用操作、可变与不可变序列各自支持哪些方法）、文本与二进制序列（str/bytes/bytearray/memoryview，包括 f-string、百分号格式化的完整语法）、集合类型、映射类型（dict 极其完整的方法列表和保留插入顺序这一语言保证）、上下文管理器类型，以及泛型别名和联合类型（list[int]、X | None）的运行时对象表示。这份文档篇幅巨大但结构清晰，日常不需要通读，遇到这个方法到底支持什么参数、这个类型到底能不能这样用时按目录定位查阅即可，是内建类型行为的最终裁决来源。
