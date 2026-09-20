---
id: problems-e-commerce-reservation-timing-tradeoff
node: problems.commerce.e-commerce
type: qa
step: 5
tags: [grown]
---
## Q
In an e-commerce design, why is reserving inventory at checkout-start (with a short TTL) preferred over reserving at add-to-cart or only decrementing after payment succeeds?

## A
Reserving at add-to-cart locks stock for the entire cart dwell time (minutes to days), creating widespread phantom out-of-stock on popular items. Waiting until payment succeeds to decrement allows two concurrent buyers to both receive a successful-payment confirmation for the last unit before either decrement runs, causing oversell that can only be fixed by an after-the-fact refund. Reserving with a short TTL (roughly the time to fill out a payment form, ~10-15 minutes) at the moment checkout starts bounds the phantom-stock window to that short interval while still using a strongly-consistent conditional update, so checkout-time oversell is prevented without long-lived stock lockup.

## Q zh
在电商设计中，为什么在结账开始时（带短 TTL）预留库存比加购时预留或只在支付成功后才扣减更好？

## A zh
加购时锁定库存会占用整个购物车停留时间（几十分钟到几天），在热门商品上造成大范围'假库存'。等支付成功才扣减,会让两个并发买家在任一方扣减执行前都收到最后一件库存的支付成功确认，造成只能靠事后退款解决的超卖。在结账开始那一刻用短 TTL（大约是填写支付表单的时间，10-15 分钟）预留，把假库存窗口压缩到这个短区间内，同时仍然使用强一致的条件更新，从而在不长期锁定库存的前提下防止结账时刻的超卖。
