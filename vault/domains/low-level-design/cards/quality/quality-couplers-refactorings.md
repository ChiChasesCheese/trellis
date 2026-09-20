---
id: quality-couplers-refactorings
node: quality.smells
type: qa
---
## Q
诊断并修复这四种 coupler：feature envy、message chains、inappropriate intimacy、middle man。

## A
- **Feature envy** —— 一个方法用别人的数据比用自己的还多（`order.getCustomer().getAddress().format()` 这段逻辑却住在 `InvoicePrinter` 里）。修法：**move method**，搬到数据所在的地方；行为属于状态。
- **Message chains** —— `a.getB().getC().doIt()` 把调用方耦合到整条导航路径上（违反 Law of Demeter）。修法：**hide delegate** —— 让第一个对象自己去做（`a.doIt()`）。
- **Inappropriate intimacy** —— 两个类互相掏对方的内部。修法：move method/field 把这段交互集中到一个类里，或者把共享部分抽出来。
- **Middle man** —— 一个只做转发的类。修法：**remove middle man**，直接和目标对话。（注意：它正是 message chains 那副药*用过头*的产物 —— 这两个坏味道方向相反，所以要瞄准中间地带。）
