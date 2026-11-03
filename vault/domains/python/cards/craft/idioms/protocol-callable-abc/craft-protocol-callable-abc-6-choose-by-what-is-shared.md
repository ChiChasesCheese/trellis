---
id: craft-protocol-callable-abc-6-choose-by-what-is-shared
node: craft.idioms.protocol-callable-abc
type: qa
step: 6
---
## Q
**策略接口 · 按「到底共享了什么」在三种形式里选**｜写法

在这几个系统里，航班的超售 / 退款是 Callable 别名，文件监听器的 `FileSystem` 与计费规则是 Protocol，分账与限流是 ABC，find 的过滤器也是 ABC。它们的选择依据是同一条吗？

## A
**要点。** 同一条：看实现之间**共享的是什么**。什么都不共享、只有一个行为，用函数；只共享一个「长什么样」的约定，用 Protocol；共享代码（流程、默认实现、运算符），用 ABC。变的只是共享物，机制不变。

```python
# airline：只有一个行为 -> Callable 别名 + 普通函数
RefundPolicy = Callable[["Booking", datetime], int]

# amz-file-watcher：只共享一个约定 -> Protocol，测试换内存假实现
class FileSystem(Protocol):
    def scan(self, root: str, recursive: bool) -> Snapshot: ...

# splitwise：共享取整 + 最大余数算法 -> ABC 里放静态方法 _proportional
class Split(ABC):
    @abstractmethod
    def compute(self, amount: int, participants: Sequence[User]) -> dict[User, int]: ...
    @staticmethod
    def _proportional(...): ...        # 均分 / 百分比 / 份额共用

# amz-linux-find：接口上要放 & | ~ -> ABC
class Filter(ABC):
    def __and__(self, other): return AndFilter(self, other)
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

选错的代价各不相同：给单方法写 ABC 只是仪式；给要共享骨架的写 Protocol，会把同一段取整算法复制到每个实现里，然后走样；给要换假实现的外部依赖写 ABC，测试里就得先写一个子类。放大到系统里，通知渠道与存储后端的插件接口（SPI）也是这样：对外公开的是最小的稳定接口，内部才共享代码。

**见于。** airline、amz-file-watcher、billing-tax-engine、splitwise、rate-limiter、amz-linux-find。

**信号。** 要让某个行为可替换时，先问：它有几个方法？实现之间有没有想共享的代码？答案是「一个、没有」就写函数。
