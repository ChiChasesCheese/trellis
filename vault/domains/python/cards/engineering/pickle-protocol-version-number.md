---
id: pickle-protocol-version-number
node: engineering.serialization
type: qa
source: python-docs
---
## Q
pickle 协议（protocol）版本号越高，对「读取这份 pickle 数据所需的 Python 版本」意味着什么？目前（3.14 起）的默认协议是第几版？

## A
pickle 目前一共有 0–5 共 6 个协议版本，协议版本号越高，读取该数据所需的 Python 版本就越新——用高版本协议序列化的数据，不能被只支持更早协议的旧版 Python 反序列化。默认协议在 Python 3.0–3.7 是协议 3，3.8–3.13 是协议 4，3.14 起默认是协议 5（支持带外数据传输）。跨版本、跨环境交换 pickle 数据时，需要显式指定双方都支持的协议号，而不是依赖默认值。
