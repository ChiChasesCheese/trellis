import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.*;

/**
 * J16 例 5：CAS 与 ABA。
 *   第 1 部分：CAS 循环——"读-算-比较并交换"，失败重试（用 AtomicLong.updateAndGet / compareAndSet 手写）
 *   第 2 部分：Treiber 无锁栈 + 一个确定性的 ABA 复现（用 latch 控制交错），再用 AtomicStampedReference 修复
 */
public class J16Ex5Cas {
    // ---------- 第 1 部分 ----------
    static long casMax(AtomicLong cur, long candidate) {
        long prev;
        do {
            prev = cur.get();
            if (candidate <= prev) return prev;                 // 不需要更新
        } while (!cur.compareAndSet(prev, candidate));         // 别人改过 cur -> 失败 -> 重读重试
        return candidate;
    }

    // ---------- 第 2 部分 ----------
    static final class Node {
        final String name; Node next;
        Node(String n) { name = n; }
        public String toString() { return name; }
    }

    /** 有 ABA 缺陷的版本：只比较引用 */
    static final class NaiveStack {
        final AtomicReference<Node> top = new AtomicReference<>();
        void push(Node n) { Node t; do { t = top.get(); n.next = t; } while (!top.compareAndSet(t, n)); }
        Node pop(Runnable afterRead) {
            Node t, nx;
            do {
                t = top.get();
                if (t == null) return null;
                nx = t.next;
                afterRead.run();                                   // 测试钩子：在"读完"与"CAS"之间让别的线程插进来
            } while (!top.compareAndSet(t, nx));
            return t;
        }
        String dump() { var sb = new StringBuilder("["); for (Node n = top.get(); n != null; n = n.next) sb.append(n).append(' '); return sb.append(']').toString(); }
    }

    /** 修复版：引用 + 版本号（stamp），每次改动 stamp+1，A 回来了 stamp 也不同了 */
    static final class StampedStack {
        final AtomicStampedReference<Node> top = new AtomicStampedReference<>(null, 0);
        void push(Node n) {
            int[] st = new int[1]; Node t;
            do { t = top.get(st); n.next = t; } while (!top.compareAndSet(t, n, st[0], st[0] + 1));
        }
        Node pop(Runnable afterRead) {
            int[] st = new int[1]; Node t, nx;
            do {
                t = top.get(st);
                if (t == null) return null;
                nx = t.next;
                afterRead.run();
            } while (!top.compareAndSet(t, nx, st[0], st[0] + 1));
            return t;
        }
        String dump() { var sb = new StringBuilder("["); for (Node n = top.getReference(); n != null; n = n.next) sb.append(n).append(' '); return sb.append(']').toString(); }
    }

    interface Stack { void push(Node n); Node pop(Runnable hook); String dump(); }

    static String abaScenario(Stack s) throws Exception {
        Node a = new Node("A"), b = new Node("B"), c = new Node("C");
        s.push(c); s.push(b); s.push(a);                          // 栈顶 -> A -> B -> C
        CountDownLatch t1HasRead = new CountDownLatch(1), t2Done = new CountDownLatch(1);

        Thread t1 = new Thread(() -> {
            boolean[] first = {true};
            s.pop(() -> {
                if (first[0]) {                                    // 只在第一次读完之后暂停
                    first[0] = false;
                    t1HasRead.countDown();                         // "我已经读到 top=A, next=B 了"
                    try { t2Done.await(); } catch (InterruptedException e) { throw new RuntimeException(e); }
                }
            });
        });
        t1.start();
        t1HasRead.await();

        // 线程 2：pop A，pop B，再把 A 压回去（A.next 现在是 C）。栈顶还是 A —— 但"世界已经变了"
        Node p1 = s.pop(() -> {});
        Node p2 = s.pop(() -> {});
        s.push(p1);
        t2Done.countDown();
        t1.join();
        return s.dump();
    }

    public static void main(String[] args) throws Exception {
        AtomicLong m = new AtomicLong(10);
        casMax(m, 5); casMax(m, 42); casMax(m, 17);
        System.out.println("casMax 结果 = " + m.get() + " (期望 42)");

        System.out.println("--- ABA：初始 栈顶 -> A -> B -> C；线程1 读到 A/B 后暂停；线程2 pop A, pop B, push A");
        System.out.println("正确结果应是 [C ]：A、B 都被弹走过，线程 2 把 A 压回，线程 1 再把 A 弹掉，只剩 C");
        var naive = new NaiveStack();
        System.out.println("朴素版 最终栈 = " + abaScenario(new Stack() {
            public void push(Node n) { naive.push(n); } public Node pop(Runnable h) { return naive.pop(h); } public String dump() { return naive.dump(); } })
            + "   <- B 已被线程 2 弹走，却又回到栈里（线程 1 的 CAS 看到 top 仍是 A 就成功，把 top 设成了过期的 B）");
        var stamped = new StampedStack();
        System.out.println("加版本号 最终栈 = " + abaScenario(new Stack() {
            public void push(Node n) { stamped.push(n); } public Node pop(Runnable h) { return stamped.pop(h); } public String dump() { return stamped.dump(); } }));
    }
}
