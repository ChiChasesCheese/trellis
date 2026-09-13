---
id: cache-freshness-s-maxage
node: caching.freshness
type: qa
---
## Q
You want browsers to revalidate HTML immediately but let the CDN reuse it for 60 seconds. Which response policy captures that split?

## A
Use a shared-cache override such as `Cache-Control: max-age=0, s-maxage=60` plus a validator. `max-age` governs private and shared caches unless overridden; `s-maxage` applies to shared caches. Verify actual CDN support and emitted `Age`, because vendor configuration can override origin headers.

## Q zh
希望 browser 立即 revalidate HTML，但允许 CDN 复用 60 秒。哪个 response policy 能表达这种差异？

## A zh
使用 shared-cache override，例如 `Cache-Control: max-age=0, s-maxage=60`，并提供 validator。`max-age` 默认控制 private/shared cache，`s-maxage` 对 shared cache 覆盖它。还要验证 CDN 的实际支持与输出 `Age`，因为 vendor configuration 可能覆盖 origin header。
