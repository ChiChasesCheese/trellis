/** volatile vs plain flag: does the reader thread ever see the writer's update? (JMM visibility) */
public class K01Visibility {
    static boolean plain;
    static volatile boolean vol;

    static void run(String name, java.util.function.BooleanSupplier read, Runnable write) throws Exception {
        Thread t = new Thread(() -> { long n = 0; while (!read.getAsBoolean()) n++; }, "spin-" + name);
        t.setDaemon(true);
        t.start();
        Thread.sleep(300);
        write.run();
        t.join(1500);
        System.out.println(name + ": reader finished within 1.5s after the write? " + !t.isAlive());
    }

    public static void main(String[] a) throws Exception {
        run("plain   ", () -> plain, () -> plain = true);
        run("volatile", () -> vol, () -> vol = true);
    }
}
