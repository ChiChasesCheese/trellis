---
id: hi-c-sd-camelcamelcamel-n03-entities-api
node: sd.problem-breakdowns.camelcamelcamel.notes
type: qa
step: 3
---
## Q
**价格追踪服务 · 实体、接口与数据流**｜摘要 · 必会

价格追踪服务要哪些核心实体和接口？为什么说"数据从哪来"是一个藏在需求背后的隐含需求？

## A
- **实体：**
  - Product：被追踪的商品，含当前价格和展示、通知需要的元数据；
  - User：联系方式与通知偏好；
  - Subscription：把用户与商品连起来，带触发通知的价格阈值；
  - Price：每个商品随时间变化的价格，是时序数据，用来画图。
- **接口：**
  - `GET /products/{product_id}/price?period=30d&granularity=daily` 返回价格点数组。`product_id` 放路径而非请求体，利于缓存且符合 REST；`granularity` 让长周期返回日均、近期返回小时级，防止一次返回几千个点；
  - `POST /subscriptions`，体里有商品、阈值、通知方式。
- **数据流：** 采集（爬虫和扩展）→ 校验后写价格库 → 价格变化触发事件 → 价格低于阈值就给用户发邮件。
- **隐含需求：** 题面只讲"看历史、订阅"，却没有说数据怎么得到。亚马逊不给接口，所以采集本身就是要设计的系统；先画数据流能让你和面试官对齐这一点，并提前暴露瓶颈。
- **面试做法：** 实体先报一个简短清单，高层设计时再补字段，并把计划告诉面试官。
