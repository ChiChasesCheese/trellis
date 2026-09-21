---
id: str-is-codepoint-sequence-bytes-is-byte-sequence
node: model.text-bytes
type: qa
source: python-docs
---
## Q
Python 里 `str` 和 `bytes` 在存储内容的本质上有什么不同？编码（encode）和解码（decode）分别是在哪两种类型之间转换？

## A
`str` 是 Unicode 码点（code point）序列——每个码点是一个整数，代表一个抽象字符的编号，与具体的字节表示无关；`bytes` 是字节（byte，取值 0–255 的整数）序列，是数据在磁盘、网络或内存里的具体二进制表示。`str.encode(encoding)` 把码点序列按某种编码规则转换成字节序列（bytes）；`bytes.decode(encoding)` 反过来把字节序列按同一种编码规则还原成码点序列（str）。两者不能直接混用比较或拼接，必须显式指定编码在两者间转换。
