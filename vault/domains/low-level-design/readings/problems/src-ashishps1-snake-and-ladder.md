---
nodes: [problems.games.snake-and-ladder]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/snake-and-ladder.md
tags: []
---
# awesome-low-level-design — Designing Snake and Ladder Game

值得读：六种语言（Java / Python / C++ / C# / Go）并排的教科书式写法，用来对照"这道题通常
被要求到什么程度"。类划分是 `Board` + `Player` + `Snake` + `Ladder` + `Dice` +
`SnakeAndLadderGame`，再加一个单例 `GameManager` 用线程跑多局。两处值得当反面教材：`Board`
完全不校验蛇梯布局（于是连跳和死循环都是可能的），以及把"多局并发"用单例加线程塞进模型层
——本题解认为并发属于服务层，`Game` 里一把锁都不该有，模型里出现线程只会让它更难测试。
`Snake`/`Ladder` 两个类在本题解里也被合成了一个 `Jump`，方向是算出来的。
