---
id: unicode-sandwich-decode-early-encode-late
node: model.text-bytes
type: qa
source: python-docs
---
## Q
处理文本 I/O 时经常提到的「Unicode 三明治（Unicode sandwich）」原则说的是什么？为什么按这个原则组织代码能减少 `str`/`bytes` 混用导致的 `TypeError`？

## A
原则是：在程序的输入边界（读文件、收网络包）尽早用 `bytes.decode()` 把字节转换成 `str`，在输出边界（写文件、发网络包）尽晚用 `str.encode()` 把 `str` 转换回字节，程序内部的业务逻辑自始至终只处理 `str`，像三明治一样把「解码-处理-编码」分成三层。这样做的好处是内部逻辑不需要到处判断「这个变量到底是 str 还是 bytes」；如果解码/编码分散在代码各处，很容易在某处把 bytes 和 str 直接拼接或比较，触发 `TypeError`，而且编码错误会散落在难以定位的地方。
