---
id: problems-video-streaming-ladder-storage-amplification
node: problems.media.video-streaming
type: qa
step: 1
tags: [grown]
---
## Q
In a video streaming platform that generates a 6-rung bitrate ladder (240p–4K) in two codec families (H.264 + AV1/VP9) for every uploaded video, why does the resulting ~6.1x storage multiplier over the master file force a design decision about which videos get the full ladder?

## A
Summing the ladder's per-rendition bitrates across two codec families comes to roughly 6.1x the master's own bitrate, so if every uploaded video is eagerly transcoded into the full ladder, transcoded storage alone dwarfs master storage at platform scale. Because video popularity is heavy-tailed, most uploads get few or no views, so generating expensive high-resolution renditions for all of them wastes most of that storage; the fix is to generate only base renditions (e.g. 360p–720p) at upload time and defer costly renditions like 4K until a video's view count crosses a threshold that justifies the extra storage.

## Q zh
在一个视频流媒体平台中，每个上传的视频都会生成一套 6 档的码率阶梯（240p–4K），再乘以两套编码格式（H.264 + AV1/VP9），为什么由此产生的约 6.1 倍存储放大倍数会迫使团队做出一个关于哪些视频该拿到全套阶梯的设计决策？

## A zh
把阶梯里各档码率在两套编码格式下加总，大约是母版自身码率的 6.1 倍，所以如果对每个上传的视频都无差别生成全套阶梯，转码产物存储在平台规模下会远远超过母版存储。由于视频播放量分布是重尾的，大多数上传视频播放量很少甚至为零，为它们全部生成昂贵的高分辨率版本会浪费大部分存储；解决办法是上传时只生成基础档位（如 360p–720p），把 4K 这类高成本档位延迟到该视频的播放量超过某个阈值、值得为它多花这部分存储时才生成。
