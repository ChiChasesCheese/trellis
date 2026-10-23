---
id: hl-bv-stories-a
node: behavioral.value-matrix
type: qa
step: 4
---
## Q
Headlands 背景题的 15 个故事里，雇主工作的 S1–S6 各是什么故事？

## A
- **S1** Amex 结算管线（settlement pipeline）：出错就记日志、绝不丢弃。
- **S2** 质量检查框架 + ADR：表级门会让少数商户拦住成千上万商户，被批评后重新审视。
- **S3** ACH 手续费 NULL 事故的根因分析（RCA）：没有报错的 bug。
- **S4** 澳洲 Amex 退款手续费：用数据结束一场跨团队争论。
- **S5** 手续费数据源切换（interchange source cutover）：用生产查询验证。
- **S6** 异常检测器 go/no-go：上线前用规模估算叫停逐行方案。
