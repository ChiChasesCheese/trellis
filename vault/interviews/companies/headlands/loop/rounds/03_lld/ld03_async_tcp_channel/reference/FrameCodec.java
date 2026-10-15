/** Part 1b：帧格式 = 4 字节大端长度 + 负载。TCP 是字节流，没有「消息边界」，边界必须自己带。 */
public final class FrameCodec {
    public static final int HEADER = 4;

    private FrameCodec() {}

    /**
     * 把一条消息编码进 out。放不下返回 false（out 不变）；负载超过 maxFrame 抛 IllegalArgumentException。空负载合法。
     */
    public static boolean encode(ByteRing out, byte[] payload, int maxFrame) {
        java.util.Objects.requireNonNull(payload, "payload");
        if (payload.length > maxFrame) throw new IllegalArgumentException("payload " + payload.length + " > maxFrame " + maxFrame);
        if (out.free() < HEADER + payload.length) return false;
        int n = payload.length;
        out.writeAll(new byte[]{(byte) (n >>> 24), (byte) (n >>> 16), (byte) (n >>> 8), (byte) n}, 0, HEADER);
        out.writeAll(payload, 0, n);
        return true;
    }
}
