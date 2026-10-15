import java.util.function.BooleanSupplier;

/** 测试辅助：轮询直到条件成立，超时则失败。只用于「最终会发生」的断言；不是用 sleep 猜时序。 */
final class Await {
    private Await() {}

    static void until(String what, long timeoutMs, BooleanSupplier cond) {
        long deadline = System.nanoTime() + timeoutMs * 1_000_000L;
        while (!cond.getAsBoolean()) {
            if (System.nanoTime() > deadline) throw new AssertionError("timed out waiting for: " + what);
            try { Thread.sleep(1); } catch (InterruptedException e) { Thread.currentThread().interrupt(); throw new AssertionError(e); }
        }
    }

    /** 确定性的测试消息：长度 4..64，前 4 字节是序号（大端），其余字节由序号决定。 */
    static byte[] msg(int seq) {
        int len = 4 + (int) ((seq * 31L) % 61);
        byte[] b = new byte[len];
        b[0] = (byte) (seq >>> 24); b[1] = (byte) (seq >>> 16); b[2] = (byte) (seq >>> 8); b[3] = (byte) seq;
        for (int i = 4; i < len; i++) b[i] = (byte) (seq + i);
        return b;
    }

    static boolean isMsg(byte[] m, int seq) { return m != null && java.util.Arrays.equals(m, msg(seq)); }
}
