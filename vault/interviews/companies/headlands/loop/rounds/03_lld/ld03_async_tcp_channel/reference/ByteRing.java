import java.nio.ByteBuffer;

/**
 * Part 1a：字节环形缓冲区（有界，非线程安全，容量任意正整数）。
 * 与 ld01 的区别：这里是单线程（调用方加锁），只关心「部分写 / 部分读」和回绕时分两段拷贝。
 */
public final class ByteRing {
    private final byte[] buf;
    private int head;      // 下一个要读的位置
    private int size;      // 当前字节数

    public ByteRing(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        buf = new byte[capacity];
    }

    public int capacity() { return buf.length; }
    public int size() { return size; }
    public int free() { return buf.length - size; }
    public boolean isEmpty() { return size == 0; }

    /** 尽量多写：返回实际写入的字节数（<= src.remaining()），src.position 前进相同数量。 */
    public int write(ByteBuffer src) {
        int n = Math.min(src.remaining(), free());
        int tail = (head + size) % buf.length;
        int first = Math.min(n, buf.length - tail);
        src.get(buf, tail, first);
        src.get(buf, 0, n - first);
        size += n;
        return n;
    }

    /** 尽量多读：返回实际读出的字节数（<= dst.remaining()），dst.position 前进相同数量。 */
    public int read(ByteBuffer dst) {
        int n = Math.min(dst.remaining(), size);
        int first = Math.min(n, buf.length - head);
        dst.put(buf, head, first);
        dst.put(buf, 0, n - first);
        head = (head + n) % buf.length;
        size -= n;
        return n;
    }

    /** 全有或全无：放得下 len 字节就全写入并返回 true；否则一个字节也不写，返回 false。 */
    public boolean writeAll(byte[] src, int off, int len) {
        java.util.Objects.checkFromIndexSize(off, len, src.length);
        if (len > free()) return false;
        write(ByteBuffer.wrap(src, off, len));
        return true;
    }

    /** 从头部偏移 offset 处读一个大端 int，不消费。要求 size >= offset + 4。 */
    public int peekInt(int offset) {
        if (offset < 0 || size < offset + 4) throw new IllegalStateException("fewer than 4 bytes at offset " + offset);
        int v = 0;
        for (int i = 0; i < 4; i++) v = (v << 8) | (buf[(head + offset + i) % buf.length] & 0xFF);
        return v;
    }

    public int peekInt() { return peekInt(0); }

    /** 取走 n 字节。size < n 抛 IllegalStateException（状态不变）。 */
    public byte[] take(int n) {
        if (n < 0) throw new IllegalArgumentException("n < 0");
        if (n > size) throw new IllegalStateException("only " + size + " bytes buffered, wanted " + n);
        byte[] out = new byte[n];
        read(ByteBuffer.wrap(out));
        return out;
    }

    public void skip(int n) {
        if (n < 0) throw new IllegalArgumentException("n < 0");
        if (n > size) throw new IllegalStateException("only " + size + " bytes buffered, wanted " + n);
        head = (head + n) % buf.length;
        size -= n;
    }

    public void clear() { head = 0; size = 0; }
}
