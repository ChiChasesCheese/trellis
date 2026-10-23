---
id: hft-java-flyweight-sbe-pitfalls
node: java.flyweight-sbe
type: qa
step: 3
---
## Q
使用 flyweight 编解码器时，最容易踩哪些坑？

## A
因为视图只是缓冲区上的一扇“窗”，坑也都来自这点：
- **生命周期**：缓冲区被复用或覆盖后，窗口里的值就变了。需要保留的字段要立刻复制成局部的 `long`、`int`，或复制字节。
- **线程安全**：视图持有可变的偏移状态，不能多线程共享，每个线程各用一个。
- **字节序**（byte order）：SBE 默认小端（little-endian，和 x86 一致），而 ITCH 等交易所协议常用大端（big-endian），读取时要转换，否则价格差几个数量级。
- **越界**：偏移算错会读到相邻消息的内容，没有类型保护；可以用带边界检查的缓冲区在测试时发现。
