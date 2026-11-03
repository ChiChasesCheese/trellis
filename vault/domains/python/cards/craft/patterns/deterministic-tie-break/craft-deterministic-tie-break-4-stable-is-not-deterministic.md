---
id: craft-deterministic-tie-break-4-stable-is-not-deterministic
node: craft.patterns.deterministic-tie-break
type: qa
step: 4
---
## Q
**确定性平局规则 · `sorted` 是稳定的，为什么输出还会随运行变化**｜写法

文件监视器比较两张快照，用集合运算得到新增、删除、变化的文件，合成一个事件列表后用 `sorted(events, key=lambda e: e[0])` 按事件种类排序。Python 的排序是稳定的（并列元素保持原来的相对顺序），这样输出是确定的吗？

## A
**要点。** 稳定排序只保证"并列元素保持输入里的相对顺序"。输入顺序若来自集合运算（`new.keys() - old.keys()`），它自己就随哈希盐变化，稳定也只是把这种不确定原样保留。要确定，排序键必须是**全序**：路径加种类 `(path, kind)`，任何两个事件都能分出先后。

```python
import subprocess, sys

CODE = '''
old = {"a.txt": 1, "b.txt": 1, "c.txt": 1}
new = {"a.txt": 2, "b.txt": 1, "d.txt": 1, "e.txt": 1}
events  = [("created", p) for p in new.keys() - old.keys()]       # 集合差：顺序随进程变化
events += [("deleted", p) for p in old.keys() - new.keys()]
events += [("modified", p) for p in old.keys() & new.keys() if old[p] != new[p]]
by_kind = sorted(events, key=lambda e: e[0])          # 稳定，但并列的先后取决于上面
total   = sorted(events, key=lambda e: (e[1], e[0]))  # 全序键：路径 + 种类
print("只按种类:", [p for _, p in by_kind], " 全序:", [p for _, p in total])
'''
for seed in ("1", "2", "3", "4"):
    out = subprocess.run([sys.executable, "-c", CODE], env={"PYTHONHASHSEED": seed},
                         capture_output=True, text=True).stdout.strip()
    print(f"seed={seed}:", out)
```

四个不同的哈希盐下各跑一次：

```
seed=1: 只按种类: ['e.txt', 'd.txt', 'c.txt', 'a.txt']  全序: ['a.txt', 'c.txt', 'd.txt', 'e.txt']
seed=2: 只按种类: ['d.txt', 'e.txt', 'c.txt', 'a.txt']  全序: ['a.txt', 'c.txt', 'd.txt', 'e.txt']
seed=3: 只按种类: ['e.txt', 'd.txt', 'c.txt', 'a.txt']  全序: ['a.txt', 'c.txt', 'd.txt', 'e.txt']
seed=4: 只按种类: ['d.txt', 'e.txt', 'c.txt', 'a.txt']  全序: ['a.txt', 'c.txt', 'd.txt', 'e.txt']
```

**为什么。** "稳定"和"确定"是两个不同的性质：稳定是排序算法的性质，确定是整个程序输出的性质。只要输入顺序有任何不确定来源（集合、并发收集的结果、`os.scandir` 的返回顺序），就必须用全序键把它消掉。`diff` 里还有一点：同一个路径可能同时出现在两类事件里吗？不会，但全序键里仍然带上种类，让这个"不会"不必依赖证明。

**检查方法。** 用 `PYTHONHASHSEED` 的不同取值跑同一个测试，或者把输入列表随机打乱再排序，断言输出相同（性质测试：对输入的任意排列，输出相同）。
