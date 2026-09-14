---
id: serverless-separate-line-item
node: cost.serverless-feature-billing
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 账单上，无服务器（serverless）功能的费用出现在哪里？它会计入某个仓库的消耗，或者参与云服务 10% 免费额度的计算吗？

## A
每个无服务器功能在账单上单独列为一个计费项，该功能消耗的 Snowflake 管理计算与云服务费用合并为同一个计费项，不计入任何虚拟仓库。无服务器计算也不参与云服务的 10% 调整：云服务的每日免费额度只按当天虚拟仓库用量的 10% 计算，无服务器用量不会抬高这个额度。
