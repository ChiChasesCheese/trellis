---
id: net-proxy-tls-termination-boundary
node: networking.proxies
type: qa
tags: [grown]
---
## Q
A reverse proxy accepts HTTPS connections from the internet and forwards each request to upstream servers over plain HTTP inside a private network. What is this pattern called, what header must the proxy add so upstream code doesn't misjudge the request's security, and when does the pattern become unsafe?

## A
This is **TLS termination** (SSL termination): the proxy decrypts once at the edge so every upstream server doesn't have to pay its own TLS handshake cost. Because the hop past the proxy is plaintext, the proxy must set a header such as `X-Forwarded-Proto: https` so upstream code that inspects the request's scheme — to redirect HTTP to HTTPS, or to set a cookie's `Secure` flag — doesn't see `http` and behaves as if the connection were insecure. The pattern is unsafe whenever the plaintext hop crosses a network segment an attacker could observe or inject traffic into; there, the proxy must re-encrypt to the upstream (TLS re-encryption, sometimes with mutual TLS) instead of relying on the network being trusted.

## Q zh
一个 reverse proxy 从互联网接受 HTTPS 连接，然后在私有网络内以明文 HTTP 把每个请求转发给 upstream server。这种模式叫什么？proxy 必须加什么 header 才能让 upstream 代码不误判请求的安全性？这种模式在什么情况下不安全？

## A zh
这就是 **TLS termination**（SSL termination）：proxy 在边缘只解密一次，这样每个 upstream server 就不必各自承担 TLS handshake 的开销。因为经过 proxy 之后的这一跳是明文的，proxy 必须设置类似 `X-Forwarded-Proto: https` 这样的 header，这样检查请求 scheme 的 upstream 代码——比如用于把 HTTP 重定向到 HTTPS，或给 cookie 设置 `Secure` 标志——就不会看到 `http` 而把连接当作不安全处理。当这段明文链路会经过攻击者可以窃听或注入流量的网络段时，这种模式就不安全；此时 proxy 必须对 upstream 重新加密（TLS re-encryption，有时配合 mutual TLS），而不能依赖网络本身是可信的。
