---
id: encode-decode-errors-strategies
node: model.text-bytes
type: qa
source: python-docs
---
## Q
`bytes.decode(encoding, errors=...)` 和 `str.encode(encoding, errors=...)` 遇到无法按该编码转换的内容时，`'strict'`、`'ignore'`、`'replace'` 三种 `errors` 策略分别怎么处理？

## A
`'strict'`（默认）直接抛出异常——解码失败抛 `UnicodeDecodeError`，编码失败抛 `UnicodeEncodeError`；`'ignore'` 直接丢弃无法转换的字符或字节，结果里少了这部分内容；`'replace'` 用占位符替代——解码失败时插入 `U+FFFD`（替换字符），编码失败时插入 `?`。此外编码时还有 `'backslashreplace'`（插入 `\uNNNN` 转义序列）、`'xmlcharrefreplace'`（插入 XML 字符引用）等更细的策略，选哪种取决于下游系统能不能容忍丢失信息或需不需要保留可还原的痕迹。
