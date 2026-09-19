---
id: kafka-connect-smt-common-types
node: connect.smt
type: cloze
step: 1
source: kafka-2e
---
Connect 内置的单一消息转换（SMT）覆盖了几类常见的轻量加工需求，包括：{{c1::Cast——改变某个字段的数据类型}}、{{c2::MaskField——把某个字段的内容替换成 null，常用于遮蔽个人识别信息等敏感数据}}、{{c3::Filter——按主题名、消息头或是否为墓碑消息（值为 null 的消息）等条件丢弃或保留记录}}、{{c4::RegexRouter——用正则表达式和替换字符串动态改变消息要写入的目标主题}}、{{c5::InsertHeader——给每条消息的消息头（header）里加入一个固定的字符串}}。这些转换都不需要写代码，只需在连接器配置里声明即可生效。
