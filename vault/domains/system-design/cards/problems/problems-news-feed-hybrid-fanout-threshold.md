---
id: problems-news-feed-hybrid-fanout-threshold
node: problems.social.news-feed
type: qa
step: 2
tags: [grown]
---
## Q
In a news feed design with a power-law follower distribution (95% of accounts average 150 followers, 4.9% average 10,000, and the top 0.1% average 5 million), why does excluding only that top 0.1% of accounts from write-time fan-out reduce the average fan-out write QPS by nearly 9x, from about 260,764 to about 29,282?

## A
The weighted-average followers per post is dominated by the tiny top-0.1% segment: including it gives a weighted average of 5,632.5 followers/post (0.95x150 + 0.049x10,000 + 0.001x5,000,000), but excluding it drops the weighted average to about 633 followers/post. Because fan-out write volume scales directly with average followers per post, removing the small fraction of accounts that contributes most of the weighted average collapses the fan-out write rate from ~260,764 QPS to ~29,282 QPS — an 8.9x reduction — even though 99.9% of posts still get pushed normally.

## Q zh
在一个信息流设计中，粉丝数呈幂律分布（95% 的账号平均 150 粉丝，4.9% 平均 1 万粉丝，头部 0.1% 平均 500 万粉丝），为什么仅仅把这最上层 0.1% 的账号从写时 fan-out 中剔除，就能把平均 fan-out 写 QPS 从约 260,764 降到约 29,282，降低近 9 倍？

## A zh
每条帖子的加权平均粉丝数主要由这极小的头部 0.1% 拉高：算上它，加权平均是每帖 5,632.5 个粉丝（0.95×150 + 0.049×10,000 + 0.001×5,000,000）；剔除它之后，加权平均降到约每帖 633 个粉丝。因为 fan-out 写入量直接正比于每帖平均粉丝数，去掉这一小部分贡献了大部分加权平均值的账号，就能把 fan-out 写速率从约 260,764 QPS 压到约 29,282 QPS——降低 8.9 倍——即便 99.9% 的帖子依然正常走推送。
