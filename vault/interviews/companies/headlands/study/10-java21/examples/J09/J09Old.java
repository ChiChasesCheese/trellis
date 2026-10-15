import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Deque;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/** J09 旧写法：「第一个 / 最后一个」在每种集合里写法都不同；有的根本没有 O(1) 写法。 */
public class J09Old {

    public static void main(String[] args) {
        // List：最后一个元素 —— 要自己算下标，还不能处理空列表（会抛 IndexOutOfBounds）
        List<String> list = new ArrayList<>(List.of("a", "b", "c"));
        String last = list.get(list.size() - 1);
        String first = list.get(0);
        System.out.println(first + last);

        // Deque：另一套名字（peekFirst / peekLast / pollFirst / pollLast）
        Deque<String> dq = new ArrayDeque<>(list);
        System.out.println(dq.peekFirst() + dq.peekLast());

        // LinkedHashSet：虽然有顺序，但完全没有 getFirst / getLast —— 取最后一个只能遍历到底，O(n)
        Set<String> set = new LinkedHashSet<>(list);
        String lastOfSet = null;
        for (String s : set) lastOfSet = s;
        System.out.println(lastOfSet);

        // LinkedHashMap：取第一个 entry 要走迭代器；最后一个又只能遍历到底
        Map<String, Integer> lhm = new LinkedHashMap<>();
        lhm.put("x", 1); lhm.put("y", 2); lhm.put("z", 3);
        Iterator<Map.Entry<String, Integer>> it = lhm.entrySet().iterator();
        Map.Entry<String, Integer> firstEntry = it.next();
        Map.Entry<String, Integer> lastEntry = firstEntry;
        while (it.hasNext()) lastEntry = it.next();
        System.out.println(firstEntry.getKey() + lastEntry.getKey());

        // 反向遍历：List 要 copy + Collections.reverse（或者倒着写 for）；Set / Map 没有简单办法
        List<String> copy = new ArrayList<>(list);
        Collections.reverse(copy);
        System.out.println(copy);

        // TreeMap 倒是有 firstEntry / lastEntry（来自 NavigableMap），但这个能力和 LinkedHashMap 不通用
        TreeMap<Integer, String> tm = new TreeMap<>(Map.of(1, "one", 2, "two"));
        System.out.println(tm.firstEntry().getValue() + tm.lastEntry().getValue());
    }
}
