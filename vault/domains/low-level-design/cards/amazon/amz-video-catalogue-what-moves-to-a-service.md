---
id: amz-video-catalogue-what-moves-to-a-service
node: amazon.amz-video-catalogue
type: qa
step: 6
tags: [grown]
---
## Q
在视频目录设计里，用户量变成千万级后，目录和续播点分别应该怎么拆？

## A
两者读写特征相反，拆成两个服务。目录读多写少：前面放缓存（CDN），类型倒排索引搬到搜索服务或带二级索引的表。续播点写多读少：放键值存储，按档案 id 分区，主键 `(档案, 视频)`，写入靠客户端 30 秒心跳合并成低频写。目录可以接受分钟级过期，续播点要求自己的写马上读到。
