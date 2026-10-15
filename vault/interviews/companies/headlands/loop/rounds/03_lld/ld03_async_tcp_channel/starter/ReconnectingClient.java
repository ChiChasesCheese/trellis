import java.net.InetSocketAddress;

/**
 * Part 4b：自动重连的客户端。断线期间 offer 进入有界的 pending（字节口径 = 4 + len 之和，上限 cfg.outCapacity()），
 * 满了返回 false；重连后按原顺序发出。已交给旧通道的消息断线时可能丢失（abandonedBytes 记录丢了多少字节）。
 * close() 之后 offer 抛 IllegalStateException，且不再重连。
 */
public final class ReconnectingClient implements AutoCloseable {
    public ReconnectingClient(InetSocketAddress addr, ChannelConfig cfg, Backoff backoff) {
        throw new UnsupportedOperationException("TODO");
    }

    public boolean offer(byte[] msg) { throw new UnsupportedOperationException("TODO"); }

    /** 当前连接上的下一条入站消息；断线期间返回 null。 */
    public byte[] poll() { throw new UnsupportedOperationException("TODO"); }

    public boolean isConnected() { throw new UnsupportedOperationException("TODO"); }
    public int connectCount() { throw new UnsupportedOperationException("TODO"); }
    public int failedAttempts() { throw new UnsupportedOperationException("TODO"); }
    public long abandonedBytes() { throw new UnsupportedOperationException("TODO"); }
    public int pendingBytes() { throw new UnsupportedOperationException("TODO"); }

    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }
}
