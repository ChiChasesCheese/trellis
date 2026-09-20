---
id: problems-pastebin-burn-after-reading-atomicity
node: problems.foundations.pastebin
type: qa
step: 8
tags: [grown]
---
## Q
In a pastebin design supporting burn-after-reading pastes, why must the 'read and destroy' operation be a single atomic conditional update at the paste's authoritative storage location, and why must burn-after-reading responses also bypass CDN caching?

## A
If reading and deleting were two separate steps, two concurrent requests arriving close together could both read the content before either deletion takes effect, breaking the 'readable exactly once' guarantee — the same check-then-act race that affects any concurrent unique-claim operation. The fix is a single atomic conditional update (e.g. flip a consumed flag from false to true) at storage; only the request that actually flips it is allowed to return the content, and it must happen at the paste's linearizable authoritative copy, not at a regional replica or cache, or different regions could each believe they served the 'first' read. Separately, if the first successful read's response were cached at a CDN edge, every subsequent request — which should be rejected — would instead be served the cached content straight from the edge, completely bypassing the origin's conditional-update logic; so burn-after-reading responses must be marked non-cacheable and always go to origin.

## Q zh
在一个支持阅后即焚（burn-after-reading）粘贴的 pastebin 设计中，为什么「读取并销毁」必须是在该粘贴权威存储位置上的一次原子条件操作，为什么阅后即焚的响应还必须绕开 CDN 缓存？

## A zh
如果读取和删除是两个独立的步骤，两个几乎同时到达的并发请求可能都会在删除生效前读到内容，从而打破「只能被读取恰好一次」的承诺——这和任何并发唯一性申领操作面临的先检查后动作（check-then-act）竞态是同一类问题。解法是在存储层做一次原子条件更新（例如把一个 consumed 标志从 false 翻转为 true）；只有真正完成这次翻转的那个请求才被允许返回内容，且这个操作必须发生在该粘贴线性一致的权威副本上，而不是某个区域副本或缓存上，否则不同区域可能各自认为自己提供了「第一次」读取。另外，如果第一次成功读取的响应被 CDN 边缘节点缓存下来，后续所有本应被拒绝的请求就会直接从边缘拿到缓存内容，完全绕开源站的条件更新逻辑；因此阅后即焚的响应必须标记为不可缓存，强制每次都回源。
