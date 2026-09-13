---
id: runtime-go-http-reverse-proxy-boundary
node: runtimes.go-http
type: qa
---
## Q
You are adding cache routing to a Go reverse proxy. Which logic belongs around `ReverseProxy`, and which behavior must remain an explicit policy rather than an accidental default?

## A
Use the proxy as the HTTP transport boundary: rewrite the upstream URL and `Host`, remove hop-by-hop headers, stream the body, and surface upstream errors. Keep cache-key construction, retry eligibility, timeout budgets, header allowlists, and fail-open/fail-closed decisions in explicit surrounding policy. A generic proxy can move bytes correctly; it cannot infer whether a personalized response is safe to cache or whether replaying a request is safe.

## Q zh
你要在 Go reverse proxy 中加入 cache routing。哪些逻辑属于 `ReverseProxy` 的传输边界，哪些行为必须是显式 policy，而不能依赖偶然的默认值？

## A zh
把 proxy 当作 HTTP transport boundary：改写 upstream URL 和 `Host`、移除 hop-by-hop headers、流式转发 body，并暴露 upstream error。cache key、retry eligibility、timeout budget、header allowlist，以及 fail-open/fail-closed 必须放在外围的显式 policy 中。通用 proxy 能正确搬运 bytes，却无法判断 personalized response 是否可缓存，也无法判断重放请求是否安全。
