---
id: pl-functional-recursion-tco-pitfall-untrusted-depth
node: functional.recursion-tco
type: qa
step: 11
---
## Q
递归解析不可信输入在生产里会出什么事？一个深度嵌套的输入怎么成为拒绝服务攻击？

## A
递归下降解析器、JSON / XML / 表达式求值，深度跟随输入的嵌套层数。攻击者只需发送 `[[[[...` 十万层，便能让毫无防备的递归实现耗尽栈。

```java
// 递归解析括号：每遇到一个 '[' 递归一层
static int parse(String s, int i) {
    return i < s.length() && s.charAt(i) == '[' ? parse(s, i + 1) : i;
}
// 输入 100000 个 '[' -> StackOverflowError
```

```python
json.loads('[' * 100000)
# RecursionError（Python 的 json 解析器会在深度上限处抛出异常）
```

几种语言的失败模式不同，危害也不同：

- **Python**：`RecursionError`，可捕获，服务继续运行，是最"友好"的失败。
- **Java**：`StackOverflowError`，可捕获，但线程可能处于不一致状态；线程池里的线程被一个恶意请求打死，其余请求受影响。
- **Rust / Go**：栈溢出直接中止整个进程，一个请求就能让服务宕机，无法 `recover`。这是最严重的失败模式，必须在解析层预防。

防御：
1. 解析器带**最大深度参数**，超过就返回错误（例如 Go 的 `encoding/json` 对嵌套深度有 10000 层的限制；Jackson 有 `StreamReadConstraints` 的最大嵌套深度，默认 1000）。
2. 对外部输入的递归，改用显式栈迭代。
3. 在请求入口限制输入大小，间接限制深度。
4. 模糊测试（fuzzing）专门喂深嵌套输入，这是最容易被遗漏的测试用例之一。
