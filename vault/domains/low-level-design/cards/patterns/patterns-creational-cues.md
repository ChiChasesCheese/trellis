---
id: patterns-creational-cues
node: patterns.creational
type: cloze
---
Creational pattern selection cues: many optional constructor parameters → {{c1::builder}}; must create consistent **families** of related objects (theme, vendor) → {{c2::abstract factory}}; let subclasses/plug-ins decide the concrete class of one product → {{c3::factory method}}; new instances are cheap copies of configured exemplars → {{c4::prototype}}; exactly one shared instance — prefer {{c5::a single instance wired at the composition root (DI)}} over a classic singleton.

## zh
Creational pattern 选择提示：许多可选构造函数参数 → {{c1::builder}}；必须创建相关对象的一致**系列**（主题、供应商）→ {{c2::abstract factory}}；让子类/插件决定一个产品的具体类 → {{c3::factory method}}；新实例是配置好的范例的便宜副本 → {{c4::prototype}}；恰好一个共享实例——优先选择 {{c5::在组合根处连接的单个实例（DI）}} 而不是经典 singleton。
