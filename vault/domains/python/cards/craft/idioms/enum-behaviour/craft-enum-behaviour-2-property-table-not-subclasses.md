---
id: craft-enum-behaviour-2-property-table-not-subclasses
node: craft.idioms.enum-behaviour
type: qa
step: 2
---
## Q
**Enum 的行为 · 给枚举挂 @property，代替每个状态一个类**｜写法

自动售货机的每个状态要显示一句提示文案。有人想按状态模式（State pattern）给每个状态写一个子类，类里只有一个返回字符串的方法。什么时候这样做是过度设计？枚举上加 `@property` 查表为什么够用，又在哪一步该换回子类？

## A
**要点。** 状态模式把「不同状态下不同的行为」放进多态。若状态之间只有数据不同（一句文案、一个颜色、一个超时），数据放在枚举旁边的一张表里就够了，枚举成员是状态的名字，表是它的属性。只有当状态需要不同的代码逻辑，或者需要各自的实例状态时才值得用子类。

```python
from enum import Enum

class State(Enum):
    IDLE = "idle"
    COIN_INSERTED = "coin_inserted"
    DISPENSING = "dispensing"

    @property
    def prompt(self) -> str:             # 状态携带的数据：一张表
        return _PROMPTS[self]

_PROMPTS = {
    State.IDLE: "请投币或刷卡",
    State.COIN_INSERTED: "请选择商品，或按退币",
    State.DISPENSING: "正在出货",
}
assert set(_PROMPTS) == set(State)       # 加了状态却漏写文案，导入时就失败

for s in State:
    print(s.name, "->", s.prompt)
```

实际输出：

```
IDLE -> 请投币或刷卡
COIN_INSERTED -> 请选择商品，或按退币
DISPENSING -> 正在出货
```

**为什么。** 表放在类外是因为类体里还不能引用自己的成员；用 `@property` 包一层，调用处就写 `state.prompt`，不必知道背后是表。那条 `assert` 把「枚举和表同步」这条不变量放到了启动时检查。

**信号。** 当 `prompt` 旁边开始出现 `on_coin()`、`on_select()` 这类每个状态做不同事的方法，且每个方法里都是 `if self is ...`，就该升级成状态类，转移规则也一起移到类里。
