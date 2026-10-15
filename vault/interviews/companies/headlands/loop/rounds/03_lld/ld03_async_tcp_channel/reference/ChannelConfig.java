/**
 * 通道参数。
 *
 * @param maxFrame    单条消息负载的最大字节数（不含 4 字节长度头）。超过的 offer 抛 IllegalArgumentException，收到的帧头超过则 FrameException
 * @param outCapacity 出站环形缓冲区字节数（装的是「已编码的帧」，含 4 字节头）
 * @param inCapacity  入站环形缓冲区字节数。必须 >= maxFrame + 4，否则一条最大的消息永远凑不齐
 */
public record ChannelConfig(int maxFrame, int outCapacity, int inCapacity) {
    public ChannelConfig {
        if (maxFrame < 0) throw new IllegalArgumentException("maxFrame < 0");
        if (maxFrame > Integer.MAX_VALUE - 4) throw new IllegalArgumentException("maxFrame too large");
        if (outCapacity < maxFrame + 4) throw new IllegalArgumentException("outCapacity must be >= maxFrame + 4");
        if (inCapacity < maxFrame + 4) throw new IllegalArgumentException("inCapacity must be >= maxFrame + 4");
    }

    public static ChannelConfig of(int maxFrame) { return new ChannelConfig(maxFrame, 64 * 1024, 64 * 1024); }
}
