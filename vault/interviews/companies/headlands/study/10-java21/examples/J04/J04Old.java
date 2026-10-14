/** J04 旧写法：Java 8 要「拆开」一个嵌套的值，只能一层一层判断、强转、调 getter。 */
public class J04Old {

    static final class Mean {
        final long numerator, denominator;
        Mean(long n, long d) { numerator = n; denominator = d; }
        long getNumerator() { return numerator; }
        long getDenominator() { return denominator; }
    }
    interface Answer {}
    static final class Value implements Answer {
        final Mean mean;
        Value(Mean m) { mean = m; }
        Mean getMean() { return mean; }
    }
    static final class Empty implements Answer {}

    /** 「是 Value，并且它里面的分母是 1，就打印分子」——三步：判断类型、取 Mean、取字段。 */
    static String render(Answer a) {
        if (a instanceof Value) {
            Value v = (Value) a;
            Mean m = v.getMean();
            long n = m.getNumerator();
            long d = m.getDenominator();
            if (d == 1) {
                return Long.toString(n);
            } else {
                return n + "/" + d;
            }
        } else if (a instanceof Empty) {
            return "empty";
        }
        throw new IllegalArgumentException();
    }

    public static void main(String[] args) {
        System.out.println(render(new Value(new Mean(7, 1))));
        System.out.println(render(new Value(new Mean(-7, 2))));
        System.out.println(render(new Empty()));
    }
}
