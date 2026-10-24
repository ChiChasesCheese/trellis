---
id: pl-foundations-paradigms-pitfall-sort-none
node: foundations.paradigms
type: qa
step: 6
---
## Q
Python 里 `x = lst.sort()` 为什么得到 `None`？这反映了多范式语言的哪个坑？

## A
`list.sort()` 是命令式风格：原地修改列表，返回 `None`，目的是让你不会误以为它产生了新列表。内置函数 `sorted()` 是函数式风格：不碰原列表，返回一个新列表。

```python
lst = [3, 1, 2]
x = lst.sort()
print(x, lst)     # None [1, 2, 3]
y = sorted([3, 1, 2])
print(y)          # [1, 2, 3]
```

实际运行输出就是上面注释里的两行。坑在于：同一个标准库里混着「修改自己」和「返回新值」两种风格，名字却很像，写错了不会报错，只会在后面某处拿到 `None` 再爆出 `TypeError`。

多范式的代价就在这里：语言不替你选风格，一致性要靠记忆和约定。Rust 用 `&mut self` 把「会修改」写进方法签名，调用处必须有 `mut`，Java 的 `Collections.sort(list)` 返回 `void` 也是同样意图。判断一个方法是「改自己」还是「返新值」，要看文档，而不是看名字。
