# Coupled Heap and Two-Processor Job Scheduler

A heap built from scratch that supports two independent priority orders at once, and a greedy two-processor job scheduler that uses it.

*Individual assignment for a Programming with Data Structures course at IIT Delhi (2026).*

## Coupled Heap

Keeps elements ordered under two priorities, X and Y, at the same time. Ties go to the larger id, on both axes.

| Operation | Complexity |
|---|---|
| `enqueue(id, x_pri, y_pri)` | O(log n) |
| `peekMaxX()` / `peekMaxY()` | O(1) |
| `extractMaxX()` / `extractMaxY()` | O(log n) |

**Implementation.** Two array-based binary heaps, one per priority, hold the same element objects. Each element records its index in both arrays, and every swap in one heap updates the stored index seen by the other. To extract from one heap:
1. Replace the root with the last element and sift down.
2. Use the removed element's stored index to find it in the other heap.
3. Replace it there with that heap's last element, and repair the hole with a sift-up and a sift-down, since the replacement may need to move in either direction.

An element removed through one axis disappears from both. No `heapq` or other library heap is used.

## Scheduler

`solve_scheduling(jobs)` takes jobs `(arrival, t0, t1, p0, p1)`. Here t0 and t1 are the processing times on processors P0 and P1, and p0 and p1 are the profits earned on them. It returns `(total_profit, total_waiting_time)`.

- Each idle processor immediately takes the waiting job with the best profit-to-time ratio for itself (p0/t0 for P0, p1/t1 for P1). P0 chooses first when both are free.
- Jobs run without pre-emption, and a processor can start a new job at the instant it finishes one.
- Ties go to the smaller job index. The heap prefers the larger id, so jobs are enqueued with id `-i`, which reverses the order and still lets the job be recovered from the id.
- The simulation jumps from event to event (job arrivals and processor completions) instead of stepping through time.

Each job is enqueued once and extracted once, so the scheduler runs in O(N log N) time and O(N) space.

## Example

```python
from student_code import solve_scheduling

jobs = [(1, 2, 2, 6, 2),
        (1, 2, 2, 2, 6)]
solve_scheduling(jobs)   # (12, 0)
```

P0 takes job 0 (ratio 3 vs 1) and P1 takes job 1 (ratio 3 vs 1), both at time 1, so profit is 6 + 6 = 12 and nobody waits.
