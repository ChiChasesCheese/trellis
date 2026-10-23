---
id: hl-sd01-fu-reflection
node: system-design.sd01-unused-code
type: qa
step: 29
---
## Q
追问：反射、依赖注入、`ServiceLoader`、序列化，静态分析看不见怎么办？

## A
这是静态分析的天花板问题。不要说「处理不了」，要说「分类、保守、记录 blocker、从失败中学习」：
1. 把动态入口**建模成规则化的根**：Spring 注解（`@Component`、`@Bean`、`@Scheduled`）、`META-INF/services`、`readObject` / `readResolve`、Jackson / Protobuf 反射字段、JNI 导出名；
2. **字符串命中当弱根**：常量池 + 仓库文本文件里出现该类 FQN → 记为 blocker，降低可信度，不直接保活；
3. **输出里写 blocker**，让审阅者知道这条为什么是 MEDIUM；
4. **闭环学习**：owner 拒绝某个候选并说「其实是被 X 机制用的」→ 新增一条根规则，下次所有同类自动受保护；
5. 动态证据兜底。

可以说：「静态分析永远是保守的近似，所以我用规则化的根模型 + 字符串弱根，并把每次误报变成一条新规则。」
