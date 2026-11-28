---
id: hi-c-sd-in-the-wild-n02-filters
node: sd.in-the-wild.in-the-wild.notes
type: qa
step: 2
---
## Q
**真实系统案例 · 怎么按维度找案例**｜摘要 · 追问

想为某个模式或某种技术找一个真实佐证，这一栏提供哪几个筛选维度？

## A
- **三个维度：** 按模式（如读扩展、竞争处理）、按技术（如 Kafka、Redis）、按来源（哪家公司）筛选。
- **用法一，从模式反查：** 准备"处理竞争"时，筛出 Figma、Discord、Shopify 三篇，各自展示不同的竞争场景（协同编辑、热点分区、库存争抢）。
- **用法二，从技术反查：** 准备 Redis 时，看 Slack 和 Shopify：同一个 Redis，一个因为内存里的队列被打满而在前面加 Kafka，另一个因为一致性不够而换成 MySQL。
- **提醒：** 一篇案例通常同时对应多个模式，真实问题很少只落在一个模式里。
