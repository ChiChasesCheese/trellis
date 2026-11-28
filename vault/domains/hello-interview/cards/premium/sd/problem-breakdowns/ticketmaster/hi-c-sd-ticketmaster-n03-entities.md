---
id: hi-c-sd-ticketmaster-n03-entities
node: sd.problem-breakdowns.ticketmaster.notes
type: qa
step: 3
---
## Q
**票务系统 · 核心实体**｜摘要 · 必会

Ticketmaster 有哪些核心实体？为什么 Ticket 要为每个座位生成一张，Booking 为什么要单独成实体？

## A
- **Event：** 活动的日期、描述、类型，是中心信息。
- **User：** 系统用户。
- **Performer：** 表演者（艺人、球队、团体），名字故意取得宽泛，覆盖各种类型。
- **Venue：** 场馆，含地址、容量和座位图（各区、排、座位及渲染用坐标，如 JSON）。
- **Ticket：** 对应活动的某个座位的票，含区、排、座号、价格、状态。创建活动时，按场馆座位图为每个座位生成一张。客户端用座位图加每张票的状态渲染选座界面。
- **Booking：** 一次购买记录：用户、票 ID 列表、总价、状态（进行中或已确认）。可以并入 Ticket，但单独成实体能把一次买多张的票归为同一单，共享支付状态和总价。
