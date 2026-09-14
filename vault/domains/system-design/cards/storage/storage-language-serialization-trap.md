---
id: storage-language-serialization-trap
node: storage.encoding
type: qa
---
## Q
Java's `Serializable`, Python's `pickle`, Ruby's `Marshal` are one line of code. Why is language-native serialization considered unacceptable for anything persisted or sent between services? Give the four standing objections.

## A
- **Security**: decoding must be able to instantiate arbitrary classes named in the byte stream — untrusted input can therefore trigger attacker-chosen code paths; deserialization RCEs are a recurring vulnerability class.
- **No cross-language story**: the bytes encode one runtime's object graph; committing to them welds your stored data and your APIs to that language, possibly for decades.
- **Versioning is an afterthought**: the format tracks internal class layout, so renaming a class or changing a field commonly breaks reads of old data — the opposite of the deliberate forward/backward evolution rules schema formats provide.
- **Efficiency**: encodings tend to be bloated (class metadata per record) and slow relative to purpose-built formats.

Verdict: acceptable only for transient, same-process-family use (never for untrusted bytes); anything crossing a service boundary or landing on disk deserves JSON or a schema format (Protobuf, Avro, Thrift).

## Q zh
Java 的 `Serializable`、Python 的 `pickle`、Ruby 的 `Marshal` 都只要一行代码。为什么语言内建的序列化被认为不能用于任何持久化或服务间传输的数据？给出四条常设的反对理由。

## A zh
- **安全**：解码必须能够实例化字节流中指名的任意类 — 因此不可信输入可以触发攻击者选择的代码路径；反序列化 RCE 是一个反复出现的漏洞类别。
- **没有跨语言故事**：这些字节编码的是某一个运行时的对象图；押注它们就把你的存储数据和 API 焊死在那门语言上，可能一焊几十年。
- **版本演化是事后补丁**：格式跟踪的是类的内部布局，所以重命名一个类或改动一个字段常会弄坏对旧数据的读取 — 与 schema 格式提供的、深思熟虑的 forward/backward 演化规则恰恰相反。
- **效率**：这类编码往往臃肿（每条记录带类元数据）且相对专用格式更慢。

结论：只在瞬态的、同进程家族内的用途可接受（永远不要喂不可信字节）；任何跨服务边界或落盘的数据都配得上 JSON 或 schema 格式（Protobuf、Avro、Thrift）。
