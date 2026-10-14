import java.nio.file.Path;

/**
 * 子进程入口（由 SharedChannelTest 用 `java -cp ... SpscChild <mode> <file> <count> <timeoutMs>` 启动）。
 *
 *   consume：打开通道，按序收 count 条消息并逐条校验（序号、长度、内容），然后确认通道 drained；
 *   produce：打开通道，发 count 条消息（满了就自旋等），最后 finish()。
 *
 * 成功：stdout 打印 "OK <count>" 并以退出码 0 结束；失败：打印 "FAIL <原因>"，退出码 1。
 * produce / consume 也是 public static，父进程的测试直接复用同一份逻辑，保证两边对「正确」的定义一致。
 */
public final class SpscChild {
    private SpscChild() {}

    /** null = 成功；否则是错误描述。 */
    public static String consume(SharedChannel ch, long count, long deadlineNanos) {
        long expect = 0;
        int spins = 0;
        while (expect < count) {
            byte[] m = ch.receive();
            if (m == null) {
                if ((++spins & 0x3FF) == 0 && System.nanoTime() > deadlineNanos) return "timeout after " + expect + " of " + count + " messages";
                Thread.onSpinWait();
                continue;
            }
            String err = Msgs.check(m, expect);
            if (err != null) return err;
            expect++;
        }
        // 应当恰好 count 条：之后必须没有多余的消息，并且生产者已经 finish
        while (!ch.isDrained()) {
            byte[] extra = ch.receive();
            if (extra != null) return "unexpected extra message after " + count + " (duplicate?)";
            if (System.nanoTime() > deadlineNanos) return "producer never finished";
            Thread.onSpinWait();
        }
        return null;
    }

    public static String produce(SharedChannel ch, long count, long deadlineNanos) {
        int spins = 0;
        for (long i = 0; i < count; i++) {
            byte[] m = Msgs.make(i);
            while (!ch.send(m)) {
                if ((++spins & 0x3FF) == 0 && System.nanoTime() > deadlineNanos) return "timeout: consumer too slow at seq " + i;
                Thread.onSpinWait();
            }
        }
        ch.finish();
        return null;
    }

    public static void main(String[] args) throws Exception {
        String mode = args[0];
        Path file = Path.of(args[1]);
        long count = Long.parseLong(args[2]);
        long deadline = System.nanoTime() + Long.parseLong(args[3]) * 1_000_000L;
        try (SharedChannel ch = SharedChannel.open(file)) {
            String err = switch (mode) {
                case "consume" -> consume(ch, count, deadline);
                case "produce" -> produce(ch, count, deadline);
                default -> "unknown mode " + mode;
            };
            if (err != null) {
                System.out.println("FAIL " + err);
                System.exit(1);
            }
            System.out.println("OK " + count);
        } catch (Throwable t) {
            System.out.println("FAIL " + t);
            System.exit(1);
        }
    }
}
