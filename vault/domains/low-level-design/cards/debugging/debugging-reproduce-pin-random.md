---
id: debugging-reproduce-pin-random
node: debugging.reproduce
type: qa
step: 3
---
## Q
随机生成输入的测试，跑一百次才红一次，下次再跑又绿了。怎么让这次失败可以重放？还有哪些“每次进程启动都不同”的东西会让缺陷时有时无？

## A
**随机数用显式的种子，失败时把种子打出来**

- **给每个用例一个独立的生成器**：`rng = random.Random(seed)`，不用全局的 `random.random()`，别的代码调用随机数不会打乱你的序列；
- **失败时报出种子（和输入）**：之后用同一个种子，必然得到同一份输入；
- **字符串的哈希每个进程不同**：`str` 的哈希默认随机化，`set` 里字符串的遍历顺序因此在不同次运行间变化；`PYTHONHASHSEED=0` 可以固定；
- **其他隐藏输入**：当前时间、环境变量、工作目录、文件系统顺序（`os.listdir` 不保证顺序）、线程调度；
- **缺陷要靠顺序才出现，就是顺序在作怪**：该排序的地方排序，而不是靠固定种子掩盖。

```python
import random

def second_largest(xs):                 # 缺陷：重复的最大值被当成第二大
    return sorted(xs)[-2]

def case(seed):
    rng = random.Random(seed)
    return [rng.randrange(5) for _ in range(rng.randrange(2, 6))]

for seed in range(1000):
    xs = case(seed)
    if len(set(xs)) > 1 and second_largest(xs) != sorted(set(xs))[-2]:
        print("失败 seed =", seed, xs)   # 记住 seed
        break
print(case(seed) == xs)                 # True：同一个种子，同一份输入
```

<details class="pt"><summary>延伸</summary>

用 `hypothesis` 这类属性测试库时，它会自动缩小失败输入并记住失败例子；在 CI 里也要把它打印的种子或重现命令留在日志里。

</details>

**知识点：**稳定复现（Reproduce）
