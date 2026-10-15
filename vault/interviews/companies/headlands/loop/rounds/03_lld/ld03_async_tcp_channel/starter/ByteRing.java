import java.nio.ByteBuffer;

/**
 * Part 1a：字节环形缓冲区（有界，非线程安全，容量任意正整数，不要求 2 的幂）。
 * 注意回绕时一次拷贝要拆成两段；容量 <= 0 抛 IllegalArgumentException。
 */
public final class ByteRing {
    public ByteRing(int capacity) {
        throw new UnsupportedOperationException("TODO");
    }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int size() { throw new UnsupportedOperationException("TODO"); }
    public int free() { throw new UnsupportedOperationException("TODO"); }
    public boolean isEmpty() { throw new UnsupportedOperationException("TODO"); }

    /** 尽量多写：返回实际写入的字节数（<= src.remaining()），src.position 前进相同数量。 */
    public int write(ByteBuffer src) { throw new UnsupportedOperationException("TODO"); }

    /** 尽量多读：返回实际读出的字节数（<= dst.remaining()），dst.position 前进相同数量。 */
    public int read(ByteBuffer dst) { throw new UnsupportedOperationException("TODO"); }

    /** 全有或全无：放得下 len 字节就全写入并返回 true；否则一个字节也不写，返回 false。越界抛 IndexOutOfBoundsException。 */
    public boolean writeAll(byte[] src, int off, int len) { throw new UnsupportedOperationException("TODO"); }

    /** 从头部偏移 offset 处读一个大端 int，不消费。size < offset + 4 抛 IllegalStateException。 */
    public int peekInt(int offset) { throw new UnsupportedOperationException("TODO"); }

    public int peekInt() { throw new UnsupportedOperationException("TODO"); }

    /** 取走 n 字节。n < 0 抛 IllegalArgumentException；size < n 抛 IllegalStateException（状态不变）。 */
    public byte[] take(int n) { throw new UnsupportedOperationException("TODO"); }

    /** 丢弃 n 字节，错误规则同 take。 */
    public void skip(int n) { throw new UnsupportedOperationException("TODO"); }

    public void clear() { throw new UnsupportedOperationException("TODO"); }
}
