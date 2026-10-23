%% trellis:begin %%
# flyweight 编解码与 SBE
*低延迟 Java*

不创建消息对象，而是用一个可复用的 flyweight 直接在字节缓冲区上按偏移量读写字段；SBE 生成的 Java 编解码器就是这样。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.off-heap|堆外内存：DirectByteBuffer、Unsafe、FFM API 与 mmap]], [[domains/hft/map/protocols.sbe-mdp3|SBE 与 CME MDP 3.0]]

## Readings
- [[sbe-wiki|Simple Binary Encoding（SBE）设计说明]]

## Cards (5)
1. [[hft-java-flyweight-sbe-idea]]
2. [[hft-java-flyweight-sbe-sbe]]
3. [[hft-java-flyweight-sbe-pitfalls]]
4. [[hft-java-flyweight-sbe-vs-pojo]]
5. [[hft-java-flyweight-sbe-zero-copy]]
%% trellis:end %%

## Notes
