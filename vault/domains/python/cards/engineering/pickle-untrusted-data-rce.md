---
id: pickle-untrusted-data-rce
node: engineering.serialization
type: qa
source: python-docs
---
## Q
为什么绝对不能用 `pickle.loads()` 反序列化来自不可信来源（比如用户上传、未加密的网络消息）的数据？

## A
`pickle` 的反序列化（unpickling）过程本身可以在还原对象时执行任意代码——精心构造的恶意 pickle 数据在被加载时就能直接运行攻击者指定的代码，这不是某种边缘 bug，而是这个二进制协议本身的设计特性。所以只应该反序列化自己生成、或来源完全可信且未被篡改的 pickle 数据；处理不可信数据要么改用 `json` 这类不会在反序列化阶段执行代码的格式，要么先用 `hmac` 这样的签名机制验证数据未被篡改。
