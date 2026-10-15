/**
 * J19 例 1：JIT 预热与分层编译。同一个方法 work() 被反复调用，每一轮测每次调用的平均耗时：
 * 前几轮在解释器 / C1 里慢，后面 C2 编译完成后变快。
 * 观察编译事件：java --enable-preview -XX:+PrintCompilation J19Ex1Jit | grep J19Ex1Jit::work
 * 对照稳态速度： -Xint（只解释） / -XX:TieredStopAtLevel=1（只用 C1） / 默认（C1 -> C2）
 */
public class J19Ex1Jit {
    static long work(long x) {
        // 一小段有分支、有算术的代码；足够热才会被 C2 编译
        long acc = x;
        for (int i = 0; i < 50; i++) {
            acc = acc * 31 + (i ^ (acc >>> 7));
            if ((acc & 1) == 0) acc += i; else acc -= i;
        }
        return acc;
    }

    public static void main(String[] args) {
        long sink = 0;
        for (int round = 1; round <= 14; round++) {
            int calls = round <= 9 ? 25 << round : 400_000;       // 前 9 轮调用次数逐轮翻倍：50, 100, 200, ... 12800
            long t0 = System.nanoTime();
            for (int i = 0; i < calls; i++) sink += work(i);
            long ns = System.nanoTime() - t0;
            System.out.printf("round %2d: %,8d 次调用, 平均 %7.1f ns/次%n", round, calls, (double) ns / calls);
        }
        System.out.println("sink=" + sink);   // 用掉结果，防止整段被当作死代码消除
    }
}
