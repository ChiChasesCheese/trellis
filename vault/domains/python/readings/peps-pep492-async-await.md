---
nodes:
- asyncio.coroutines-tasks
- iteration.yield-from
title: PEP 492：async/await 语法与原生协程
corpus: peps
section: 06-pep-0492
url: https://peps.python.org/pep-0492/
tags:
- canonical
---

# PEP 492：async/await 语法与原生协程

说明为什么 async/await 不是简单给生成器加语法糖，而是把“原生协程”做成完全独立的类型。Rationale 列出用生成器模拟协程（PEP 342 + PEP 380 的 yield from）的三个痛点：协程和普通生成器语法相同容易混淆；一个函数是不是协程取决于函数体里有没有 yield，重构时容易悄悄改变语义；yield 只能出现在语法允许的位置，限制了 with/for 这类语句里做异步调用。async/await 通过 async def、await、async with、async for 从根上解决了这些问题，也让 linter 和 IDE 能可靠识别协程。读这篇要建立的直觉是：async/await 是 yield from 协程用法的“正名”和收口，理解它和 PEP 380/342 的关系，才能回答“协程和生成器到底是什么关系”这类高频追问。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0492/)

## Archived copy
![[peps-pep492-async-await-clip]]
%% trellis:end %%
