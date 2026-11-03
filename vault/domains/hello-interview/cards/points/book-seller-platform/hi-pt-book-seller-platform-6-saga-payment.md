---
id: hi-pt-book-seller-platform-6-saga-payment
node: qb.sd.book-seller-platform.points
type: qa
step: 7
---
## Q
**图书比价代购平台 · 支付 Saga**｜追问 · 出自：图书比价代购平台 › 深入 3

图书平台由平台代收款：顾客付款、书商成交、可能失败。支付与购买两步怎样编排，才能让每一步失败时都能回退？

## A
**要点。** 这是 Saga：预授权（authorize，冻结最高价额度）→ 向书商购买 → 按实际成交价扣款（capture），失败则作废预授权（void）。
**顺序原则。** 可补偿的步骤放前面，不可撤销的放后面；书商购买是枢轴（pivot）。
**对照。** 若书商自己收款，平台只传令牌，没有资金风险，只对订单状态负责。
