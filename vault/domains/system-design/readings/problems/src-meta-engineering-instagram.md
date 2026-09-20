---
nodes: [problems.social.instagram]
url: https://engineering.fb.com/2022/11/04/video-engineering/instagram-video-processing-encoding-reduction/
---
# Reducing Instagram's basic video compute time by 94 percent

值得读：Meta 官方工程博客披露的真实优化——把一段 23 秒视频独立转码到 720p 自适应码率
（ABR）版本需要约 86.17 秒 CPU 时间，改为复用已有的渐进式（progressive）编码帧数据、
重新打包成 ABR 文件结构，只需要约 0.36 秒，约 239 倍的速度差，整体基础 ABR 编码的计算
成本下降 94%。本题解「深入探讨」的视频转码一节直接引用这组真实数字作为"减少重复编码
比堆算力更重要"这一结论的依据，并补充了这一节原文没有展开的对比：如果每一档码率都独立
转码，会在容量估算里"视频只占 20% 上传量却贡献约 73% 存储"这个结论之外，成为一个隐藏
更大的计算成本大头。

%% trellis:begin %%
## Source
[Open the original ↗](https://engineering.fb.com/2022/11/04/video-engineering/instagram-video-processing-encoding-reduction/)

## Archived copy
![[src-meta-engineering-instagram-clip]]
%% trellis:end %%
