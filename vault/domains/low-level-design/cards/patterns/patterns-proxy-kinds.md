---
id: patterns-proxy-kinds
node: patterns.structural
type: cloze
---
The four classic proxy variants, by what they gate: {{c1::virtual}} proxy defers creating an expensive object until first use; {{c2::protection}} proxy checks the caller's permissions before delegating; {{c3::remote}} proxy makes a network object look local (RPC stubs); {{c4::caching}} proxy memoizes results of expensive calls. All keep the real subject's interface, so clients need no changes.

## zh
四种经典 proxy 变体，按它们守护的东西分类：{{c1::virtual}} proxy 延迟创建昂贵对象直到第一次使用；{{c2::protection}} proxy 在委托前检查调用者的权限；{{c3::remote}} proxy 让网络对象看起来本地（RPC stubs）；{{c4::caching}} proxy 记忆昂贵调用的结果。所有都保持真实 subject 的接口，所以客户端无需改变。
