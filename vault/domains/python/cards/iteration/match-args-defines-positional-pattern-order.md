---
id: match-args-defines-positional-pattern-order
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
写 `case Click((x, y)):` 这种不带属性名的「位置模式」匹配对象属性时，Python 怎么知道 `(x, y)` 对应的是对象的哪个属性？

## A
靠类上的 `__match_args__` 属性，它是一个字符串元组，规定了位置模式里各个位置分别对应哪个属性名，比如 `__match_args__ = ('position', 'button')` 就让 `Click((x, y))` 里的第一个位置模式去匹配 `.position` 属性。用 `@dataclass` 定义的类会按字段声明顺序自动生成 `__match_args__`，所以 dataclass 通常不需要手写就能直接支持位置模式；普通类没有天然的属性顺序，需要显式声明 `__match_args__` 才能用位置模式，否则只能用具名的 `case Click(position=(x, y)):`。
