---
id: pl-data-strings-intro-python
node: data.strings-text
type: qa
step: 6
---
## Q
Python 3 的 `str` 是什么？它与 `bytes` 为什么被严格分开，内部怎样用灵活的宽度存储码点？

## A
**是什么**：`str` 是不可变的 Unicode 码点序列。`len(s)` 和 `s[i]` 都按码点，O(1)。`"a😀é"` 的 `len` 是 3，`ord` 分别是 `0x61`、`0x1f600`、`0xe9`。

**`str` 与 `bytes` 严格分开**：`str` 是文本，`bytes` 是字节；二者互不隐式转换。要变成字节必须显式 `s.encode("utf-8")`，反过来 `b.decode("utf-8")`。这个设计是 Python 2 到 3 的最大断裂之一：2 里 `str` 其实是字节，混用时在遇到非 ASCII 才报错；3 里在边界上就强制你选编码。

**内部存储（PEP 393）**：为了让下标 O(1) 又不浪费内存，CPython 按字符串中最大的码点选择每字符宽度：全是 ASCII 或 Latin-1 用 1 字节，含 U+FFFF 以内字符用 2 字节，含 emoji 之类则全串用 4 字节。一次本机测量：100 个 `a` 占 141 字节，100 个 `é` 占 157 字节，100 个 `😀` 占 460 字节。**一个 emoji 会让整串的每个字符膨胀到 4 字节。**

**孤立代理码点**：Python 的 `str` 允许存放不合法的单独代理码点 `"\ud800"`，但 `encode()` 时会报 `UnicodeEncodeError: surrogates not allowed`，这是文本进入文件或网络时才暴露的问题。

**要记住的一点**：Python 的 `len` 是码点数，而不是用户看到的字符数；国旗 `len("🇯🇵")` 是 2，`é` 的组合写法 `len("é")` 是 2。
