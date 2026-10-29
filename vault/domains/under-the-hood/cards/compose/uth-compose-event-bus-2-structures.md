---
id: uth-compose-event-bus-2-structures
node: compose.event-bus
type: qa
step: 2
---
## Q
**组合：类型表 + 写时复制集合**｜Guava EventBus · 33.5.0

Guava 的订阅表怎样组织，才能让发布时不加锁、登记时也不出错？`post` 碰哪几个结构？

## A
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="10" y="8" width="130" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="75.0" y="26.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">post(OrderPaid)</text>
<rect x="10" y="62" width="130" height="44" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="75.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">展开类型</text>
<text x="75.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">类 + 父类 + 接口</text>
<line x1="75" y1="36" x2="75.0" y2="56.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="75,62 72.0,56.0 78.0,56.0" fill="currentColor"/>
<rect x="170" y="14" width="84" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212.0" y="32.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OrderPaid</text>
<rect x="268" y="14" width="62" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="299.0" y="32.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{S1, S2}</text>
<line x1="254" y1="28" x2="262.0" y2="28.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268,28 262.0,31.0 262.0,25.0" fill="currentColor"/>
<line x1="140" y1="84" x2="167.2" y2="33.3" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,28 169.8,34.7 164.5,31.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="170" y="54" width="84" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212.0" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PayEvent</text>
<rect x="268" y="54" width="62" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="299.0" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{S3}</text>
<line x1="254" y1="68" x2="262.0" y2="68.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268,68 262.0,71.0 262.0,65.0" fill="currentColor"/>
<line x1="140" y1="84" x2="164.7" y2="70.8" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,68 166.1,73.5 163.3,68.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="170" y="94" width="84" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212.0" y="112.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Object</text>
<rect x="268" y="94" width="62" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="299.0" y="112.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{S4}</text>
<line x1="254" y1="108" x2="262.0" y2="108.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268,108 262.0,111.0 262.0,105.0" fill="currentColor"/>
<line x1="140" y1="84" x2="165.3" y2="104.3" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,108 163.4,106.6 167.2,101.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="299" y1="122" x2="299.0" y2="142.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="299,148 296.0,142.0 302.0,142.0" fill="currentColor"/>
<text x="293" y="140" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快照</text>
<rect x="170" y="148" width="160" height="36" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="250.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Dispatcher</text>
<text x="250.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按线程排队 逐个调用</text>
<text x="10" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ConcurrentMap</text>
<text x="10" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">类型 -&gt; 写时复制集合</text>
</svg>
```

**结构。** 一张并发表 `ConcurrentMap<Class, CopyOnWriteArraySet<Subscriber>>`：键是事件类型，值是订阅者集合。`CopyOnWriteArraySet` 是写时复制（copy-on-write）集合：每次增删都复制出一份新数组再换上，读者手里始终是一份完整的旧数组。

**细节。**

- 发布前先把事件的类展开成「它自己 + 所有父类 + 接口」，每个类型各查一次表，所以订阅 `Object` 的监听器能收到一切事件。
- 展开结果，和「哪些方法带 `@Subscribe`」，都缓存了起来，免得每次反射。
- dispatcher（派发器）负责按顺序把事件交给订阅者。

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `register` | 缓存查出带 `@Subscribe` 的方法；按类型找到（或新建）集合，复制添加 | O(该类型订阅者数) |
| `post` | 展开类型；逐类型查表，拿集合的快照迭代器，交给 dispatcher | O(类型数 + 订阅者数) |
| `unregister` | 同样找出方法，从各集合里删除 | O(订阅者数) |

**对应 LeetCode：** 无直接对应的题
