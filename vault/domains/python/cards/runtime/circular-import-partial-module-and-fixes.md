---
id: circular-import-partial-module-and-fixes
node: runtime.import-system
type: qa
source: python-docs
---
## Q
两个模块循环导入彼此（A import B、B 又 import A）会得到什么结果？工程上通常怎么绕开？

## A
不会无限递归崩溃，但先执行到的一方拿到的可能是对方「半初始化」的模块对象——如果此时就去访问对方模块里还没执行到的名字，会触发 `AttributeError` 或 `ImportError`。常见解法：①把其中一个 import 挪到函数体内部，延迟到真正调用时才导入；②把两个模块共同依赖的部分抽到第三个模块里，打破环；③只 `import module` 拿模块对象、在使用处再点属性访问，而不是在顶层 `from module import name`（后者要求那个名字在导入当时就已存在）。
