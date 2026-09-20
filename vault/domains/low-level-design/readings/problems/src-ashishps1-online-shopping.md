---
nodes: [problems.marketplaces.online-shopping]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-shopping-service.md
---
# awesome-low-level-design — Online Shopping Service

值得读：需求清单写得最全（浏览、搜索、购物车、订单跟踪、库存、多种支付方式、并发一致性、
可扩展性），适合拿来核对自己有没有漏项；六种语言并排给同一份设计，`Order`/`OrderItem`/
`ShoppingCart`/`OrderStatus` 的实体切分和本题解一致。
不同之处：它把价格和库存直接放在 `Product` 上（一个 `quantity` 字段加 `updateQuantity`），
没有"预留"这个中间态，于是加购到下单之间的超卖窗口完全没有被处理；`OnlineShoppingService`
是 Singleton；订单状态只是一个枚举字段，没有任何转移约束，也没有跨支付/库存/履约的补偿。
本题解在"关键设计决策"和"常见错误"两节逐条说明了为什么不这样做。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/online-shopping-service.md)
%% trellis:end %%
