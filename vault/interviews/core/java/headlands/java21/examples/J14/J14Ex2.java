import java.util.*;
import java.util.stream.*;

/** J14 例 2：mapMulti（Java 16）——一个元素产出 0..n 个结果，不为每个元素建中间 Stream。和 flatMap 对照。 */
public class J14Ex2 {
    sealed interface Event permits Fill, Cancel {}
    record Fill(long orderId, long qty, long px) implements Event {}
    record Cancel(long orderId) implements Event {}

    public static void main(String[] args) {
        List<Event> events = List.of(new Fill(1, 100, 18950), new Cancel(2), new Fill(3, 0, 18951), new Fill(4, 50, 18952));

        // flatMap 版：每个元素都 new 一个小 Stream（Stream.of / Stream.empty）
        List<Fill> viaFlat = events.stream()
                .flatMap(e -> e instanceof Fill f && f.qty() > 0 ? Stream.of(f) : Stream.empty())
                .toList();

        // mapMulti 版：往 sink 里"推"0 个或多个结果；<Fill> 是显式类型参数——lambda 无法推断输出类型时必需
        List<Fill> viaMulti = events.stream()
                .<Fill>mapMulti((e, sink) -> {
                    if (e instanceof Fill f && f.qty() > 0) sink.accept(f);
                })
                .toList();

        System.out.println("flatMap  : " + viaFlat);
        System.out.println("mapMulti : " + viaMulti);
        System.out.println("相同? " + viaFlat.equals(viaMulti));

        // mapMulti 更适合"一个元素展开成几个"：把一个多腿订单拆成每条腿
        record Parent(String id, int legs) {}
        List<String> legs = Stream.of(new Parent("P1", 2), new Parent("P2", 0), new Parent("P3", 3))
                .<String>mapMulti((p, sink) -> {
                    for (int i = 1; i <= p.legs(); i++) sink.accept(p.id() + "-leg" + i);
                })
                .toList();
        System.out.println(legs);
    }
}
