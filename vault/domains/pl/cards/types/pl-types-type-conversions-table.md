---
id: pl-types-type-conversions-table
node: types.type-conversions
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 对数值缩窄、向下转型、字符串解析这三类转换，各用什么方式表示失败？换来什么，付出什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Go | 数值 `T(x)` 静默截断；断言 `v.(T)` 带 `ok` 或 panic；`strconv` 返回 `error` | 写法统一、简短，三类失败都显式可处理 | 数值缩窄不报错，截断悄悄发生 |
| Java | `(T) x` 数值静默截断；对象转型抛 `ClassCastException`；`Integer.parseInt` 抛 `NumberFormatException` | 异常集中在调用栈上方处理 | 数值强制转换不检查；异常不出现在方法签名里 |
| Rust | `as` 有损（截断或饱和）；`From` 无损；`TryFrom` 返回 `Result`；`parse` 返回 `Result`；`Any::downcast_ref` 返回 `Option` | 风险在类型里分级，调用者必须处理失败 | 写法最啰嗦；`as` 依然会悄悄截断，要靠 lint 约束 |
| Python | `int()`、`str()`、`float()` 构造函数转换，失败抛 `ValueError`/`TypeError`；`isinstance` 检查类型 | 动态语言里转换是普通函数调用，统一易懂 | 失败在运行时才出现；`int(3.9)` 是 3（截断），`bool("0")` 是 `True`，规则要记 |

背后的逻辑：转换失败应当被看见，还是应该被忽略，各语言的哲学不同。Rust 的选择是把风险分级、让类型来表达，理由是转换点正是 bug 的高发处。Go 倾向于让常见情况简短、失败显式（`ok`、`error`），而数值缩窄为简短保持了 C 的随意。Java 用异常把失败从代码路径中拿出来，代价是容易被忽略。Python 把转换当作普通函数，错误在运行时报告。
