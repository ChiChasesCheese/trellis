---
id: craft-default-forms-2-for-else
node: craft.idioms.default-forms
type: qa
step: 2
---
## Q
**省掉标志变量 · `for ... else` 的 `else` 什么时候执行，候位队列里它替掉了什么**｜写法

候位 `_drain` 要从队首往后找第一个有桌可坐的人，找到就入座并重新开始，整队都没人能坐就结束。用 `for-else` 是怎么写的？`else` 到底在什么条件下执行？

## A
**要点。** 循环的 `else` 在**没有被 `break` 打断**时执行：循环自然结束（包括遍历的序列是空的）就走 `else`，被 `break` 跳出就不走。所以「找到了就 `break`，整个循环都没找到，就执行 else」可以直接写出来，不需要一个 `found = False` 再在循环里改成 `True`。

```python
def first_fit_flag(queue, can_sit):
    found = False                              # 标志变量: 记「有没有人坐下」
    for w in queue:
        if can_sit(w):
            found = True
            seated = w
            break
    if not found:
        return None
    return seated

def first_fit_else(queue, can_sit):
    for w in queue:
        if can_sit(w):
            seated = w
            break
    else:                                      # 循环没有被 break 打断才执行
        return None
    return seated

q = [5, 6, 3]
print(first_fit_flag(q, lambda w: w <= 4), first_fit_else(q, lambda w: w <= 4))
print(first_fit_flag(q, lambda w: w <= 1), first_fit_else(q, lambda w: w <= 1))

# else 的触发条件: 没有 break。空序列也会触发
for x in []:
    pass
else:
    print("空序列也走 else")
for x in [1, 2]:
    if x == 3:
        break
else:
    print("从头到尾没 break 也走 else")
for x in [1, 3]:
    if x == 3:
        break
else:
    print("不会打印")
```

实际输出：

```
3 3
None None
空序列也走 else
从头到尾没 break 也走 else
```

**为什么。** 标志变量是一个“要同步”的状态：每个退出路径都得记得把它设对。`for-else` 把“没找到”和循环结构绑定在一起，没有可忘的状态。

**易错。** `else` 这个名字有迷惑性，常被理解成「if 不成立」。把它读成 `nobreak`（没有 break）。因为难读，团队里不熟悉的人多时，加一行注释 `# 没有 break`，或者把循环抽成返回值的函数（`return` 代替 `break`，找不到就 `return None`），往往更清晰。
