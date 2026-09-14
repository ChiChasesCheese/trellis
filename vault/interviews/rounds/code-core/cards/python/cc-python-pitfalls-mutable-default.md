---
id: cc-python-pitfalls-mutable-default
node: python.pitfalls
type: qa
---
## Q
`def add(item, bucket=[]):` passes your first test and returns other rows' data in the second. Explain, and give the fix in each place it appears.

## A
**The default is evaluated once, when the function is defined**, so every call that omits `bucket` shares one list. State leaks between calls — and between tests, in whatever order the runner picks.

```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
```

- Same for `{}`, `set()`, and a `Decimal` context object.
- In a `@dataclass`, `items: list = []` is a hard error at class creation; use `field(default_factory=list)` ([[cc-python-classes-default-factory]]).
- The tell: a function that returns more every time you call it, and a test that only fails when run second.

## Q zh
`def add(item, bucket=[]):` 在第一个测试里通过，在第二个测试里返回了别人的数据。解释原因，并给出它出现的每个地方的修法。

## A zh
**默认值只在函数定义时求值一次**，所以每个省略 `bucket` 的调用都共享同一个 list。状态在调用之间泄漏 —— 也在测试之间泄漏，顺序由 runner 决定。

```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
```

- `{}`、`set()`、以及一个 `Decimal` context 对象同理。
- 在 `@dataclass` 里，`items: list = []` 会在建类时直接报错；请用 `field(default_factory=list)`（[[cc-python-classes-default-factory]]）。
- 症状：一个每次调用返回得更多的函数，以及一个只在第二次运行时才失败的测试。
