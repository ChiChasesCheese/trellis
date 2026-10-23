---
id: hl-javaq-b-q05-cautions
node: java-questions.b-versions
type: qa
step: 4
---
## Q
聊 Java 版本特性时，哪些不要说、哪些要说清是预览？追问"sealed + 模式 switch 为什么比 visitor 好""record 到底是什么、是不是 Lombok `@Value`"怎么答？
Why sealed + pattern switch instead of the visitor pattern? What is a record exactly?

## A
- **不要说**：String Templates——Java 21 里是预览，后来被撤回。
- **预览特性**（结构化并发、`ScopedValue` 等）要说清楚是预览，需要 `--enable-preview`。
- **sealed + switch vs visitor**：编译器穷尽检查；不用 `accept` 样板；加新类型时漏处理会编译失败。
- **record 是什么**：**语言级**特性，不是 Lombok 注解。有规范构造器、紧凑构造器可做校验；`equals / hashCode / toString` 由 `ObjectMethods` 引导方法生成；不能被继承，字段都是 `final`。
