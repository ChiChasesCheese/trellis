---
id: hi-sdx-rel-parallel-correlated
node: more.reliability
type: qa
step: 2
---
## Q
**两个 99.9% 副本为什么不是六个九**｜补充 · 可靠性 · 必会

面试官：「单个实例可用性 99.9%。串联依赖两个这样的服务，整体可用性是多少？并联部署两个副本呢？公式算出来是六个九，为什么真实系统远达不到？」

## A
**结论。** 串联相乘：两个 99.9% 是 99.8%。并联是 1−(1−A)²：两个副本得 99.9999%，但前提是故障互相独立，真实故障常常相关，所以实际远低于六个九。

**要点。**
- **串联相乘：** 0.999×0.999≈99.8%，每多一个硬依赖就少一个九的零头。
- **并联公式：** 1−(0.001)²=99.9999%，只有两个副本不会同时坏才成立。
- **共享命运：** 同机架、同可用区、同负载均衡、同云控制面，一次故障带走全部副本。
- **同一份软件：** 一次坏发布或坏配置同时推给所有副本，这是最常见的相关故障。
- **负载耦合：** 一个副本死了，流量压到存活者上，把它也压垮，形成级联。
- **恢复独立性：** 副本分散到不同故障域（可用区、区域），发布分批错开，冗余路径上去掉共享的硬依赖。

**为什么。** 公式里的「独立」是假设，不是事实。冗余买到的只是对独立故障的保护，对相关故障要靠分散故障域和分批发布来买。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="20" y="10" width="130" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 A</text>
<text x="85" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<rect x="190" y="10" width="130" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 B</text>
<text x="255" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">99.9%</text>
<text x="104" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">独立时 99.9999%</text>
<rect x="20" y="98" width="300" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共享命运</text>
<text x="170" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一次发布 · 同一可用区 · 同一控制面</text>
<polyline points="85,98 85,54" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,54 88.0,60.3 82.0,60.3" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="255,98 255,54" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,54 258.0,60.3 252.0,60.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共享层一坏，两个副本同时消失，</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并联公式不再成立。</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对策：分散可用区，分批发布。</text>
</svg>

**面试里这样说。** 「并联的六个九假设故障独立。真实里同一次发布、同一个可用区、同一个控制面会同时带走所有副本，所以我把副本放在不同可用区，发布按批错开，不让两份副本同时换版本。」

**易错。**
- **把公式当承诺：** 按六个九做容量和赔付规划，第一次相关故障就违约。
- **两个副本同机房：** 冗余形同虚设，机房断电全部消失。
- **同时发布所有副本：** 冗余挡不住软件缺陷，反而一次放大全部。
