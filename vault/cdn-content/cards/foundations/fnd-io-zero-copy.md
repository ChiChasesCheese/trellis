---
id: fnd-io-zero-copy
node: foundations.os-io
type: qa
---
## Q
A static-file server is CPU-bound copying large bodies between kernel and user space. When does a zero-copy path help, and when does it not?

## A
`sendfile`-style zero-copy can move file-backed bytes from page cache to a socket without a user-space copy, reducing CPU and memory bandwidth. It helps immutable pass-through bodies. It does not remove disk/network cost, and it stops being a clean fit when the body must be decrypted, compressed, resized, or otherwise transformed in user space.

## Q zh
静态文件服务因为在 kernel 与 user space 之间复制大响应体而 CPU-bound。zero-copy 什么时候有用，什么时候没用？

## A zh
`sendfile` 一类 zero-copy 可以把 file-backed bytes 从 page cache 直接送到 socket，避免一次 user-space copy，降低 CPU 与 memory bandwidth。它适合 immutable pass-through body；但不会消除 disk/network 成本，而且当响应体需要 decrypt、compress、resize 或其他 user-space transformation 时就不再适合。
