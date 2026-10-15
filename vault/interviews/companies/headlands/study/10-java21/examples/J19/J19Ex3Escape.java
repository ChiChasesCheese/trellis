import java.lang.management.ManagementFactory;

/**
 * J19 例 3：逃逸分析（escape analysis）与标量替换。每次循环 new 一个 Point，但它不"逃出"方法 ->
 * JIT 可以根本不在堆上分配它，把两个字段当作两个局部变量（标量替换）。
 * 对比：默认  vs  -XX:-DoEscapeAnalysis（关掉逃逸分析）
 * 用 com.sun.management.ThreadMXBean 读本线程累计分配的字节数。
 */
public class J19Ex3Escape {
    record Point(long x, long y) {}

    static long sumNoEscape(int n) {
        long s = 0;
        for (int i = 0; i < n; i++) {
            Point p = new Point(i, i + 1);         // p 只在这里用，没有存进字段/集合/返回值 -> 不逃逸
            s += p.x() + p.y();
        }
        return s;
    }

    static Point leaked;
    static long sumEscape(int n) {
        long s = 0;
        for (int i = 0; i < n; i++) {
            Point p = new Point(i, i + 1);
            leaked = p;                             // 存进静态字段 -> 逃逸，必须在堆上真分配
            s += p.x() + p.y();
        }
        return s;
    }

    public static void main(String[] args) {
        var tmx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
        long tid = Thread.currentThread().threadId();
        int n = 20_000_000;
        sumNoEscape(2_000_000); sumEscape(2_000_000);          // 预热，让 C2 编译

        long b0 = tmx.getThreadAllocatedBytes(tid);
        long r1 = sumNoEscape(n);
        long b1 = tmx.getThreadAllocatedBytes(tid);
        long r2 = sumEscape(n);
        long b2 = tmx.getThreadAllocatedBytes(tid);
        System.out.printf("不逃逸: 分配 %,d 字节 (%.1f 字节/次)   逃逸: 分配 %,d 字节 (%.1f 字节/次)   (结果相同: %b)%n",
                b1 - b0, (double) (b1 - b0) / n, b2 - b1, (double) (b2 - b1) / n, r1 == r2);
    }
}
