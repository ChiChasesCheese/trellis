---
id: problems-deck-of-cards-two-cards-and-settle-order
node: problems.games.deck-of-cards
type: cloze
step: 4
tags: [grown]
---
二十一点（Blackjack）一局的结算里有两处特别容易写错。第一处：黑杰克（blackjack）的定义是{{c1::恰好两张牌凑成 21}}——三张 7 也是 21 点但**不是**黑杰克，因为{{c2::两者赔率不同（黑杰克通常 3:2，普通胜 1:1）}}。第二处是判定顺序，必须是{{c3::先判黑杰克、再判爆牌（bust）、最后才比点数}}；顺序错了，「双方都是黑杰克」会被算成{{c4::普通平局甚至某一方胜}}。另外，玩家爆牌之后庄家{{c5::根本不用补牌——庄家已经赢了，补牌只会多消耗牌并影响算牌的人看到的牌序}}。
