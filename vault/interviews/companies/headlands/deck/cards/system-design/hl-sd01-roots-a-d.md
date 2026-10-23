---
id: hl-sd01-roots-a-d
node: system-design.sd01-unused-code
type: qa
step: 10
---
## Q
可达性分析里「根」（roots）的 A–D 四类是什么？为什么要用权威部署清单？

## A
- **A 已部署二进制的入口**：`main()`，权威依据是部署清单 / 启动脚本 / systemd unit / crontab，**不是**「所有含 main 的类」；
- **B 框架入口**：`@Scheduled`、`@Subscribe`、Servlet、`@Bean` / `@Component`（Spring）、JAX-RS 资源、Kafka 监听器，用框架模型规则把注解映射为根；
- **C 反射 / SPI / 序列化**：`ServiceLoader` 的 `META-INF/services`、`Class.forName("literal")`、`readObject` / `readResolve`、Jackson / Protobuf 的反射字段、JNI 导出符号；
- **D 导出的公共 API**：库的对外契约，属 L2，标「开放世界」。

用部署清单的原因：「所有含 main 的类」会把早已不部署的工具类当作根，让它们的整棵依赖树都显得「有用」，**假根导致漏报**。
