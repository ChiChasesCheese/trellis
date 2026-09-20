---
nodes: [problems.media.video-conferencing]
url: https://www.rfc-editor.org/rfc/rfc9605
---
# RFC 9605 — SFrame
值得读：定义了帧级端到端加密如何与 SFU 的逐跳转发共存——帧头（Key ID、
Counter）不加密,使 SFU 可以在不解密媒体内容的前提下仍然做 simulcast 层选择等
转发决策。本题解「深入探讨」第 6 节的端到端加密方案，以及第 7 节"录制机器人
必须以参会者身份参与密钥协商"的推论，都建立在这份规范描述的双层加密结构上。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9605)

## Archived copy
![[src-rfc9605-video-conferencing-clip]]
%% trellis:end %%
