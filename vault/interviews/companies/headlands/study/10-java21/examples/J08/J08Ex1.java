import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/** J08 例 1（最简单）：局部变量、增强 for、传统 for、try-with-resources。var 仍然是静态类型。 */
public class J08Ex1 {

    static final class Fill {
        final String symbol; final long qty;
        Fill(String symbol, long qty) { this.symbol = symbol; this.qty = qty; }
    }

    public static void main(String[] args) throws IOException {
        var fills = new ArrayList<Fill>();            // 推断为 ArrayList<Fill>
        fills.add(new Fill("AAPL", 100));
        fills.add(new Fill("MSFT", 50));
        fills.add(new Fill("AAPL", 25));

        var bySymbol = new HashMap<String, List<Fill>>();   // 推断为 HashMap<String, List<Fill>>
        for (var f : fills) {                               // f : Fill
            bySymbol.computeIfAbsent(f.symbol, k -> new ArrayList<>()).add(f);
        }

        for (var e : bySymbol.entrySet()) {                 // e : Map.Entry<String, List<Fill>>，不用写
            long total = 0;
            for (var f : e.getValue()) total += f.qty;
            System.out.println(e.getKey() + " " + total);
        }

        for (var i = 0; i < 3; i++) System.out.print(i + " ");   // i : int
        System.out.println();

        try (var in = new BufferedReader(new StringReader("line1\nline2"))) {   // in : BufferedReader
            var line = in.readLine();                              // line : String
            System.out.println(line.toUpperCase());               // 能调用 String 的方法 —— 类型是静态确定的
        }
    }
}
