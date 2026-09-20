---
nodes: [problems.media.video-conferencing]
url: https://datatracker.ietf.org/doc/html/draft-ietf-rmcat-gcc-02
---
# Google Congestion Control (draft-ietf-rmcat-gcc-02)
值得读：定义了基于丢包和基于延迟梯度的双估计器带宽预测算法——延迟梯度估计器
能在真正丢包之前就检测到网络排队正在累积，从而提前降码率，并采用"快降慢升"的
非对称调整避免振荡。本题解「深入探讨」第 4 节的拥塞检测机制直接来自这份草案；
草案本身不涉及"该先降分辨率还是先关视频"这类产品层降级顺序，这部分是本题解
自己的论证。

%% trellis:begin %%
## Source
[Open the original ↗](https://datatracker.ietf.org/doc/html/draft-ietf-rmcat-gcc-02)

## Archived copy
![[src-gcc-video-conferencing-clip]]
%% trellis:end %%
