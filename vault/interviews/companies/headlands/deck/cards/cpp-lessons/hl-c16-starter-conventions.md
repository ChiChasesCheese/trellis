---
id: hl-c16-starter-conventions
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 25
---
## Q
C++ 起点文件有哪些约定？异常类型为什么是接口的一部分？

## A
- 公共类型与签名已给出，函数体抛 `std::logic_error("TODO")`。
- 未使用的参数**不写名字**，免得警告。
- 异常类型（`std::out_of_range`、`std::invalid_argument`、各题自定义的异常）是**接口的一部分**，测试按类型检查（`CHECK_THROWS_AS`），所以抛错类型要对。
