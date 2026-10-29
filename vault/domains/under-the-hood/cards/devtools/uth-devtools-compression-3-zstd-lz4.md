---
id: uth-devtools-compression-3-zstd-lz4
node: devtools.compression
type: qa
step: 3
---
## Q
**LZ4 一个压缩块长什么样**｜LZ4 · 1.10 与 zstd · 1.5.7

LZ4 为什么解压极快？zstd 在它的基础上多做了什么？

## A
**结构。** LZ4 只做 LZ77、不做熵编码：每个序列是 1 字节 token（高 4 位是字面量长度，低 4 位是匹配长度）、字面量、2 字节偏移。zstd 在 LZ 之上再用 FSE 和哈夫曼做熵编码。

**细节。**

- LZ4：偏移最大 65535（64 KB 窗口），最短匹配 4 字节；长度字段填满 15 就后续字节继续累加
- 解压只是读 token、拷贝字面量、按偏移复制，没有位级解码
- zstd 默认级别 3，RFC 8878 建议解码器至少支持 8 MB 窗口

**为什么。** LZ4 用压缩率换速度；zstd 补上熵编码，窗口也更大，压缩率更高；DEFLATE 的窗口只有 32 KB。

**对应 LeetCode：** LC 394 字符串解码 · LC 443 压缩字符串
