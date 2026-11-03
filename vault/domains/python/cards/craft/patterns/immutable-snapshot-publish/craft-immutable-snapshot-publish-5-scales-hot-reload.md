---
id: craft-immutable-snapshot-publish-5-scales-hot-reload
node: craft.patterns.immutable-snapshot-publish
type: qa
step: 5
---
## Q
**不可变快照整体替换 · 从税率表到配置热更新（RCU）**｜模式

服务运行中要热更新功能开关：一个请求处理到一半，开关被更新了。请求的前半段用旧开关、后半段用新开关会出什么问题？这和税率发布是同一个想法吗？

## A
**要点。** 是同一个想法，叫 RCU（read-copy-update）式发布：写者造新配置、原子换指针；读者在请求开始时取一次快照，整个请求都用它。同一个请求内看到的配置前后一致，旧快照没人用后自然被回收。

```python
def handle_reading_global(cfg):
    use_checkout = cfg.current.new_checkout   # 请求开始读一次
    cfg.reload()                              # 请求处理过程中配置热更新
    use_pricing = cfg.current.new_pricing     # 又读一次：已经是新配置

def handle_with_snapshot(cfg):
    flags = cfg.current                       # 请求开始时取一次快照，整个请求都用它
    cfg.reload()
    ...
```

请求中途配置从 v1 换成 v2：

```
每次用到都读全局: checkout=old pricing=new
请求开始取快照  : checkout=old pricing=old (v1)
```

**尺度对照。** 税率引擎的 `quote` 读一次 `_Schedule`；一个服务里的请求取一次配置；多台机器上则是版本号加拉取：配置中心推送带版本的完整快照，各实例原子切换，并记录当前版本以便排查「这个请求用的是哪一版」。

**易错。** 第一种写法会让一个请求同时用到「新结账流程」和「旧计价」，两个都是合法配置，组合却从没被测试过。

**信号。** 配置、路由表、特性开关、权限表这类「读很多、改很少、要求读到的是一致的一份」的数据。
