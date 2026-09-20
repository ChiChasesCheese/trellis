---
nodes: [problems.games.deck-of-cards, python.dataclasses-enums]
tags: [problem]
---
# Drill：扑克牌与二十一点（Deck of Cards / Blackjack）

"设计一副扑克牌，然后在上面实现二十一点。"——这两句话之间的那个"然后"就是全部考点。它不是
游戏题，是**抽象题**：线的这一侧是"扑克牌这个东西本身"，那一侧是"某个游戏怎么用它"。线画
错了，第二个游戏就再也接不上去，而面试官一定会加第二个游戏。按真实机考的节奏分关做。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：`Rank`、`Suit`、`Card` 三个不可变值——可哈希（能进集合和字典）、
  可排序、`__repr__` 打出来人一眼能读懂；`Deck` 能洗（**随机源是必填参数**）、能发、能报
  还剩几张，**而且永远不把内部那份牌列表交出去**。空牌堆继续发牌要有名字。写之前先回答：
  "一次发 5 张但只剩 3 张"该少发还是全不发？牌堆顶放在列表的哪一端，为什么？
- 第 2 关（约 15 分钟）：在牌组之上做二十一点——A 算 11 或 1、爆牌、黑杰克、庄家固定策略，
  **`Deck` 一个字都不许知道 21 点**。做到这里会撞上两堵墙：A 的点数别用 2ⁿ 枚举（想清楚
  为什么最多只有一张 A 能算 11）；黑杰克不是"凑够 21"。然后**必须再写第二个游戏**（战争
  最省事）共用同一副牌——一个抽象只有被用过两次才算被验证过。
- 第 3 关（约 15 分钟）：几副牌摞进一只牌鞋（shoe），插一张切牌（cut card），切到就该重洗
  （但**不许自动洗**，一局牌要打完）。算牌（card counting）做成一个**观察者**：牌鞋只广播
  事件，算牌器只从事件里取数。两个必答的细节：事件里该带哪几样数据？洗牌时算牌器要做什么？
- 第 4 关（选做，约 10 分钟）：给牌堆加小丑牌，或者加第五门花色。验收标准很硬：**游戏代码
  一行不改**。顺便想清楚：21 点遇到取值表里没有的牌，该抛异常还是按 0 分兜住？

**怎么练**：把 `vault/domains/low-level-design/problems/deck-of-cards/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/deck-of-cards -q`。

**评分点**
- `Card` 上没有任何游戏规则（没有 `value`、没有 `BlackJackCard` 子类、没有 `is_available`），
  并说得出检验标准："正确值取决于在玩哪个游戏的属性，就不属于 `Card`"
  （[[problems-deck-of-cards-rules-not-on-card]]、[[oop-entity-vs-value-object]]）。
- `Deck` 不交出内部列表，只给 `remaining` 和 `deal`；发牌是原子的；牌堆顶在列表末尾所以
  发牌是 O(1)（[[problems-deck-of-cards-deck-hides-its-cards]]、[[oop-getter-collection-leak]]）。
- 牌是 `frozen=True` 的 dataclass，因此可哈希、能当字典键、跨线程共享不用同步
  （[[python-dataclass-hash-rule]]、[[problems-deck-of-cards-shoe-lock-and-immutable-cards]]）。
- A 的点数用"最多一张 A 能算 11"的一次加法，而不是 2ⁿ 枚举；顺手得到 `is_soft`
  （[[problems-deck-of-cards-ace-eleven-or-one]]）。
- 黑杰克是**恰好两张**牌凑 21；结算顺序是先黑杰克、再爆牌、最后比点数
  （[[problems-deck-of-cards-two-cards-and-settle-order]]）。
- 真的写了第二个游戏，而且它对 A 的排序和 21 点不同——这是分界线画对了的唯一证据
  （[[problems-deck-of-cards-rules-not-on-card]]）。
- 算牌是观察者，事件自带"发了哪几张、还剩几副"，洗牌事件让计数归零，订阅能取消
  （[[problems-deck-of-cards-counting-is-an-observer]]）。
- 造牌遍历显式的点数／花色清单而不是整个枚举，所以加小丑或第五门花色是换参数
  （[[problems-deck-of-cards-enum-closed-extend-the-composition]]）。
- 不认识的牌大声抛异常，而不是 `values.get(rank, 0)` 悄悄算 0 分
  （[[problems-deck-of-cards-unknown-card-fails-loudly]]）。
- 洗牌的随机源必填、没有默认值；测试要么用定死牌序，要么固定种子只断言与种子无关的不变量
  （[[problems-deck-of-cards-injected-rng-and-scripted-decks]]）。

**题解**：[[solution-deck-of-cards]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
