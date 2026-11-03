---
id: craft-protocol-callable-abc-4-operators-on-base
node: craft.idioms.protocol-callable-abc
type: qa
step: 4
---
## Q
**策略接口 · 为什么 find 的过滤器非得是 ABC**｜写法

Linux `find` 的过滤器要能写成 `(ext(".py") | ext(".md")) & ~ext("_test.py")`。过滤器只有一个方法 `matches`，按「单方法用 Callable / Protocol」的经验好像不需要 ABC，`find` 为什么还是用了 ABC？

## A
**要点。** 判据是：接口上是否有**不属于任何实现者、而属于接口本身的行为**。`&`、`|`、`~` 对所有过滤器含义相同（与、或、非），应该写一次，放在基类上，所有子类自动得到。Callable 是函数，没有地方挂运算符；Protocol 的实现者不继承它，也拿不到这些方法。

```python
class Filter(ABC):
    @abstractmethod
    def matches(self, name: str) -> bool: ...
    # 组合运算符放在基类上：所有子类免费得到 & | ~
    def __and__(self, o: "Filter") -> "Filter": return And(self, o)
    def __or__(self, o: "Filter") -> "Filter": return Or(self, o)
    def __invert__(self) -> "Filter": return Not(self)

@dataclass(frozen=True)
class Ext(Filter):
    ext: str
    def matches(self, name): return name.endswith(self.ext)

@dataclass(frozen=True)
class And(Filter):
    l: Filter; r: Filter
    def matches(self, name): return self.l.matches(name) and self.r.matches(name)

@dataclass(frozen=True)
class Or(Filter):
    l: Filter; r: Filter
    def matches(self, name): return self.l.matches(name) or self.r.matches(name)

@dataclass(frozen=True)
class Not(Filter):
    f: Filter
    def matches(self, name): return not self.f.matches(name)

f = (Ext(".py") | Ext(".md")) & ~Ext("_test.py")
for n in ["a.py", "a_test.py", "r.md", "x.txt"]:
    print(n, f.matches(n))

class P(Protocol):
    def matches(self, name: str) -> bool: ...
class Duck:                                # 结构上满足 P，但它没有 & | ~
    def matches(self, name): return True
try:
    Duck() & Duck()
except TypeError as e:
    print("Protocol 实现者拿不到基类里的运算符:", e)
```

实际输出：

```
a.py True
a_test.py False
r.md True
x.txt False
Protocol 实现者拿不到基类里的运算符: unsupported operand type(s) for &: 'Duck' and 'Duck'
```

**为什么。** 运算符返回新的组合对象（`And`、`Or`、`Not`），原对象不变，所以过滤器是不可变的，可以复用、跨线程共享。

**代价。** 继承让所有过滤器绑定在同一个基类上，第三方对象想当过滤器用就得套一层适配。组合层（And / Or / Not）本身也是 Filter，这是 Composite 与 Specification 模式的常见形态。

**信号。** 「接口上要放默认实现、运算符重载或模板流程」，就是 ABC 的信号；只有一个方法的话，先想想是不是一个函数就够了。
