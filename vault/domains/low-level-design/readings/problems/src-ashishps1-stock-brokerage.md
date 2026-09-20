---
nodes: [problems.marketplaces.stock-brokerage]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-stock-brokerage-system.md
tags: [no-archive]
---
# awesome-low-level-design — Designing an Online Stock Brokerage System

值得读：这是这道题最流行的免费题面，八条需求（开户、买卖、组合与流水、实时行情、下单与
结算、余额与持仓校验、并发一致性、可扩展）适合拿来核对自己分关有没有漏项；六种语言并排给出
同一份实体切法（`User` / `Account` / `Stock` / `Order` / `Portfolio` / `StockBroker`）。
它的 Python 实现更值得当**对照组**读，本题解在五处正面给出了不同答案：`StockExchange` 用
`__new__` 做单例，使得测试拿不到干净实例；`_find_best_buy` 用 `max()` 线性扫描全部挂单，
既是 O(n) 也彻底丢掉了同价的时间优先；`_update_order_status` 的注释自己承认"简化了，没做
部分成交"，于是 `PARTIALLY_FILLED` 成了摆设；成交价一律取卖单价，买单先挂时这是错的；
扣款发生在撮合之后，一旦钱不够就必须回滚已经改过的簿子。它的 `ExecutionStrategy` 与
`OrderState` 两族抽象基类在 Python 里可以（也应该）被一个枚举加一行 `if` 取代。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-stock-brokerage-system.md)
%% trellis:end %%
