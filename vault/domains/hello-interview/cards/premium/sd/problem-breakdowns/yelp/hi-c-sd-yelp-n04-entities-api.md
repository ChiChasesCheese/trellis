---
id: hi-c-sd-yelp-n04-entities-api
node: sd.problem-breakdowns.yelp.notes
type: qa
step: 4
---
## Q
**Yelp · 实体与接口**｜摘要 · 必会

点评网站有哪些实体？搜索、查看商户、写评价三个接口怎么定义？为什么要考虑分页？

## A
- **实体：** 商户（Business，名称、位置、类别、平均评分）、用户（User，搜索并写评价）、评价（Review，评分和可选文字）。
- **搜索：** `GET /businesses?query&location&category&page` 返回商户列表。会返回大量结果的接口应加分页，减小载荷、让系统更灵敏。
- **查看：** `GET /businesses/:businessId` 返回商户和评价。更好的是拆开：商户一个接口，评价另一个 `GET /businesses/:id/reviews?page=`，这样评价可以单独分页。
- **写评价：** `POST /businesses/:businessId/reviews`，body 里只有 `rating` 和可选 `text`；用户身份取自令牌，不放在 body 里。
- **做法：** 接口按功能需求一一对应，它是后面高层设计的第一个参照。
