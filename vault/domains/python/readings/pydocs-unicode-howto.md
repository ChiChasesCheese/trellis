---
nodes:
- model.text-bytes
title: Unicode HOWTO：字符串与字节的边界
corpus: python-docs
section: 11-unicode
url: https://docs.python.org/3/howto/unicode.html
tags:
- canonical
---

# Unicode HOWTO：字符串与字节的边界

这篇 HOWTO 讲清了 Python 3 字符串模型的根本设定：str 是 Unicode 码点（code point）序列，bytes 是原始字节序列，两者之间必须显式通过编码（encode）/解码（decode）转换，绝不会隐式互转。文中详细讲了各种编码方式（UTF-8/UTF-16/Latin-1 等）的取舍，以及为什么 UTF-8 是网络传输和文件存储的事实标准。特别有价值的是读写 Unicode 数据一节：建议尽早把输入解码成 str，只在程序内部处理文本，写出前再编码成 bytes，这就是常说的 Unicode 三明治原则，能一次性避免大部分乱码和 UnicodeDecodeError。文末还讨论了不同操作系统上文件名编码的坑。读完能准确判断一段报错到底是编码问题还是解码问题，而不是靠试错加 .encode()/.decode()。
