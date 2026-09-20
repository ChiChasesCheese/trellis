---
nodes: [problems.social.tinder]
url: https://medium.com/tinder/taming-elasticache-with-auto-discovery-at-scale-dc5e7c4c9ad0
---
# Taming ElastiCache with Auto-discovery at Scale

值得读：Tinder 工程团队披露了真实的产品规模数字——"每天超过 20 亿次 Swipe 功能调用，
全球累计超过 300 亿次匹配"——本题解的容量估算用这两个数字做数量级交叉验证。文章主体
讲的是 Redis/ElastiCache 缓存旁路（cache-aside）架构和故障转移客户端的运维细节，比多数
题解文章更具体的地方是给出了故障转移期间连接不到新主节点导致的真实生产事故描述，本题解
没有覆盖这部分运维细节，因为它属于基础设施可靠性范畴，不是这道题在候选人生成/匹配判定
上的核心难点。

%% trellis:begin %%
## Source
[Open the original ↗](https://medium.com/tinder/taming-elasticache-with-auto-discovery-at-scale-dc5e7c4c9ad0)
%% trellis:end %%
