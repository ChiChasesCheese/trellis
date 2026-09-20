---
nodes: [problems.marketplaces.food-delivery]
url: https://docs.python.org/3/library/enum.html
---
# Python 文档：enum —— Support for enumerations

值得读：外卖这道题有两组有限集合——订单状态（OrderState）和参与方（Actor），它们必须是 `Enum`
而不是字符串常量，否则 `"resturant"` 这样的拼写错误会一路滑到运行时才炸，而且 `frozenset`
里的成员也没法被静态检查。文档里对本题有用的两点：`Enum` 成员是单例，所以比较一律用 `is`
而不是 `==`（本题解的每一处状态比较都遵守这一条）；成员可哈希，所以能直接做字典键和
`frozenset` 元素——`{当前态: {目标态: 允许的角色}}` 这张嵌套表正是靠这一点写成三行数据而不是
三十行 `if`。配套要读的是[`threading`](https://docs.python.org/3/library/threading.html)：
`Restaurant.quote` 的"校验可售 + 抄下价格"和 `CourierPool.assign` 的"查空闲 + 写占用"都靠
`Lock` 合成一次原子操作，GIL 两件事都不负责。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/enum.html)

## Archived copy
![[src-python-docs-enum-linkedin-clip]]
%% trellis:end %%
