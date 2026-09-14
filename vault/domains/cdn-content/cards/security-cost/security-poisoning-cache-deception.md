---
id: security-poisoning-cache-deception
node: security-cost.poisoning
type: qa
---
## Q
An authenticated page at `/account` also responds to `/account/avatar.jpg`, and the CDN caches `.jpg` paths by extension. What is the vulnerability?

## A
Web cache deception. The attacker induces a victim to request a path the origin treats as private dynamic content but the CDN classifies as a public static asset, then retrieves the cached response. Align cache eligibility with origin routing and response `Content-Type`/cache policy, reject misleading path suffixes, and test authenticated routes through the CDN—not only at origin.

## Q zh
authenticated page `/account` 也会响应 `/account/avatar.jpg`，而 CDN 按 `.jpg` extension 缓存 path。这是什么漏洞？

## A zh
这是 web cache deception。attacker 诱导 victim 请求一个 origin 当作 private dynamic content、但 CDN 当作 public static asset 的 path，然后读取 cached response。应让 cache eligibility 与 origin routing、response `Content-Type`/cache policy 对齐，reject misleading path suffix，并通过 CDN 测试 authenticated route，而不只是在 origin 测试。
