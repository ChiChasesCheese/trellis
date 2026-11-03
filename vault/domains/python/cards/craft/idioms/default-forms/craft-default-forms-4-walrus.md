---
id: craft-default-forms-4-walrus
node: craft.idioms.default-forms
type: qa
step: 4
---
## Q
**省掉标志变量 · 海象运算符 `:=` 解决了什么重复，作用域有什么坑**｜写法

缓存清理要循环弹出所有到期的 key：`while (key := pop_due(now)) is not None`。账本查重也写成 `if (seq := d.get(id)) is not None`。不用海象会怎样？它在推导式里的作用域规则是什么？

## A
**要点。** 海象运算符（walrus operator）`:=` 是在表达式里赋值。典型场景是 loop-and-a-half：先取一个值，判断，再处理，再取下一个。没有海象，要么在循环前后各调一次 `pop_due()`（两处调用必须保持一致，改了一处容易忘另一处），要么写 `while True` 加 `break`。有了它，取值与判断在同一个位置。`if (x := d.get(k)) is not None` 同理：查一次、判一次、用一次。

```python
pending = [3, 1, 2]
def pop_due():
    return pending.pop() if pending else None

# loop-and-a-half: 取值和判断在同一行, 不重复调用
out = []
while (key := pop_due()) is not None:
    out.append(key)
print("海象 while:", out)

# 没有海象的写法: 要么重复调用, 要么 while True + break
pending[:] = [3, 1, 2]
out = []
key = pop_due()
while key is not None:
    out.append(key)
    key = pop_due()                            # 一旦改了其中一处，另一处容易忘

by_id = {"e1": "entry1"}
if (entry := by_id.get("e1")) is not None:     # 查到就用, 不重复 get
    print("命中:", entry)

# 推导式里的海象: 变量泄漏到外层作用域
data = ["a1", "b", "c22"]
lens = [n for s in data if (n := len(re.sub(r"\D", "", s))) > 0]
print("推导式:", lens, "| 外层也能看到 n =", n)

# 括号不能省: := 的优先级很低
try:
    compile("x = y := 3", "<m>", "exec")
except SyntaxError as e:
    print("SyntaxError:", e.msg)
```

实际输出：

```
海象 while: [2, 1, 3]
命中: entry1
推导式: [1, 2] | 外层也能看到 n = 2
SyntaxError: invalid syntax
```

**作用域。** 推导式里的 `:=` 绑定的是**外层**作用域的变量（推导式自己的循环变量才是局部的），所以上例的 `n` 在推导式结束后依然可见。这是有意设计，方便取出“最后一次满足条件的值”，但也容易意外覆盖外层同名变量。

**易错。** 优先级很低，几乎总是要加括号：`x = y := 3` 是语法错误；`while (key := f()) is not None` 里括号保证先赋值再比较。不要把它塞进复杂的表达式里炫技，一行里同时出现赋值和多个条件时，读者很难一眼看出哪个变量在哪里被改。
