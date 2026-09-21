---
nodes: [engineering.testing, memory.leaks-tracemalloc]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 13 章 测试与调试
---
# Effective Python 3e · 第 13 章 测试与调试

这一章讲测试金字塔和 `unittest`/`pytest` 的基本写法，以及用 `pdb`/`tracemalloc` 定位运行时错误和内存泄漏的具体手段，强调可重复的测试用例比事后调试更划算。

**读时提取：**
- 单元测试为什么要覆盖边界条件而不只是『happy path』
- `pdb` 断点调试和 `tracemalloc` 定位内存增长各自适用的场景
- mock/patch 替换依赖，让测试不依赖外部系统

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
