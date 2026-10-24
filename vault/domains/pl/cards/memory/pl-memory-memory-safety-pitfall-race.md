---
id: pl-memory-memory-safety-pitfall-race
node: memory.memory-safety
type: qa
step: 6
---
## Q
有 GC 的 Go 为什么仍然可能出现内存安全问题？怎么用工具发现数据竞争？

## A
GC 解决了「释放后使用」，但没有解决「多个线程同时读写同一块内存」。下面这段 Go 代码编译通过：

```go
n := 0
done := make(chan bool)
for i := 0; i < 2; i++ {
	go func() {
		for j := 0; j < 1000; j++ { n++ }   // unsynchronised read-modify-write
		done <- true
	}()
}
<-done; <-done
fmt.Println(n)
```

`n++` 是读、加、写三步，两个 goroutine 交错就会丢失更新，理论上结果可能小于 2000。直接运行时常常看到 2000，这恰恰是危险之处：bug 藏在偶发里。

加上 `-race` 运行：

```console
$ go run -race r.go
WARNING: DATA RACE
Read at 0x00c000012148 by goroutine 8:
  main.main.func1()
Previous write at 0x00c000012148 by goroutine 7:
  main.main.func1()
```

race detector 在运行时记录每次内存访问，发现没有同步关系的并发读写就报告，附带两处调用栈。限制：它只报告实际执行到的路径，有 2 到 20 倍的运行开销，所以放在测试和 CI 里跑，不放在生产。

更危险的是撕裂：对一个接口值或 slice 头（多字）做竞争写入，读者可能读到一半旧一半新，指针和类型对不上，造成真正的内存破坏。

修复手段是使用同步：`sync.Mutex`、`sync/atomic`、或通过 channel 传递所有权。Rust 对应的错误无法通过编译，Java 同样的 `count++` 虽然不会损坏 JVM，也会丢失更新。
