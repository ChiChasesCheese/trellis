---
id: hi-pt-payment-batch-processing-10-security-batch-tradeoff
node: qb.sd.payment-batch-processing.points
type: qa
step: 10
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 安全与攒批的取舍**｜追问 · 出自：支付处理系统（授权冻结加每日批量结算） › 深入 6

支付处理器怎样保护卡号和密钥？为什么扣款不实时发网络而要攒批？

## A
**安全。** 卡号在边缘令牌化，真实卡号只存隔离的 PCI 保险库；API Key 只存哈希，请求用 HMAC 加时间戳和随机数防重放；双向 TLS；密钥放 HSM/KMS 轮换。
**攒批。** 网络对批量结算费率更低、对账更简单、电汇按净额一次完成。
**代价。** 商户资金 T+1 到账，且承担冻结已批准但批量被拒的坏账风险。
