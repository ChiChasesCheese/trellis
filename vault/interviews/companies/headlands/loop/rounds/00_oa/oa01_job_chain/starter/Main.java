import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** HackerRank 形态：stdin → stdout；非法输入时以非零码退出。 */
public class Main {
    public static void main(String[] args) {
        var in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        var outcome = JobChains.analyze(in.lines().toList());
        JobChains.render(outcome).forEach(System.out::println);
        if (outcome instanceof JobChains.Malformed) System.exit(1);
    }
}
