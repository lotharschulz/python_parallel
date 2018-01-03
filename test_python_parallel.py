#!/usr/bin/env python3
import time
from threading import Thread
from multiprocessing import Process, Queue
import math
import datetime

iterations = 100  # 250000 100 10
last_fib_number_digits = 21  # 52247 21 2
queue_stop = "STOP"


def fib(n):
    curr, next_number, counter = 0, 1, 0
    while True:
        if counter >= n:
            return
        yield curr
        curr, next_number = next_number, curr + next_number
        counter += 1


def collect_fibs(ns, results, queue):
    fibonaccies = fib(ns)
    for fibonacci in fibonaccies:
        if results is not None:
            results.append(fibonacci)
        if queue is not None:
            queue.put(fibonacci)
    if queue is not None:
        queue.put(queue_stop)
    return True


def test_fib():
    fibs = fib(iterations)
    last_fib = 0
    for fs in fibs:
        last_fib = fs
    assert last_fib_number_digits <= int(math.log10(last_fib))+1


def test_collect_fibs():
    result_list = []
    que = Queue()
    t1 = Thread(target=collect_fibs, args=(iterations, result_list, que, ))
    t1.start()
    t1.join()
    assert last_fib_number_digits <= int(math.log10(max(result_list)))+1
    queue_list = get_complete_queue(que)
    assert last_fib_number_digits <= int(math.log10(max(queue_list)))+1


def get_complete_queue(que):
    queue_values = set()
    if not que.empty():
        for i in iter(que.get, queue_stop):
            queue_values.add(i)
        time.sleep(.1)
    return list(queue_values)


if __name__ == "__main__":
    print("sequential execution")
    start = datetime.datetime.now()
    f = fib(iterations)
    fib_list = []
    for x in f:
        fib_list.append(x)
    end = (datetime.datetime.now() - start).total_seconds()
    print("fibonacci list length: {:d}\n"
          "number of digits fibonacci list last item : {:d}\ntime taken: {:f}\n".
          format(
            len(fib_list), int(math.log10(fib_list[-1]))+1, end))

    print("multi threading")
    start = datetime.datetime.now()
    multi_threading_results1 = []
    multi_threading_results2 = []
    p1 = Thread(target=collect_fibs, args=(iterations / 2, multi_threading_results1, None, ))
    p2 = Thread(target=collect_fibs, args=(iterations / 2, multi_threading_results2, None, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = (datetime.datetime.now() - start).total_seconds()
    print("fibonacci list 1 length: {:d}\n"
          "fibonacci list 2 length: {:d}\n"
          "number of digits fibonacci list 1 last item : {:d}\n"
          "number of digits fibonacci list 2 last item : {:d}\n"
          "time taken: {:f}\n"
          .format(
                len(multi_threading_results1), len(multi_threading_results2),
                int(math.log10(multi_threading_results1[-1])) + 1, int(math.log10(multi_threading_results2[-1]))+1,
                end))

    print("multi processing")
    start = datetime.datetime.now()
    q = Queue()
    p1 = Process(target=collect_fibs, args=(iterations, None, q, ))
    p2 = Process(target=collect_fibs, args=(iterations, None, q, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    result = p1.exitcode == 0 and p2.exitcode == 0
    end = (datetime.datetime.now() - start).total_seconds()
    queue_items = get_complete_queue(q)
    print("successfully finished: {}\n"
          "fibonacci list length: {:d}\n"
          "number of digits fibonacci list biggest item : {:d}\ntime taken: {:f}\n"
          .format(result,
                  len(queue_items),
                  int(math.log10(max(queue_items))) + 1, end))
