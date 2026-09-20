---
nodes: [problems.games.tic-tac-toe]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/tic-tac-toe.md
tags: [no-archive]
---
# awesome-low-level-design — Tic Tac Toe

值得读：同一份设计用六种语言（含 Python）并排给出，是这道题在市面上流传最广的参照系，
知道它长什么样，才知道面试官心里的"标准答案"是什么。类划分是 `Board` + `Game` + `Player`
外加一个只有 `main` 的 `TicTacToe` 入口类；`Board.check_winner()` 每次扫全盘，棋盘边长写死
3×3，`Player` 只有名字和符号、不具备决策能力，没有悔棋也没有 K 子连珠。本题解正是反着做的：
不设入口类（Python 用 `if __name__ == "__main__":`），判赢做成增量计数与局部行走两种规则，
并把"决策"作为一个可选的函数字段放进 `Player`，这样接入电脑玩家不需要任何新的继承层次。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/tic-tac-toe.md)
%% trellis:end %%
