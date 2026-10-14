import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

/**
 * 讲义 ld01 §4 的实验：同一个 SPSC 环形缓冲区的五种写法，一个生产者线程 + 一个消费者线程，每种传 5000 万个 long，看吞吐。
 *
 *   A  volatile    : head / tail 是 volatile 字段，每次 offer / poll 都读对方的 volatile；四个热字段挤在一起
 *   B  acq/rel     : 改用 VarHandle 的 setRelease / getAcquire（不用 volatile 的全栅栏）；仍然每次读对方的下标；字段挤在一起
 *   C  acq/rel+pad : B + 填充（生产者字段与消费者字段相隔 128 字节）
 *   D  acq/rel+cache: B + 缓存对方下标（cached index）；字段仍挤在一起
 *   E  acq/rel+cache+pad : D + 填充 —— 就是 reference/SpscLongRing 的写法
 *
 * poll 用 Long.MIN_VALUE 当「空」的哨兵（本实验只发正数），省掉 isEmpty() 的重复读，让五个版本公平。
 *
 * 编译 / 运行（在 kit 根目录）：
 *   javac --release 21 -d /tmp/ld01b study/30-articles/examples/ld01/SpscBench.java
 *   java -cp /tmp/ld01b SpscBench
 */
public class SpscBench {
    static final long EMPTY = Long.MIN_VALUE;
    static final int CAP = 1024;
    static final long N = 50_000_000L;

    interface Q { boolean offer(long v); long poll(); }

    // ───── A：volatile ─────
    static final class A implements Q {
        final long[] buf = new long[CAP];
        volatile long head, tail;
        public boolean offer(long v) {
            long t = tail;
            if (t - head == CAP) return false;
            buf[(int) (t & (CAP - 1))] = v;
            tail = t + 1;                       // volatile 写
            return true;
        }
        public long poll() {
            long h = head;
            if (h == tail) return EMPTY;
            long v = buf[(int) (h & (CAP - 1))];
            head = h + 1;
            return v;
        }
    }

    // ───── B：acquire / release，字段挤在一起 ─────
    static class BFields { long tail, head; }
    static final VarHandle B_TAIL, B_HEAD, D_TAIL, D_HEAD, C_TAIL, C_HEAD, E_TAIL, E_HEAD;
    static {
        try {
            var l = MethodHandles.lookup();
            B_TAIL = l.findVarHandle(BFields.class, "tail", long.class);
            B_HEAD = l.findVarHandle(BFields.class, "head", long.class);
            D_TAIL = l.findVarHandle(DFields.class, "tail", long.class);
            D_HEAD = l.findVarHandle(DFields.class, "head", long.class);
            C_TAIL = l.findVarHandle(CProd.class, "tail", long.class);
            C_HEAD = l.findVarHandle(CCons.class, "head", long.class);
            E_TAIL = l.findVarHandle(EProd.class, "tail", long.class);
            E_HEAD = l.findVarHandle(ECons.class, "head", long.class);
        } catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
    }
    static final class B extends BFields implements Q {
        final long[] buf = new long[CAP];
        public boolean offer(long v) {
            long t = tail;
            if (t - (long) B_HEAD.getAcquire(this) == CAP) return false;
            buf[(int) (t & (CAP - 1))] = v;
            B_TAIL.setRelease(this, t + 1);
            return true;
        }
        public long poll() {
            long h = head;
            if (h == (long) B_TAIL.getAcquire(this)) return EMPTY;
            long v = buf[(int) (h & (CAP - 1))];
            B_HEAD.setRelease(this, h + 1);
            return v;
        }
    }

