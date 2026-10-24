---
id: pl-binding-binding-time-foundation-python-late
node: binding.binding-time
type: qa
step: 3
---
## Q
Python 说「一切都在运行时查」具体指什么？猴子补丁（monkey patching）为什么在 Python 里能做、在 Go 和 Rust 里做不到？

## A
在 Python 里，名字、属性、方法都是**每次使用时才去查**的：

- 函数里引用的全局名字，到执行那一行才查模块字典，所以可以引用还没定义的函数，只要调用时它已存在。
- `obj.attr` 先查对象自己的字典，再查类，再查父类，每次都可能得到不同结果。
- 类和对象的字典随时可以改。

```python
class Dog:
    def speak(self): return "woof"
d = Dog()
Dog.speak = lambda self: "meow"   # rebind the class's method at run time
print(d.speak())                  # meow  (existing object sees it)
d.speak = lambda: "own"           # per-object override
print(d.speak())                  # own

def caller(): return helper()     # helper does not exist yet
# caller() -> NameError: name 'helper' is not defined
def helper(): return "found"
print(caller())                   # found
```

**猴子补丁**就是运行时替换别人的函数或方法，测试里常用来替换网络调用，库里用来给第三方代码打补丁。这有效是因为调用点没有绑定到具体代码，而是绑定到「名字」，名字在运行时指向什么就调用什么。

Go 和 Rust 做不到：函数调用在编译或链接时已经成了固定地址（接口和 `dyn` 例外，但它们的实现集合在编译时就已列出，不能凭空替换）。要得到同样的可替换性，必须在设计上留好缝隙：传入接口、函数值或 trait 对象。

Python 的代价也在这里：任何调用都不能提前假设被调函数不变，编译器因此几乎无法内联；错误如拼错方法名要到执行到那一行才暴露。
