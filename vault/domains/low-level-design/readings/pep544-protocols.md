---
nodes: [python.protocols-abc]
url: https://peps.python.org/pep-0544/
---
# PEP 544 – Protocols: Structural subtyping (static duck typing)

值得读：`typing.Protocol` 结构化子类型的原始设计动机和取舍，是
`python-protocol-structural`、`python-protocol-vs-abc-decision` 两张卡的源头——为什么"只要有对的方法签名就算实现了接口"
不需要显式继承，PEP 本身给出了鸭子类型和静态检查如何共存的完整论证，读它能补上 Protocol 和继承式接口该怎么选这条边界判断。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0544/)

## Archived copy
![[pep544-protocols-clip]]
%% trellis:end %%
