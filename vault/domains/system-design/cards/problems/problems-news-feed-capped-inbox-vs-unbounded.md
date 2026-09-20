---
id: problems-news-feed-capped-inbox-vs-unbounded
node: problems.social.news-feed
type: qa
step: 5
tags: [grown]
---
## Q
In a news feed design, why does capping each user's precomputed inbox (home timeline cache) at a fixed size like 800 entries matter more as the system runs over time than it does on day one?

## A
An uncapped inbox grows without bound as a function of both how many accounts a user follows and how long the system has been running: a user following 5,000 accounts that each post about once a day accumulates roughly 5,000 new entries per day, or about 1.8 million entries after a year, for a single user. A fixed 800-entry cap keeps each user's inbox memory footprint constant regardless of elapsed time or follow count, with older entries archived to cold storage that the normal read path never touches — trading unlimited scroll-back depth (which users rarely use) for bounded, predictable memory cost.

## Q zh
在一个信息流设计中，为什么把每个用户预计算收件箱（home timeline 缓存）的容量固定在类似 800 条这样的上限，会随着系统运行时间增长而变得越来越重要，而不只是上线第一天的细节？

## A zh
不设上限的收件箱会随着'用户关注了多少账号'和'系统已经运行了多久'这两个维度同时无界增长：一个关注了 5,000 个账号、且这些账号平均每天各发一条帖子的用户，每天大约新增 5,000 条记录，一年后单个用户的收件箱就会累积约 180 万条。固定 800 条的上限能让每个用户的收件箱内存占用不随时间或关注数增长而变化，更早的条目归档到冷存储、正常读路径不会访问——用几乎没人会翻到的无限回溯深度，换取有界且可预测的内存开销。
