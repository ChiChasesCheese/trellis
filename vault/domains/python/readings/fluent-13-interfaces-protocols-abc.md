---
nodes: [classes.abc-protocols]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 13 章 接口、协议与抽象基类
---
# Fluent Python 2e · 第 13 章 接口、协议与抽象基类

这一章对比三种“接口”手段：鸭子类型（不做检查）、`abc.ABC` 定义的名义子类型（继承或注册），以及 `typing.Protocol` 的结构化子类型（不需要继承，只要形状匹配）。

**读时提取：**
- 鸭子类型、名义子类型（ABC）、结构化子类型（Protocol）三者的区别
- `abstractmethod` 如何强制子类必须实现某方法，否则不能实例化
- `Protocol` 为什么能让第三方类『事后』满足一个接口而无需继承

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
