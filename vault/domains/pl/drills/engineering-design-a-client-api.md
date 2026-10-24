---
nodes: [engineering.api-design, engineering.static-analysis]
tags: [drill]
---
# 练习：把一个六参数的客户端构造函数改成各语言地道的 API

公司的内部 SDK 有一个构造函数 `Client(host, port, timeout, retries, tls, user_agent)`，其中除了 `host` 全是可选参数，四种语言的版本都是原样翻译过去的：调用点出现 `Client("x", 443, 5, 3, true, "")` 这样一长串位置参数，已经有人把 `timeout` 和 `retries` 写反。Python 版本里还有一个 `add_event(e, log=[])` 的辅助函数，线上出现过两个请求互相看到对方的事件。你要为每门语言重新设计构造入口，并解释哪种设计让错误在更早的阶段暴露。

**要你给出的**
- Go、Java、Python、Rust 各一个构造入口的签名和一个调用示例，要求：`host` 必填、其余有默认值、可以只改一项、构造后不可变。
- 说明每个设计分别由语言的哪些特性支撑（没有默认参数、没有具名参数、有关键字参数、所有权等）。
- 预测下面 Python 片段的输出，解释原因，并给出修复和能自动发现它的工具。

```python
def add_event(e, log=[]):
    log.append(e)
    return log
print(add_event("a"), add_event("b"))
```

- 参数校验放在哪个阶段：编译期、构造期、使用期。

**评分要点**
- Go 用函数式选项（functional options）：`New(host string, opts ...Option) (*Client, error)`，选项是 `func(*Client)`，如 `WithRetries(1)`；Go 没有默认参数和具名参数，这是用变长参数模拟的。示例 `New("x", WithRetries(1))` 得到 `{host:x timeout:5000000000 retries:1}`，`New("")` 返回错误 `host required`；校验在构造期 ([[pl-eng-apidesign-found-go-options]], [[pl-eng-apidesign-principle]])。
- Java 用 `record` 加构建器（builder）：`Client.builder("x").retries(1).build()` 输出 `Client[host=x, timeout=PT5S, retries=1]`，`record` 的紧凑构造器里校验，`host` 为空时抛 `IllegalArgumentException: host required`。Java 没有具名参数，构建器让每个值在调用点有名字 ([[pl-eng-apidesign-found-java-builder]], [[pl-eng-apidesign-table]])。
- Python 用仅限关键字的参数或 `@dataclass(frozen=True, kw_only=True)`：`ClientConfig(host="x")` 输出 `ClientConfig(host='x', port=443, timeout_s=5.0, retries=3)`；写成位置参数 `ClientConfig("x", 80)` 抛 `TypeError`，赋值 `c.port = 1` 抛 `FrozenInstanceError`。函数用 `fetch(url, *, timeout=5.0, retries=3)` 让调用点必须写关键字 ([[pl-eng-apidesign-found-python-kwargs]], [[pl-eng-apidesign-best-practice]])。
- Rust 用构建器并让方法按值取 `self`：`Client::builder("x").retries(1).build()`，返回 `Result<Client, BuildError>`，空 `host` 得到 `Err(EmptyHost)`；按值传递 `self` 让构建器用完即消耗，不可能拿着半成品继续改，所有权成为 API 设计的一部分 ([[pl-eng-apidesign-found-rust-ownership]], [[pl-eng-apidesign-unique-rust-names-carry-cost]])。
- `add_event` 输出 `['a', 'b'] ['a', 'b']`：默认值在 `def` 执行时只求值一次，所有调用共享同一个列表，两次打印的是同一个对象。修复是用 `None` 作哨兵，函数体里新建列表，输出变成 `['a'] ['b']`；`ruff` 的 `B006` 规则会直接报告「Do not use mutable data structures for argument defaults」，应当放进 CI ([[pl-eng-apidesign-pitfall-mutable-default]], [[pl-static-found-python]])。
- 暴露阶段：Rust 的所有权错误、Go 的类型不匹配在编译期；Java 的 `record` 与 Python 的关键字参数在构造期或调用期；Go 的 `go vet`、Rust 的 clippy、Python 的 ruff 与 mypy 在静态检查阶段补上语言本身不拦的问题 ([[pl-static-principle]], [[pl-static-table]])。
- 共同原则：必填项放在签名里，可选项用名字而不是位置，构造完成后对象不可变，非法状态在构造时就拒绝；不要让配置对象在调用方之间共享可变状态 ([[pl-eng-apidesign-pitfall-leaked-state]], [[pl-eng-apidesign-found-context]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
