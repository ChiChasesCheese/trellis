import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.nio.channels.SocketChannel;

/**
 * Part 2/3：一条 TCP 连接上的有界消息通道。
 * 提示：一个 Selector I/O 线程 + 两个环（出站 ByteRing、入站 FrameDecoder）+ 一把锁；
 * offer 不阻塞（满了返回 false）；入站环满了就停止监听 OP_READ；write 可能只写一部分。
 * 语义细节见 problem.md 的 Part 2/3。
 */
public final class TcpMessageChannel implements AutoCloseable {
    private TcpMessageChannel() {}

    /** 阻塞地连接（最多 timeoutMs），成功后切到非阻塞并启动 I/O 线程。 */
    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg, int timeoutMs) throws IOException {
        throw new UnsupportedOperationException("TODO");
    }

    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg) throws IOException {
        throw new UnsupportedOperationException("TODO");
    }

    /** 接管一个已经连接好的 SocketChannel。 */
    public static TcpMessageChannel wrap(SocketChannel connected, ChannelConfig cfg) throws IOException {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * 非阻塞发送。true = 已进入出站缓冲区；false = 缓冲区满。
     * 消息超过 maxFrame 抛 IllegalArgumentException；通道已关闭 / 已 finishSending 抛 IllegalStateException。
     */
    public boolean offer(byte[] msg) { throw new UnsupportedOperationException("TODO"); }

    /** 最多等 timeoutMs 毫秒直到放得下。 */
    public boolean offer(byte[] msg, long timeoutMs) throws InterruptedException { throw new UnsupportedOperationException("TODO"); }

    /** 下一条完整消息，没有返回 null。通道关闭后，已缓冲的完整消息仍可取。帧头非法时抛 FrameException 并使通道失败。 */
    public byte[] poll() { throw new UnsupportedOperationException("TODO"); }

    /** 等到有消息、或不会再有消息（drained）、或超时（返回 null）。 */
    public byte[] poll(long timeoutMs) throws InterruptedException { throw new UnsupportedOperationException("TODO"); }

    /** 不再接受 offer；已接受的消息刷完后发 FIN（半关闭）。对端也结束后通道关闭。 */
    public void finishSending() { throw new UnsupportedOperationException("TODO"); }

    /** 立刻关闭，丢弃未发送的数据。幂等。 */
    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }

    public boolean isOpen() { throw new UnsupportedOperationException("TODO"); }

    public boolean isPeerClosed() { throw new UnsupportedOperationException("TODO"); }

    /** 不会再有新消息了（对端已关闭或本端已关闭）且缓冲区里没有完整的消息了。 */
    public boolean isDrained() { throw new UnsupportedOperationException("TODO"); }

    /** 因错误而关闭时的原因（FrameException / EOFException / IOException）；正常关闭 / 仍打开为 null。 */
    public Throwable failure() { throw new UnsupportedOperationException("TODO"); }

    /** 已接受但尚未写进 socket 的字节数。 */
    public int unsentBytes() { throw new UnsupportedOperationException("TODO"); }

    public boolean awaitClosed(long timeoutMs) throws InterruptedException { throw new UnsupportedOperationException("TODO"); }

    public InetSocketAddress localAddress() throws IOException { throw new UnsupportedOperationException("TODO"); }

    public SocketAddress remoteAddress() throws IOException { throw new UnsupportedOperationException("TODO"); }
}
