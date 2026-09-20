---
id: problems-snake-and-ladder-validate-at-construction
node: problems.games.snake-and-ladder
type: qa
step: 1
tags: [grown]
---
## Q
在蛇梯棋（Snake and Ladder）设计里，棋盘允许出现「一条蛇的尾巴正好是一架梯子的脚」这种布局时，走子代码通常写成 `while` 一路追跳跃链。为什么这份看起来更通用的写法是错的？该换成什么？

## A
因为它可以**死循环**：梯子 12→25、蛇 25→12 首尾互指，追链的循环永远转不出来，而这不是某一次掷骰的问题、是棋盘配置的问题，任何输入校验都发现不了。

正确做法是把问题提前到构造时：`Board.__init__` 里一行集合求交，拒绝「任何跳跃的终点同时是另一跳跃的起点」的棋盘。

```python
chained = {j.end for j in table.values()} & set(table)
if chained:
    raise InvalidBoardError(f"{sorted(chained)} 会连跳")
```

校验通过后，「一次移动最多触发一次跳跃」就是**结构上成立**的事实，走子里那个 `while` 直接消失——没有循环就没有环。只有面试官明确要求支持连跳时才保留循环，而那时必须同时加环检测（用一个 `seen` 集合），代价是错误在一局棋下到一半才抛出、状态已经改了一半。
