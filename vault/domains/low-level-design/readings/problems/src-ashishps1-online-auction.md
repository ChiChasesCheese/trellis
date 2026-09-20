---
nodes: [problems.marketplaces.online-auction]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-auction-system.md
---
# awesome-low-level-design — Designing an Online Auction System

值得读：这是这道题最流行的免费题面，八条需求（注册登录、上架、浏览与搜索、出价、自动更新
最高价并通知、到点公布赢家、并发与数据一致性、可扩展）适合拿来核对自己分关有没有漏项，
五种语言并排给出同一份实体切法（`User` / `AuctionListing` / `Bid` / `AuctionSystem`）。
它的 Python 实现更值得当对照组读，本题解在三处正面给出了不同答案：它的出价就是"一口价"
（`place_bid` 收一个金额直接与当前最高价比大小），本题解按 eBay 的真实做法实现了代理出价
（proxy bidding）——出价者交一个愿意付的最高额，系统替他出"刚好压过对手所需的最小金额"，
这才是整道题真正的难点所在；它的 `AuctionSystem` 用双重检查锁定实现单例（Singleton），
并且给每场拍卖用 `ThreadPoolExecutor.submit` 调度一个 `time.sleep(delay)` 的任务来结束
拍卖——上架量一大待命任务就撑不住，反狙击一延时那个任务的睡眠时间就已经错了，得取消重排，
本题解改成"任何一次读写都先把状态推进到当前时刻应有的样子"，结束不依赖任何定时器存活；
它的通知机制（`auction_observer.py`）是一个抽象基类加 `on_bid_update` 方法，本题解把观察者
换成一个普通的 `Callable[[AuctionEvent], None]`，事件自带现价、领先者与结束时间，订阅者
不必回头去问 `Auction` 要数据。
