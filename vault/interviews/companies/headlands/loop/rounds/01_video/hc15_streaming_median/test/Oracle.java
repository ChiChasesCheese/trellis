import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

/** 明显正确的慢实现，供对拍：每次都排序。 */
final class Oracle {
    private Oracle() {}

    /** 最近秩百分位：排序后第 ceil(p × n / 100) 个。 */
    static long percentile(long[] values, int p) {
        long[] s = values.clone();
        Arrays.sort(s);
        long rank = Math.ceilDiv((long) p * s.length, 100L);
        return s[(int) rank - 1];
    }

    static long lowerMedian(long[] values) {
        return percentile(values, 50);
    }

    /** 最近 k 个。 */
    static long[] lastK(List<Long> all, int k) {
        int from = Math.max(0, all.size() - k);
        return all.subList(from, all.size()).stream().mapToLong(Long::longValue).toArray();
    }

    static long[] stream(int n, long bound, long seed) {
        var rnd = new Random(seed);
        long[] out = new long[n];
        for (int i = 0; i < n; i++) out[i] = rnd.nextLong(bound);
        return out;
    }

    static List<Long> boxed(long... xs) {
        var l = new ArrayList<Long>();
        for (long x : xs) l.add(x);
        return l;
    }
}
