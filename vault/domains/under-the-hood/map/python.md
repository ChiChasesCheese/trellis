%% trellis:begin %%
# Python 内置类型与标准库

从对象模型、名字绑定、作用域、属性查找、协议、生成器、字节码、GIL 到常用容器的内部实现：看完能从根上理解 Python 怎样运行。

## Topics
- [[domains/under-the-hood/map/python.list|list：动态数组与过度分配]]
- [[domains/under-the-hood/map/python.dict|dict：紧凑哈希表]]
- [[domains/under-the-hood/map/python.set|set：开放寻址与哈希随机化]]
- [[domains/under-the-hood/map/python.str-int|str 与 int：不可变对象的实现]]
- [[domains/under-the-hood/map/python.sort|sorted / list.sort：Timsort 与 Powersort]]
- [[domains/under-the-hood/map/python.heapq-bisect|heapq 与 bisect：数组上的堆与二分]]
- [[domains/under-the-hood/map/python.deque-ordereddict|deque 与 OrderedDict：块链表与双向链表]]
- [[domains/under-the-hood/map/python.lru-cache|functools.lru_cache：哈希表 + 环形双向链表]]
- [[domains/under-the-hood/map/python.memory-gc|引用计数与分代 GC]]
- [[domains/under-the-hood/map/python.asyncio|asyncio 事件循环：就绪队列 + 定时器堆]]
- [[domains/under-the-hood/map/python.objects-names|一切皆对象：名字只是标签]]
- [[domains/under-the-hood/map/python.mutability-args|可变性与传参：按共享传递]]
- [[domains/under-the-hood/map/python.scope-closures|作用域与闭包：LEGB 与 cell]]
- [[domains/under-the-hood/map/python.functions-decorators|函数是一等对象：装饰器与 functools]]
- [[domains/under-the-hood/map/python.attribute-lookup|属性查找：实例字典、类与描述符]]
- [[domains/under-the-hood/map/python.classes-mro|类、继承与 MRO]]
- [[domains/under-the-hood/map/python.dunder-protocols|协议与特殊方法：鸭子类型]]
- [[domains/under-the-hood/map/python.iterators-generators|迭代器与生成器：挂起的栈帧]]
- [[domains/under-the-hood/map/python.bytecode-eval|从源码到执行：字节码与求值循环]]
- [[domains/under-the-hood/map/python.gil-concurrency|GIL 与并发：线程、进程与 asyncio]]
- [[domains/under-the-hood/map/python.exceptions-context|异常与上下文管理器]]
- [[domains/under-the-hood/map/python.numbers-floats|数值：任意精度整数、浮点数与取整]]
- [[domains/under-the-hood/map/python.typing-dataclasses|类型注解与 dataclass]]
- [[domains/under-the-hood/map/python.imports-modules|模块与导入系统]]
%% trellis:end %%

## Notes
