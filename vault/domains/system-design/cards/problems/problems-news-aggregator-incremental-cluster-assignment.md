---
id: problems-news-aggregator-incremental-cluster-assignment
node: problems.search.news-aggregator
type: qa
step: 5
tags: [grown]
---
## Q
In a news aggregator's story-clustering design, why is batch reclustering (periodically re-running full clustering over all active articles) worse than incremental cluster assignment for a breaking news story specifically, and what consistency trade-off does incremental assignment accept in exchange?

## A
Batch reclustering means any two publishers covering the same breaking story within the same batch window before the next reclustering run stay as separate stories in the feed for up to that entire window — exactly during the highest-traffic moment of a breaking story. Incremental assignment instead probes the near-duplicate index for each new article's fingerprint as it arrives and immediately upserts it into a matching existing cluster (or creates a new one if no match is found), so a story starts corroborating within one lookup rather than waiting for the next batch cycle. In exchange, this design accepts that an article can briefly sit in the 'wrong' (not-yet-merged) cluster if two independently-created early clusters turn out later to be the same event — a bounded, cheaply-fixed inconsistency handled by a periodic background job that retroactively merges such clusters, rather than delaying all display until a full reclustering pass confirms correctness.

## Q zh
在一个新闻聚合器的故事聚类设计中，为什么批量重新聚类（定期对全部活跃文章重新跑一次聚类）对突发新闻这个具体场景特别不利？增量聚类分配换来这个好处的代价是什么一致性妥协？

## A zh
批量重新聚类意味着，如果多家发布方在同一个批次窗口内报道同一条突发新闻，在下一次重新聚类运行之前它们会作为多个独立故事留在信息流里长达一整个窗口——而这恰好是突发新闻流量最大的时刻。增量分配则在每篇新文章的指纹到达时立即探测近似重复索引，命中就直接并入已有故事，没命中就新建一个，所以一个故事只需一次查找就能开始积累佐证，不用等下一个批次周期。作为交换，这个设计接受了一种情况：如果两个各自独立创建的早期故事后来发现其实是同一事件，一篇文章可能短暂待在「错误的（尚未合并的）」故事里——这是一个有界、修复成本低的不一致，由一个定期后台任务回溯性合并这类故事来解决，而不是让所有展示都等到一次完整的重新聚类确认正确性之后。
