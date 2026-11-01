---
id: hi-x-hot-key-contention-3-choose
node: sd.cross.hot-key-contention
type: qa
step: 3
---
## Q
**热点键与竞争 (Hot Keys / Sharded Counters)**｜跨题模式 · 怎么选

面对一道新题里的热点，怎么决定用哪种手法？请按判断信号分支，各举一题。

## A
**第一步算数字：** 热点流量除以单键上限（单行约 500 次/秒，单 Redis 节点约 10 万次/秒）。没超过就不要上复杂方案。例：[[tt-live-gift-coin-settlement|直播虚拟礼物]]里 5000 对 500，差 10 倍，所以主播侧不能同步更新。

再按信号分支：
1. **热点在读还是写？** 读：本地缓存、副本、回源合并，不动数据。例：[[tt-cache-consistency-hot-keys|缓存一致性与热点 Key]]。写：继续往下。
2. **这个数字允许近似或延迟几秒吗？** 允许（点赞数、票数、播放数）：窗口内合并批量写，事实另存，每天对账。例：[[like-unlike-system|点赞与取消点赞系统]]、[[food-item-reviews|带打赏的菜品评价系统]]。
3. **基数巨大且只要前几名？** 先局部聚合，再考虑近似草图换内存。例：[[top-k-counts|Top-K 热门榜]]。
4. **是钱，但读它的人可以晚几秒？** 同步路径只写事实（追加分录、事件），余额或收益由异步汇总派生。例：[[tt-wallet-ledger-service|钱包与复式账本服务]]。
5. **必须精确且要唯一顺序（出价、库存）？** 单写者串行加数据库条件更新仲裁，热门时批量提交；库存可拆成仍然精确的子行，但要接受读求和与尾部碎片。例：[[tt-realtime-auction-bidding|实时竞价拍卖]]、[[hotel-booking-system|酒店预订系统]]。
