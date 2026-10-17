---
nodes: [amazon.amz-linux-find]
url: https://docs.python.org/3/library/fnmatch.html
---
# fnmatch — Unix filename pattern matching
值得读：Python 官方文档，说明 `*`、`?`、`[seq]` 通配符的语义，以及 `fnmatchcase` 与 `fnmatch` 在大小写上的区别（后者随操作系统变化）。名字匹配用 `fnmatchcase`，结果就不随平台变化；通配符只匹配最后一段名字，因为名字里不含 `/`。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/fnmatch.html)
%% trellis:end %%
