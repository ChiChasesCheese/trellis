import java.nio.ByteBuffer;

/**
 * Part 1c：增量帧解码器，有界（内部一个 capacity 字节的 ByteRing）。
 * 帧头非法（< 0 或 > maxFrame）→ FrameException，粘性（之后每次 next() 都抛）。必须只看到头就报错，不能等负载。
 */
public final class FrameDecoder {
    /** capacity < maxFrame + 4 抛 IllegalArgumentException。 */
    public FrameDecoder(int maxFrame, int capacity) {
        throw new UnsupportedOperationException("TODO");
    }

    /** @return 实际消费的字节数（src.position 前进相同数量）；缓冲区满时可能小于 src.remaining()。 */
    public int feed(ByteBuffer src) { throw new UnsupportedOperationException("TODO"); }

    /** 下一条完整消息；不够一帧返回 null。 */
    public byte[] next() { throw new UnsupportedOperationException("TODO"); }

    /** next() 现在会返回一条消息（或抛 FrameException）吗？不消费。 */
    public boolean hasFrame() { throw new UnsupportedOperationException("TODO"); }

    public int buffered() { throw new UnsupportedOperationException("TODO"); }

    public int free() { throw new UnsupportedOperationException("TODO"); }

    /** 缓冲区里除了完整的帧之外，是否还有一截不完整的尾巴？非法帧头不算截断。 */
    public boolean hasTruncatedTail() { throw new UnsupportedOperationException("TODO"); }
}
