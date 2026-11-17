---
id: psy-game-beauty-contest
node: game.theory.beauty-contest
type: qa
step: 1
tags: [证据强]
---
## Q
团建时玩个游戏：每人在 0 到 100 之间写一个数，谁最接近全体平均数的 2/3 谁赢。你写多少？

## A
**猜数与 k 层思考（k-level thinking, Keynesian beauty contest）：赢不靠推到最深，靠猜对别人推了几步；多数人只推一两步。**

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<line x1="30" y1="110" x2="310" y2="110" stroke="currentColor"/>
<g stroke="currentColor">
<line x1="30" y1="104" x2="30" y2="116"/>
<line x1="310" y1="104" x2="310" y2="116"/>
<line x1="170" y1="104" x2="170" y2="116"/>
<line x1="122" y1="104" x2="122" y2="116"/>
<line x1="92" y1="104" x2="92" y2="116"/>
</g>
<circle cx="66" cy="110" r="6" fill="currentColor"/>
<g fill="currentColor">
<text x="30" y="135">0</text>
<text x="30" y="152">全推到底</text>
<text x="310" y="135">100</text>
<text x="170" y="92">50</text>
<text x="170" y="75">不推</text>
<text x="122" y="135">33</text>
<text x="122" y="152">推一步</text>
<text x="92" y="92">22</text>
<text x="92" y="75">推两步</text>
<text x="66" y="185">13 赢</text>
<text x="66" y="202">FT 1997</text>
</g>
<line x1="66" y1="118" x2="66" y2="170" stroke="currentColor" stroke-dasharray="3 3"/>
</g>
</svg>

**故事。** 1997 年，Thaler 在《金融时报》上办了这个比赛，奖品是两张飞北美的商务舱机票，收到 1,382 份答案。完全理性的推法一路往下砍：大家都写 50 我就写 33，都写 33 我就写 22……一直到 0。实际平均数是 18.9，赢家写的是 13。写 0 的人推得最深，却没赢。2015 年他在同一份报纸重办，平均 17.3，赢家写 12。

- **证据 · 强：** Nagel 1995 年在实验室让学生连玩几轮：第一轮的答案多停在推一步、推两步的位置，多玩几轮，中位数一轮轮往下走。Keynes 1936 年用报纸选美比赛比喻股市：要猜的不是谁最美，是大家以为大家会选谁。
- **动手：** 下次在要预判别人的局里（定价、投标、抢热门名额），先估对手会推几步，比他们多推一步就够，别直接跳到理论上的最优解。
