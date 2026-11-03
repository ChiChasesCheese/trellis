%% trellis:begin %%
# 惰性过期：每次访问先结清，不起后台线程（settle on access）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

过期不靠定时器：每个公开操作开头先把已到点的东西结清，读到的数字永远已经算过期。

**Requires:** [[domains/python/map/engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]], [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]

## Cards (5)
1. [[craft-lazy-expiry-settle-on-access-1-settle-on-read]]
2. [[craft-lazy-expiry-settle-on-access-2-settle-in-decorator]]
3. [[craft-lazy-expiry-settle-on-access-3-laziness-not-enough]]
4. [[craft-lazy-expiry-settle-on-access-4-across-problems]]
5. [[craft-lazy-expiry-settle-on-access-5-scales-redis]]
%% trellis:end %%

## Notes
