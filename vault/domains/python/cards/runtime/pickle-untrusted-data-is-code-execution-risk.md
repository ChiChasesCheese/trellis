---
id: pickle-untrusted-data-is-code-execution-risk
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
为什么官方文档强调「永远不要 unpickle 不可信来源的数据」？需要自定义某个类被 pickle 的方式时，标准钩子是什么？

## A
pickle 的反序列化格式本身可以构造出「unpickle 时执行任意代码」的恶意数据——这是协议设计使然，不是某个具体漏洞，所以来路不明或可能被篡改过的数据绝不能直接 unpickle（更安全的替代是 json 这类不会触发任意代码执行的格式，或者用 `hmac` 之类工具对数据做签名校验）。需要自定义序列化行为时，标准做法是给类实现 `__reduce__()` 方法，或把处理函数注册进 `copyreg` 模块维护的全局 dispatch table，而不是自己发明一套格式。
