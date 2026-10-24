---
id: pl-binding-binding-time-foundation-link-load
node: binding.binding-time
type: qa
step: 2
---
## Q
链接（linking）和加载（loading）是什么？Go、Rust 的静态链接，Java 的类加载，Python 的 `import` 各在哪个时刻把代码绑定进程序？

## A
**链接**：把程序引用的外部函数或库，解析成具体地址。**静态链接**在构建时把库的代码拷进可执行文件；**动态链接**把这一步推迟到程序启动（或首次调用）时由系统加载器完成。

- **Go**：默认把整个运行时和依赖拷进一个可执行文件。在 Linux 上通常完全不依赖外部共享库，拷到机器上直接运行；一个只打印 `hi` 的程序约 2.4 MB。macOS 上仍会链接系统自带的库。
- **Rust**：Rust 依赖（crate）默认静态链接进二进制，C 标准库默认动态链接。

**Java** 把绑定推迟得更晚：`.class` 文件由类加载器在**第一次真正用到该类时**才加载、链接、初始化。

```java
static class Lazy {
    static { System.out.println("Lazy initialized"); }
    static void hi() { System.out.println("hi"); }
}
// main prints "start", then if a flag is set calls Lazy.hi(), then "end"
// flag off: start, end        flag on: start, Lazy initialized, hi, end
```

没用到的类永远不加载，静态初始化块也永远不运行。

**Python** 的 `import` 是一条**可执行语句**：第一次导入时找到文件、编译、**运行整个模块体**，把结果缓存在 `sys.modules`；之后的 `import` 只取缓存。

```python
print("start")
import plugin          # plugin.py prints "plugin module body runs"
print("end", plugin.X)
# start / plugin module body runs / end 1
```

结论：越晚绑定，越能做到按需加载与插件化（Java 的 SPI、Python 的插件目录），代价是启动与首次调用有额外成本，也可能直到运行时才发现某个模块缺失。
