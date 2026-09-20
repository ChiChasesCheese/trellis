---
nodes: [problems.games.tic-tac-toe]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/tic-tac-toe
tags: [no-archive]
---
# lld-python — Design Tic Tac Toe

值得读：少见的**纯 Python** 井字棋题解，而且开篇就点出了两个真正的评分点——判赢不要扫全盘、
机器人的难度应该是一个可换的策略而不是一个标志位。它把每行、每列、两条对角线的计数器直接
放进 `Board` 的四个字段里维护，并用 `MoveResult` 这条不可变记录通知观察者。本题解在两处
往前推了一格：计数器的 O(1) **只在 K == N 时成立**，所以判赢被抽成 `WinRule` 这个 seam，
K 子连珠换成 O(K) 的局部行走；另外机器人在这里是一个普通函数（闭包）而不是策略类，并且
额外提供了"假设判定"`completes_line`，让机器人问"我走这里会赢吗"时不必碰棋盘的记账状态。
