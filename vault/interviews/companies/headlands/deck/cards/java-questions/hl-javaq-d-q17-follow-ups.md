---
id: hl-javaq-d-q17-follow-ups
node: java-questions.d-memory
type: qa
step: 27
---
## Q
追问：怎么为缓存效率设计订单簿（order book）的内存布局？JVM 会替你预取吗？
How would you lay out an order book for cache efficiency? Does the JVM prefetch for you?

## A
- **订单簿布局**：价格档位用数组或紧凑的 long 编码；同一档位的订单放在连续区域；**避免每个订单一个对象**。
- **预取**：硬件预取器对顺序访问有效；JVM 本身只有少量预取指令（分配时），别依赖。
