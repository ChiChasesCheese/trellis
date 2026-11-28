---
id: hi-sdx-unknown-field-loss
node: more.encoding
type: qa
step: 5
---
## Q
**昵称莫名其妙变空：未知字段丢失**｜补充 · 编码与模式演进（Encoding & Evolution） · 追问

面试官：「滚动升级时，新代码给用户记录加了 `nickname` 字段。用户设置了昵称，过一阵有的又变回空，日志里没有任何错误。你怎么推出原因？」

## A
**结论。** 旧实例读到带 `nickname` 的新记录，解码时跳过了这个未知字段，改了别的字段后把整条记录写回，`nickname` 就悄悄没了。前向兼容只在读取时成立还不够。

**要点。**
- **第一步：** 新实例写入带 `nickname` 的记录。
- **第二步：** 旧实例读取，解码器容忍地跳过未知字段，不报错。
- **第三步：** 旧实例把记录解码成自己的模型对象，模型里没有 `nickname` 的位置。
- **第四步：** 它修改了别的字段，把整条记录写回，`nickname` 永久丢失。
- **规律：** 任何读—改—写路径都必须在往返中保留不认识的字段。Protobuf 解码时会保留未知字段并在重新序列化时带回（3.5 起默认如此，但转成 JSON 再写回会丢）；ORM 和手写模型类最容易丢掉没映射的字段。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="40" y="8" width="260" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 新实例写入</text>
<text x="170.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">{name, nickname}</text>
<rect x="40" y="78" width="260" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 旧实例读取</text>
<text x="170.0" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nickname 未知，被跳过</text>
<rect x="40" y="148" width="260" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 旧实例改 name</text>
<text x="170.0" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">模型里没有 nickname</text>
<rect x="40" y="218" width="260" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="237.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 整条写回</text>
<text x="170.0" y="252.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">{name}  nickname 没了</text>
<polyline points="170,54 170.0,79.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,86 166.8,79.0 173.2,79.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,124 170.0,149.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,156 166.8,149.0 173.2,149.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,194 170.0,219.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,226 166.8,219.0 173.2,219.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="288" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读时不报错，所以日志里什么都没有</text>
<text x="8" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读改写要保留不认识的字段</text>
<text x="8" y="324" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">或只做字段级更新</text>
</svg>

**面试里这样说。** 「这是未知字段的往返丢失：旧实例读到新字段时跳过，改完再整条写回，字段就没了。我会让读改写路径保留未知字段，或者只做字段级的局部更新，而不是写回整个模型。」

**易错。**
- **只验证读不报错：** 不报错不等于不丢，这个缺陷本来就不报错。
- **用 JSON 做中转：** 反序列化到固定模型再序列化，没有映射的字段全丢。
