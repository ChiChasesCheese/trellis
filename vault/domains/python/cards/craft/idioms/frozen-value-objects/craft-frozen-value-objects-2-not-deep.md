---
id: craft-frozen-value-objects-2-not-deep
node: craft.idioms.frozen-value-objects
type: qa
step: 2
---
## Q
**不可变值对象 · frozen 为什么不等于深不可变**｜写法

图像处理流水线想用「(图像, 步骤前缀)」当缓存键，于是把图像写成 `frozen=True` 的数据类，像素用 `list[list[int]]`。结果要么哈希报错，要么缓存悄悄命中了错误的结果。`frozen` 保证了什么、没保证什么？怎么补上？

## A
**要点。** `frozen=True` 只禁止「给字段重新赋值」，不管字段指向的对象。字段是 list，列表照样能被 `append`，而且 list 本身不可哈希。要真正不可变，字段本身就得是不可变类型（tuple、frozenset、另一个冻结对象），并且在构造时把调用方传来的 list 转掉，防止调用方手里的引用继续改它。

```python
@dataclass(frozen=True)
class Bad:
    pixels: list            # frozen 只冻结「字段指向谁」，不冻结列表里的内容

@dataclass(frozen=True)
class Image:
    pixels: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        # 调用方可能传 list：统一转成 tuple，才真正不可变、可哈希
        rows = tuple(tuple(r) for r in self.pixels)
        # frozen 的 __setattr__ 会抛错，所以绕过它给自己赋值一次
        object.__setattr__(self, "pixels", rows)

b = Bad([1, 2, 3])
b.pixels.append(4)                          # 字段没被重新绑定，所以不报错
print("Bad 被改了:", b.pixels)
try:
    hash(b)
except TypeError as e:
    print("Bad 不能哈希:", e)

grid = [[0, 1], [2, 3]]
img = Image(grid)
grid[0][0] = 99                             # 改调用方手里的原列表
print("Image 不受影响:", img.pixels)
cache = {(img, "blur"): "result"}           # (图像, 步骤) 可以当缓存键
print("缓存命中:", cache[(Image([[0, 1], [2, 3]]), "blur")])
```

实际输出：

```
Bad 被改了: [1, 2, 3, 4]
Bad 不能哈希: unhashable type: 'list'
Image 不受影响: ((0, 1), (2, 3))
缓存命中: result
```

**为什么。** `__post_init__` 里不能写 `self.pixels = rows`，冻结后 `__setattr__` 已被换成抛错的版本，所以用 `object.__setattr__` 绕开一次，这是标准做法，只在构造时用。

**易错。** 哈希对象放进缓存后，如果内部可变，缓存里的键会被悄悄改变；转 tuple 的复制代价是 O(n)，大对象每次构造都付一次。
