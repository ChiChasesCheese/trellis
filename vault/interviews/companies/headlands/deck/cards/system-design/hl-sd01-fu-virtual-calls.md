---
id: hl-sd01-fu-virtual-calls
node: system-design.sd01-unused-code
type: qa
step: 30
---
## Q
追问：虚调用和接口怎么避免把活的实现类判成死的？为什么不用更精确的指向分析？

## A
思路：想 CHA / RTA 的精度-成本曲线，以及「误判活为死」的方向要保守。
- CHA：接口所有实现都可能被调用（过度保守）；
- RTA：只考虑可达的 `new X()` 的类，不动点迭代，仍近线性；
- points-to：精度更高，但规模和实现复杂度不划算；
- 偏保守：无法确定的虚调用目标一律保活；lambda / 方法引用靠 `invokedynamic` 的引导参数恢复。

可以说：「我选 RTA：近线性、比 CHA 精度好得多；精度不够的地方宁可漏报。」
