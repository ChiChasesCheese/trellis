---
id: uth-compose-spring-bean-registry-2-parts
node: compose.spring-bean-registry
type: qa
step: 2
---
## Q
**一张 Map、一个列表、两张依赖表**｜Spring Framework · 7.0

Spring 的 Bean 注册表由哪几个结构组成？它们之间怎么互相指？

## A
**结构。** 定义放在 `DefaultListableBeanFactory`，依赖和销毁记录放在它的祖先类 `DefaultSingletonBeanRegistry`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="84" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定义注册表</text>
<text x="256" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">依赖记录</text>
<rect x="4" y="26" width="160" height="42" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="84.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">beanDefinitionMap</text>
<text x="84.0" y="58.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">名字 -&gt; 定义 按名字 O(1)</text>
<rect x="4" y="94" width="160" height="42" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="84.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">beanDefinitionNames</text>
<text x="84.0" y="126.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">注册顺序的名字列表</text>
<line x1="84" y1="94" x2="84" y2="68" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,68.0 86.5,73.0 81.5,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="26" width="160" height="42" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="256.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dependenciesForBeanMap</text>
<text x="256.0" y="58.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">我 -&gt; 我依赖的</text>
<rect x="176" y="94" width="160" height="42" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="256.0" y="113.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dependentBeanMap</text>
<text x="256.0" y="126.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">我 -&gt; 依赖我的</text>
<line x1="256" y1="68" x2="256" y2="94" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,94.0 253.5,89.0 258.5,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="256.0,68.0 258.5,73.0 253.5,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="160" x2="256" y2="136" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="256.0,136.0 258.5,141.0 253.5,141.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="4" y="160" width="332" height="40" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="170.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">disposableBeans</text>
<text x="170.0" y="191.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按创建的顺序 关闭时反序走</text>
<text x="170" y="222" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">销毁一个 Bean: 先销毁 dependentBeanMap 里的依赖者</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| 注册定义 | 查重（Map），Map 放入，列表追加 | O(1) |
| 按名字取定义 | Map | O(1) |
| 按注册顺序遍历 | 列表，逐个去 Map 取定义 | O(n) |
| 登记依赖 | 两张依赖表各加一条 | O(1) |
| 销毁一个 Bean | 依赖我的表（先销毁它们）、两张依赖表清理 | O(依赖数) |

**细节。** 依赖在创建时登记：字段注入、构造器注入、`@DependsOn` 都会调用 `registerDependentBean`。

**对应 LeetCode：** 无直接对应的题
