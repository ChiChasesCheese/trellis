---
id: pl-data-serialization-best-practice
node: data.serialization
type: qa
step: 10
---
## Q
资深工程师怎样做序列化？通用规则是什么，Go、Java、Rust、Python 里各自要注意什么，何时破例？

## A
**通用规则**：
1. **数据格式是公共接口**：改字段名、类型和语义要像改 API 一样谨慎；新增字段可选，旧读者要忽略未知字段，旧数据要有默认值。
2. **越过信任边界的数据，用「只是数据」的格式**（JSON、Protocol Buffers），不用能指定类型或触发代码的格式。
3. **在边界处校验**：长度、范围、必填字段、嵌套深度、总大小。
4. **传输用 DTO（专门的数据传输类型），不直接序列化领域对象或数据库模型**，避免内部字段泄漏、内部重构破坏接口。
5. **数字要小心**：超过 2⁵³ 的整数、金额用字符串或定点，时间用 ISO 8601 或明确的时间戳单位。

按语言：
- **Go**：关键输入用 `DisallowUnknownFields()` 加校验函数；大整数不要解码进 `any`，用具体结构体或 `UseNumber()`；敏感字段打 `json:"-"`；`time.Time` 默认是 RFC 3339。
- **Java**：不用内建 `Serializable` 传输数据；若必须读取，配置 `ObjectInputFilter` 白名单；Jackson 里关闭默认类型推断（default typing），多态用显式的 `@JsonTypeInfo` 加子类型白名单；关掉 `FAIL_ON_UNKNOWN_PROPERTIES` 要有意识地决定。
- **Rust**：serde 用 `deny_unknown_fields` 视接口策略而定；用枚举表达变体；版本演进用 `#[serde(default)]`。
- **Python**：外部数据用 `json` 加 `pydantic` 或 `dataclass` 校验；永远不要 `pickle.loads` 不可信数据；需要存模型文件时用 `safetensors` 这类只存张量的格式，或对 pickle 做签名校验。

**何时破例**：进程内缓存、同一代码库同一版本内的临时文件，`pickle`/`Serializable` 可以用，但要写明「不跨版本、不跨信任边界」。
