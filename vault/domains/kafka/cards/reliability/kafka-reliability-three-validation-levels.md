---
id: kafka-reliability-three-validation-levels
node: reliability.validation
type: cloze
step: 1
source: kafka-2e
---
把生产者、broker、消费者都按可靠性需求配置好之后，还要从三个层面持续验证系统真的可靠：{{c1::验证配置（用工具单独测试 broker/客户端配置，不涉及应用逻辑）}}、{{c2::验证应用程序（对错误处理、偏移量提交、再均衡监听器等做集成测试，模拟故障场景）}}、{{c3::在生产环境中监控可靠性（持续观察客户端指标、消费者滞后和端到端数据流）}}。三者缺一不可：配置对不代表代码写对，代码在测试环境里对也不代表生产环境长期正常。
