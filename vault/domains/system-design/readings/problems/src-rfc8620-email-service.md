---
nodes: [problems.media.email-service]
url: https://www.rfc-editor.org/rfc/rfc8620
---
# RFC 8620 — The JSON Meta Application Protocol (JMAP)
值得读：为移动/间歇连接场景设计的现代邮箱同步协议——用服务端状态号做增量同步，
取代 IMAP 反复拉取整个文件夹的模式，并内建基于状态变化的推送。本题解「深入探讨」
第 7 节用它作为"移动 push 唤醒后按增量而不是全量拉取"这一设计选择的依据，和
IMAP `IDLE` 的常连接推送互为对照的两条通道。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc8620)

## Archived copy
![[src-rfc8620-email-service-clip]]
%% trellis:end %%
