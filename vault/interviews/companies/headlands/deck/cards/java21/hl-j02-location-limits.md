---
id: hl-j02-location-limits
node: java21.j02-sealed
type: qa
step: 7
---
## Q
`sealed` 类型对子类的位置和形式有哪四条限制？

## A
1. 子类与父类须在**同一模块**；没用模块系统就是**同一个包**，这样"封印"才封得住。
2. 许可的子类必须**直接**继承父类。
3. **匿名类、局部类、lambda** 都不能继承 / 实现 `sealed` 类型，报 `anonymous classes must not extend sealed classes`。
4. `sealed` 类型**至少要有一个**子类。
