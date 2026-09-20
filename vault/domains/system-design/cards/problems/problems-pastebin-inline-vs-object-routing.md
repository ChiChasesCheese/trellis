---
id: problems-pastebin-inline-vs-object-routing
node: problems.foundations.pastebin
type: qa
step: 3
tags: [grown]
---
## Q
In a pastebin design, why route pastes smaller than a threshold (e.g. 4KB) to be stored inline inside the metadata row, instead of sending every paste's content to object storage regardless of size?

## A
Because the large majority of pastes are tiny (in one such design, 85% average around 1.5KB), and object storage's first-byte latency is typically an order of magnitude higher than a row-store lookup (tens of milliseconds vs single-digit milliseconds). Forcing every read/write of a small paste through object storage would add an unnecessary network hop to the common case. Inlining content directly in the metadata row for pastes under the threshold keeps the dominant, high-frequency small-paste path fast, while larger pastes — which are rarer but dominate total bytes — still get routed to object storage, the technology class actually built for large blob throughput and cheap per-GB storage.

## Q zh
在一个 pastebin 设计中，为什么要把小于某个阈值（例如 4KB）的粘贴内容内联存进元数据行，而不是不论大小一律把内容发到对象存储？

## A zh
因为绝大多数粘贴都很小（在某个此类设计里，85% 的粘贴平均约 1.5KB），而对象存储的首字节延迟通常比行存储查找高一个数量级（几十毫秒 vs 个位数毫秒）。如果不论大小都强制经过对象存储，会给最常见、高频的小粘贴场景多加一次不必要的网络往返。把阈值以下的粘贴内容直接内联存进元数据行，能让占主导地位的小粘贴路径保持快速；更大的粘贴——虽然更少见，但主导了总字节量——仍然路由到对象存储，这才是真正为大 blob 吞吐量和低廉的按 GB 存储成本而设计的存储技术类别。
