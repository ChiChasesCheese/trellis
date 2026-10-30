%% trellis:begin %%
# 属性查找：实例字典、类与描述符
*Python 内置类型与标准库*

obj.x 先查数据描述符、再查实例 __dict__、再查类和父类；函数在类里是描述符，取出来时绑定成方法；property 就是描述符；__slots__ 用固定槽位代替 __dict__ 省内存。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-python-attribute-lookup-1-instance-class]]
2. [[uth-python-attribute-lookup-2-bound-method]]
3. [[uth-python-attribute-lookup-3-descriptor-order]]
4. [[uth-python-attribute-lookup-4-property-cached]]
5. [[uth-python-attribute-lookup-5-slots]]
%% trellis:end %%

## Notes
