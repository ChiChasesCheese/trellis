---
id: pl-abstraction-encapsulation-foundation-go-package-scope
node: abstraction.encapsulation
type: qa
step: 3
---
## Q
Go 的封装单位是什么？首字母大小写规则和 `internal` 目录各管什么？

## A
Go 的封装单位是**包**（package，一个目录下的所有 `.go` 文件），而不是类型。规则只有一条：**标识符首字母大写即导出（包外可见），小写则只在本包内可见**，字段、方法、函数、类型都适用。

```go
type Counter struct{ n int }          // n 小写：包内可见
func (c *Counter) Inc() { c.n++ }     // Inc 大写：包外可见
```

关键含义：**同一个包里的任何代码都能直接读写 `n`**，没有「类私有」。设计者的理由是：一个包由同一个团队维护，他们应该能互相信任；真正的边界在包的 API。

`internal` 目录是第二层：路径里含 `internal` 的包，只能被它的**父目录树**内的代码导入。比如 `myapp/internal/db` 只能被 `myapp/...` 下的包使用，外部项目引入会被编译器拒绝。这样库作者可以把「同一个库的多个包之间共享、但不想对外承诺」的代码放进去。

反射也受这个规则约束：`reflect` 不能设置未导出字段，会 panic：`using value obtained using unexported field`。想绕过只能用 `unsafe`，而 `unsafe` 的存在本身就写在代码里，显眼，容易审查。

可见性写在名字上有一个附带好处：读代码时，看到 `x.Foo` 还是 `x.foo`，当场就知道它是不是包外 API，不必查定义。
