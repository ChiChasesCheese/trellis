---
id: problems-splitwise-largest-remainder
node: problems.marketplaces.splitwise
type: qa
step: 3
tags: [grown]
---
## Q
分账（Splitwise）里 100 分要三个人均分，33+33+33 只有 99，多出来的那 1 分该归谁？给出一条可复现、可向用户解释的规则。

## A
用最大余数法（largest remainder）：先用 `fractions.Fraction` 算出每人的精确份额（不引入任何浮点误差），向下取整，再把 `总额 - 取整之和` 个最小货币单位按“小数部分从大到小”依次补给参与人；小数部分并列时按参与人列表里出现的先后顺序补。于是 `compute(100, [a, b, c])` 稳定地给出 `{a: 34, b: 33, c: 33}`，可以对着账单解释“你排在参与人第一位，这一分的取整优先补给你”。把余数全塞给第一个人在均分时无伤大雅，但按 33.33/33.33/33.34 这类比例拆分时会明显不公；用 float 算完再 round 则会让余数悄悄消失在误差里。
