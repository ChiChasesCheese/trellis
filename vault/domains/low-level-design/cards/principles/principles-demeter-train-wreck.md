---
id: principles-demeter-train-wreck
node: principles.coupling
type: qa
---
## Q
什么是 Demeter 法则的违反？为什么 train wreck 是个名字？

## A
Demeter 法则说你只应该和你的 "朋友" 交流——方法只应该调用：
- 它自己的类中的方法
- 参数对象的方法
- 本地创建或获取的对象的方法

Train wreck（火车碰撞）是因为每个点像一节火车车厢：`a.getB().getC().getD().doIt()`。每个点都是一个对象，链在一起像是无控制地滑动。这暴露了中间对象的内部结构。
