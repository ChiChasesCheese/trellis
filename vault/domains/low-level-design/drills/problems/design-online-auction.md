---
nodes: [problems.marketplaces.online-auction, concurrency.primitives]
tags: [problem]
---
# Drill：在线拍卖（Online Auction）

一场拍卖：一个卖家、一件拍品、一个底价、一段时间，和一台代理出价（proxy bidding）机——像
eBay 那样，出价者交一个愿意付的**上限**，系统替他出刚好压过对手所需的最小金额。时间只从
注入的时钟来，金额一律整数分。支付、登录、商品搜索都不在这道题里。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一场拍卖有卖家、拍品、起拍价、底价、开始与结束时间。买家出价要过
  校验：拍卖必须已开始、未结束，卖家不能给自己出价，出价上限必须达到"现价加一个加价档"。
  先决定钱用什么类型（别用 `float`），以及起拍价和底价是不是同一个字段。
- 第 2 关（约 15 分钟）：**代理出价**（proxy bidding）。出价者交上限，系统替他出刚好够的
  那个数；并列要确定性地裁决；领先者自己提高上限时价格该不该动，是这一关最容易翻车的地方。
- 第 3 关（约 15 分钟）：收尾时刻的一切——并发出价、反狙击（anti-sniping）延时、**恰好
  结算一次**。回答"进程半夜重启、没人访问这场拍卖，它算不算结束了"，以及锁应该挂在每场
  拍卖上还是挂在整个拍卖行上。还要说清两个容器怎么缩小：关注者表和拍品目录。
- 第 4 关（选做）：一口价（buy it now），评分点是"加它有没有动到出价那段代码的任何一行"。

**怎么练**：把 `vault/domains/low-level-design/problems/online-auction/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/online-auction -q`。

**评分点**
- 代理出价（proxy bidding）算的是 `min(挑战者上限, 在位上限+一档)` 与 `min(在位上限, 挑战者上限+一档)`，最后一律 `max(当前价, 新价)` 保证价格只涨不跌（[[problems-online-auction-proxy-bidding-three-rules]]）。
- 领先者自己提高上限时价格**不动**，不走"新挑战者"那条分支——没有人应该和自己竞价（[[problems-online-auction-leader-raises-own-max]]）。
- 上限并列时**先提交的赢**，后到者一秒钟都没有真正领先过（[[problems-online-auction-tie-goes-to-earliest]]）。
- "恰好结算一次"靠**惰性推进**（任何读写先把状态推进到当前时刻），不靠每场一个 `sleep` 定时器，也不单靠周期扫描线程（[[problems-online-auction-exactly-once-lazy-tick]]）。
- 锁的粒度是**一场拍卖一把**，因为两场拍卖之间没有共享状态；GIL 在"读上限、算新价、写领先者"这种复合操作上帮不上忙（[[problems-online-auction-lock-per-auction]]、[[concurrency-lock-rlock]]）。
- 通知用一个普通的 `Callable`，不需要观察者的抽象基类；事件自带现价与领先者，退订函数和订阅一起交出去（[[problems-online-auction-callable-watcher-not-abc]]）。
- 起拍价（公开、只管首次出价门槛）和底价（不公开、只在结算时决定卖不卖）必须是两个字段（[[problems-online-auction-reserve-vs-starting-price]]）。
- 关注者表在拍卖结束时清空、拍品目录靠 `purge_closed_before` 收缩——两个容器都要有出口（[[problems-online-auction-shrinking-containers]]）。

**题解**：[[solution-online-auction]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
