---
id: pl-foundations-execution-models-found-go-toolchain
node: foundations.execution-models
type: qa
step: 4
---
## Q
`go build` 产出的是什么？为什么 Go 程序只有一个文件就能部署，还能很方便地交叉编译？

## A
`go build` 把你的包以及所有依赖的包编译成机器码，并且静态链接（statically link）成一个独立的可执行文件。文件里不仅有你的代码，还有 Go 运行时（runtime）：垃圾回收器、goroutine 调度器、内存分配器、字符串和 map 的实现。操作系统只要能加载这个文件就能运行，不需要目标机器安装 Go 或任何共享库。

代价是体积：一个只打印一行字的程序，二进制约 1.8 MB，因为运行时也在里面。

交叉编译只需要设置两个环境变量，因为 Go 工具链自带所有目标平台的后端，不依赖外部 C 工具链：

```console
$ GOOS=linux GOARCH=amd64 go build -o hello_linux h.go
$ file hello_linux
hello_linux: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked
```

在 macOS（ARM64）上实际生成了一个 x86-64 Linux 的静态可执行文件，约 1.9 MB。拷到任何 Linux 服务器或最小化的容器镜像（甚至空镜像）里就能运行。这是 Go 在云原生领域流行的原因之一：部署产物就是单个文件。
