---
nodes: [runtime.import-system, runtime.exceptions, runtime.compile-bytecode, performance.containers]
tags: [drill, interview]
---
# Drill：解释一个循环导入报错，再解释一个「异常被吞掉」的 traceback

**症状 1**：项目里 `orders.py` 顶部 `from billing import charge`，`billing.py` 顶部 `from orders import Order`，启动时抛：

```
ImportError: cannot import name 'Order' from partially initialized module 'orders'
(most likely due to a circular import)
```

**症状 2**：一段代码线上从不报错，但确实有一条分支应该抛 `ValueError`，日志里却完全看不到：

```python
def process(order):
    try:
        validate(order)
    except ValueError:
        return "invalid"
    finally:
        return "ok"  # 这一行是真实线上代码里的
```

**限制与要求**
- 症状 1 要解释清楚「为什么不是无限递归」以及「为什么现在才报错」，不能只说「因为循环导入」。
- 症状 2 要精确说出被吞掉的具体机制，不能只说「有 bug」。
- 各给出至少两种修复症状 1 的具体做法。
- 8 分钟内完成两个症状的分析。

**分关要求**
- 第 1 关（约 4 分钟）：解释症状 1 的机制，给出修复方案。
- 第 2 关（约 3 分钟）：解释症状 2 的机制，给出修复方案。
- 第 3 关（约 3 分钟）：追问——用 `dis` 能验证「`x in a_set` 比 `x in a_list` 快」这句话吗？该怎么验证，验证的到底是什么？

**评分点（强答案会命中）**
- 两个模块循环 import 彼此不会无限递归崩溃，但先执行到的一方可能拿到对方「半初始化」的模块对象——此时去访问对方还没执行到的名字才会触发 `ImportError`/`AttributeError`，报错时机取决于代码执行到具体访问那个名字的那一行 [[circular-import-partial-module-and-fixes]]
- 导入机制在真正执行模块代码之前，会先把这个（还没执行完的）模块对象塞进 `sys.modules` 占位，就是为了在模块代码执行过程中再次被 import 自己时截断无限递归，代价是拿到手的可能是属性还没全部定义的半成品模块 [[sys-modules-inserted-before-exec-breaks-recursion]]
- 一个模块第二次被 import 时会先查 `sys.modules`，命中就直接返回缓存的模块对象、不重新执行代码，这也是为什么循环导入报错只在第一次加载路径上出现 [[module-executes-once-via-sys-modules-cache]]
- `finally` 块里的 `return` 会直接丢弃 try/except 路径上任何暂存待重新抛出的异常，也会覆盖 try/except 里已经执行过的 `return`——函数最终返回值以 `finally` 里最后执行的那条 `return` 为准，这就是「`ValueError` 被 finally 吞掉」的确切机制 [[finally-return-swallows-exception]]
- `except ValueError as e:` 结束时 `e` 会被自动删除，是为了打破「异常对象→回溯→帧→局部变量 e」这条引用环，让这些帧不用等下一次循环 GC 才能被释放 [[except-as-name-deleted-to-break-refcycle]]
- `try` 块没有异常时不执行任何额外插桩指令，只有真的抛出异常才去查这一帧的异常表（存在 code 对象的 `co_exceptiontable`），查不到就继续向上冒泡到调用者的帧重复这个过程 [[zero-cost-exception-handling]] [[exception-table-lookup-and-propagation]]
- `x in a_list` 要从头线性扫描逐个比较是 O(n)；`x in a_set` 先对 x 计算哈希值直接定位槽位，平均 O(1) [[containers-in-list-vs-set]]
- `dis` 反汇编出的是字节码指令序列，能验证的是「某种写法是否真的比另一种少几条指令」这类静态结构问题，而不是直接告诉你两条指令各自的运行耗时；`x in list` 和 `x in set` 在字节码层面都只是一条 `CONTAINS_OP`，`dis` 看不出复杂度差异，复杂度差异来自这条指令背后 `list.__contains__` 和 `set.__contains__` 的具体实现，要用 `timeit` 实测而不是 `dis` [[interpreted-language-dis-soundbite]]

**参考答案**
症状 1：`orders.py` 先被 import，执行到 `from billing import charge` 时转去执行 `billing.py`；`billing.py` 执行到 `from orders import Order` 时，`orders` 已经在 `sys.modules` 里占了位（哪怕它自己还没执行完），于是不会再重新执行 `orders.py`、也不会死循环，而是直接返回这个半成品的 `orders` 模块对象——但此时 `orders.py` 的执行还停在第一行 `from billing import charge`，`Order` 这个类还没被定义，所以 `from orders import Order` 找不到这个名字，抛出 `ImportError`。两种修复：①把其中一侧的 import 挪到函数体内部，推迟到真正调用时才导入；②把 `orders`、`billing` 都依赖的公共部分（比如 `Order`/`charge` 用到的基础类型）抽到第三个模块里，让两边都只依赖它、不再互相依赖。

症状 2：`validate(order)` 抛出的 `ValueError` 被 `except ValueError:` 捕获，`return "invalid"` 本该让函数返回 `"invalid"`；但紧接着 `finally: return "ok"` 里的 `return` 会覆盖前面这条已执行的 `return`（不管它来自 try 还是 except），函数最终必然返回 `"ok"`，看起来就像异常「什么都没发生」。修复：把 `finally` 里的 `return "ok"` 删掉或挪到 try 块的 `else` 子句里（只在 try 完全没抛异常时才执行），`finally` 只保留真正的清理逻辑（关资源、释放锁），不要在里面写 `return`。

第 3 关：能间接验证，但验证的不是「快多少」。`dis.dis` 会显示 `x in a_list` 和 `x in a_set` 在字节码层面都编译成同一条 `CONTAINS_OP` 指令，指令数量完全一样——`dis` 证明不了 set 更快，只能证明两种写法在这一层没有指令数差异。真正的速度差异发生在 `CONTAINS_OP` 执行时分别调用 `list.__contains__`（线性扫描）还是 `set.__contains__`（哈希定位）这一步，这是运行时行为，要用 `timeit` 对不同规模的容器实测才能验证复杂度差异，`dis` 只适合验证「某段代码是否真的比另一段少几条指令」这类问题。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
