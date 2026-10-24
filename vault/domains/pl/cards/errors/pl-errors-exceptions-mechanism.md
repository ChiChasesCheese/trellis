---
id: pl-errors-exceptions-mechanism
node: errors.exceptions
type: qa
step: 5
---
## Q
抛出异常时运行时做了什么？栈展开、`finally` 与异常链在行为上是怎样的？

## A
抛出一个异常大致分四步：
1. **创建异常对象**，并在构造时捕获当前的调用栈（Java 的 `fillInStackTrace`、Python 的 traceback 对象）。遍历栈帧与栈深度成正比。
2. **查找处理器**：运行时在当前方法的异常表（编译期生成的 `[起点, 终点) → 处理器` 区间表）里找覆盖当前指令的条目，类型匹配就跳转；找不到，弹出这个栈帧，到调用者里继续找。
3. **展开（unwind）途中**执行 `finally` 块与 `with` 的清理。
4. 一直找不到则线程终止，打印栈追踪。

**`finally` 的行为**很容易误解：无论正常结束、异常或 `return`，它都会执行。如果 `finally` 里自己 `return` 或抛出，会覆盖原本在传播的异常。

**异常链**保存了「为什么」。把底层异常包装成高层异常时，保留 cause，栈追踪里能看到两段：

```console
Exception in thread "main" java.lang.IllegalStateException: startup failed
	at Ex.start(Ex.java:6)
Caused by: java.io.FileNotFoundException: cfg.yml
	at Ex.load(Ex.java:3)
```

Python 对应 `raise RuntimeError("startup failed") from e`，之后可通过 `e.__cause__` 取到原因；不写 `from` 时，Python 也会自动保存上下文（`__context__`）。

C++ 的做法是同一模板的原型，细节略有不同：展开分两阶段，先沿栈向上找到会接住的 `catch`，再回头逐帧展开并运行局部对象的析构函数；异常对象不带栈追踪；任何类型都可以被抛出（惯例是继承 `std::exception`）。
**零成本模型**：不抛异常时，`try` 不执行任何指令，因为异常表是静态的。Java 如此，CPython 3.11 起也采用这种零成本的 `try`。抛出时才付出创建对象、填栈追踪、查表的代价，所以异常是「正常路径免费，失败路径昂贵」。
