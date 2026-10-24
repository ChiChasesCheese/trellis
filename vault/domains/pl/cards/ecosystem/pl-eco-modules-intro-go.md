---
id: pl-eco-modules-intro-go
node: ecosystem.modules
type: qa
step: 2
---
## Q
Go 的 package 与 module 分别是什么？导出规则、`internal` 目录和禁止循环依赖怎样工作？

## A
**package**：一个目录下所有 `.go` 文件属于同一个 package，它是 Go 的命名空间，也是编译单位。导入时用路径：`import "example.com/app/pkg/util"`，使用时用包名 `util.Hello()`。

**module**：一棵目录树，根目录有 `go.mod` 文件，声明模块路径（如 `module example.com/app`）和依赖。module 是版本化和发布的单位；一个 module 内含许多 package。

**导出规则极简**：标识符首字母大写就是导出（对其他 package 可见），小写就是包内私有。没有 `public`/`private` 关键字。尝试使用私有名字：

```go
fmt.Println(util.helper())
// ./main.go:3:59: undefined: util.helper
```

**`internal` 目录**：路径中含 `internal` 的 package，只有 `internal` 的父目录树里的代码能导入。别的 module 去导入会被编译器拒绝，真实报错：`use of internal package example.com/app/internal/secret not allowed`。库作者用它划出「可以随便改」的内部区域。

**禁止循环依赖**：package A 导入 B，B 就不能导入 A，编译器直接拒绝：`import cycle not allowed`。因此 package 依赖图一定是有向无环图。

**要记住的一点**：Go 用很少的概念（目录即包，大小写即可见性，go.mod 即版本边界）把命名、可见性、编译和发布四个问题压成了几条规则，而且全部由编译器强制。
