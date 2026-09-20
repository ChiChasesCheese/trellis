---
nodes: [problems.games.chess, oop.pillars, patterns.command]
tags: [problem]
---
# Drill：国际象棋（Chess）

题库里最狠的一道，狠不在算法而在**做不完**：完整规则写熟了也要两三个小时，面试只给 45 分钟。
所以这道题的第一个评分点是**你会不会先把范围谈妥**，第二个才是你划下的那条线里代码有没有被
特殊规则冲垮。不做搜索、不做局面评估——那是引擎，不是规则。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 25 分钟）：8×8 棋盘、六种棋子，每种按自己的规则生成**伪合法着法**（只管走法，
  不管走完自己的王会不会挨将）。硬要求：车、象、后共用**一段**"沿方向一直滑"的代码；棋盘里
  不许出现一串 `isinstance` 的类型阶梯。动手前先回答：棋子该不该知道自己在哪一格？说出另一个
  候选的代价。
- 第 2 关（约 20 分钟）：合法性。一手棋合法当且仅当走完之后自己的王不被攻击——生成伪合法着法，
  逐个走一遍再精确退回来。然后把将军、将死、逼和**推导**出来，不要为它们各写一套算法。
  做完数一数：你为"牵制""闪将""两王不能相邻""被将时只能应将"写了几行专门代码？答案应该是 0。
- 第 3 关（约 25 分钟）：三条会冲垮朴素模型的特殊规则。建议顺序是**吃过路兵 → 升变 → 易位**，
  因为吃过路兵逼你把"被吃的子"和"被吃的格"拆成两个字段（一开始不拆，后面改起来很疼）。
  易位要做全：权利在王或车一动时永久失去、车在原地被吃也失去、不能从被将中易位、不能经过
  被攻击的格。
- 第 4 关（选做，约 15 分钟）：悔棋、五十步计数、三次重复，外加一个能序列化的着法记录。
  验收标准很硬：**加记谱不许改走法生成的任何一行**——先想清楚记号该选哪一种。
  自检用 perft：从开局数深度 1/2/3 的叶子局面，必须是 20 / 400 / 8902。

**怎么练**：把 `vault/domains/low-level-design/problems/chess/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/chess -q`。

**评分点**
- 棋子不存坐标：位置只有棋盘那张字典知道，棋子退化成不可变的值对象
  （[[problems-chess-piece-is-a-value]]、[[oop-encapsulation-anemic-model]]）。
- 合法性属于局面不属于棋子：伪合法生成 + 统一过滤，牵制与闪将是副产品，将死 = 无合法着法 + 在将中
  （[[problems-chess-pseudo-then-filter]]、[[oop-polymorphism-vs-switch]]）。
- 试走用 make/unmake 而不是深拷贝，并把被覆盖的旧状态随着法记录存成备忘录；说得出"生成合法着法
  会临时改棋盘，所以它不是可并发的只读方法"
  （[[problems-chess-make-unmake-memento]]、[[patterns-memento-vs-command-undo]]）。
- 易位权是棋盘的状态，不是棋子上的 `has_moved`；答得出"车在原地被吃"这一种
  （[[problems-chess-castling-rights-not-has-moved]]）。
- 吃过路兵：被吃的格不是目标格，而且只在紧接着的一手有效
  （[[problems-chess-en-passant-two-squares]]）。
- 升变：一个落点对应四手棋，接口强制声明升变成什么，不默认升后
  （[[problems-chess-promotion-four-moves]]）。
- 记谱选长代数而不是 SAN，理由是 SAN 消歧要回头重新生成合法着法
  （[[problems-chess-notation-long-algebraic]]、[[patterns-command-callable-vs-class]]）。
- 三次重复的局面指纹含该谁走、易位权、吃过路兵格；计数表减到 0 要删键，悔到开局必须缩回原样
  （[[problems-chess-repetition-fingerprint]]）。

**题解**：[[solution-chess]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
