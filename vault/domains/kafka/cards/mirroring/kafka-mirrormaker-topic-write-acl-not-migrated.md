---
id: kafka-mirrormaker-topic-write-acl-not-migrated
node: mirroring.mirrormaker
type: qa
step: 4
source: kafka-2e
---
## Q
MirrorMaker 会把源主题的配置信息和访问控制列表（ACL）一并迁移到目标主题，但源主题上关于「谁能写入这个主题」的 `Topic:Write` 权限，默认却不会被迁移到目标集群。这样设计的用意是什么？

## A
如果把源主题原有的 `Topic:Write` 权限原样复制到目标集群，那么原本只能写源主题的那些生产者，理论上也会被允许直接写入目标主题（灾备/镜像集群），这就破坏了「目标集群上的数据只应该来自镜像流程本身」这个前提——万一有生产者绕过源集群直接写到目标主题，会造成目标集群数据与源集群不一致，且这类写入根本不会被再镜像回源集群。默认不迁移 `Topic:Write` 权限，就保证了在正常运行期间，只有 MirrorMaker 自己能写入目标主题；等真正发生故障转移、应用要切换到目标集群时，再显式地为这些应用单独授予写入权限。
