---
id: hi-c-sd-online-auction-n03-entities-api
node: sd.problem-breakdowns.online-auction.notes
type: qa
step: 3
---
## Q
**在线拍卖 · 实体与接口**｜摘要 · 必会

拍卖有哪些实体？为什么把 Item 从 Auction 里拆出来？接口有哪些？

## A
- **实体：**
  - Auction：起拍价、结束时间、所拍的物品；
  - Item：名称、描述、图片；
  - Bid：出价金额、出价人、所属拍卖；
  - User：卖家或买家。
- **拆出 Item 的理由：** 卖家可以对流拍的物品重新上架（一个 Item 对应多个 Auction）；物品信息能独立于拍卖更新；以后加分类、搜索更容易。把 Item 嵌在 Auction 里也可以，关键是说出理由。
- **接口：**
  - `POST /auctions`（体：物品、开始与结束时间、起拍价）→ Auction 与 Item；
  - `POST /auctions/:auctionId/bids`（体：出价）→ Bid；
  - `GET /auctions/:auctionId` → Auction 与 Item。
- **图片：** 放对象存储，物品表里存链接。面试里说一句并约定不是重点即可。
