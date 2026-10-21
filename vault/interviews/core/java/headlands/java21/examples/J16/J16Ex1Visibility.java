/**
 * J16 例 1：可见性。reader 在循环里等 stop 变 true。
 *   * 普通字段：JIT 编译后，reader 可能把 stop 读一次就不再读 -> 永远停不下来（这里 join(1000) 超时）
 *   * volatile 字段：保证看到写入
 *   * 解释执行(-Xint)：碰巧每次都真去读内存，所以普通字段"看起来正常"——这正是并发 bug 难查的原因
 * 运行：java --enable-preview J16Ex1Visibility          （默认 JIT）
 *       java --enable-preview -Xint J16Ex1Visibility    （只解释执行）
 */
public class J16Ex1Visibility {
    static boolean plainStop;
    static volatile boolean volatileStop;

    static long spinPlain() { long n = 0; while (!plainStop) n++; return n; }
    static long spinVolatile() { long n = 0; while (!volatileStop) n++; return n; }

    static void run(String name, Runnable body, Runnable stopper) throws Exception {
        Thread reader = new Thread(body, name);
        reader.setDaemon(true);                       // 万一停不下来，别拖住 JVM 退出
        reader.start();
        Thread.sleep(300);                            // 让 reader 先跑热（被 JIT 编译）
        stopper.run();
        reader.join(1000);
        System.out.println(name + ": " + (reader.isAlive() ? "1 秒后仍在运行 —— 没看到 stop 的写入！" : "已正常结束"));
    }

    public static void main(String[] args) throws Exception {
        run("plain   ", J16Ex1Visibility::spinPlain, () -> plainStop = true);
        run("volatile", J16Ex1Visibility::spinVolatile, () -> volatileStop = true);
    }
}
