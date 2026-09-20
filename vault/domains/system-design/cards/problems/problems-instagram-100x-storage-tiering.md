---
id: problems-instagram-100x-storage-tiering
node: problems.social.instagram
type: qa
step: 8
tags: [grown]
---
## Q
In a photo/video sharing system scaling to roughly 100x its original daily active users, why does the storage cost problem shift from 'can we store this much data' to 'is it worth keeping this data on fast storage', and what design change does that motivate?

## A
At the original scale, total media storage per year is a manageable, bounded number even though it is large; at 100x scale, the accumulated historical media (most of which is rarely accessed after the first few days or weeks) makes keeping everything on the same standard object storage tier increasingly wasteful relative to its actual access frequency. This motivates hot/warm/cold storage tiering: recently uploaded or frequently accessed media stays on the standard tier for low-latency reads, while old, rarely-accessed media is automatically migrated to a cheaper archival tier that accepts higher read latency, using existing access-frequency statistics to drive the migration decision rather than a new dedicated mechanism.

## Q zh
在一个图片/视频分享系统扩展到约 100 倍原始日活规模的场景下，为什么存储成本问题会从'能不能存得下这么多数据'变成'这些数据是否值得一直放在快速存储上'？这会推动什么样的设计变化？

## A zh
在原始规模下，每年的媒体总存储量虽然很大，但仍是一个可控、有界的数字；扩展到 100 倍规模后，积累下来的历史媒体（其中大部分在发布后的头几天或几周就很少再被访问）如果继续全部放在同一个标准对象存储层上，相对于它们实际的访问频率会变得越来越浪费。这会推动引入热/温/冷分层存储（tiering）：近期上传或高频访问的媒体留在标准层以保证低延迟读取，长期低频访问的旧媒体自动迁移到更便宜、接受更高读取延迟的归档层，迁移决策可以直接复用已有的访问频率统计，不需要单独设计一套新的判定机制。
