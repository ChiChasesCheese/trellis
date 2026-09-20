---
id: quality-bloaters-refactorings
node: quality.smells
type: qa
---
## Q
什么是代码膨胀（bloaters），如何识别和重构它们？

## A
代码膨胀是东西变得太大、难以理解的地方。

**大方法/类**：
- 做太多事情
- 难以测试和理解
- 重构：Extract Method、提取类、移除重复

**长参数列表**：
- `doSomething(a, b, c, d, e, f, g)`
- 难以调用和维护
- 重构：Parameter Object、使用 Builder、引入配置对象

**数据团**：
- 总是在一起传递的参数（如 x, y, z 坐标）
- 重构：创建一个 Coordinates 类

**switch 语句**：
- 在许多地方重复相同的 switch
- 重构：多态性、策略模式
