---
id: delivery-cicd-promote-artifact
node: delivery.cicd
type: qa
---
## Q
Why should production receive the exact artifact tested in staging instead of rebuilding the same Git commit?

## A
A rebuild can change dependencies, toolchains, timestamps, generated assets, or supply-chain inputs even at the same commit. Build once, record source revision and builder provenance, sign or digest the immutable artifact, then promote that identity through environments. Environment-specific configuration should be separate, versioned, and validated—not baked by an unrepeatable rebuild.

## Q zh
为什么 production 应接收 staging 测过的完全相同 artifact，而不是重新 build 同一个 Git commit？

## A zh
即使 commit 相同，rebuild 也可能改变 dependency、toolchain、timestamp、generated asset 或 supply-chain input。应 build once，记录 source revision 与 builder provenance，对 immutable artifact 做 signature 或 digest，然后在 environment 间 promote 同一 identity。environment-specific config 应独立、versioned 且经过验证，而不是通过不可重复的 rebuild bake 进去。
