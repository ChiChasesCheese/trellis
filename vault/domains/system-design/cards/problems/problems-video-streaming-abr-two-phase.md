---
id: problems-video-streaming-abr-two-phase
node: problems.media.video-streaming
type: qa
step: 8
tags: [grown]
---
## Q
In a video player implementing adaptive bitrate (ABR) streaming, why does a well-designed client use a different selection policy for startup than it uses once playback is stable, rather than running one throughput-plus-buffer algorithm throughout?

## A
At startup there is no playback buffer yet and no history of recent segment download speed, so a buffer-aware algorithm has nothing to react to — the client instead blind-selects a safe mid-or-low rendition to minimize time-to-first-frame. Once playback is underway, a hybrid policy that weighs both recent throughput and current buffer occupancy is used instead: high buffer occupancy tolerates a noisier throughput estimate and can safely step up quality, while low buffer occupancy favors a conservative rendition even if throughput looks adequate, to avoid rebuffering. Using the buffer-aware algorithm at startup would either stall waiting for buffer data that doesn't exist yet, or make a poorly-informed first choice.

## Q zh
在实现自适应码率（ABR）流媒体的播放器中，为什么设计良好的客户端在起播阶段和播放稳定后使用不同的选码策略，而不是从头到尾用同一套吞吐量+缓冲区算法？

## A zh
起播时还没有播放缓冲区、也没有最近分段下载速度的历史数据，所以一个依赖缓冲区状态的算法根本无东西可依据——客户端此时直接盲选一个安全的中低档位以最小化首帧延迟。播放开始后则切换到同时权衡最近吞吐量和当前缓冲区水位的混合策略：缓冲区水位高时即使吞吐量估计有噪声也能安全升档，缓冲区水位低时即使吞吐量看起来足够也优先选保守档位以避免卡顿。如果起播阶段就用依赖缓冲区的算法，要么会卡在等待尚不存在的缓冲区数据，要么会做出信息不足的错误首选。
