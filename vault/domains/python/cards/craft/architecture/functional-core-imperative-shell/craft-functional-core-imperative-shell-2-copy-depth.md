---
id: craft-functional-core-imperative-shell-2-copy-depth
node: craft.architecture.functional-core-imperative-shell
type: qa
step: 2
---
## Q
**函数式核心 + 命令式外壳 · 「纯」到底允许改参数吗**｜架构

候位系统的核心 `_drain` 会就地修改传进来的队列和空闲桌集合，还会给被插队的人加 `skipped` 计数。那它还算「纯」吗？预测路径只做了 `list(queue)` 浅拷贝，试跑之后真实队列里会出什么问题？

## A
**要点。** 对核心真正的要求是没有隐藏输入、没有隐藏输出：它能读到的只有参数，能改动的只有参数。就地改参数可以，前提是外壳传进来的就是它愿意被改的那份。所以拷贝要拷到「核心会写到的最深一层」。

```python
@dataclass(slots=True)
class Waiting:
    id: str
    skipped: int = 0     # 被插队次数

def overtake(queue, i):                 # 核心会写到元素的字段
    for earlier in queue[:i]:
        earlier.skipped += 1

real = [Waiting("甲"), Waiting("乙")]
overtake(list(real), 1)                 # 浅拷贝：列表是新的，元素是同一批
print("浅拷贝试跑后，真实队列:", real)

real = [Waiting("甲"), Waiting("乙")]
overtake([Waiting(w.id, w.skipped) for w in real], 1)   # 逐元素重建
print("逐元素拷贝试跑后，真实队列:", real)
```

（第二种之前，`real` 也重新建了一份。）

两种试跑之后，真实队列的实际输出：

```
浅拷贝试跑后，真实队列: [Waiting(id='甲', skipped=1), Waiting(id='乙', skipped=0)]
逐元素拷贝试跑后，真实队列: [Waiting(id='甲', skipped=0), Waiting(id='乙', skipped=0)]
```

**易错。** 浅拷贝是新列表装旧对象，试跑的副作用悄悄写进真状态，等位估计一次就把真队列的插队计数改了。餐厅候位的 `estimate_wait` 因此逐个 `_Waiting(w.id, w.size, w.skipped)` 重建。

**代价。** 想不用操心拷贝深度，就让核心返回新状态而不是就地改，代价是每次多分配；元素用冻结 dataclass 时，浅拷贝才够用。
