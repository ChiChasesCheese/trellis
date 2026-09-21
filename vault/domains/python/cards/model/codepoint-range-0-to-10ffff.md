---
id: codepoint-range-0-to-10ffff
node: model.text-bytes
type: qa
source: python-docs
---
## Q
Unicode 码点（code point）的合法取值范围是多少？Python 的 `str` 类型和这个范围是什么关系？

## A
Unicode 码点是一个整数，取值范围是 `0` 到 `0x10FFFF`（十进制 1,114,111），约 111 万个可能取值（实际已分配的字符数比这个上限少）。自 Python 3.0 起，`str` 类型的每个元素就是这个范围内的一个码点，字符串字面量、三引号字符串都按码点序列存储，这也是 Python 3 的字符串能原生表示任意语言文字和 emoji 的原因。
