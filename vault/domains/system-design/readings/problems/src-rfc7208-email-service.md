---
nodes: [problems.media.email-service]
url: https://www.rfc-editor.org/rfc/rfc7208
---
# RFC 7208 — Sender Policy Framework (SPF)
值得读：明确 SPF 检查的是信封发件人（`MAIL FROM`/`HELO` 域名的 DNS TXT 授权 IP
列表），而不是用户在客户端看到的 `From:` 头，并且不能穿越转发。本题解「深入探讨」
第 2 节把这一点作为和 DKIM、DMARC 区分开的第一个论据——单独 SPF 通过不代表用户
看到的发件人可信。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc7208)

## Archived copy
![[src-rfc7208-email-service-clip]]
%% trellis:end %%
