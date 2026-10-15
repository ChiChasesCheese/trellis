import java.util.Map;
import java.util.NavigableMap;
import java.util.Random;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentSkipListMap;

/**
 * Companion to ordered_maps_trees.md: unbalanced BST vs random BST height, a minimal skip list,
 * and the TreeMap / ConcurrentSkipListMap navigation API on an order-book-like example.
 * Run:  javac --release 21 --enable-preview TreeDemo.java && java --enable-preview TreeDemo
 */
public class TreeDemo {

    // ---- a plain (unbalanced) binary search tree, iterative insert so deep trees do not overflow the stack ----
    static final class Bst {
        static final class Node { final int key; Node left, right; Node(int k) { key = k; } }
        Node root;
        int size;

        void insert(int key) {
            if (root == null) { root = new Node(key); size++; return; }
            Node cur = root;
            while (true) {
                if (key == cur.key) return;
                if (key < cur.key) { if (cur.left == null) { cur.left = new Node(key); size++; return; } cur = cur.left; }
                else               { if (cur.right == null) { cur.right = new Node(key); size++; return; } cur = cur.right; }
            }
        }

        int height() { return height(root); }
        private int height(Node n) {   // recursion depth = tree height; only call on trees of modest height
            return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right));
        }
    }

    // ---- a minimal skip list (insert + contains), Pugh 1990 -----------------------------------------------
    static final class SkipList {
        static final int MAX_LEVEL = 32;
        static final class Node {
            final int key; final Node[] next;
            Node(int key, int level) { this.key = key; this.next = new Node[level]; }
        }
        final Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
        final Random rnd = new Random(1);
        int levels = 1;

        int randomLevel() {                        // coin flips: P(level >= k) = 2^-(k-1)
            int lvl = 1;
            while (lvl < MAX_LEVEL && rnd.nextBoolean()) lvl++;
            return lvl;
        }

        boolean contains(int key) {
            Node x = head;
            for (int i = levels - 1; i >= 0; i--) {            // start at the top lane, drop down when we would overshoot
                while (x.next[i] != null && x.next[i].key < key) x = x.next[i];
            }
            x = x.next[0];
            return x != null && x.key == key;
        }

        void insert(int key) {
            Node[] update = new Node[MAX_LEVEL];               // last node before `key` on each lane
            Node x = head;
            for (int i = levels - 1; i >= 0; i--) {
                while (x.next[i] != null && x.next[i].key < key) x = x.next[i];
                update[i] = x;
            }
            int lvl = randomLevel();
            if (lvl > levels) { for (int i = levels; i < lvl; i++) update[i] = head; levels = lvl; }
            Node n = new Node(key, lvl);
            for (int i = 0; i < lvl; i++) { n.next[i] = update[i].next[i]; update[i].next[i] = n; }
        }
    }

    public static void main(String[] args) {
        heights();
        skipList();
        treeMapApi();
        skipListMapApi();
    }

    static void heights() {
        System.out.println("== 1. BST height: sorted inserts vs random inserts (n = 5,000) ==");
        int n = 5_000;
        Bst sorted = new Bst();
        for (int i = 0; i < n; i++) sorted.insert(i);
        Bst random = new Bst();
        int[] keys = new Random(3).ints(0, 1_000_000).distinct().limit(n).toArray();
        for (int k : keys) random.insert(k);
        System.out.printf("sorted inserts: height %d  (a linked list)%n", sorted.height());
        System.out.printf("random inserts: height %d  (log2(%d) = %.1f)%n", random.height(), random.size, Math.log(random.size) / Math.log(2));
    }

    static void skipList() {
        System.out.println("\n== 2. skip list: 1,000,000 sorted inserts (the worst case for a plain BST) ==");
        SkipList sl = new SkipList();
        int n = 1_000_000;
        for (int i = 0; i < n; i++) sl.insert(i);
        int hits = 0;
        for (int i = 0; i < n; i += 1000) if (sl.contains(i)) hits++;
        System.out.printf("lanes used: %d (log2(n) = %.1f), lookups found: %d of 1000%n", sl.levels, Math.log(n) / Math.log(2), hits);
    }

    static void treeMapApi() {
        System.out.println("\n== 3. TreeMap navigation on an order-book-like map (price -> resting quantity) ==");
        TreeMap<Integer, Integer> asks = new TreeMap<>();
        asks.put(101, 50); asks.put(103, 20); asks.put(105, 70); asks.put(110, 10);
        System.out.println("asks                  = " + asks);
        System.out.println("firstKey / lastKey    = " + asks.firstKey() + " / " + asks.lastKey());
        System.out.println("floorKey(104)   (<=)  = " + asks.floorKey(104));
        System.out.println("lowerKey(103)   (< )  = " + asks.lowerKey(103));
        System.out.println("ceilingKey(104) (>=)  = " + asks.ceilingKey(104));
        System.out.println("higherKey(105)  (> )  = " + asks.higherKey(105));
        System.out.println("floorKey(100)         = " + asks.floorKey(100) + "   (null: nothing <= 100)");
        System.out.println("headMap(105)          = " + asks.headMap(105) + "   (exclusive)");
        System.out.println("headMap(105, true)    = " + asks.headMap(105, true));
        System.out.println("tailMap(105)          = " + asks.tailMap(105) + "   (inclusive)");
        System.out.println("subMap(103, 110)      = " + asks.subMap(103, 110) + "   ([from, to) )");
        System.out.println("descendingMap()       = " + asks.descendingMap());

        Map.Entry<Integer, Integer> best = asks.firstEntry();
        System.out.println("firstEntry()          = " + best);
        try { best.setValue(0); } catch (UnsupportedOperationException e) { System.out.println("firstEntry().setValue -> UnsupportedOperationException (snapshot entry)"); }

        // views are live
        NavigableMap<Integer, Integer> cheap = asks.headMap(104, true);
        asks.put(102, 5);
        System.out.println("live view after put(102): " + cheap);
        try { cheap.put(200, 1); } catch (IllegalArgumentException e) { System.out.println("put outside view range -> IllegalArgumentException"); }

        // sweeping: consume the best level until 80 units are bought
        int need = 80;
        System.out.print("buy 80 units sweeping asks: ");
        while (need > 0 && !asks.isEmpty()) {
            Map.Entry<Integer, Integer> lvl = asks.firstEntry();
            int take = Math.min(need, lvl.getValue());
            System.out.print(take + "@" + lvl.getKey() + " ");
            need -= take;
            if (take == lvl.getValue()) asks.pollFirstEntry(); else asks.put(lvl.getKey(), lvl.getValue() - take);
        }
        System.out.println("-> remaining book " + asks);

        // comparator-defined equality
        TreeMap<String, Integer> ci = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
        ci.put("AAPL", 1); ci.put("aapl", 2);
        System.out.println("case-insensitive TreeMap after put(AAPL), put(aapl): " + ci + "  size=" + ci.size());
    }

    static void skipListMapApi() {
        System.out.println("\n== 4. ConcurrentSkipListMap: same NavigableMap API, safe for concurrent use ==");
        ConcurrentSkipListMap<Integer, String> m = new ConcurrentSkipListMap<>();
        m.put(30, "c"); m.put(10, "a"); m.put(20, "b");
        System.out.println("map = " + m + ", ceilingKey(11) = " + m.ceilingKey(11) + ", pollFirstEntry = " + m.pollFirstEntry());
        System.out.println("after poll = " + m);
    }
}
