---
id: psy-judge-small-numbers
node: judge.prob.small-numbers
type: qa
step: 1
tags: [证据强]
---
## Q
你们 A/B 测试开了两天，每组 40 个用户，新版转化率高了一倍，产品经理要立刻全量。这个数字能信吗？

## A
**小数定律（law of small numbers）：小样本的平均值波动大，更容易出极端结果；人却把小样本当成总体的缩影。**

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor" opacity="0.6">
<line x1="30" y1="105" x2="325" y2="105"/>
</g>
<g fill="none" stroke="currentColor" stroke-dasharray="4 3" opacity="0.7">
<polyline points="40,17.0 58,42.8 76,54.2 94,61.0 112,65.6 130,69.1 148,71.7 166,73.9 184,75.7 202,77.2 220,78.5 238,79.6 256,80.6 274,81.5 292,82.3 310,83.0"/>
<polyline points="40,193.0 58,167.2 76,155.8 94,149.0 112,144.4 130,140.9 148,138.3 166,136.1 184,134.3 202,132.8 220,131.5 238,130.4 256,129.4 274,128.5 292,127.7 310,127.0"/>
</g>
<g fill="currentColor">
<circle cx="40" cy="35" r="2.6"/>
<circle cx="40" cy="160" r="2.6"/>
<circle cx="58" cy="153" r="2.6"/>
<circle cx="58" cy="75" r="2.6"/>
<circle cx="76" cy="61" r="2.6"/>
<circle cx="76" cy="125" r="2.6"/>
<circle cx="94" cy="141" r="2.6"/>
<circle cx="112" cy="77" r="2.6"/>
<circle cx="130" cy="127" r="2.6"/>
<circle cx="148" cy="93" r="2.6"/>
<circle cx="166" cy="130" r="2.6"/>
<circle cx="184" cy="85" r="2.6"/>
<circle cx="202" cy="113" r="2.6"/>
<circle cx="220" cy="123" r="2.6"/>
<circle cx="238" cy="91" r="2.6"/>
<circle cx="256" cy="111" r="2.6"/>
<circle cx="274" cy="95" r="2.6"/>
<circle cx="292" cy="117" r="2.6"/>
<circle cx="310" cy="101" r="2.6"/>
<circle cx="40" cy="185" r="2.6"/>
<circle cx="58" cy="47" r="2.6"/>
<circle cx="94" cy="95" r="2.6"/>
<circle cx="130" cy="75" r="2.6"/>
<text x="92" y="14">小样本：最高和最低都在这头</text>
<text x="270" y="60">大样本：挤在</text>
<text x="270" y="76">真实水平附近</text>
<text x="170" y="206">样本量 →</text>
</g>
</g>
</svg>

**故事。** 1990 年代末，盖茨基金会拿出约 17 亿美元，资助把大学校拆成小学校。理由是一份成绩榜：成绩最好的学校里，小学校特别多。统计学家 Howard Wainer 和 Zwerling 去看了同一份榜的另一头：宾夕法尼亚州成绩最差的 50 所学校里，小学校同样偏多。原因是 de Moivre 1730 年的公式：平均值的波动等于个体的离散程度除以样本量的平方根，学校人少，平均分就上下乱跳，所以最好和最差都是它们。

- **证据 · 强：** 这是数学，不是心理实验：样本越小，平均值离真实水平越远，方向随机。Wainer 的批评是，一笔 10 亿美元以上的投入，建立在不懂这个公式之上。Tversky 和 Kahneman 1971 年把「以为小样本像总体」叫做小数定律。
- **动手：** 下次有人拿一个小样本里的最高或最低值说事（转化率、排行榜、「某城市某病发病率最高」），先问样本有多大；每组不到几百个事件，就把它当噪声，等数据翻到 10 倍再看。
