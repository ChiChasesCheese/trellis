import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

/**
 * Companion to heap_priority_queue.md.
 * Part A: a tiny int min-heap that prints every swap (so you can follow sift-up / sift-down by hand).
 * Part B: PriorityQueue pitfalls, demonstrated.
 * Run:  javac --release 21 --enable-preview HeapDemo.java && java --enable-preview HeapDemo
 */
public class HeapDemo {

    /** Array-backed binary min-heap of ints. Children of i are 2i+1 and 2i+2; parent of i is (i-1)/2. */
    static final class MinHeap {
        int[] a = new int[16];
        int size;
        long swaps;
        boolean trace;

        void add(int x) {
            if (size == a.length) a = Arrays.copyOf(a, size * 2);
            a[size] = x;
            siftUp(size++);
        }

        int poll() {
            int top = a[0];
            a[0] = a[--size];
            if (size > 0) siftDown(0);
            return top;
        }

        void siftUp(int i) {
            while (i > 0) {
                int p = (i - 1) / 2;
                if (a[p] <= a[i]) break;          // parent already <= child: heap property holds
                swap(i, p);
                i = p;
            }
        }

        void siftDown(int i) {
            while (true) {
                int l = 2 * i + 1, r = l + 1, m = i;
                if (l < size && a[l] < a[m]) m = l;
                if (r < size && a[r] < a[m]) m = r;
                if (m == i) break;                 // both children >= a[i]
                swap(i, m);
                i = m;
            }
        }

        void swap(int i, int j) {
            swaps++;
            if (trace) System.out.println("    swap a[" + i + "]=" + a[i] + " <-> a[" + j + "]=" + a[j]);
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        /** Floyd's O(n) build: sift down every internal node, from the last one back to the root. */
        static MinHeap heapify(int[] src) {
            MinHeap h = new MinHeap();
            h.a = src.clone();
            h.size = src.length;
            for (int i = h.size / 2 - 1; i >= 0; i--) h.siftDown(i);
            return h;
        }

        public String toString() { return Arrays.toString(Arrays.copyOf(a, size)); }
    }

    record Task(String name, int priority) {}

    public static void main(String[] args) {
        partA();
        partB();
    }

    static void partA() {
        System.out.println("== A1. insert 5 3 8 1 2 one by one (sift-up) ==");
        MinHeap h = new MinHeap();
        h.trace = true;
        for (int x : new int[]{5, 3, 8, 1, 2}) {
            System.out.println("  add " + x);
            h.add(x);
            System.out.println("    -> " + h);
        }
        System.out.println("\n== A2. poll (sift-down) until empty ==");
        while (h.size > 0) {
            System.out.println("  poll");
            int v = h.poll();
            System.out.println("    -> got " + v + ", heap now " + h);
        }

        System.out.println("\n== A3. heapify vs repeated add: number of swaps, n = 1,000,000 random ints ==");
        int n = 1_000_000;
        int[] data = new Random(5).ints(n).toArray();
        MinHeap built = MinHeap.heapify(data);
        MinHeap added = new MinHeap();
        for (int x : data) added.add(x);
        System.out.printf("heapify (sift-down from n/2-1): %,d swaps  (%.2f per element)%n", built.swaps, built.swaps / (double) n);
        System.out.printf("n x add (sift-up)             : %,d swaps  (%.2f per element)%n", added.swaps, added.swaps / (double) n);
    }

    static void partB() {
        System.out.println("\n== B1. iteration order of a PriorityQueue is NOT sorted ==");
        PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(9, 4, 7, 1, 8, 2, 6));
        System.out.println("toString / iterator : " + pq);
        StringBuilder sb = new StringBuilder();
        while (!pq.isEmpty()) sb.append(pq.poll()).append(' ');
        System.out.println("poll() until empty  : " + sb);

        System.out.println("\n== B2. ties: PriorityQueue is not stable ==");
        PriorityQueue<Task> byPrio = new PriorityQueue<>(Comparator.comparingInt(Task::priority));
        for (int i = 0; i < 8; i++) byPrio.add(new Task("t" + i, i % 2));   // priorities 0,1,0,1,...
        StringBuilder order = new StringBuilder();
        while (!byPrio.isEmpty()) order.append(byPrio.poll().name()).append(' ');
        System.out.println("arrival t0..t7, priorities 0 1 0 1 0 1 0 1 -> " + order);

        record Seq(Task t, long seq) {}
        PriorityQueue<Seq> stable = new PriorityQueue<>(
                Comparator.<Seq>comparingInt(s -> s.t().priority()).thenComparingLong(Seq::seq));
        long counter = 0;
        for (int i = 0; i < 8; i++) stable.add(new Seq(new Task("t" + i, i % 2), counter++));
        order.setLength(0);
        while (!stable.isEmpty()) order.append(stable.poll().t().name()).append(' ');
        System.out.println("with sequence-number tie-break            -> " + order);

        System.out.println("\n== B3. mutating a key after insertion silently breaks the heap ==");
        class Box { int k; Box(int k) { this.k = k; } public String toString() { return "" + k; } }
        PriorityQueue<Box> bq = new PriorityQueue<>(Comparator.comparingInt((Box b) -> b.k));
        Box b5 = new Box(5), b6 = new Box(6), b7 = new Box(7), b8 = new Box(8);
        for (Box b : List.of(b5, b6, b7, b8)) bq.add(b);
        b8.k = 1;                                         // "decrease key" done the wrong way
        System.out.println("peek() after b8.k = 1 -> " + bq.peek() + "   (should be 1)");
        bq.remove(b8); bq.add(b8);                        // the correct way: remove (O(n)) and re-add
        System.out.println("peek() after remove+add -> " + bq.peek());

        System.out.println("\n== B4. comparator by subtraction overflows ==");
        PriorityQueue<Integer> bad = new PriorityQueue<>((x, y) -> x - y);
        bad.add(Integer.MIN_VALUE); bad.add(1); bad.add(-1);
        System.out.println("bad comparator poll order  : " + bad.poll() + " " + bad.poll() + " " + bad.poll());
        PriorityQueue<Integer> good = new PriorityQueue<>(Integer::compare);
        good.add(Integer.MIN_VALUE); good.add(1); good.add(-1);
        System.out.println("Integer::compare poll order: " + good.poll() + " " + good.poll() + " " + good.poll());

        System.out.println("\n== B5. max-heap and top-k ==");
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        maxHeap.addAll(List.of(3, 9, 4));
        System.out.println("max-heap peek: " + maxHeap.peek());
        int k = 3;
        PriorityQueue<Integer> topK = new PriorityQueue<>();      // min-heap of the k largest seen so far
        for (int x : new int[]{5, 1, 9, 3, 7, 8, 2}) {
            topK.add(x);
            if (topK.size() > k) topK.poll();
        }
        List<Integer> sorted = new ArrayList<>(topK);
        sorted.sort(null);
        System.out.println("3 largest of 5 1 9 3 7 8 2: " + sorted);
    }
}
