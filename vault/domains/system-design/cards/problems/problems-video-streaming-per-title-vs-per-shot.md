---
id: problems-video-streaming-per-title-vs-per-shot
node: problems.media.video-streaming
type: qa
step: 5
tags: [grown]
---
## Q
Why does per-title bitrate encoding (choosing a custom resolution/bitrate ladder per video based on its complexity) save less bandwidth than per-shot encoding (choosing quality per shot within the same video), and what does per-shot encoding cost in return?

## A
Per-title encoding treats a whole video's complexity as uniform, so a video with both a quiet dialogue scene and a fast action scene still gets one ladder sized for its average complexity — it cannot give the quiet scene less bitrate and the action scene more. Per-shot encoding splits the video into shots and optimizes bits per shot under a total bitrate budget (e.g. via Lagrangian optimization), letting simple shots drop further and complex shots reclaim the saved bits, which is why it captures additional savings (an extra ~17.1% on top of per-title in Netflix's reported numbers) beyond per-title alone. The cost is an extra round of exploratory encoding at finer granularity, which only pays off for content with enough repeat views to amortize that one-time encoding cost.

## Q zh
为什么按标题定制码率（per-title encoding，按整个视频的复杂度选一套自定义分辨率/码率阶梯）比按镜头定制（per-shot encoding，在同一视频内部按镜头选质量）省下更少的带宽？按镜头定制的代价是什么？

## A zh
按标题定制把整部视频的复杂度当作均匀的，所以一部既有安静对话场景又有快速动作场景的视频，仍然只用一套按其平均复杂度定的阶梯——无法给安静场景更少码率、给动作场景更多码率。按镜头定制把视频切成镜头，在总码率预算下按镜头优化码率分配（例如用拉格朗日优化），让简单镜头进一步降码率、复杂镜头把省下来的码率要回来，这就是为什么它能在按标题定制之外再省下额外的带宽（Netflix 披露的数字是额外约 17.1%）。代价是要多跑一轮更细粒度的探测编码，只有播放次数足够多、能摊薄这次一次性编码成本的内容才划算。
