---
nodes: [problems.social.linkedin]
url: https://docs.python.org/3/library/enum.html
---
# enum — 为什么连接请求和申请的状态是 `Enum`，转移规则是一张表

值得读：`ConnectionStatus` 与 `ApplicationStatus` 都是这一节描述的 `Enum`：有限的、
互斥的取值集合，比用裸字符串或整数表达状态更早地暴露拼写错误（`ConnectionStatus.ACCEPTD`
在赋值时就会被解释器拒绝，字符串 `"acceptd"` 不会）。这一页也是
`APPLICATION_TRANSITIONS: dict[ApplicationStatus, frozenset[ApplicationStatus]]`
这种写法的依据——`Enum` 成员是可哈希、可比较身份的单例，天然适合做字典的键，"当前状态
允许转到哪些状态"因此可以整个收进一张表，而不是在每个转移方法里各写一遍
`if status == ApplicationStatus.SUBMITTED and ...`。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/enum.html)

## Archived copy
![[src-python-docs-enum-linkedin-clip]]
%% trellis:end %%
