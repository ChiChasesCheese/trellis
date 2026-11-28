---
id: bagu-java-reflection-proxy-spi-1-proxy-spi-serialization
node: b.runtime.java-reflection-proxy-spi
type: qa
step: 1
---
## Q
**反射、动态代理、SPI 与序列化选型**｜加分

面试官：「JDK 动态代理和 CGLIB 有什么区别？SPI 和 API 有何不同？RPC 序列化怎么选？」

## A
**基本回答。** JDK 动态代理基于接口：运行时生成实现接口的代理类，调用都转进 `InvocationHandler`；代理对象 `instanceof` 实现类为 false，只能转成接口。CGLIB 生成目标类的子类、重写方法插逻辑，不需要接口，但 final 类和 final 方法代理不了；目标没有接口时只能用它。反射是运行时查看并调用类成员，比直接调用慢，还能绕过 private。SPI 的接口由调用方定义、第三方提供实现，靠 `META-INF/services/<接口>` 和 `ServiceLoader` 发现（JDBC 驱动就是）；API 则是实现方提供、调用方使用。RPC 内部选 Protobuf（紧凑、快、跨语言，字段编号做兼容），对外开放接口选 JSON；JDK `Serializable` 体积大、慢、只限 Java，还有反序列化安全风险。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 318">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JDK 动态代理（要有接口）</text>
<text x="185" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CGLIB（生成子类）</text>
<rect x="10" y="26" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="85.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接口 PayService</text>
<rect x="185" y="26" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目标类 PayImpl</text>
<rect x="10" y="78" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代理类 $Proxy</text>
<text x="85.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（实现接口）</text>
<rect x="185" y="78" width="150" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子类（重写方法）</text>
<text x="260.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PayImpl$$CGLIB</text>
<line x1="85" y1="78" x2="85" y2="52" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="85.0,52.0 87.9,58.4 82.1,58.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="260" y1="78" x2="260" y2="52" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="260.0,52.0 262.9,58.4 257.1,58.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="85" y1="118" x2="85" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,146.0 82.1,139.6 87.9,139.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="146" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="163.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">InvocationHandler</text>
<line x1="85" y1="172" x2="85" y2="192" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,192.0 82.1,185.6 87.9,185.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="192" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="209.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目标对象</text>
<text x="185" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">final 类、final 方法</text>
<text x="185" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不能被子类重写，</text>
<text x="185" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以代理不了</text>
<line x1="10" y1="232" x2="330" y2="232" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SPI：调用方定义接口，第三方提供实现</text>
<rect x="6" y="262" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调用方的接口</text>
<rect x="118" y="262" width="96" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="166.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ServiceLoader</text>
<rect x="230" y="262" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="280.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第三方实现</text>
<line x1="102" y1="276" x2="118" y2="276" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,276.0 111.6,278.9 111.6,273.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="214" y1="276" x2="230" y2="276" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,276.0 223.6,278.9 223.6,273.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="10" y="310" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实现类名写在 META-INF/services/&lt;接口名&gt; 里</text>
</svg>
上半部分对比两种代理：JDK 代理造一个实现同一接口的新类，调用转进 InvocationHandler；CGLIB 造目标类的子类。下半部分是 SPI：接口在调用方手里，实现由第三方 jar 提供。
**举个例子。** 给 `PayService.pay()` 加日志：JDK 代理的类是 `$Proxy` 开头的运行时生成类，转成 `PayImpl` 会报错，`p.pay()` 进 `InvocationHandler` 先打日志再反射调目标；`PayImpl` 没有接口时 CGLIB 生成 `PayImpl$$CGLIB` 重写 `pay()`，`pay()` 若是 final 就做不到。Protobuf 给消息新增字段用新编号：旧服务忽略不认识的编号，新服务读旧消息得默认值，新旧仍能互相解析。
**容易错。**
- **把 SPI 当成 API：** 方向相反，接口在调用方，实现由第三方提供。
- **以为 CGLIB 什么类都能代理：** final 类、final 方法不行。
