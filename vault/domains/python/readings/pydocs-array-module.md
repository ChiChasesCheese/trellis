---
nodes:
- performance.less-ram
- model.sequences
title: array 模块：紧凑数值数组
corpus: python-docs
section: 59-array
url: https://docs.python.org/3/library/array.html
tags:
- canonical
---

# array 模块：紧凑数值数组

array 模块提供了一种比普通 list 更节省内存的同质数值数组：list 存的是一串指向 Python 对象的指针，即使全是整数，每个元素依然是一个完整的 Python int 对象，有可观的对象头开销；array 则按 C 语言的方式紧凑存储原始数值（通过类型码指定是 int、float 等哪种 C 类型及字节宽度），内存占用能降低数倍。文档列出了支持的类型码表（i 表示有符号 int、d 表示 double 等）。这是存海量同质数值但又不想引入 NumPy 依赖时的轻量选择，如果确实需要向量化运算，NumPy 数组通常是更好的选择，array 更适合只需要紧凑存储、顺序读写，不需要复杂数值运算的场景，比如从二进制协议里解析出的定长数值序列。
