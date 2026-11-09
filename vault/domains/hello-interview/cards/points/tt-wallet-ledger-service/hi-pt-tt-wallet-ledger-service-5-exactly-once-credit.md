---
id: hi-pt-tt-wallet-ledger-service-5-exactly-once-credit
node: tt.sd.tt-wallet-ledger-service.points
type: qa
step: 4
---
## Q
**钱包与复式账本服务 · 充值恰好一次**｜必会 · 出自：钱包与复式账本服务 › 深入 1

商店支付通知会重发、乱序、延迟几天。钱包怎么保证充值只入账一次？

## A
**要点。** 键是 (source, source_txn_id)，TopUp 以它为主键，journal_id 由同一个键确定性生成；两个实例同时处理也只一个插入成功。
**去重表永久保留。** 退款和补发可晚到数周，不能像请求级幂等键 24 小时过期；按每天 500 万笔、留 7 年、每行约 80 B 估算约 1.0 TB，分片后很小。
**否决。** 先查后写、与支付系统两阶段提交、Redis 去重（异步复制丢键会重复入账）。
**兜底。** 每天两侧计数核对。
