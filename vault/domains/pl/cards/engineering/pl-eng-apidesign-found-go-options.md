---
id: pl-eng-apidesign-found-go-options
node: engineering.api-design
type: qa
step: 2
---
## Q
Go 没有默认参数和方法重载，库作者怎样给构造函数提供“可选配置”？函数式选项（functional options）模式是什么，为什么 Go 社区偏爱它？

## A
Go 的函数签名固定：每个参数必须传，没有默认值，没有重载，没有命名参数。要提供一个“大部分用默认值”的构造函数，常见两种做法：

1. **配置结构体**：`NewServer(Config{Addr: ":8080", Timeout: 2 * time.Second})`。简单，零值字段表示“用默认”。Go 的惯例是**让零值可用**（`sync.Mutex`、`bytes.Buffer` 的零值就能直接使用）。
2. **函数式选项**：构造函数接受可变数量的“修改器”函数。
```go
type Option func(*Server)
func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }
func NewServer(addr string, opts ...Option) *Server {
	s := &Server{addr: addr, timeout: 30 * time.Second, retries: 3} // defaults
	for _, o := range opts { o(s) }
	return s
}
// NewServer(":8080")                                   -> 30s 3
// NewServer(":8080", WithTimeout(2*time.Second), WithRetries(0)) -> 2s 0
```
**为什么受欢迎**：
- **可演进**：新增一个选项只是新增一个函数 `WithX`，不改变 `NewServer` 的签名，旧代码照常编译。结构体也能加字段，但调用者用位置写法时会破坏。
- **能区分“没设置”和“设成零”**：`WithRetries(0)` 明确表示“零次重试”，而结构体里 `Retries: 0` 无法区分“默认”和“显式零”。
- **自带文档**：每个选项一个函数，有自己的注释，补全时一目了然。
- **选项可以做校验、组合**。

**代价**：样板多（每个选项一个函数），每个选项是一个闭包（有轻微的分配成本），选项无法序列化或比较，不适合由配置文件驱动。

**选择规则**：配置项不到三四个、基本是纯数据 → 配置结构体；选项多、需要保持向后兼容、需要区分“未设置” → 函数式选项。标准库自己多用结构体（`http.Server{}`），第三方库多用选项。
