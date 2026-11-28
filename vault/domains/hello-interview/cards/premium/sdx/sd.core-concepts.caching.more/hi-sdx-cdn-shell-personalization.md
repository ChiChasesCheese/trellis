---
id: hi-sdx-cdn-shell-personalization
node: sd.core-concepts.caching.more
type: qa
step: 5
---
## Q
**页面九成共享一成个性化**｜补充 · 缓存 · 追问

一个页面 90% 的内容对所有人相同（商品图文），10% 是个性化的（昵称、购物车数量、推荐位）。流量翻倍，哪部分由 CDN 吸收？有人提议把 Cookie 放进 CDN 缓存键，整页都缓存，行吗？

## A
**结论。** 不行。共享的外壳放 CDN，个性化部分走单独的带鉴权的小接口，这个接口才是流量翻倍后要扩容的地方。

**要点。**
- **外壳放边缘：** 内容由 URL 决定、与用户无关的响应，缓存键只用 URL，命中率可以到 99%。
- **个性化走小接口：** 页面加载后再请求 `/api/me/summary`，带身份，响应标 `Cache-Control: private`，CDN 不存；服务端用按用户的 Redis 缓存。
- **Cookie 入键的后果：** 每个用户一份副本，命中率接近 0，回源量等于全部请求，还撑满边缘存储。
- **更严重的风险：** 键里漏掉身份信息，就会把 A 的页面发给 B，这是数据泄露事故。
- **折中：** 按分群（语言、国家、实验分组，几十种）而不是按用户分键，命中率仍然很高。

**为什么。** 以每秒 1 万次页面请求翻倍到 2 万为例：外壳命中率 99%，回源只从 100 涨到 200；个性化接口从 1 万涨到 2 万，是全额翻倍。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="100" y="6" width="140" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<polyline points="130,36 80,74" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,74 83.2,67.8 86.9,72.6" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="210,36 260,74" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,74 253.1,72.6 256.8,67.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 页面外壳</text>
<text x="212" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 个性化</text>
<rect x="8" y="74" width="150" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CDN 边缘</text>
<text x="83" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">键=URL，所有人共享</text>
<text x="83" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率 99%</text>
<rect x="182" y="74" width="150" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="257" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用小接口</text>
<text x="257" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">GET /api/me/summary</text>
<text x="257" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">private，不入 CDN</text>
<polyline points="83,136 83,174" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,174 80.0,167.7 86.0,167.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="92" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1% 回源</text>
<rect x="8" y="174" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">源站 / 应用</text>
<polyline points="257,136 257,174" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,174 254.0,167.7 260.0,167.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="182" y="174" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="257" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 按用户缓存</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">流量翻倍：外壳回源只多一点，</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">个性化接口几乎全额翻倍。</text>
</svg>

**面试里这样说。** 「外壳放 CDN，缓存键只用 URL；个性化走 private 的小接口，不进 CDN。流量翻倍时外壳回源只多一百，个性化接口要翻倍，所以我扩容的是后者。」

**易错。**
- **给个性化响应加 public：** 共享缓存会把一个人的数据发给所有人。
- **以为 CDN 只能缓存静态文件：** 所有人共享的动态响应，设短 TTL 也可以缓存。
