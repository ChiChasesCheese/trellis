---
id: hl-sd01-multilang-config
node: system-design.sd01-unused-code
type: qa
step: 25
---
## Q
多语言代码库的跨语言边怎么建？多个构建配置（`#ifdef`、Maven profile）怎么处理？

## A
跨语言边：
- **JNI**：Java `native` 方法 ↔ C++ 导出符号 `Java_pkg_Class_method`，按名字规则连边；
- **协议 / IDL**（protobuf、Thrift、SBE 模板）：生成的类是叶子，但消息类型是否被用要看生成代码的引用，别把生成代码当死代码，从 IDL 文件出发建边；
- 配置 / 脚本里的类名：字符串命中；
- SQL / 动态查询里的表名列名：可选，低可信度；
- **覆盖率阈值**：任何模块的索引覆盖率低于阈值（构建失败、缺文件），则不对依赖它的符号做死判定（fail closed）。

多构建配置：对**所有配置取并集**，某个配置下用到的符号就是活的，即「死 = 在所有配置里都死」。没覆盖到的配置（如只在生产机上构建的 profile）是最大的假阴性来源，要把「索引覆盖了哪些配置」写进证据卡。
