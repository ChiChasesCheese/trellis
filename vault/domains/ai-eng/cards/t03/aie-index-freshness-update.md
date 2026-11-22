---
id: aie-index-freshness-update
node: t03.index-incremental-update-data-freshness
type: qa
step: 1
tags: [实践]
---
## Q
**Index freshness · 增量更新与发现不一致**｜实践 · 追问

产品文档每天都在改，你的向量索引每个月全量重建一次。用户开始抱怨「答案是旧的」，还引用了已删除的页面。怎么设计更新，怎么发现索引和源数据不一致？

## A
**增量更新的方式：**

| 源 | 变更捕获 |
|---|---|
| 数据库 | **CDC**（change data capture：监听行的增删改，只对变动的行重新 embedding） |
| 文件 | 每个 chunk 存**内容哈希**，哈希变了才重新 embedding |
| SaaS 文档 | webhook 或最后修改时间 |

**三个必须做的事：**
1. **删除要同步：** 源文档删了，对应的向量也要删（不删就是「孤儿向量」，会继续被检索到）；可以先标记删除再清理。
2. **记录嵌入版本：** 每个向量存下 embedding 模型版本、chunking 参数、源内容哈希、时间。换模型或改 chunking 后只重算一部分，会得到**混合版本**的索引，向量彼此不可比；发现多个版本并存就应全量重建。
3. **定期全量重建作为对账点**（常见节奏：每天增量、每周或每月全量），顺便清理漂移。

**怎么发现不一致：**
- 金丝雀测试：改动源里一个已知事实，确认检索返回新版本；评测集里同时放旧版和新版的问题；
- 按文档类别记录最后验证时间，超出保鲜期的向量报警；
- 抽样把索引里的 chunk 和源文档逐一对比；
- 从用户的负面反馈（点踩、重问）反推。

**出处：** tianpan.co《The RAG Freshness Problem》（2026-04，2026-11-21 读）；Oracle 开发者博客《Real-Time RAG: Live SQL, Incremental Indexing, and Freshness Tests》的新鲜度测试思路
