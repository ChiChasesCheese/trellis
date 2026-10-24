---
id: pl-eco-modules-pitfall-python-imports
node: ecosystem.modules
type: qa
step: 10
---
## Q
Python 导入系统在线上最常见的两个坑是什么？循环导入和标准库遮蔽的真实表现是什么，怎样防？

## A
**坑一：循环导入**。两个模块互相 `from ... import`：

```python
# a.py: from b import fb      def fa(): ...
# b.py: from a import fa      def fb(): ...
# python -c "import a"
# ImportError: cannot import name 'fa' from 'a'
```

执行顺序是：开始执行 `a` → 第一行导入 `b` → 开始执行 `b` → 第一行 `from a import fa`，此时 `a` 在 `sys.modules` 里，但只执行到第一行，`fa` 还没定义 → 报错。关键点：**取决于谁先被导入**，换一个入口可能就好了，所以表现为「本地测试能过、线上入口不同就崩」。

**防线**：把共享的东西抽成第三个模块；在函数内部延迟导入；导入模块而不是名字（`import a` 然后用 `a.fa`，到调用时再解析）。

**坑二：自己的文件遮蔽标准库**。脚本目录总是排在 `sys.path` 最前。你在项目里放了 `random.py`（或 `logging.py`、`types.py`、`email.py`），所有 `import random` 拿到的都是你的文件：

```python
# random.py exists next to t.py;  t.py: import random; random.randint(1, 6)
# AttributeError: module 'random' has no attribute 'randint'
```

较新的 Python（本机 3.14）会在报错末尾提示 `consider renaming ... since it has the same name as the standard library module`；老版本只有莫名其妙的 `AttributeError`。更糟的情形是第三方库内部的 `import random` 也被替换，在很深的调用栈里崩溃。

**防线**：文件名避开标准库；项目用 `src/` 布局；入口脚本放到包外，用 `python -m package.module` 运行，这样 `sys.path` 首位是当前目录而不是模块目录；CI 里用 `python -I`（隔离模式）跑一遍。

**共同教训**：Python 的导入是运行时的、顺序相关的，所以必须测试每个入口，不能只测一个。
