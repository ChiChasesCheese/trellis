/** Part 1b：帧格式 = 4 字节大端长度 + 负载。 */
public final class FrameCodec {
    public static final int HEADER = 4;

    private FrameCodec() {}

    /**
     * 把一条消息编码进 out。放不下返回 false（out 不变，不能留下半个头）；负载超过 maxFrame 抛 IllegalArgumentException；
     * payload 为 null 抛 NullPointerException。空负载合法。
     */
    public static boolean encode(ByteRing out, byte[] payload, int maxFrame) {
        throw new UnsupportedOperationException("TODO");
    }
}
