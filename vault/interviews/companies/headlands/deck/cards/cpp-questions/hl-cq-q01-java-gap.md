---
id: hl-cq-q01-java-gap
node: cpp-questions.a-why-fast
type: qa
step: 3
---
## Q
追问：C++ 是不是总比 Java 快？
Is C++ always faster than Java?

## A
**不是。** 稳态下的热循环可以很接近，因为即时编译器（JIT）会利用运行期的剖析信息来优化。

真正的差距在三处：
- **尾延迟**（tail latency）：GC 暂停和预热（warm-up）。
- **对象头与指针追逐**：Java 对象带头部，引用要多一次跳转。
- **布局控制**：C++ 可以决定数据怎么摆。
