---
id: pl-sig-python-intro-duck-typing
node: signatures.python
type: qa
step: 2
---
## Q
鸭子类型（duck typing）是什么？Python 为什么在运行时才检查“能不能做这件事”，这带来什么好处与风险？

## A
**是什么**：Python 不问“这个对象是什么类型”，而是问“它**能不能**做我要它做的事”。“如果它走路像鸭子，叫起来像鸭子，那它就是鸭子。”函数只要对象有它要调用的方法，就能工作，不需要共同的基类或接口声明。

```python
class Duck:  
    def quack(self): return "quack"
class Robot: 
    def quack(self): return "beep"
def make_noise(x): return x.quack()
make_noise(Duck()), make_noise(Robot())   # ('quack', 'beep')
make_noise(42)
# AttributeError: 'int' object has no attribute 'quack'
```

真实输出：前两个调用得到 `quack` 与 `beep`，第三个在**运行到那一行时**才报 `AttributeError`。

**好处**：
1. **灵活**：测试时传一个假对象就行，不用接口、不用继承。
2. **代码短**：没有类型声明与适配代码。
3. **快速探索**：先让东西跑起来，再逐步整理。
4. **对所有“像文件的对象”（file-like）、“像字典的对象”（mapping）一视同仁**：协议靠约定，标准库的 `with`、`for`、`len()` 都是这样工作的。

**风险**：
1. 类型错误只在运行时暴露，可能在很少走的分支里。
2. 大型代码库里，一个函数到底接受什么，要读实现才知道。
3. 重构缺少编译器的保护。

**补偿机制**：类型注解加 `mypy`/`pyright`；`typing.Protocol` 用静态方式表达“鸭子类型”的接口（结构化类型）；单元测试；运行时校验库。

**要记住的一点**：鸭子类型是 Python 灵活与易用的根源，也是它在规模化时需要补偿的根源。