    // ───── C：acquire / release + 填充，不缓存 ─────
    static class CPad0 { long p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15; }
    static class CProd extends CPad0 { long tail; }
    static class CPad1 extends CProd { long q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15; }
    static class CCons extends CPad1 { long head; }
    static final class C extends CCons implements Q {
        final long[] buf = new long[CAP];
        public boolean offer(long v) {
            long t = ((CProd) this).tail;
            if (t - (long) C_HEAD.getAcquire(this) == CAP) return false;
            buf[(int) (t & (CAP - 1))] = v;
            C_TAIL.setRelease(this, t + 1);
            return true;
        }
        public long poll() {
            long h = head;
            if (h == (long) C_TAIL.getAcquire(this)) return EMPTY;
            long v = buf[(int) (h & (CAP - 1))];
            C_HEAD.setRelease(this, h + 1);
            return v;
        }
    }

    // ───── D：acquire / release + 缓存，字段挤在一起 ─────
    static class DFields { long tail, cachedHead, head, cachedTail; }
    static final class D extends DFields implements Q {
        final long[] buf = new long[CAP];
        public boolean offer(long v) {
            long t = tail;
            if (t - cachedHead == CAP) {
                cachedHead = (long) D_HEAD.getAcquire(this);
                if (t - cachedHead == CAP) return false;
            }
            buf[(int) (t & (CAP - 1))] = v;
            D_TAIL.setRelease(this, t + 1);
            return true;
        }
        public long poll() {
            long h = head;
            if (h == cachedTail) {
                cachedTail = (long) D_TAIL.getAcquire(this);
                if (h == cachedTail) return EMPTY;
            }
            long v = buf[(int) (h & (CAP - 1))];
            D_HEAD.setRelease(this, h + 1);
            return v;
        }
    }

    // ───── E：acquire / release + 缓存 + 填充 ─────
    static class EPad0 { long p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15; }
    static class EProd extends EPad0 { long tail, cachedHead; }
    static class EPad1 extends EProd { long q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15; }
    static class ECons extends EPad1 { long head, cachedTail; }
    static final class E extends ECons implements Q {
        final long[] buf = new long[CAP];
        public boolean offer(long v) {
            long t = tail;
            if (t - cachedHead == CAP) {
                cachedHead = (long) E_HEAD.getAcquire(this);
                if (t - cachedHead == CAP) return false;
            }
            buf[(int) (t & (CAP - 1))] = v;
            E_TAIL.setRelease(this, t + 1);
            return true;
        }
        public long poll() {
            long h = head;
            if (h == cachedTail) {
                cachedTail = (long) E_TAIL.getAcquire(this);
                if (h == cachedTail) return EMPTY;
            }
            long v = buf[(int) (h & (CAP - 1))];
            E_HEAD.setRelease(this, h + 1);
            return v;
        }
    }

    static double run(Q q) throws Exception {
        long t0 = System.nanoTime();
        Thread p = new Thread(() -> {
            for (long i = 1; i <= N; i++) while (!q.offer(i)) Thread.onSpinWait();
        });
        p.start();
        long sum = 0;
        for (long i = 1; i <= N; i++) {
            long v;
            while ((v = q.poll()) == EMPTY) Thread.onSpinWait();
            sum += v;
        }
        p.join();
        if (sum != N * (N + 1) / 2) throw new AssertionError("lost or duplicated messages");
        return N / ((System.nanoTime() - t0) / 1e9) / 1e6;
    }

    public static void main(String[] args) throws Exception {
        String[] names = {"A volatile", "B acq/rel", "C acq/rel+pad", "D acq/rel+cache", "E acq/rel+cache+pad"};
        double[] best = new double[5];
        for (int rep = 0; rep < 6; rep++) {                      // 第 0 轮预热，不计入
            Q[] qs = {new A(), new B(), new C(), new D(), new E()};
            for (int i = 0; i < qs.length; i++) {
                double mps = run(qs[i]);
                if (rep > 0) best[i] = Math.max(best[i], mps);
            }
        }
        System.out.println("百万消息/秒（每种 5 轮取最好），容量 " + CAP + "，每轮 " + N / 1_000_000 + "M 条");
        for (int i = 0; i < 5; i++) System.out.printf("  %-22s %8.1f%n", names[i], best[i]);
    }
}
