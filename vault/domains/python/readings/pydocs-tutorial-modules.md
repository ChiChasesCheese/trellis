---
nodes:
- runtime.import-system
- runtime.compile-bytecode
title: Python 教程第 6 章：模块
corpus: python-docs
section: 18-modules
url: https://docs.python.org/3/tutorial/modules.html
tags:
- canonical
---

# Python 教程第 6 章：模块

官方教程讲模块系统的入门篇，比参考手册的 import 系统章节好懂得多：模块搜索路径（sys.path）的构成顺序、.pyc 编译缓存文件为什么会出现在 __pycache__ 目录下（按文件名加版本标签存放，避免不同 Python 版本互相覆盖）、以及为什么 .pyc 只是加载更快而不是运行更快。6.4 节讲包（package）的 __init__.py 作用和 from package import * 如何通过 __all__ 控制导出内容，还讲了包内如何用相对导入互相引用。这是理解为什么改了 .py 文件有时候不生效（多半是读到了过期的 .pyc 缓存或者装的是另一个同名包）的基础，适合作为深入学习 import 系统权威文档之前的热身读物。
