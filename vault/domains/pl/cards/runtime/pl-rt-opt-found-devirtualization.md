---
id: pl-rt-opt-found-devirtualization
node: runtime.optimizations
type: qa
step: 4
---
## Q
去虚化（devirtualization）是什么？Go 编译器和 Java 的 JIT 分别在什么条件下能把接口/虚方法调用变成直接调用并内联？

## A
接口调用或虚方法调用（Go 的 `Shape` 接口、Java 的 `S s; s.area()`）要在运行时通过方法表间接找到函数，目标不确定就无法内联，也就丢掉了后续一连串优化。**去虚化**就是编译器想办法**证明或赌**目标是确定的，把间接调用换成直接调用。

**AOT 的做法：静态证明**。变量声明为接口，但赋值处能看出具体类型时，Go 编译器直接改写：
```go
var sh Shape = Sq{3}
fmt.Println(sh.Area())
// go build -gcflags=-m=2:
// main.go:43:52: devirtualizing sh.Area to Sq
// can inline Sq.Area with cost 6
```
证明不了（比如接口来自函数参数）就只能保留间接调用。Go 1.21 起支持 PGO（用生产环境采集的 profile 再编译），能依据热点调用点的实际类型做有保护的去虚化。

**JIT 的做法：推测**。HotSpot 观察一个调用点：如果只出现过一种接收者类型（单态，monomorphic），就按这个类型内联，并在入口放一个类型检查；如果类加载分析（CHA）显示接口只有一个实现类，连检查都可以省。实测 `-XX:+PrintInlining`：
```
@ 37   I$Sq::area (10 bytes)   inline (hot)
```
接口调用被直接内联了。如果后来出现第二种类型，JIT 去优化重新编译。类型多了变成 megamorphic 就退化为查虚表。

**Rust**：泛型 `T: Shape` 在单态化时就是静态派发；`&dyn Shape` 是真正的动态派发，LLVM 只有在能看到具体类型时才能去虚化。

**Python**：每次调用都做属性查找，没有去虚化。

要点：**多态不是免费的，但“有没有成本”取决于编译器能否看到具体类型**。热路径里的接口调用，如果实际总是同一种类型，AOT 语言要靠代码结构让它可见（或 PGO），JIT 语言靠运行时观察就会自动做到。
