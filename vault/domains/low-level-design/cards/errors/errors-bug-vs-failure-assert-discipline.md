---
id: errors-bug-vs-failure-assert-discipline
node: errors.bug-vs-failure
type: qa
step: 3
---
## Q
`assert` 在服务代码里该用来做什么？把 `assert items.pop() == 2` 这样的语句放进生产代码，会有什么后果？

## A
**`assert` 只断言“不可能”，表达式不带副作用**

- **用途**：标记程序员的假设，比如“进到这里时列表一定非空”。触发就是缺陷，让它崩出来；
- **不用来校验外部输入**：外部输入出错是预期失败，要走 `raise` 和合同；
- **`python -O` 会把整条 `assert` 语句删掉**：连里面的表达式一起不执行；
- **副作用放进 `assert` 就是埋雷**：开发时 `pop()` 执行了，优化模式下没执行，同一份代码在两种模式下状态不同；
- **规矩**：先把结果取出来存进变量，再 `assert` 这个变量。

```python
import sys

items = [1, 2]
assert items.pop() == 2              # 副作用藏在 assert 里：坏习惯
print(sys.flags.optimize, items)     # 普通运行：0 [1]；python -O 运行：1 [1, 2]

last = items.pop()                   # 好习惯：先做事
assert last == 1, "stack order broke"
```

<details class="pt"><summary>延伸</summary>

测试代码里的 `assert` 由 pytest 改写，不受 `-O` 影响；这条规矩说的是库和服务里的 `assert`。

</details>

**知识点：**缺陷与预期失败（Bugs vs Failures）
