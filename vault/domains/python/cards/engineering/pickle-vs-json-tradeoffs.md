---
id: pickle-vs-json-tradeoffs
node: engineering.serialization
type: qa
source: python-docs
---
## Q
在「支持的类型范围」「是否跨语言」「反序列化不可信数据的风险」三个维度上，`pickle` 和 `json` 分别有什么取舍？

## A
`pickle` 是二进制格式，能表示几乎任意 Python 类型（包括自定义类实例），但是 Python 专属、不可读也不跨语言，且反序列化不可信数据本身就是代码执行漏洞。`json` 是文本格式，默认只能表示内置类型的一个子集（不含自定义类），但可读、跨语言互通广泛使用，并且反序列化不可信的 JSON 本身不会造成任意代码执行。需要与外部系统交换数据、或数据来源不可信时选 `json`；只在纯 Python 内部、数据自己可信时才用 `pickle`。
