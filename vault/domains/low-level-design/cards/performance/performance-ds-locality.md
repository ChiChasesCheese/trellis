---
id: performance-ds-locality
node: performance.data-structures
type: qa
step: 6
---
## Q
同样是对 200 万个整数求和，为什么 `array('q')` 反而比 `list` 慢？同一批对象换成随机顺序访问，为什么又慢了好几倍？Python 里“缓存局部性”到底还有没有用？

## A
**list 存的是指针；访问顺序贴近内存顺序才快**

- **`list` 的元素是对象指针**：求和时每一项要先取指针、再跳到整数对象读值；
- **顺序创建的对象在内存里大致相邻**：按创建顺序遍历，CPU 缓存命中；打乱顺序遍历，每一步都跳到远处，缓存频繁未命中；
- **`array('q')` 每项只占 8 字节、紧凑存放**，省内存；但每次读取要新建一个 Python 整数（装箱，boxing），纯 Python 循环里更慢；
- **要用紧凑存储换速度，得把循环交给 C**：`memoryview`、NumPy 这类批量运算；
- **所以结论是**：Python 里的局部性影响小于 C，但不为零；数据已经顺序存放时，别为了“逻辑上的顺序”去按另一个顺序访问。

实测（3.11，本机，200 万个整数，`sum` 三次取平均）：

| 写法 | 耗时 |
|---|---|
| `list`，创建顺序 | 4.4 ms |
| 同一批对象，随机顺序（`random.shuffle` 后的列表） | 28.1 ms |
| `array('q')` | 11.0 ms |

内存：`array('q')` 每项 8 字节；list 每项 8 字节指针外加整数对象 28 字节（`sys.getsizeof(1000)`）。

```python
import array, random, timeit

objs = [i * 1000 + 7 for i in range(2_000_000)]
shuf = objs[:]; random.shuffle(shuf)
arr = array.array("q", objs)
for name, c in (("list", objs), ("shuffled", shuf), ("array", arr)):
    t = timeit.timeit("sum(c)", globals={"c": c}, number=3) / 3
    print(name, round(t * 1000, 1), "ms")
```

**知识点：**按访问模式选结构（Choosing Structures）
