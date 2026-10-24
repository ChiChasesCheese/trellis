---
id: pl-types-null-safety-table
node: types.null-safety
type: qa
step: 7
---
## Q
C++、Go、Java、Rust、Python 各怎样表示「没有值」？换来什么，付出什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| C++ | 引用（`T&`）保证非空，指针可以是 `nullptr`；`std::optional<T>`（C++17）表示可能没有的值，内联存储 | 用引用与指针的区别表达「一定有 / 可能没有」，`optional` 无堆分配 | 空指针解引用是未定义行为；对空的 `optional` 写 `*o` 同样是未定义行为，不报错；指针类 `optional` 没有空指针优化，体积翻倍 |
| Go | `nil` 适用于指针、切片、map、接口、函数；加上「零值可用」的设计 | 很多 `nil` 无害（`nil` 切片可 `append`），不必处处构造对象 | 解引用 `nil` 指针 panic；`nil` map 写入 panic；类型化 `nil` 放进接口后不等于 `nil` |
| Java | 每个引用都可能是 `null`；`Optional<T>` 只作为返回值的约定 | 简单，与历史代码兼容 | `NullPointerException` 是最常见的运行时异常；`Optional` 本身也可以是 `null` |
| Rust | 安全代码里没有 `null`，缺失用 `Option<T>` | 编译器强制处理缺失；指针类 `Option` 零开销 | 到处是 `match`、`?`、`unwrap` 的仪式；与 C 交互时要手工转换 |
| Python | `None` 是一个单例对象，任何变量都可以指向它 | 一致，`is None` 判断简单 | `AttributeError: 'NoneType' ...` 晚暴露；没写 `return` 的函数隐式返回 `None` |

背后的逻辑：Rust 的哲学是让非法状态不可表示，所以把缺失放进类型，全部检查前移到编译期；Go 的哲学是让零值有用，所以尽量让缺失不成为问题，用 `(value, ok)` 或 `error` 返回值代替；Java 和 Python 是早期设计，空值是语言内置的，后来用 `Optional`、类型提示和静态分析工具补课；C++ 从 C 继承了空指针，又用「引用不能为空」把大部分场景分流出去，再在 C++17 补上 `optional`，但两者都不阻止你写出错误的解引用：它相信程序员，而不是类型系统，所以对空值的保护不如 Rust 的 `Option` 彻底。选择的真实成本在于：越早强制处理，写代码时越慢，上线后越稳。
