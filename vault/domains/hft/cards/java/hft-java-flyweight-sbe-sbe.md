---
id: hft-java-flyweight-sbe-sbe
node: java.flyweight-sbe
type: qa
step: 2
---
## Q
SBE（Simple Binary Encoding）生成的 Java 编解码器是怎样工作的？

## A
SBE 用一份 XML schema 定义消息：字段名、类型、顺序、长度。代码生成器据此输出 Java（或 C++）的 Encoder 和 Decoder 类，它们本质上就是 flyweight：先 `decoder.wrap(buffer, offset, blockLength, version)`，之后每个 getter 都是在固定偏移上的一次缓冲区读取。

定长字段放在消息开头的定长块里，位置在编译期就确定，所以不需要扫描分隔符、不需要转换数字、不需要创建对象；用到哪个字段才读哪个字段。变长数据（重复组、可变长字符串）放在定长块之后，必须按 schema 顺序读取。

对比 FIX 文本（要扫描 tag=value 并把字符串转成数字），SBE 没有“解析阶段”，这也是 CME 的 MDP 3.0 行情选用它的原因。
