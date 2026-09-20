---
id: patterns-proxy-kinds
node: patterns.structural
type: cloze
step: 1
---
四种经典 proxy 变体，按它们守护的东西分类：{{c1::virtual}} proxy 延迟创建昂贵对象，直到第一次真正用到；{{c2::protection}} proxy 在把调用转发给真实对象之前先检查调用者的权限；{{c3::remote}} proxy 让另一台机器上的对象看起来像本地对象（RPC stub）；{{c4::caching}} proxy 记住上一次昂贵调用的结果。四种都保持和真实 subject 一样的接口，所以客户端完全不用改代码。
