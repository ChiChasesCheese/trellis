---
id: pl-trends-effects-best-practice
node: trends.effects
type: qa
step: 9
---
## Q
即使语言不追踪效应，资深工程师怎样在 Go、Java、Rust、Python 里用设计手段管理它们？

## A
核心做法：**把效应推到程序的边缘，让核心逻辑保持纯。**这被称为「函数式核心，命令式外壳」（functional core, imperative shell）：

- **外壳**：读写文件、数据库、网络、时钟、随机数、日志，集中在少数入口和适配层；
- **核心**：纯函数，输入是值，输出是值，不做 I/O，不依赖全局状态。

好处：核心可以不用任何 mock 地测试；失败的原因更容易定位；以后要换存储或加缓存，只动外壳。

**各语言的具体做法**

- **所有语言**：把时钟、随机数、环境变量、HTTP 客户端作为参数传入，不在函数内部直接取；这样测试里可以传一个固定值。
- **Rust**：利用类型表达效应。可失败的函数返回 `Result`，错误类型用 `thiserror` 定义；不要用 `unwrap()` 把失败悄悄变成 `panic`；`async` 只用于真正做 I/O 的函数，纯计算保持同步；`async` 里不要持有 `std::sync::Mutex` 的守卫穿过 `.await`。
- **Go**：定义小接口描述外部依赖（`type Clock interface { Now() time.Time }`），让调用者注入；错误用 `fmt.Errorf("…: %w", err)` 包装保留信息；`context.Context` 作为首个参数携带取消和超时，它是 Go 版的「可传递的环境效应」。
- **Java**：受检异常只用于调用者真能恢复的失败；在 lambda 中需要抛异常时，包装成带原因的非受检异常，不吞掉；虚拟线程让你写同步风格的阻塞代码，不要在其上再叠一层 `CompletableFuture` 链。
- **Python**：`async` 函数里不调用阻塞库函数（`time.sleep`、`requests`），需要时用 `asyncio.to_thread`；用 `contextvars` 传递请求级上下文；纯函数加 `functools.cache` 才安全。

**什么时候违反**：小脚本和一次性工具直接混写 I/O 与逻辑，分层的收益小于成本。

**一个自检问题**：读到一个函数，能否不看实现就回答「它会不会失败、会不会阻塞、会不会修改参数、会不会访问外部系统」？回答不了，就用命名、类型和参数把答案放到签名上。
