---
nodes: [python.modules]
url: https://docs.python.org/3/library/importlib.html
---
# importlib — The implementation of import

值得读：`import` 语句底层机制的官方文档，对应 `python-modules-circular-import-cause`、`python-modules-break-circular`
两张卡——循环导入为什么会在"模块正在初始化、还没执行完就被另一个模块 import"时炸掉，是 `sys.modules` 缓存和加载顺序共同造成的，
读它能补上这条机制本身，而不是只记住"延迟导入能解决"这个结论。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/importlib.html)
%% trellis:end %%
