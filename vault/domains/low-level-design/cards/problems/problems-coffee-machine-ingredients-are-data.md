---
id: problems-coffee-machine-ingredients-are-data
node: problems.machines.coffee-machine
type: qa
step: 11
tags: [grown]
---
## Q
咖啡机的原料（浓缩、牛奶、糖浆、抹茶粉）应该做成 `Enum` 还是字符串键？和售货机里的硬币面额有什么不同？

## A
用字符串键，库存是 `dict[str, int]`，配方是 `Mapping[str, int]`。判据是**这个集合会不会被业务方在运行时扩展**：糖浆和燕麦奶是运维在后台配的，写成枚举意味着上一款新糖浆就要改代码、改类型标注、重新发一次版。硬币和钞票面额恰好相反——它是国家定死的封闭有限集合，枚举成员就是面值还能直接参与算术，那里用 `IntEnum` 才对。代价是丢掉拼写检查（`milk` 写成 `mlik` 没人发现），所以必须配一条补偿：机器不认识的原料要算成『缺口等于全部用量』的缺料错误，而不是抛 `KeyError`，报错里那句『matcha 差 8』能让运维一眼分辨是拼错了还是没进货。
