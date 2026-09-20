---
nodes: [problems.games.chess]
url: https://www.chessprogramming.org/Perft_Results
tags: [no-archive]
---
# Chess Programming Wiki — Perft Results

值得读：棋类程序社区维护的 perft（performance test）标准答案——从给定局面出发，深度 N 的
叶子局面个数是多少，全世界公认。开局局面是 1 层 20、2 层 400、3 层 8902；常用的 "Kiwipete"
局面（两边都还能双向易位、满盘牵制与吃子）是 1 层 48、2 层 2039。设计轮不需要写引擎，
但这几个数字是**走法生成唯一一条便宜又彻底的正确性保险**：一旦对上，伪合法生成、合法性过滤、
易位、吃过路兵、升变，以及落子与回滚是否严格互逆，全部被一次性验到。本题解的测试就用了这两组数。
