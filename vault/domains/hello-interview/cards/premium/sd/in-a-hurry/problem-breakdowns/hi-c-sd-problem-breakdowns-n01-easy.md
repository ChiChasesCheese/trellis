---
id: hi-c-sd-problem-breakdowns-n01-easy
node: sd.in-a-hurry.problem-breakdowns.notes
type: qa
step: 1
---
## Q
**常见题目拆解 · 简单题（4 道）**｜摘要 · 必会

简单难度的四道题（Bitly、Dropbox、Yelp、Local Delivery Service）各自主要考什么？

## A
- **Bitly（短链接）：** 考短码怎么唯一生成（自增计数器编码、哈希加冲突处理）、读远多于写所以靠缓存加速、重定向用 301 还是 302（永久重定向会被浏览器缓存，统计点击就丢了）。
- **Dropbox（网盘）：** 考大文件上传下载——元数据放库、文件放对象存储、预签名 URL 直传、分块上传与断点续传、多设备同步。
- **Yelp（点评 / 找附近的店）：** 考"按位置 + 关键词 + 评分"检索，地理空间索引、读多写少、平均评分怎么聚合。
- **Local Delivery Service**（本地配送）：考按位置找就近仓库、聚合多个仓库的库存给出"有没有货"、下单时扣库存不超卖。
- **共同点：** 都是单一主线，适合先练完整走一遍交付框架。
