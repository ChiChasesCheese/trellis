---
id: metaclass-typical-uses
node: classes.metaprogramming
type: qa
source: python-docs
---
## Q
元类（metaclass）典型能用来做哪些事？这些用途现在有没有更轻量的替代方案？

## A
官方文档举的典型用途包括：类注册（比如插件自动登记到一张表里）、日志、接口检查、自动委托、自动生成属性、代理、框架基础设施、资源加锁/同步。其中很大一部分（尤其是『子类创建时自动做点什么』这类需求）现在可以用 3.6 起提供的 `__init_subclass__()` 或类装饰器实现，不需要真正去写一个元类——元类仍然保留给那些需要控制类对象本身构造过程（比如自定义类的 `__dict__` 准备方式、拦截 `type(name, bases, namespace)` 调用本身）的场景。
