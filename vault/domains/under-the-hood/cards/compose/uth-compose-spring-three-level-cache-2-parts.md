---
id: uth-compose-spring-three-level-cache-2-parts
node: compose.spring-three-level-cache
type: qa
step: 2
---
## Q
**三张表加一个集合：每一级放什么**｜Spring Framework · 7.0

Spring 的单例缓存由哪几个结构组成？一个 Bean 从开始创建到完成，会依次经过哪几级？

## A
**结构。** 同一个类 `DefaultSingletonBeanRegistry` 里有三张 Map 和一个 Set：

- `singletonObjects`：一级，名字 → 成品
- `earlySingletonObjects`：二级，名字 → 早期引用（还没造完的对象，可能已经是代理）
- `singletonFactories`：三级，名字 → 工厂（一段能产出早期引用的代码）
- `singletonsCurrentlyInCreation`：集合，正在创建的名字

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="12" y="40" width="86" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">三级 工厂</text>
<text x="55.0" y="71.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名字 -&gt; 工厂</text>
<rect x="128" y="40" width="86" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="171.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">二级 早期引用</text>
<text x="171.0" y="71.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名字 -&gt; 半成品</text>
<rect x="244" y="40" width="86" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="287.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一级 成品</text>
<text x="287.0" y="71.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名字 -&gt; 成品</text>
<line x1="55" y1="22" x2="55" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="55.0,40.0 52.5,35.0 57.5,35.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="68" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="98" y1="60" x2="128" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,60.0 123.0,62.5 123.0,57.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="214" y1="60" x2="244" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="244.0,60.0 239.0,62.5 239.0,57.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="229" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="14" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 实例化之后: 把工厂放进三级</text>
<text x="14" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2 环上邻居来要: 调用工厂 结果放进二级</text>
<text x="14" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 创建完成: 放进一级 删掉另两级</text>
<rect x="12" y="160" width="316" height="34" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="170.0" y="175.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正在创建的名字 Set</text>
<text x="170.0" y="188.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">开始创建时加入 完成后移出</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| 开始创建 | 集合加入名字 | O(1) |
| 实例化之后 | 三级放入工厂 | O(1) |
| 取 Bean | 先查一级；名字在创建中再查二级、三级，用了三级就把结果挪进二级 | O(1) |
| 创建完成 | 一级放入；三级、二级删除；集合移出 | O(1) |

**细节。** 查询顺序是一级 → 二级 → 三级，越靠前越稳定、越常被读。

**对应 LeetCode：** 无直接对应的题
