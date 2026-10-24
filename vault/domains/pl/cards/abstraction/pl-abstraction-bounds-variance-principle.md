---
id: pl-abstraction-bounds-variance-principle
node: abstraction.bounds-variance
type: qa
step: 1
---
## Q
泛型里的「约束」（bound）和「型变」（variance）分别回答什么问题？为什么两者都是为了让泛型既灵活又安全？

## A
**约束**回答：类型参数 `T` 必须具备什么能力？没有约束，泛型函数体只能存取 `T`；加上「`T` 能比较」「`T` 是某个类的子类」后，函数体才能调用对应操作。约束是泛型函数与调用者之间的契约。

**型变**回答：如果 `Cat` 是 `Animal` 的子类型，那么 `List<Cat>` 是不是 `List<Animal>` 的子类型？直觉上是，但直觉有时是错的（见下一张卡）。语言有三种答案：

- **协变**（covariant）：保持方向，`List<Cat>` 可用在要 `List<Animal>` 的地方。
- **逆变**（contravariant）：方向反过来，`Handler<Animal>` 可用在要 `Handler<Cat>` 的地方。
- **不变**（invariant）：互不相干，`List<Cat>` 与 `List<Animal>` 没有关系。

答案取决于这个类型参数怎么被使用：只**读出**，协变是安全的；只**写入**，逆变是安全的；既读又写，只能不变。

设计空间沿着**灵活性与健全性**取舍：型变越宽松，API 越容易复用，但越可能在运行期出现类型错误；越严格，越安全，但用户需要写更多适配。语言又分两派：**使用处型变**（use-site，Java 的 `? extends`，每次使用时声明）与**声明处型变**（declaration-site，C#、Kotlin、Scala，在类定义时一次声明）。
