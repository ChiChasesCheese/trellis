---
nodes: [model.text-bytes]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 4 章 Unicode 文本与字节序列
---
# Fluent Python 2e · 第 4 章 Unicode 文本与字节序列

这一章讲 Python 3 里 `str` 是 Unicode 码点序列、`bytes`/`bytearray` 是原始字节，两者靠编码/解码转换；混用会直接报 `TypeError`，而不是像 Python 2 那样悄悄坏掉。

**读时提取：**
- `str.encode()` / `bytes.decode()` 的方向不要记反
- 为什么『先解码晚编码』是处理文本 I/O 的推荐姿势
- 编码错误处理策略（strict/ignore/replace）在什么场景该选哪个

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
