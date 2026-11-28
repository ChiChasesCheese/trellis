---
id: hi-sdx-arch-expand-contract-api
node: more.architecture
type: qa
step: 5
---
## Q
**破坏性改动：先扩展再收缩**｜补充 · 服务架构：微服务、服务发现、Serverless · 追问

面试官：「你要重命名一个字段，还要改变它的含义，调用方是你管不到的外部团队，各自按自己的节奏发布。怎么迁移？」

## A
**结论。** 用并行变更（parallel change）：先扩展，新旧形状同时提供；再迁移，调用方按自己的节奏搬，你按调用方统计旧形状的用量；用量归零才收缩，删掉旧形状。再用消费者驱动的契约测试（如 Pact）把「有没有弄坏谁」变成 CI 里的失败。

**要点。**
- **扩展：** 新字段或新端点与旧的并存，服务端双写或做翻译。
- **迁移：** 给旧形状加按调用方统计的用量指标，催具体的团队，不靠群发公告。
- **收缩：** 遥测显示零调用者之后，先公告再删；删之前可以先返回弃用提示头。
- **契约测试：** 每个调用方登记自己真正用到的请求和字段，提供方的 CI 在合并前先跑这些契约。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<rect x="8" y="10" width="100" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扩展</text>
<text x="58.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新旧形状</text>
<text x="58.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并存</text>
<rect x="120" y="10" width="100" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">迁移</text>
<text x="170.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用方自己搬</text>
<text x="170.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">盯旧形状用量</text>
<rect x="232" y="10" width="100" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收缩</text>
<text x="282.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用量归零</text>
<text x="282.0" y="57.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">才删旧形状</text>
<polyline points="108,38 113.0,38.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120,38 113.0,41.2 113.0,34.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="220,38 225.0,38.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="232,38 225.0,41.2 225.0,34.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">护栏：消费者驱动契约测试</text>
<text x="8" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个调用方登记自己真正用到的字段，</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提供方的 CI 在合并前就跑一遍：</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">弄坏任何调用方的改动，构建直接失败</text>
<line x1="8" y1="170" x2="332" y2="170" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">顺序：先加，再搬，最后删；</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用量没归零就不删。</text>
</svg>

**面试里这样说。** 「我不会一次性切换。先让新旧字段并存，按调用方盯旧字段的用量；用量归零才删。同时让各调用方把依赖的字段登记成契约测试，谁的改动会弄坏别人，CI 当场就红。」

**易错。**
- **靠公告等所有人迁完：** 总有人不看，只有按调用方的用量数据才知道能不能删。
- **契约写成整份 schema：** 任何改动都会让契约失败；契约只写调用方真正用到的字段。
