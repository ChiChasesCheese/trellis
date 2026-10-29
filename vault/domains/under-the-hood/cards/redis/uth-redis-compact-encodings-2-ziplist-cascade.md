---
id: uth-redis-compact-encodings-2-ziplist-cascade
node: redis.compact-encodings
type: qa
step: 2
---
## Q
**listpack 为什么取代 ziplist**｜Redis · 7.0 起

老的 ziplist 有什么毛病，让 Redis 7.0 把它换成了 listpack？

## A
**背景。** 紧凑数组要支持从后往前走，就得让每个元素带上“怎么跳到前一个元素”的信息。老的 ziplist 的办法是：每个元素开头记前一个元素的长度。可这样一来，一个元素变长，会逼后一个元素改自己的记录。

**结构。** ziplist 的每个元素开头记“前一个元素的长度”（1 到 5 字节）；listpack 把长度挪到元素末尾，只记自己的长度。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">ziplist: 每个元素开头记「前一个元素的长度」</text>
<text x="8" y="36" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之前</text>
<rect x="40" y="44" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="51" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">前</text>
<rect x="62" y="44" width="66" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="95" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">元素</text>
<rect x="136" y="44" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="147" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">前</text>
<rect x="158" y="44" width="66" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="191" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">元素</text>
<rect x="232" y="44" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="243" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">前</text>
<rect x="254" y="44" width="66" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="287" y="59.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">元素</text>
<text x="8" y="94" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">在最前面插入一个很长的元素:</text>
<rect x="10" y="106" width="70" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="45" y="121.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">长元素</text>
<rect x="84" y="106" width="56" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="112" y="121.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">前长 5 字节</text>
<rect x="140" y="106" width="62" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="171" y="121.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">元素</text>
<rect x="208" y="106" width="56" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="236" y="121.15" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">前长 5 字节</text>
<rect x="264" y="106" width="62" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="295" y="121.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">元素</text>
<text x="8" y="152" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">后一个元素的「前长」从 1 字节变 5 字节, 它自己变长,</text>
<text x="8" y="168" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再逼着再后一个改「前长」: 连锁更新 (cascade)</text>
<text x="8" y="192" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">listpack: 长度挪到元素末尾, 每个元素只记自己的,</text>
<text x="8" y="208" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有连锁, 倒着遍历依然成立</text>
</svg>
```

**细节。**

- ziplist 在中间插入或删除元素，后一个元素的“前长度”可能从 1 字节变 5 字节
- 它自己也随之变长，再改变后面元素的前长度，一路连锁更新（cascade update）
- listpack 每个元素只依赖自己，没有连锁

**为什么。** 连锁更新让实现复杂、难审计；元素只用本地信息，代码更简单，倒着遍历依然成立。

**对应 LeetCode：** 无直接对应的题（编码格式的取舍）
