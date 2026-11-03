%% trellis:begin %%
# 依赖方向：接口由使用方定义，核心不依赖基础设施
*编码功力（Coding Craft） / 架构理解（Architecture）*

Watcher 定义自己需要的 FileSystem.scan；业务核心不 import 磁盘/网络/时间；基础设施去适配核心。

**Requires:** [[domains/python/map/classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]], [[domains/python/map/types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]]

## Cards (4)
1. [[craft-dependency-direction-consumer-owns-interface-1-consumer-defines-port]]
2. [[craft-dependency-direction-consumer-owns-interface-2-missing-method]]
3. [[craft-dependency-direction-consumer-owns-interface-3-contract-in-docstring]]
4. [[craft-dependency-direction-consumer-owns-interface-4-anti-corruption]]
%% trellis:end %%

## Notes
