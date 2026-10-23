%% trellis:begin %%
# 交易所协议：行情与下单

行情和订单在网线上长什么样：二进制编码、FIX、Nasdaq ITCH / OUCH、MoldUDP64、丢包恢复、SBE，以及 feed handler 的职责。

## Topics
- [[domains/hft/map/protocols.binary-encoding|二进制定长编码、字节序与定点价格]]
- [[domains/hft/map/protocols.fix|FIX 协议：会话层与应用层]]
- [[domains/hft/map/protocols.itch-model|ITCH 行情模型：逐笔订单（order-by-order）]]
- [[domains/hft/map/protocols.itch-messages|ITCH 5.0 关键消息与字段]]
- [[domains/hft/map/protocols.ouch|OUCH 下单协议]]
- [[domains/hft/map/protocols.moldudp64|MoldUDP64：给 UDP 行情加上序列号]]
- [[domains/hft/map/protocols.gap-recovery|丢包恢复：A/B 线仲裁、重传与快照]]
- [[domains/hft/map/protocols.sbe-mdp3|SBE 与 CME MDP 3.0]]
- [[domains/hft/map/protocols.feed-handler|feed handler 的职责]]
%% trellis:end %%

## Notes
