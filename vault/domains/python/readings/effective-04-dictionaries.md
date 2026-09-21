---
nodes: [model.dict-set-internals, runtime.stdlib-map]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 4 章 字典
---
# Effective Python 3e · 第 4 章 字典

这一章讲字典的惯用写法：用 `get`/`setdefault`/`defaultdict` 替代『先判断键在不在再赋值』的模板代码，以及为什么『在字典里插入默认值』这个动作值得一个专门的容器类型来简化。

**读时提取：**
- `dict.get(key, default)` 与 `setdefault` 分别适合什么场景
- `collections.defaultdict` 如何免去显式的『键不存在就初始化』分支
- 遍历字典时增删键为什么会报 `RuntimeError`

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
