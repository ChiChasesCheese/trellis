---
id: wrong-direction-encode-decode-error
node: model.text-bytes
type: qa
source: python-docs
---
## Q
`u.encode('ascii')` 在 `u` 含有超出 ASCII 范围的字符时会报什么错？这和 `b'\x80abc'.decode('utf-8')` 报的错是同一类问题吗？

## A
`str.encode('ascii')` 遇到码点超出 0–127 范围的字符会抛 `UnicodeEncodeError`（无法把这个码点表示成合法的 ASCII 字节）；`bytes.decode('utf-8')` 遇到不构成合法 UTF-8 字节序列的输入（如单独一个 `0x80` 起始字节）会抛 `UnicodeDecodeError`（无法把这些字节还原成合法码点）。二者方向相反但本质是同一类问题：选用的编码规则覆盖不了实际内容，`errors` 参数（strict/ignore/replace 等）决定遇到这种情况时是报错、丢弃还是用占位符顶替。
