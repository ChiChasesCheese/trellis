---
id: craft-exhaustive-match-assert-never-3-if-chain-and-test-net
node: craft.idioms.exhaustive-match-assert-never
type: qa
step: 3
---
## Q
**穷尽性检查 · `if / elif` 链怎么做同样的检查，类型检查器没跑到的地方怎么兜底**｜写法

团队里有人更喜欢 `if / elif`，也有些分支写在没有类型检查的脚本里。穷尽性保证还能做到吗？Python 的 `match` 和 Rust、OCaml 的 `match` 差在哪一半？

## A
**要点。** Rust、OCaml 的编译器自带穷尽性检查，漏分支直接编译不过。Python 的 `match` 没有：这一半要靠类型检查器加 `assert_never` 补上。`if / elif` 链可以写出等价的保证：每个值都用 `is` 或 `isinstance` 列出，最后的 `else` 里调用 `assert_never`，类型检查器会做同样的窄化。类型检查没覆盖到的代码，用一个**遍历所有枚举成员**的测试兜底：新增成员后，测试在对应的成员上立刻失败。

```python
class Status(Enum):
    ACTIVE = auto(); CONFIRMED = auto(); CANCELLED = auto(); EXPIRED = auto()

# if/elif 链也能写出同样的保证: 最后的 else 里调用 assert_never
def describe(s: Status) -> str:
    if s is Status.ACTIVE:
        return "进行中"
    elif s is Status.CONFIRMED:
        return "已确认"
    elif s is Status.CANCELLED:
        return "已取消"
    elif s is Status.EXPIRED:
        return "已过期"
    else:
        assert_never(s)

# 类型检查没有跑到的地方(例如动态传入的值)，用一个遍历全部枚举成员的测试兜底
def test_every_status_is_handled() -> None:
    for s in Status:
        assert isinstance(describe(s), str)

test_every_status_is_handled()
print("全部", len(Status), "个状态都有分支")
```

实际输出：

```
全部 4 个状态都有分支
```

**为什么。** 测试遍历 `Status` 而不是手写几个值，所以新增成员不需要改测试就会被覆盖，这是它能兜底的原因。同样的方法适合用在「枚举成员到某个表的映射」上：断言 `set(table) == set(Status)`。

**易错。** 新增枚举成员时，会静默漏掉处理的不只是 `match`：字典映射、序列化、数据库列、展示文案，每个出现枚举的地方都是一处。能被类型检查器覆盖的用 `assert_never`，其余用遍历枚举的测试。
