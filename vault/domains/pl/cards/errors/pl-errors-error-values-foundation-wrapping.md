---
id: pl-errors-error-values-foundation-wrapping
node: errors.error-values
type: qa
step: 3
---
## Q
Go 的错误包装（`%w`）、`errors.Is` 和 `errors.As` 是怎么工作的？

## A
一个错误从深处返回，每一层都想加上“我在做什么”，同时又不能丢掉原始错误，让上层还能判断它是什么。办法是**包装**（wrap）：

```go
return fmt.Errorf("find %d: %w", id, ErrNotFound)
```

`%w` 把 `ErrNotFound` 嵌进新错误里，新错误实现了 `Unwrap() error`，返回被包装的那个。逐层包装后形成一条**错误链**，打印出来就是各层上下文的拼接：

```console
run: parse config: open /nope: no such file or directory
```

判断链里有什么：
- `errors.Is(err, target)`：沿着链逐层 `Unwrap`，看有没有哪一层等于 `target`。包装之后 `err == ErrNotFound` 就不成立了，必须用 `Is`：`errors.Is(err, fs.ErrNotExist)`。
- `errors.As(err, &x)`：沿着链找到第一个类型匹配 `x` 的错误并取出它，用来读自定义类型里的字段。
- `errors.Join(a, b)`（Go 1.20）：把多个错误合成一个。

`%w` 让调用者能 `Is` 到底层错误，因此底层错误成了你的 API 的一部分；如果不想暴露，改用 `%v` 只保留文本。成本：`fmt.Errorf` 要格式化字符串并分配，本机实测约 37 ns 每次。

要记住的一个事实：包装保留因果链，`Is`/`As` 让你按种类而不是按字符串判断。
