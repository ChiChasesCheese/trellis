import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.MathContext;
import java.util.NoSuchElementException;

/**
 * Headlands 电面 hc04 Part 1：FIFO 队列 + O(1) 精确均值。题面见 ../problem.md。
 *
 * 设计：long[] 环形缓冲（无装箱、连续内存）+ 128 位累加器（hi, lo 两个 long，永不溢出：2^31 个 long 之和 < 2^94）。
 */
public final class QueueMean {

    /** 有符号 128 位整数（二进制补码，hi 有符号，lo 按无符号用）。够装 2^63 个 long 的和。 */
    public record I128(long hi, long lo) {
        public static final I128 ZERO = new I128(0, 0);

        public I128 plus(long x) {
            long l = lo + x;
            long carry = Long.compareUnsigned(l, lo) < 0 ? 1 : 0;
            return new I128(hi + (x >> 63) + carry, l);
        }

        public I128 minus(long x) {
            long l = lo - x;
            long borrow = Long.compareUnsigned(lo, x) < 0 ? 1 : 0;
            return new I128(hi - (x >> 63) - borrow, l);
        }

        private static final BigInteger TWO_64 = BigInteger.ONE.shiftLeft(64);

        public BigInteger toBigInteger() {
            BigInteger low = BigInteger.valueOf(lo);
            if (lo < 0) low = low.add(TWO_64);
            return BigInteger.valueOf(hi).shiftLeft(64).add(low);
        }
    }

    /** 精确均值：约分后的分数，分母恒正。 */
    public record Mean(BigInteger numerator, long denominator) {
        public Mean {
            if (denominator <= 0) throw new IllegalArgumentException("denominator must be positive: " + denominator);
            BigInteger g = numerator.gcd(BigInteger.valueOf(denominator));
            if (g.signum() != 0 && !g.equals(BigInteger.ONE)) {
                numerator = numerator.divide(g);
                denominator /= g.longValueExact();
            }
        }

        /** 最接近的 double。两边都能精确表示成 double 时一次 IEEE 除法就是正确舍入；否则走 BigDecimal。 */
        public double toDouble() {
            if (numerator.bitLength() <= 53 && denominator <= (1L << 53)) return numerator.doubleValue() / denominator;
            return new BigDecimal(numerator).divide(new BigDecimal(denominator), MathContext.DECIMAL128).doubleValue();
        }
    }

    private long[] buf = new long[16]; // 容量恒为 2 的幂，下标用掩码
    private int head;
    private int size;
    private long hi;
    private long lo;

    public void push(long x) {
        if (size == buf.length) grow();
        buf[(head + size) & (buf.length - 1)] = x;
        size++;
        long l = lo + x;
        hi += (x >> 63) + (Long.compareUnsigned(l, lo) < 0 ? 1 : 0);
        lo = l;
    }

    /** 弹出队头（最早 push 的）。空队列抛 NoSuchElementException。 */
    public long pop() {
        if (size == 0) throw new NoSuchElementException("pop on empty queue");
        long x = buf[head];
        head = (head + 1) & (buf.length - 1);
        size--;
        long l = lo - x;
        hi -= (x >> 63) + (Long.compareUnsigned(lo, x) < 0 ? 1 : 0);
        lo = l;
        return x;
    }

    public int size() { return size; }

    public boolean isEmpty() { return size == 0; }

    public I128 sum() { return new I128(hi, lo); }

    /** 精确均值。空队列抛 NoSuchElementException。 */
    public Mean mean() {
        if (size == 0) throw new NoSuchElementException("mean of empty queue");
        return new Mean(sum().toBigInteger(), size);
    }

    /** 均值的 double 近似（正确舍入）。快路径：和还在 ±2^53 内就不分配对象。 */
    public double getMean() {
        if (size == 0) throw new NoSuchElementException("mean of empty queue");
        if (hi == (lo >> 63) && lo >= -(1L << 53) && lo <= (1L << 53)) return (double) lo / size;
        return mean().toDouble();
    }

    private void grow() {
        long[] bigger = new long[Math.multiplyExact(buf.length, 2)];
        int firstPart = buf.length - head;
        System.arraycopy(buf, head, bigger, 0, firstPart);
        System.arraycopy(buf, 0, bigger, firstPart, head);
        buf = bigger;
        head = 0;
    }
}
