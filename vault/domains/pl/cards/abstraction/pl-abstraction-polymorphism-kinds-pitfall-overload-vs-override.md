---
id: pl-abstraction-polymorphism-kinds-pitfall-overload-vs-override
node: abstraction.polymorphism-kinds
type: qa
step: 8
---
## Q
Java 重载（overload）按静态类型选择，Python 根本没有重载：这两个事实在生产中会造成什么错误？

## A
**Java**：开发者以为重载会「自动按运行期类型分派」，实际按声明类型选。

```java
void handle(Object e) { /* generic path */ }
void handle(String e) { /* special path */ }
Object msg = queue.take();   // 运行期是 String
handle(msg);                 // 实际调用 handle(Object)，特殊路径永远不走
```

没有报错，没有警告，只是行为不对。同类坑：集合 `remove(int index)` 与 `remove(Object o)` 在 `List<Integer>` 上选哪个，要看你传的是 `int` 还是 `Integer`。

**Python**：同名函数后一个定义会静默覆盖前一个。

```python
def show(x: object): print("object")
def show(x: str): print("str")
show(1)    # 输出 str：第一个定义已经消失，类型注解不会分派
```

类型注解不参与运行期选择，`show(1)` 照样进入第二个函数，直到函数体里碰到 `int` 才炸。

修法：Java 里让「靠类型选择」的逻辑走覆写（虚方法）或访问者，而不是重载；Python 里要按类型分派就显式用 `functools.singledispatch`（`f(1)` 得到 `int`，`f(1.5)` 回退到 `object`），或者 `match` 语句。
