---
id: cleanroom-min-aggregation-threshold
node: sharing.clean-rooms-privacy
type: qa
tags: [grown]
---
## Q
洁净室（Data Clean Room）已经只允许返回聚合结果，为什么还需要最小聚合阈值（minimum aggregation threshold，例如每组至少 N 个个体）这类约束？

## A
因为聚合本身也能泄露个体：如果把分组条件收得足够窄（如按“邮编 + 出生日 + 性别”分组），某个组可能只有 1 个人，计数或求和就等于暴露了这个人的行为；多次查询做差分也能还原个体。最小组大小阈值会拒绝或抑制过小的分组，差分隐私（differential privacy）则在结果中加入受控噪声，二者都是在可用性与重识别风险之间的权衡。
