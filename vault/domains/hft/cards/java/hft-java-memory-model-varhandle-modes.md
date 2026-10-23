---
id: hft-java-memory-model-varhandle-modes
node: java.memory-model
type: qa
step: 3
---
## Q
VarHandle 的 plain、opaque、acquire/release、volatile 四种访问模式有什么区别？

## A
VarHandle 把“访问一个变量”的力度做成可选：

| 模式 | 保证 |
|---|---|
| plain | 没有额外保证，等同普通字段 |
| opaque | 单个变量上的读写不被撕裂、不被编译器缓存或消除，最终会看到；不保证与其他变量的顺序 |
| acquire / release | `setRelease` 之前的读写不会重排到它之后；`getAcquire` 之后的读写不会重排到它之前；配对使用即“发布—订阅” |
| volatile | 完整的顺序一致性，最强也最贵 |

原则是：用够用的最弱模式。线程内自己的数据用 plain，自旋标志用 opaque，单向发布数据用 acquire/release，只有需要最强保证时才用 volatile。
