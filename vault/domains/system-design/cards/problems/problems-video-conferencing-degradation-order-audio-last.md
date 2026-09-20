---
id: problems-video-conferencing-degradation-order-audio-last
node: problems.media.video-conferencing
type: qa
step: 6
tags: [grown]
---
## Q
When a video conferencing client's available bandwidth degrades under congestion control, why does the design degrade resolution first, then frame rate, then turn video off entirely, and only degrade audio as an absolute last resort?

## A
The order follows information value versus bandwidth cost, which is wildly asymmetric between the two media types: audio typically needs only 24-40 kbps, a rate that survives almost any connection bad enough to still carry a call at all, so protecting it costs almost nothing even under severe constraint, and losing audio ends the conversation outright rather than just degrading it. Video degrades in stages that cost progressively more of the experience: dropping resolution (or switching to a lower simulcast layer) is the cheapest perceptual hit, reducing frame rate (e.g. 30fps to 15fps) costs more but is still tolerable, and disabling video entirely is reserved for when bandwidth can't sustain even a minimal video layer — each step is chosen because it preserves "can the conversation continue at all" for as long as possible before sacrificing it, rather than degrading video and audio quality in lockstep.

## Q zh
当视频会议客户端在拥塞控制下可用带宽下降时，为什么设计上先降分辨率，再降帧率，然后才整体关闭视频，只有在万不得已时才会降级音频？

## A zh
这个顺序遵循的是信息价值和带宽成本的巨大不对称：音频通常只需要 24-40kbps，这个码率在几乎任何还能撑住通话的网络条件下都能保住，所以即便在严重受限下保护音频的代价也几乎为零，而一旦丢失音频，对话直接终止，而不只是体验下降。视频则分阶段降级、代价逐级增加：降低分辨率（或切到更低的 simulcast 层）对观感的损失最小，降低帧率（比如从 30fps 降到 15fps）代价更大但仍可接受，彻底关闭视频只在带宽连最低档视频层都撑不住时才用——每一步的选择都是为了尽可能长时间地保住「对话是否还能继续」这条底线，而不是让视频和音频质量同步下降。
