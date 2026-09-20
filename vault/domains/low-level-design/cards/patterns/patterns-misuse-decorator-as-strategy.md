---
id: patterns-misuse-decorator-as-strategy
node: patterns.selection
type: qa
step: 5
---
## Q
用 Decorator 给日志加时间戳是合理用法，为什么用同一套 Decorator 嵌套去实现"这三种互斥算法选一种执行"就不对？

## A
Decorator 的每一层是**叠加**——原始行为加上一点点额外的事，多层可以任意组合、顺序基本独立。"三选一执行某种算法"不是叠加关系，而是**互斥选择**：三种实现互不兼容，同时只能生效一个。硬套 Decorator 会变成用嵌套层级去模拟分支选择，读代码的人要顺着一层层包装去猜到底激活了哪个，而 Strategy 直接把"选哪个"变成一次赋值，一眼看清楚当前用的是哪个算法。
