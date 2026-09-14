---
id: kafka-admin-describeconfigs-isdefault
node: admin.dynamic-config
type: qa
source: kafka-2e
---
## Q
用 AdminClient 的 describeConfigs 查询一个主题的配置后，怎么判断某个具体配置项是使用集群默认值，还是被人为覆盖过？

## A
describeConfigs 返回的每一条 ConfigEntry（配置条目）都带有一个 isDefault() 方法：调用它返回 false，说明这个配置要么在主题级别被单独覆盖过，要么继承了 broker 级别的非默认值；返回 true 才说明它就是集群本身的默认配置。因此想找出「哪些配置被改动过」，只需要对 describeConfigs 返回的所有条目按 `!entry.isDefault()` 过滤即可，不需要自己维护一份「默认值表」去逐项比较。
