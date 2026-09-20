---
id: problems-video-streaming-long-tail-lazy-transcode
node: problems.media.video-streaming
type: qa
step: 7
tags: [grown]
---
## Q
In a video streaming platform, why does purely lazy transcoding — generating a rendition only the first time a viewer requests it — risk a bad experience during a sudden spike in a previously-cold video's popularity, and what mitigation avoids that while still controlling storage cost?

## A
Under pure lazy transcoding, if a previously unpopular video suddenly goes viral, a burst of viewers all requesting a not-yet-generated rendition at once can flood the transcode queue and each of them experiences the transcode latency (tens of seconds to minutes) instead of instant playback. The mitigation is tiered transcoding: generate a base set of renditions (e.g. 360p–720p) eagerly at upload time so there is always something playable immediately, and defer only the expensive high-end renditions (e.g. 4K) to be generated asynchronously once view count crosses a threshold, serving a lower-tier rendition in the meantime rather than blocking playback on the transcode.

## Q zh
在视频流媒体平台中，为什么纯惰性转码——只在观众第一次请求某个渲染版本时才生成它——在一个原本冷门的视频突然爆红时会带来体验风险？什么缓解方案能在控制存储成本的同时避免这个问题？

## A zh
在纯惰性转码下，如果一个原本不受欢迎的视频突然爆红，大量观众同时请求一个尚未生成的渲染版本会瞬间打满转码队列，每个人都要经历转码延迟（数十秒到几分钟）而不是立即播放。缓解方案是分层转码：上传时就主动生成一套基础渲染版本（如 360p–720p），保证随时有可播放的内容；只把昂贵的高档位（如 4K）延迟到播放量超过某个阈值后再异步生成，在此期间用低档位渲染版本播放，而不是让播放卡在转码上。
