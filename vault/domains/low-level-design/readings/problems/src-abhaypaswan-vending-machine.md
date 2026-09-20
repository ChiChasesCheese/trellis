---
nodes: [problems.machines.vending-machine]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/vending-machine
---
# abhaypaswan/lld-python — Vending Machine

值得读：Python 实现，自带 pytest，而且把这道题真正的分水岭说得很清楚——顺路径人人会写，
差距在机器"必须拒绝"的时刻，以及拒绝之后买家的钱在哪。它和本题解共享两个关键决定：金额
一律用整数分，投入的硬币在成交前**托管**（escrow）所以退币退回的就是原来那几枚；它还给每个
状态配了一句"机器在等什么"的提示语。分歧有两处：它走一状态一类的 State 形态，本题解走
`Enum` 加转移表（理由是四状态五动作下转移表能被穷举测试盖满）；它的找零停在贪心，本题解
默认用有界背包 DP，并给出了贪心明明有解却报"找不开"的实例。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/vending-machine)

## Archived copy
![[src-abhaypaswan-vending-machine-clip]]
%% trellis:end %%
