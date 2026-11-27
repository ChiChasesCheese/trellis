---
id: reliability-testing-cache-state-matrix
node: reliability.testing
type: qa
---
## Q
What integration-test matrix is the minimum for a stale-while-revalidate cache, beyond one HIT and one MISS test?

## A
Cover absent, fresh, stale-within-window, and too-stale entries against origin success, `304`, timeout, and error. Assert response body, status, `Age`/cache headers, whether the caller blocks, origin call count under concurrency, and the stored value after background work. Include cancellation and failed regeneration so a partial response never replaces the last good object.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 118" font-family="sans-serif" font-size="10">
<text x="4" y="14" fill="currentColor">entry ↓  origin →</text>
<text x="145" y="14" text-anchor="middle" fill="currentColor">success</text>
<text x="191" y="14" text-anchor="middle" fill="currentColor">304</text>
<text x="237" y="14" text-anchor="middle" fill="currentColor">timeout</text>
<text x="283" y="14" text-anchor="middle" fill="currentColor">error</text>
<text x="4" y="37" fill="currentColor">absent</text>
<rect x="122" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="33.5" r="3" fill="currentColor"/>
<rect x="168" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="33.5" r="3" fill="currentColor"/>
<rect x="214" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="33.5" r="3" fill="currentColor"/>
<rect x="260" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="33.5" r="3" fill="currentColor"/>
<text x="4" y="60" fill="currentColor">fresh</text>
<rect x="122" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="56.5" r="3" fill="currentColor"/>
<rect x="168" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="56.5" r="3" fill="currentColor"/>
<rect x="214" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="56.5" r="3" fill="currentColor"/>
<rect x="260" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="56.5" r="3" fill="currentColor"/>
<text x="4" y="83" fill="currentColor">stale-within-window</text>
<rect x="122" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="79.5" r="3" fill="currentColor"/>
<rect x="168" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="79.5" r="3" fill="currentColor"/>
<rect x="214" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="79.5" r="3" fill="currentColor"/>
<rect x="260" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="79.5" r="3" fill="currentColor"/>
<text x="4" y="106" fill="currentColor">too-stale</text>
<rect x="122" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="102.5" r="3" fill="currentColor"/>
<rect x="168" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="102.5" r="3" fill="currentColor"/>
<rect x="214" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="102.5" r="3" fill="currentColor"/>
<rect x="260" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="102.5" r="3" fill="currentColor"/>
</svg>

## Q zh
对于 stale-while-revalidate cache，除了一个 HIT 和一个 MISS test，最小 integration-test matrix 还应包括什么？

## A zh
用 origin success、`304`、timeout 和 error 分别覆盖 absent、fresh、stale-within-window 与 too-stale entry。断言 response body、status、`Age`/cache header、caller 是否 block、并发下的 origin call count，以及 background work 后保存的 value。还要覆盖 cancellation 和 failed regeneration，确保 partial response 永远不会替换 last good object。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 118" font-family="sans-serif" font-size="10">
<text x="4" y="14" fill="currentColor">entry ↓  origin →</text>
<text x="145" y="14" text-anchor="middle" fill="currentColor">success</text>
<text x="191" y="14" text-anchor="middle" fill="currentColor">304</text>
<text x="237" y="14" text-anchor="middle" fill="currentColor">timeout</text>
<text x="283" y="14" text-anchor="middle" fill="currentColor">error</text>
<text x="4" y="37" fill="currentColor">absent</text>
<rect x="122" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="33.5" r="3" fill="currentColor"/>
<rect x="168" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="33.5" r="3" fill="currentColor"/>
<rect x="214" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="33.5" r="3" fill="currentColor"/>
<rect x="260" y="22" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="33.5" r="3" fill="currentColor"/>
<text x="4" y="60" fill="currentColor">fresh</text>
<rect x="122" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="56.5" r="3" fill="currentColor"/>
<rect x="168" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="56.5" r="3" fill="currentColor"/>
<rect x="214" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="56.5" r="3" fill="currentColor"/>
<rect x="260" y="45" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="56.5" r="3" fill="currentColor"/>
<text x="4" y="83" fill="currentColor">stale-within-window</text>
<rect x="122" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="79.5" r="3" fill="currentColor"/>
<rect x="168" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="79.5" r="3" fill="currentColor"/>
<rect x="214" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="79.5" r="3" fill="currentColor"/>
<rect x="260" y="68" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="79.5" r="3" fill="currentColor"/>
<text x="4" y="106" fill="currentColor">too-stale</text>
<rect x="122" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="145" cy="102.5" r="3" fill="currentColor"/>
<rect x="168" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="191" cy="102.5" r="3" fill="currentColor"/>
<rect x="214" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="237" cy="102.5" r="3" fill="currentColor"/>
<rect x="260" y="91" width="46" height="23" fill="none" stroke="currentColor"/>
<circle cx="283" cy="102.5" r="3" fill="currentColor"/>
</svg>
