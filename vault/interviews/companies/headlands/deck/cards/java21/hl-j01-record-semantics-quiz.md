---
id: hl-j01-record-semantics-quiz
node: java21.j01-record
type: qa
step: 30
---
## Q
面试追问：Java 的 `record` 比起手写值类，保证了什么、没保证什么？各一句话。

## A
**保证**：
- 字段永远是 `private final`；
- `equals` / `hashCode` / `toString` 自动按**全部组件**生成且配套；
- 类 `final`，不能被继承；
- 紧凑构造器可以让非法值造不出来。

**没保证**：
- **深不可变**：组件是可变对象（数组、`ArrayList`、`Date`）时内容仍可改；
- 访问器被重写后与字段的一致性；
- 敏感字段不被 `toString` 打印。
