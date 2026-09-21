---
nodes: [functions.arguments, functions.scope-closure, functions.decorators]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 5 章 函数
---
# Effective Python 3e · 第 5 章 函数

这一章聚焦函数签名设计：位置参数与关键字参数、`*args`/`**kwargs`、仅关键字参数（`*` 分隔符）如何让 API 既灵活又不容易被调用者用错；也重申了闭包对外层变量的捕获时机。

**读时提取：**
- 仅位置参数 `/` 和仅关键字参数 `*` 分隔符分别解决什么 API 稳定性问题
- 可变默认参数的坑：默认值只在函数定义时求值一次
- 闭包捕获的是变量本身而不是定义时的值，循环里定义闭包容易踩这个坑

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
