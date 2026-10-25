/**
 * hc14 Part 4（starter）：热路径版本。输入是整块 byte[]（整个日志文件读进内存）。
 *
 * <p>要求：结果和 {@link TradeLog#analyze} 逐字段一致（同样的语法、同样的坏行、同样的溢出异常）；
 * 100 万行 &lt; 1 s，总分配 &lt; 4 MB。
 * 提示：一遍扫字节，不建 String，不用正则，不装箱。symbol 最长 10 个字符、字母表 37 个：每个字符 6 位，
 * 打包进一个 long 当哈希键；每个 symbol 的累计值放并行的 long[]（开放寻址，键 0 = 空槽）。
 * 注意：byte 是有符号的，用 b[i] &amp; 0xFF 当下标。
 */
public final class FastLog {
    private FastLog() {}

    public static TradeLog.Report analyze(byte[] data) {
        throw new UnsupportedOperationException("TODO");
    }
}
