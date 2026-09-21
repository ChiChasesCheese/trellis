---
id: relative-import-dot-syntax
node: runtime.import-system
type: qa
source: python-docs
---
## Q
包内相对导入（relative import）里，一个点和两个点分别代表什么？为什么不能写成 `import .moduleY` 这种形式？

## A
一个前导点表示「从当前包开始」的相对导入，每多一个点就再往上跳一级父包。相对导入只能用 `from . import X` / `from .moduleY import spam` 这种 `from` 形式，不能写成 `import .moduleY`——因为 `import XXX.YYY.ZZZ` 要求 `XXX.YYY.ZZZ` 本身是一个合法的可求值表达式，而 `.moduleY` 不是合法表达式。
