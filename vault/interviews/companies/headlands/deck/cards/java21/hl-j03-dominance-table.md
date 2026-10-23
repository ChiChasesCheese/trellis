---
id: hl-j03-dominance-table
node: java21.j03-pattern-switch
type: qa
step: 7
---
## Q
判断这四种 `switch` 模式写法哪些合法：(1) `case CharSequence cs` 然后 `case String s`；(2) `case String s when s.length() > 3` 然后 `case String s`；(3) `case String s` 然后 `case String s when ...`；(4) `default` 写在模式分支前面。

## A
- (1) **编译错误**：`CharSequence` 无守卫，支配后面的 `String`。
- (2) **合法**：带守卫的分支不支配，因为守卫可能为假。
- (3) **编译错误**：后者被前面无守卫的 `String s` 支配。
- (4) **编译错误**：`default` 之后的模式分支被支配。

另外，`case Object x`（无条件模式）和 `default` 同时出现，也是编译错误：`switch has both an unconditional pattern and a default label`。
