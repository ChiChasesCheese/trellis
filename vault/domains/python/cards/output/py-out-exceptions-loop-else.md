---
id: py-out-exceptions-loop-else
node: output.exceptions
type: qa
step: 4
---
## Q
**for 与 while 的 else**｜读代码说输出

```python
def find(xs, t):
    for x in xs:
        if x == t:
            break
    else:
        return "missing"
    return "found"
print(find([1, 2], 2), find([1, 2], 9), find([], 1))
n = 0
while n < 3:
    n += 1
else:
    print("while-else", n)
for i in range(3):
    if i == 1: continue
else:
    print("for-else", i)
```

输出什么？

## A
**输出。**
```
found missing missing
while-else 3
for-else 2
```

**为什么。**
- 循环的 `else` 在**没有 break** 时执行：循环自然结束（条件变假、迭代器耗尽）就进 `else`。
- `find([1, 2], 2)` 遇到 break 跳过 `else`，得到 "found"；没找到、空列表都走完循环，进入 `else` 返回 "missing"。
- `continue` 不算 break，所以最后一个循环仍然进 `else`，`i` 停在 2。

**语言为什么这样设计。**
- Knuth 式的“搜索循环”需要区分“找到”与“没找到”，`else` 免去了额外的标志变量；关键词复用 `else` 常被诟病，读作“no break”更准。
- C、Java、Go 没有这个语法，都要用标志变量或把循环抽成函数；Python 里一般也是抽成函数更清晰。

**怎么写才对。**
```python
return next((x for x in xs if x == t), None)   # 多数情况下一行搞定
```

**面试里一句话。**
A loop's `else` runs only if the loop finished without hitting `break`, so it reads as "no break".
