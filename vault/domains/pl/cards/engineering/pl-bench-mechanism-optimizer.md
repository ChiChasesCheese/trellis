---
id: pl-bench-mechanism-optimizer
node: engineering.benchmarking
type: qa
step: 5
---
## Q
为什么微基准里「丢掉返回值」或「传入常量」会让结果小得离谱？用 JMH 的几种写法对比说明。

## A
优化器有三招会悄悄改变你测的东西：
- **死代码消除**（dead-code elimination）：结果没人用且无副作用的计算直接删掉；
- **常量折叠**（constant folding）：输入是编译期常量，整个计算在编译时就算完；
- **循环不变量外提**（loop-invariant code motion）：输入在循环里不变，计算被提到循环外，只做一次。

JMH 实测，同一个 64 位整数混合函数 `mix`，四种写法（Apple 芯片，一次测量）：

```java
@Benchmark public void dropped()  { mix(seed); }       // 0.245 ns/op
@Benchmark public long constant() { return mix(12345L); } // 0.235 ns/op
@Benchmark public long returned() { return mix(seed); }   // 0.314 ns/op
@Benchmark public long rolling()  { return mix(seed++); } // 0.688 ns/op
```

- `dropped`：结果被丢弃，计算被删除；
- `constant`：字面量输入，编译期折叠；
- `returned`：`seed` 在循环里没变，`mix(seed)` 被提到循环外；
- `rolling`：每次输入都变，每次迭代都真正计算。

前三种都接近空循环的开销（约 0.2 到 0.3 ns），只有最后一种测到了函数本身，比前三种慢一倍以上。三种看起来很自然的写法，都低估了成本。

**识别信号**：单次操作不到 1 ns、而且往函数体里加一倍工作量数字也不变，基本就是被删掉了。**检验方法**：故意让被测函数多做一倍的工作，数字应当随之增加；不增加，说明测的不是它。
