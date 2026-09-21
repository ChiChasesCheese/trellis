---
nodes:
- iteration.pattern-matching
title: PEP 636：结构化模式匹配教程
corpus: peps
section: 23-pep-0636
url: https://peps.python.org/pep-0636/
tags:
- canonical
---

# PEP 636：结构化模式匹配教程

PEP 636 是 `match`/`case` 的官方教程，用一个文字冒险游戏的命令解析把模式匹配从最简单的字面量匹配一步步推到序列模式、通配符 `_`、捕获变量、`|` 或模式、`if` 守卫、映射模式与类模式（class pattern）。读它是为了建立一个关键认识：`match` 不是 C 的 switch，每个 case 是一次结构解构（destructuring）加名字绑定，匹配失败时已绑定的名字仍可能残留。带走三点：位置类模式依赖类的 `__match_args__`（dataclass 自动生成）；守卫在模式匹配成功之后才求值；一串只比较相等的 `if/elif` 用 `match` 只会更难读——这正是 Effective Python 第 9 条的判断标准。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0636/)

## Archived copy
![[peps-pattern-matching-tutorial-clip]]
%% trellis:end %%
