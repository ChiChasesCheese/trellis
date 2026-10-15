import java.nio.ByteBuffer;

/**
 * Part 1c：增量帧解码器。字节可以按任意大小的块到达（1 字节、半个头、两条半消息……），next() 只在凑齐一整帧时返回。
 * 有界：内部是一个 capacity 字节的 ByteRing；feed 在满时只消费放得下的部分，调用方必须先 next() 腾空间再继续喂——这就是入站背压。
 * 帧头非法（< 0 或 > maxFrame）→ FrameException，且是粘性的：之后每次 next() 都抛，因为字节流已经失去同步。
 */
public final class FrameDecoder {
    private final ByteRing ring;
    private final int maxFrame;
    private FrameException failed;

    public FrameDecoder(int maxFrame, int capacity) {
        if (maxFrame < 0) throw new IllegalArgumentException("maxFrame < 0");
        if (capacity < maxFrame + FrameCodec.HEADER) throw new IllegalArgumentException("capacity must be >= maxFrame + 4");
        this.maxFrame = maxFrame;
        this.ring = new ByteRing(capacity);
    }

    /** @return 实际消费的字节数（src.position 前进相同数量）；可能小于 src.remaining()。 */
    public int feed(ByteBuffer src) { return ring.write(src); }

    /** 下一条完整消息；不够一帧返回 null。 */
    public byte[] next() {
        if (failed != null) throw failed;
        if (ring.size() < FrameCodec.HEADER) return null;
        int len = ring.peekInt();
        if (len < 0 || len > maxFrame) {
            failed = new FrameException("bad frame length " + len + " (maxFrame " + maxFrame + ")");
            throw failed;
        }
        if (ring.size() < FrameCodec.HEADER + len) return null;
        ring.skip(FrameCodec.HEADER);
        return ring.take(len);
    }

    /** next() 现在会返回一条消息（或抛 FrameException）吗？不消费。 */
    public boolean hasFrame() {
        if (failed != null) return true;
        if (ring.size() < FrameCodec.HEADER) return false;
        int len = ring.peekInt();
        if (len < 0 || len > maxFrame) return true;
        return ring.size() >= FrameCodec.HEADER + len;
    }

    public int buffered() { return ring.size(); }

    public int free() { return ring.free(); }

    /** 缓冲区里除了完整的帧之外，是否还有一截不完整的尾巴？（对端关闭时用来判断「流被截断」。） */
    public boolean hasTruncatedTail() {
        int pos = 0;
        while (pos < ring.size()) {
            if (ring.size() - pos < FrameCodec.HEADER) return true;
            int len = ring.peekInt(pos);
            if (len < 0 || len > maxFrame) return false;      // 非法帧头由 next() 报告，不算截断
            if (ring.size() - pos < FrameCodec.HEADER + len) return true;
            pos += FrameCodec.HEADER + len;
        }
        return false;
    }
}
