---
id: pl-data-serialization-pitfall-deserialization
node: data.serialization
type: qa
step: 11
---
## Q
反序列化为什么是经典的远程代码执行入口？Java 内建序列化与 Python `pickle` 的最小复现是什么，真实输出是什么？

## A
**机制**：这两种格式里，数据决定「创建哪个类、调用哪个回调」。把攻击者控制的字节流交给反序列化函数，就是让攻击者选择在你的进程里运行哪些代码。

**Python**：一个对象通过 `__reduce__` 声明「重建我就调用这个函数」，`loads` 照办：

```python
class Evil:
    def __reduce__(self): return (print, ("code ran during pickle.loads",))
pickle.loads(pickle.dumps(Evil()))
# code ran during pickle.loads
```

真实输出如注释。例子里是 `print`，换成 `os.system` 就是任意命令执行。

**Java**：流里写的类名会被加载，并调用其 `readObject` 回调；构造函数的校验被绕过：

```java
class Gadget implements Serializable {
  private void readObject(ObjectInputStream in) throws Exception {
    in.defaultReadObject();
    System.out.println("readObject ran during deserialization"); } }
// ObjectInputStream.readObject() on its bytes prints that line
```

真实输出：`readObject ran during deserialization`。第二个实验：一个类的构造函数拒绝负数年龄，但把序列化字节里的 `5` 改成 `-1`，`readObject()` 得到 `age = -1`，**构造函数的检查完全被绕过**。

**C++ 的版本不同**：没有运行时按名字创建类的机制，所以没有 gadget chain；但手写解析器常把输入里的长度字段当真，`memcpy(buf, in, len)` 的 `len` 来自攻击者时就是堆溢出，后果是内存损坏而不是回调。防线是用有边界检查的容器和 `std::span`，对每个长度字段做上限校验，并对解析器做模糊测试。

**线上表现**：真实世界的漏洞不是自己写 `Gadget`，而是类路径里已有的第三方库里恰好有一个类的回调会做危险的事（读文件、反射调用、发网络请求），攻击者把这些类串起来（gadget chain）。你什么都没写错，只是调用了 `readObject`。

**防线**：不接受不可信输入的内建序列化；必须用时，设置 `ObjectInputFilter` 白名单；Python 不对外部数据用 `pickle`，用 `json` 加校验；任何「由数据指定类型」的特性（Jackson 默认类型、YAML 的 `!!python/object`）都当作等价于 `readObject` 的风险处理。
