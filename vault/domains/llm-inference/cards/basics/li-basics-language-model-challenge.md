---
id: li-basics-language-model-challenge
node: basics.language-model
type: qa
step: 5
tags: [挑战]
---
## Q
**挑战。** 同事想做"幻觉检测"：读出模型每个输出 token 的概率，平均概率低就判定"模型在胡编"，高就放行。试用时出现两类误判：一句完全正确的话被拦下，一个编出来的论文标题被放行。用"语言模型在预测下一个 token"解释这两类误判。

## A
**评分点（答出 3 条算过）：**

1. 概率衡量的是"这个 token 接在前文后面有多常见"，不是"这句话是不是真的"。
2. 正确却被拦：同一个意思有很多种说法，概率分摊在好几个合理的 token 上，每个都不高；少见的专有名词和数字天然概率低。
3. 编造却放行：编出来的标题通顺、符合常见搭配，每个 token 的概率都高；模型对错的内容也可以很"自信"。
4. 概率还随温度和提示措辞变化，固定阈值不稳。
5. 能用的地方和替代办法：低概率只当"这里值得查"的弱信号；事实要靠检索到的资料来核对。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 324 172" font-family="sans-serif" font-size="12">
<text x="192" y="14" text-anchor="middle" fill="currentColor">内容是否属实 →</text>
<text x="128" y="34" text-anchor="middle" fill="currentColor">真</text>
<text x="256" y="34" text-anchor="middle" fill="currentColor">假</text>
<text x="58" y="77" text-anchor="end" fill="currentColor">概率高</text>
<text x="58" y="139" text-anchor="end" fill="currentColor">概率低</text>
<rect x="64" y="42" width="128" height="62" fill="none" stroke="currentColor"/>
<text x="128" y="77" text-anchor="middle" fill="currentColor">放行 ✓</text>
<rect x="192" y="42" width="128" height="62" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/>
<text x="256" y="69" text-anchor="middle" fill="currentColor">误放</text>
<text x="256" y="87" text-anchor="middle" fill="currentColor">编的标题很通顺</text>
<rect x="64" y="104" width="128" height="62" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/>
<text x="128" y="124" text-anchor="middle" fill="currentColor">误拦</text>
<text x="128" y="141" text-anchor="middle" fill="currentColor">说法多，概率分摊</text>
<text x="128" y="157" text-anchor="middle" fill="currentColor">专有名词、数字</text>
<rect x="192" y="104" width="128" height="62" fill="none" stroke="currentColor"/>
<text x="256" y="139" text-anchor="middle" fill="currentColor">拦下 ✓</text>
</svg>

<details class="pt"><summary>参考答案</summary>语言模型给出的是下一个 token 接在前文后面的概率，它反映的是文字的常见程度，不是事实的真假。一句正确的话如果有多种说法，或者含有少见的名字和数字，概率会被分摊或天然偏低，于是被误拦。编出来的论文标题读起来通顺，每个 token 都是常见搭配，概率很高，于是被放行。所以平均概率只能当作提示哪里值得检查的弱信号，事实核对要靠检索到的资料。</details>
