---
id: principles-speculative-generality
node: principles.simplicity
type: qa
---
## Q
Name three concrete signs of the *speculative generality* smell, and the refactor for each.

## A
- Interface/abstract class with exactly one implementation and no test-seam need → **collapse hierarchy / inline**.
- Parameters or type parameters added "for flexibility" but never varied → **remove parameter**.
- Hooks and fields exercised only by tests, never by production code → **delete**.

It's YAGNI applied retroactively: generality that never earned its keep is a cost with no buyer.

## Q zh
什么是投机泛化，为什么它是问题？

## A zh
投机泛化是添加一个你认为将来可能需要的功能，但现在不需要。看起来像：
- 一个接口有操作，但只有一个实现者
- 一个参数存在但从未被使用
- 抽象层数比实际需要的多
- "我们可能想要这个"代码在 util 类中

问题：
- 增加复杂性，没有立即的益处
- 你猜测错了；需要的功能与你抽象的不一样
- 难以测试和维护过度工程的代码

解决方案：YAGNI（你不需要它）。等到有第二个实现者或实际的需求才进行抽象。
