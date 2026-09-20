---
nodes: [problems.games.chess]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/chess-game.md
tags: [no-archive]
---
# awesome-low-level-design — Chess Game

值得读：这道题在市面上流传最广的版本，六种语言（含 Python）并排给出同一份设计，知道它长什么样，
才知道面试官心里的参照系是什么。它的 `Piece` 抽象类自带 `color, row, col`，每个子类实现
`canMove(board, destRow, destCol)` 只返回布尔值，棋盘上另有 `isCheckmate()` 单独判定。
本题解在三处反着做，并在"关键设计决策"里逐条给出理由：棋子不存坐标（否则棋盘和棋子是两份真源，
每次试走都要同步）、棋子只**生成**落点而不判合法（合法性是整个局面的性质，牵制让棋子答不了这个问题）、
将死不是一个单独的算法而是"没有合法着法 + 王在将中"的推论。
