---
id: cc-python-classes-repr-for-failures
node: python.classes
type: qa
---
## Q
An assertion fails and the message reads `assert <__main__.Row object at 0x7f2a...> == <__main__.Row object at 0x7f2b...>`. Fix the class so the next failure is legible.

## A
**Give the class a `__repr__` that prints the fields you would have asked about.**

```python
def __repr__(self):
    return f"Row(day={self.day}, user={self.user!r}, amount={self.amount})"
```

- `@dataclass` generates one for free — reason enough to prefer it over a hand-written class in a timed round.
- Use `!r` on strings so whitespace and empty values are visible: `'  a'` and `'a'` look identical without it, and that is exactly the parsing bug you are hunting.
- Write `__repr__`, not `__str__`, if you only write one: containers render their elements with `repr`, so a list of records prints usefully.

## Q zh
一个断言失败，信息是 `assert <__main__.Row object at 0x7f2a...> == <__main__.Row object at 0x7f2b...>`。改造这个类，让下一次失败可读。

## A zh
**给类写一个 `__repr__`，打印出你本来会去问的那些字段。**

```python
def __repr__(self):
    return f"Row(day={self.day}, user={self.user!r}, amount={self.amount})"
```

- `@dataclass` 免费生成一个 —— 这本身就足以让你在限时轮次里优先用它而非手写类。
- 字符串上用 `!r`，让空白和空值可见：不加的话 `'  a'` 和 `'a'` 长得一模一样，而那正是你在追的解析 bug。
- 只写一个的话就写 `__repr__` 而不是 `__str__`：容器用 `repr` 渲染元素，所以一个记录列表能打印得有用。
