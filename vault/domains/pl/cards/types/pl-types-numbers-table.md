---
id: pl-types-numbers-table
node: types.numbers
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 整数溢出时的行为各是什么？它们换来什么，又付出什么？

## A
| 语言 | 溢出行为 | 换来 | 代价 |
|---|---|---|---|
| Go | 有符号和无符号都回绕，且语言规范明确规定 | 行为确定，无检查开销，哈希、校验和很好写 | 业务计算溢出时悄悄出错；常量溢出才是编译错误 |
| Java | `int` 和 `long` 静默回绕；`Math.addExact` 等版本抛 `ArithmeticException`；没有无符号类型 | 行为确定，可选检查 | 默认路径不报错，`int` 毫秒时间戳之类的 bug 要到溢出才暴露 |
| Rust | debug 构建 panic，release 构建默认回绕；`checked_`、`wrapping_`、`saturating_`、`overflowing_` 让你显式选择 | 把「溢出怎么办」变成每个调用点的显式决定 | 两种构建的默认行为不同；写法啰嗦 |
| Python | `int` 任意精度，永不溢出 | 数学语义，大数运算直接可用 | 每个整数是堆上的对象，运算比机器指令慢一个数量级以上 |

背后的逻辑：语言对溢出的态度反映它对「速度还是正确性」的优先级。Go 和 Java 选了确定的回绕：先保证行为可预测、实现简单。Rust 认为溢出几乎总是 bug，所以开发时用 panic 暴露，发布时为速度关掉检查，并提供一整套显式 API 让你决定。Python 的目标是让程序员不去想位宽，所以把成本转嫁给运行时。浮点上四门语言完全一致，都遵循 IEEE 754。
