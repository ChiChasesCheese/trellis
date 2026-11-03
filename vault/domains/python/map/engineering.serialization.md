%% trellis:begin %%
# 序列化：`json`、`pickle` 的安全与版本、`copyreg` 与 dataclass 的转换
*工程实践：健壮性、测试与交付*

理解 pickle 可执行任意代码故不可反序列化不可信数据、类改名后旧 pickle 失效的处理、json 与 Decimal/datetime 的自定义编码。

**Unlocks:** [[domains/python/map/craft.patterns.append-only-log-derived-state|只追加日志 + 派生状态：事实不可变，余额/视图可重算（event-sourced state）]], [[domains/python/map/craft.architecture.command-event-fact|命令、事件与事实：过去式、自带全部信息、不可变]]

## Readings
- [[effective-12-data-structures-algorithms|Effective Python 3e · 第 12 章 数据结构与算法]]
- [[pydocs-json-module|json 模块：JSON 编解码]]
- [[pydocs-pickle-module|pickle 模块：Python 对象序列化]]

## Cards (6)
1. [[json-custom-encode-decimal-datetime]]
2. [[pickle-class-must-be-importable]]
3. [[pickle-copyreg-customize-third-party-class]]
4. [[pickle-protocol-version-number]]
5. [[pickle-untrusted-data-rce]]
6. [[pickle-vs-json-tradeoffs]]
%% trellis:end %%

## Notes
