---
id: amz-aws-billing-how-asked-and-three-questions
node: amazon.amz-aws-billing
type: qa
step: 1
tags: [grown]
---
## Q
AWS 账单服务（AWS Billing Service）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是单个用户的月账单：每个云服务有用量和费率，算出每个服务该付多少、总共多少。三个问题，每个答案都改变设计：(1) 费率只有一口价，还是有阶梯价和免费额度——后者要把费率做成可互换的对象；(2) 用量是一次给齐，还是持续上报——持续上报会重复投递，要有按记录编号去重的仓库；(3) 月中会不会调价、有没有多币种——会，就要给价格加生效时间，金额按币种分别求和。
