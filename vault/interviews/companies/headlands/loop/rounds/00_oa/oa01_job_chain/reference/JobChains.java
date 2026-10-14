import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

/** Headlands HackerRank：job chain 报表。题面见 ../problem.md。 */
public final class JobChains {
    private JobChains() {}

    /** 一行输入。紧凑构造器只做「单行内」能判断的校验；跨行规则（重复、悬空、多前驱、环）在 chains() 里。 */
    public record Job(int id, long runtimeSeconds, int nextId) {
        public Job {
            if (id <= 0) throw new MalformedInputException("job_id must be positive: " + id);
            if (runtimeSeconds < 0) throw new MalformedInputException("negative runtime: " + runtimeSeconds);
            if (nextId < 0) throw new MalformedInputException("negative next_job_id: " + nextId);
            if (nextId == id) throw new MalformedInputException("self loop: " + id);
        }
    }

    public record Chain(int startJob, int lastJob, int count, long totalSeconds) {
        public long averageSeconds() { return totalSeconds / count; } // 题面：整秒，向下取整
    }

    /** 分析结果：要么一组链，要么非法输入。sealed + record 让调用方的 switch 必须穷尽。 */
    public sealed interface Outcome permits Ok, Malformed {}
    public record Ok(List<Chain> chains) implements Outcome {}
    public record Malformed(String reason) implements Outcome {}

    public static final class MalformedInputException extends RuntimeException {
        public MalformedInputException(String msg) { super(msg); }
    }

    private static final Pattern LINE = Pattern.compile("\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*");

    /** Part 1：解析。跳过首行表头（以 # 开头）与空行；其余每行必须正好三个整数。 */
    public static List<Job> parse(List<String> lines) {
        var jobs = new ArrayList<Job>();
        for (var raw : lines) {
            if (raw.isBlank() || raw.strip().startsWith("#")) continue;
            var m = LINE.matcher(raw);
            if (!m.matches()) throw new MalformedInputException("bad line: " + raw);
            try {
                jobs.add(new Job(Integer.parseInt(m.group(1)), Long.parseLong(m.group(2)), Integer.parseInt(m.group(3))));
            } catch (NumberFormatException e) {
                throw new MalformedInputException("number out of range: " + raw);
            }
        }
        return jobs;
    }

    /** Part 1：秒 → hh:mm:ss；小时至少两位，超过 99 不截断。 */
    public static String hhmmss(long seconds) {
        if (seconds < 0) throw new IllegalArgumentException("negative: " + seconds);
        return "%02d:%02d:%02d".formatted(seconds / 3600, seconds / 60 % 60, seconds % 60);
    }

    /** Part 2：把 jobs 拼成若干条单链；任何一条跨行规则被违反都抛 MalformedInputException。 */
    public static List<Chain> chains(List<Job> jobs) {
        var byId = new LinkedHashMap<Integer, Job>();
        for (var j : jobs) {
            if (byId.putIfAbsent(j.id(), j) != null) throw new MalformedInputException("duplicate job_id " + j.id());
        }
        var hasPredecessor = new HashSet<Integer>();
        for (var j : jobs) {
            if (j.nextId() == 0) continue;
            if (!byId.containsKey(j.nextId())) throw new MalformedInputException("dangling next_job_id " + j.nextId());
            if (!hasPredecessor.add(j.nextId())) throw new MalformedInputException("two jobs point at " + j.nextId());
        }
        var out = new ArrayList<Chain>();
        Set<Integer> visited = new HashSet<>();
        for (var head : byId.values()) {
            if (hasPredecessor.contains(head.id())) continue;
            int count = 0;
            long total = 0;
            Job cur = head;
            while (true) {
                visited.add(cur.id());
                count++;
                total = Math.addExact(total, cur.runtimeSeconds());
                if (cur.nextId() == 0) break;
                cur = byId.get(cur.nextId());
            }
            out.add(new Chain(head.id(), cur.id(), count, total));
        }
        // 每个节点入度 ≤ 1 且都从无前驱的头走过一遍；没被走到的节点只能在环上。
        if (visited.size() != byId.size()) throw new MalformedInputException("cycle among jobs not reachable from a head");
        out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed().thenComparingInt(Chain::startJob));
        return out;
    }

    /** Part 3：整题。 */
    public static Outcome analyze(List<String> lines) {
        try {
            return new Ok(chains(parse(lines)));
        } catch (MalformedInputException e) {
            return new Malformed(e.getMessage());
        }
    }

    /** Part 3：渲染。对 sealed Outcome 做模式匹配 switch，编译器保证两种情况都处理了。 */
    public static List<String> render(Outcome outcome) {
        return switch (outcome) {
            case Malformed _ -> List.of("Malformed Input");
            case Ok(var chains) -> {
                var lines = new ArrayList<String>();
                lines.add("-");
                for (var c : chains) {
                    lines.add("start_job: " + c.startJob());
                    lines.add("last_job: " + c.lastJob());
                    lines.add("number_of_jobs: " + c.count());
                    lines.add("job_chain_runtime: " + hhmmss(c.totalSeconds()));
                    lines.add("average_job_time: " + hhmmss(c.averageSeconds()));
                    lines.add("-");
                }
                yield lines;
            }
        };
    }

    public static List<String> solve(List<String> lines) {
        return render(analyze(lines));
    }
}
