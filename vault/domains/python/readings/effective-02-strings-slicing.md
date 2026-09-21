---
nodes: [model.text-bytes, model.sequences]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 2 章 字符串与切片
---
# Effective Python 3e · 第 2 章 字符串与切片

这一章讲 `bytes`/`str` 混用的具体坑（拼接、格式化、写文件模式不一致会直接报错），以及切片 `[start:stop:step]` 的边界规则和它和 `__getitem__` 收到 `slice` 对象的关系。

**读时提取：**
- `bytes` 与 `str` 混合运算为什么会抛 `TypeError`，而不是隐式转换
- 切片赋值可以改变列表长度，这点和索引赋值不同
- `f-string` 相比 `%` 和 `.format()` 在可读性和求值时机上的优势

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
