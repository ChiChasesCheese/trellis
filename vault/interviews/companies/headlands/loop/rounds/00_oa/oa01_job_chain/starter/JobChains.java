import java.util.List;

/** Headlands HackerRank：job chain 报表。题面见 ../problem.md。把每个 TODO 换成实现。 */
public final class JobChains {
    private JobChains() {}

    /** 一行输入。提示：紧凑构造器（compact constructor）里做单行校验。 */
    public record Job(int id, long runtimeSeconds, int nextId) {}

    public record Chain(int startJob, int lastJob, int count, long totalSeconds) {
        public long averageSeconds() { throw new UnsupportedOperationException("TODO"); }
    }

    /** 分析结果：要么一组链，要么非法输入。 */
    public sealed interface Outcome permits Ok, Malformed {}
    public record Ok(List<Chain> chains) implements Outcome {}
    public record Malformed(String reason) implements Outcome {}

    public static final class MalformedInputException extends RuntimeException {
        public MalformedInputException(String msg) { super(msg); }
    }

    /** Part 1：解析。跳过 # 开头的表头与空行；其余每行必须正好三个整数。 */
    public static List<Job> parse(List<String> lines) { throw new UnsupportedOperationException("TODO"); }

    /** Part 1：秒 → hh:mm:ss。 */
    public static String hhmmss(long seconds) { throw new UnsupportedOperationException("TODO"); }

    /** Part 2：拼链 + 结构校验 + 排序。 */
    public static List<Chain> chains(List<Job> jobs) { throw new UnsupportedOperationException("TODO"); }

    /** Part 3：整题，异常变成 Malformed。 */
    public static Outcome analyze(List<String> lines) { throw new UnsupportedOperationException("TODO"); }

    /** Part 3：渲染。试试对 Outcome 写一个模式匹配 switch。 */
    public static List<String> render(Outcome outcome) { throw new UnsupportedOperationException("TODO"); }

    public static List<String> solve(List<String> lines) { return render(analyze(lines)); }
}
