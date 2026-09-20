---
nodes: [problems.games.deck-of-cards]
url: https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles
tags: [no-archive]
---
# Grokking the Low Level Design Interview Using OOD Principles (Educative)

值得读：付费课程里对这道题的标准处理，值得看的是它列出的**需求清单**（几副牌、庄家规则、
多个玩家座位、下注与赔付），可以用来对照自己的澄清问题问全了没有，以及它对追问方向的排序
（分牌、加倍、保险几乎必问）。它的类划分仍然把点数规则放在牌的一侧，本题解不同意这一点：
同一张 A 在 21 点里是 1 或 11、在战争里最大，一个属性不可能同时正确，规则必须是游戏自己的
一张表。课程用 Java 讲解，本题解全部用 Python，值对象与策略的载体因此完全不同。
