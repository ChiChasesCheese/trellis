---
id: cc-transfer-quant-market-making-brainteaser
node: transfer.quant
type: qa
---
## Q
"I flip a fair coin ten times; what would you pay for a contract paying $10 per head?" Give the structure of a strong answer.

## A
**Expected value, then the market you would actually quote, then the risk that moves it.**

- Compute the EV out loud: 10 flips × 0.5 × $10 = **$50**.
- Quote two-sided around it — say **$47 / $53** — and justify the width: your own uncertainty, plus the cost of trading against someone who knows more than you.
- Name **adverse selection**: if the counterparty consistently takes one side, that side is mispriced. You widen or skew the quote rather than repeating it.
- State the assumptions explicitly (fair coin, independent flips, no counterparty information).

The question is testing whether you distinguish a *fair value* from a *price you would trade at*. They are not the same number, and saying only the first is the common miss.

## Q zh
「我抛一枚公平硬币十次；一份每出现一次正面就付 10 美元的合约，你愿意出多少钱？」给出好答案的结构。

## A zh
**先期望值，再你真正会报的双边价，最后是会推动这个价的风险。**

- 把 EV 算出声：10 次 × 0.5 × 10 美元 = **50 美元**。
- 围绕它报双边价 —— 比如 **47 / 53** —— 并解释这个宽度：你自己的不确定性，加上与比你知道更多的人成交的成本。
- 点名**逆向选择**：如果对手方总是打同一边，那一边就定错价了。你应当加宽或偏斜报价，而不是照样再报一次。
- 明确写出假设（硬币公平、各次独立、对手方没有额外信息）。

这道题考的是你是否区分*公允价值*和*你愿意成交的价格*。它们不是同一个数字，而只说出前者正是常见的失分点。
