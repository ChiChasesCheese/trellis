import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

/**
 * J16 例 4：VarHandle——用 release/acquire 发布数据；用 CAS 做原子更新。
 * 场景 A：单写者发布一个 (price, qty) 快照，读者不加锁；
 * 场景 B：单生产者-单消费者环形队列（SPSC ring），head/tail 用 acquire/release，数据槽用普通数组。
 */
public class J16Ex4VarHandle {
    // ---- 场景 A：release / acquire 发布 ----
    static final class Box {
        long price;                 // 普通字段（没有 volatile）
        long qty;
        int ready;                  // 只通过 VarHandle 访问
        static final VarHandle READY;
        static {
            try { READY = MethodHandles.lookup().findVarHandle(Box.class, "ready", int.class); }
            catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
        }
        void publish(long p, long q) {
            price = p; qty = q;                    // 1. 先写数据（普通写）
            READY.setRelease(this, 1);             // 2. release 写：保证 1 不会被重排到它后面
        }
        boolean tryRead(long[] out) {
            if ((int) READY.getAcquire(this) == 0) return false;   // acquire 读：保证它后面的读不会被重排到前面
            out[0] = price; out[1] = qty;                          // 一定看到 publish 里写的值
            return true;
        }
    }

    // ---- 场景 B：SPSC 环形队列 ----
    static final class SpscRing {
        private final long[] buf;
        private final int mask;
        private long head;   // 消费者推进（只有消费者写）
        private long tail;   // 生产者推进（只有生产者写）
        static final VarHandle HEAD, TAIL;
        static {
            try {
                var l = MethodHandles.lookup();
                HEAD = l.findVarHandle(SpscRing.class, "head", long.class);
                TAIL = l.findVarHandle(SpscRing.class, "tail", long.class);
            } catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
        }
        SpscRing(int capacityPow2) { buf = new long[capacityPow2]; mask = capacityPow2 - 1; }

        boolean offer(long v) {                                   // 仅生产者线程调用
            long t = tail;                                        // 自己写的，普通读即可
            long h = (long) HEAD.getAcquire(this);                // 读对方的进度：acquire
            if (t - h == buf.length) return false;               // 满
            buf[(int) (t & mask)] = v;                            // 先写数据
            TAIL.setRelease(this, t + 1);                         // 再 release 发布 tail
            return true;
        }
        long poll() {                                             // 仅消费者线程调用；空返回 Long.MIN_VALUE
            long h = head;
            long t = (long) TAIL.getAcquire(this);                // acquire：看到 tail 就一定能看到之前写的数据
            if (h == t) return Long.MIN_VALUE;
            long v = buf[(int) (h & mask)];
            HEAD.setRelease(this, h + 1);                         // 归还槽位
            return v;
        }
    }

    public static void main(String[] args) throws Exception {
        // 场景 A
        Box box = new Box();
        Thread w = new Thread(() -> box.publish(18950, 100));
        long[] out = new long[2];
        w.start();
        while (!box.tryRead(out)) Thread.onSpinWait();
        w.join();
        System.out.println("场景 A 读到 price=" + out[0] + " qty=" + out[1]);

        // 场景 B：生产 5,000,000 个数，消费者求和；校验和
        final int N = 5_000_000;
        SpscRing ring = new SpscRing(1 << 12);
        Thread prod = new Thread(() -> { for (long i = 1; i <= N; i++) while (!ring.offer(i)) Thread.onSpinWait(); });
        long[] sum = {0};
        Thread cons = new Thread(() -> {
            long got = 0;
            while (got < N) { long v = ring.poll(); if (v == Long.MIN_VALUE) { Thread.onSpinWait(); continue; } sum[0] += v; got++; }
        });
        long t0 = System.nanoTime();
        prod.start(); cons.start(); prod.join(); cons.join();
        long ms = (System.nanoTime() - t0) / 1_000_000;
        long expect = (long) N * (N + 1) / 2;
        System.out.println("场景 B SPSC: 和=" + sum[0] + " 期望=" + expect + " 一致=" + (sum[0] == expect) + "，约 " + ms + " ms（无锁，只用 release/acquire）");
    }
}
