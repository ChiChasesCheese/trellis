---
id: craft-make-unmake-undo-log-4-edit-is-its-own-inverse
node: craft.patterns.make-unmake-undo-log
type: qa
step: 4
---
## Q
**做/撤销与撤销日志 · 文本编辑器：插入、删除、替换为什么只要一种 Edit**｜模式

编辑器要支持撤销和重做。常见的命令模式（command pattern）会写 `InsertCommand`、`DeleteCommand`、`ReplaceCommand` 三个类，每个带 `execute` 和 `undo`。有没有更小的设计？

## A
**要点。** 一次修改的完整描述是「在 `position` 处把 `removed` 换成 `inserted`」。插入是 `removed == ""`，删除是 `inserted == ""`，替换两者都非空：只需要一种形状。逆操作就是把这两个字段对调，没有计算，也没有子类分支。应用时先核对当前文本在该处确实等于 `removed`，对不上就当场失败，而不是静默写坏。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Edit:
    position: int; removed: str; inserted: str
    def invert(self): return Edit(self.position, self.inserted, self.removed)   # 字段对调

class Doc:
    def __init__(self, text=""): self.text, self.undo_stack, self.redo_stack = text, [], []
    def apply(self, e):
        cur = self.text[e.position:e.position + len(e.removed)]
        if cur != e.removed:                           # 重放到已经变了的文本上：当场失败
            raise ValueError(f"文本在 {e.position} 处是 {cur!r}，不是 {e.removed!r}")
        self.text = self.text[:e.position] + e.inserted + self.text[e.position + len(e.removed):]
    def do(self, e): self.apply(e); self.undo_stack.append(e); self.redo_stack.clear()
    def undo(self):
        e = self.undo_stack[-1]; self.apply(e.invert())     # 先应用成功，再出栈：失败时历史原样
        self.undo_stack.pop(); self.redo_stack.append(e)
    def redo(self): e = self.redo_stack.pop(); self.apply(e); self.undo_stack.append(e)

d = Doc("hello world")
d.do(Edit(5, "", ","))                  # 插入：removed 为空
d.do(Edit(7, "world", "there"))         # 替换：两者都非空
d.do(Edit(0, "h", ""))                  # 删除：inserted 为空
print(repr(d.text))
d.undo(); d.undo(); print(repr(d.text))
d.redo(); print(repr(d.text))
d.text = "XXXX"                          # 有人绕过历史直接改了文本
try: d.undo()
except ValueError as e: print("拒绝:", e)
```

```
'ello, there'
'hello, world'
'hello, there'
拒绝: 文本在 7 处是 ''，不是 'there'
```

（三个编辑后撤销两次得到 `'hello, world'`，重做一次得到 `'hello, there'`；最后一行是有人绕过历史直接改了文本，撤销被拒绝。）

**为什么。** 三个类的重复在于每个类都要同时知道「怎么做」和「怎么撤销」，两份逻辑必须一致。一种形状 + 对调字段，撤销自动正确，而且重做 = 再应用一次同一个 `Edit`。核对 `removed` 把「重放到已经变了的文本上」这类静默错误变成立即失败。

**代价。** `removed` 要存被删的文本，删一大段就占一大段内存；超长文档要改成只存位置和哈希，或者用 rope 之类的结构共享。光标位置不便从逆操作反推，所以和 Edit 一起存（`cursor_before` / `cursor_after`）；它太小，整体快照比反推更省事。

**什么时候要多种命令。** 操作之间有不同的副作用（保存文件、网络请求），无法用「前后状态对调」表示时。
