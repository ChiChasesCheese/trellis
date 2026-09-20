---
id: patterns-creational-cues
node: patterns.creational
type: cloze
step: 1
---
Creational pattern 选择提示：可选构造参数很多、构造过程要分步校验 → {{c1::builder}}；必须创建一整套互相搭配的相关对象（同一主题的按钮、输入框） → {{c2::abstract factory}}；让子类或注册表决定实际创建哪个具体类 → {{c3::factory method}}；新实例只是一个配置好的样板的低成本拷贝 → {{c4::prototype}}；整个进程只需要一份实例——优先用 {{c5::模块级别的单例（模块本身在一个进程里只会被求值一次）}}，而不是在类里用 `__new__` 拦截实例化。
