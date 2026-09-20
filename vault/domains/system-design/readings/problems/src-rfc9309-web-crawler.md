---
nodes: [problems.search.web-crawler]
url: https://www.rfc-editor.org/rfc/rfc9309
tags: [spec]
---
# RFC 9309 — Robots Exclusion Protocol

值得读：2022 年把 robots.txt 正式标准化的 IETF 文档，标准化了 `Disallow`/`Allow` 指令，但
明确没有把 `Crawl-delay` 纳入标准范围，理由是它在真实世界里缺乏一致的行为约定。本题解「深
入探讨」第 3 节的节流设计——不把 `Crawl-delay` 当作唯一节流依据，改用基于观测延迟/错误率的
自适应节流——直接依据这份文档"有意不标准化一个没有共识行为"的立场。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9309)

## Archived copy
![[src-rfc9309-web-crawler-clip]]
%% trellis:end %%
