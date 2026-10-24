---
id: pl-foundations-execution-models-best-practice
node: foundations.execution-models
type: qa
step: 5
---
## Q
工程上应该怎样根据执行模型选语言和做性能优化？CLI、长期运行的服务、数据处理各自的经验规则是什么？

## A
先问程序的生命周期有多长，再决定要把成本放在构建期还是运行期。

- 短命进程（命令行工具、Serverless 函数、每次请求新起容器）：选提前编译的 Go 或 Rust。进程可能只活几十毫秒，JVM 的预热还没完成就结束了。
- 长期运行的服务：JVM 的 JIT 在热路径上可以追上甚至超过提前编译的代码，不要因为启动慢就否定它；需要时用 CDS、GraalVM 原生镜像缩短启动。
- Python：不要在 Python 里写热点循环，把它下放到 C 扩展。同样的 `s += i % 7` 循环一千万次，纯 Python 约 240 ms，用 NumPy 向量化约 12 ms（一次测量，约 20 倍）：

```python
for i in range(n): s += i % 7        # 约 242 ms
int((np.arange(n) % 7).sum())        # 约 12 ms
```

- 测性能前先预热：对 JVM 做基准测试要用 JMH 这类会先预热再计时的框架，只跑一次 `main` 测到的多半是解释器加编译线程。
- 先测量再迁移：别因为「Python 慢」整体重写，多数时间花在少数热点上，把这些热点换成 NumPy、Rust 扩展或 Cython，往往比换语言便宜得多。

破例的时候：对延迟尖刺敏感的场景（交易、实时音视频），JIT 的编译和去优化本身就是抖动来源，此时选提前编译，或者让 JVM 在上线前预热。
