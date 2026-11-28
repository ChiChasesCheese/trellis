---
id: mlp-design-sd01-fanout
node: design.sd01
step: 6
type: qa
---
## Q
**深挖：向订阅方扇出推送**｜设计轮

"几百个 pod 都要订阅价格更新，有的订阅几十上百个 symbol，还有几个热门 symbol 几乎人人订阅。怎么推送才不拖垮写入？"

## A
**规模。** 扇出（fan-out，一条更新要送给多个订阅方）的总量是 pod 数乘以平均订阅数，这才是真正的压力所在，而不是摄入吞吐。

**与摄入解耦。** 分发层是独立的日志尾随服务：从存储层的写日志读取变更，再推给订阅方。它和摄入层之间只有"读日志"这一个耦合点，所以慢订阅方或推送故障不会反压写路径；不能让每个订阅直接打摄入路径。

**订阅匹配与顺序。**
- **订阅形式：** `SUBSCRIBE` 支持 symbol 列表或模式；分发层按 symbol 把更新路由到订阅者。
- **推送内容：** 带上 symbol、价格、`valid_time`、`knowledge_time` 和币种，订阅方才能区分原始值和修正值。
- **每个订阅方各记一个位置：** 掉线重连后从自己的位置补发，不丢更新，也不要求摄入层重放。

**热门 symbol。** 按 symbol 哈希分片；热门 symbol 的最新价走内存缓存加多副本读；历史 as-of 和 bar 查询走单独的列存后端，两条路径不共享资源，推送的压力不会拖慢历史查询，反过来也一样。

**修正要不要推送。** 已发布的 bar 是读时聚合，不是可变的存储状态；订阅方想要"用最新已知价格看这段历史"，不带 `as_of` 重新查一次即可，不需要主动去改已经推出去的 bar，否则订阅方分不清自己拿到的是哪个 `knowledge_time` 口径。

**英文答法。**
- "Fan-out is **pods times subscriptions per pod**, so the push path must be decoupled from ingestion."
- "Distribution **tails the log** with a per-subscriber position, so a slow consumer only lags itself."
- "Hot symbols get **in-memory caching and read replicas**, separate from historical queries."
