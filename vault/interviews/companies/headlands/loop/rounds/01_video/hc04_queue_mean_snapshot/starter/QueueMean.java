import java.math.BigInteger;

/** Headlands 电面 hc04 Part 1：FIFO 队列 + O(1) 精确均值。题面见 ../problem.md，把每个 TODO 换成实现。 */
public final class QueueMean {

    /** 有符号 128 位整数（二进制补码，hi 有符号，lo 按无符号用）。提示：lo 相加后 compareUnsigned 小于原值就说明进位。 */
    public record I128(long hi, long lo) {
        public static final I128 ZERO = new I128(0, 0);
        public I128 plus(long x) { throw new UnsupportedOperationException("TODO"); }
        public I128 minus(long x) { throw new UnsupportedOperationException("TODO"); }
        public BigInteger toBigInteger() { throw new UnsupportedOperationException("TODO"); }
    }

    /** 精确均值：约分后的分数，分母恒正。提示：在紧凑构造器里校验分母并用 gcd 约分（可以重新赋值参数）。 */
    public record Mean(BigInteger numerator, long denominator) {
        public double toDouble() { throw new UnsupportedOperationException("TODO"); }
    }

    public void push(long x) { throw new UnsupportedOperationException("TODO"); }

    /** 弹出队头（最早 push 的）。空队列抛 NoSuchElementException。 */
    public long pop() { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    public boolean isEmpty() { throw new UnsupportedOperationException("TODO"); }

    /** 当前所有元素之和（128 位，不会溢出）。 */
    public I128 sum() { throw new UnsupportedOperationException("TODO"); }

    /** 精确均值。空队列抛 NoSuchElementException。 */
    public Mean mean() { throw new UnsupportedOperationException("TODO"); }

    /** 均值的 double 近似（正确舍入）。空队列抛 NoSuchElementException。 */
    public double getMean() { throw new UnsupportedOperationException("TODO"); }
}
