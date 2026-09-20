---
nodes: [python.protocols-abc]
url: https://docs.python.org/3/library/abc.html
---
# abc — Abstract Base Classes

值得读：`ABCMeta`/`@abstractmethod`/`register()` 的官方文档，对应
`python-protocol-abc-nominal` 卡里"名义子类型"那一半的依据——虚拟子类通过 `register()` 加入却不出现在 MRO 里、方法体也不会被继承，
这个和 Protocol 的结构化子类型正好对照，读它能补上 ABC 到底强制了什么、`__subclasshook__` 又能放宽到什么程度。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/abc.html)
%% trellis:end %%
