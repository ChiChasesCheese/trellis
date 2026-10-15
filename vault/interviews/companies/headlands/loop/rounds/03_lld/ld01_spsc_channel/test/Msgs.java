import java.nio.ByteBuffer;

/** 测试用的确定性消息：第 seq 条消息的长度、内容都由 seq 决定，收到的人不需要任何额外信息就能校验「是不是第 seq 条」。 */
final class Msgs {
    private Msgs() {}

    static long mix(long x) {                          // splitmix64
        x += 0x9E3779B97F4A7C15L;
        x = (x ^ (x >>> 30)) * 0xBF58476D1CE4E5B9L;
        x = (x ^ (x >>> 27)) * 0x94D049BB133111EBL;
        return x ^ (x >>> 31);
    }

    /** 长度 8..56：前 8 字节是 seq（大端），其余是 seq 的函数。 */
    static byte[] make(long seq) {
        long m = mix(seq);
        int len = 8 + (int) ((m >>> 1) % 49);
        byte[] b = new byte[len];
        ByteBuffer.wrap(b).putLong(seq);
        for (int i = 8; i < len; i++) b[i] = (byte) (m >>> ((i & 7) * 8)) ;
        return b;
    }

    /** null = 正确；否则是错误描述。 */
    static String check(byte[] got, long seq) {
        if (got == null) return "null message at seq " + seq;
        if (got.length < 8) return "short message (" + got.length + " bytes) at seq " + seq;
        long gotSeq = ByteBuffer.wrap(got).getLong();
        if (gotSeq != seq) return "expected seq " + seq + " but got " + gotSeq + " (lost, duplicated or reordered)";
        byte[] want = make(seq);
        if (!java.util.Arrays.equals(want, got)) return "corrupt payload at seq " + seq;
        return null;
    }
}
