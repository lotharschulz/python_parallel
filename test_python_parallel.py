#!/usr/bin/env python3
import time
from threading import Thread
from multiprocessing import Process, Queue
import math
import types
import datetime


iterations = 10  # 250000
last_fib_number_digits = 2  # 52247
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
        if isinstance(results, types.ListType):
            results.append(fibonacci)
        if not isinstance(queue, types.NoneType):
            queue.put(fibonacci)
    if not isinstance(queue, types.NoneType):
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
    if not collect_fibs(iterations, result_list):
        raise Exception('collect_fibs function failed to return True')
    assert last_fib_number_digits <= int(math.log10(result_list[-1]))+1


def get_complete_queue_sorted(que):
    queue_values = set()
    if not que.empty():
        for i in iter(que.get, 'STOP'):
            queue_values.add(i)
        time.sleep(.1)
    r = list(queue_values)
    r.sort()
    return r


if __name__ == "__main__":
    print("sequential execution")
    start = datetime.datetime.now()
    f = fib(iterations)
    fib_list = []
    for x in f:
        fib_list.append(x)
    end = (datetime.datetime.now() - start).total_seconds()
    print("fibonacci list: {}\nfibonacci list length: {:d}\n"
          "number of digits fibonacci list last item : {:d}\ntime taken: {:f}\n".
          format(fib_list, len(fib_list), int(math.log10(fib_list[-1]))+1, end))

    print("multi threading")
    start = datetime.datetime.now()
    multi_threading_results1 = []
    multi_threading_results2 = []
    p1 = Thread(target=collect_fibs, args=(iterations, multi_threading_results1, None, ))
    p2 = Thread(target=collect_fibs, args=(iterations, multi_threading_results2, None, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = (datetime.datetime.now() - start).total_seconds()
    print("fibonacci list 1: {}\n"
          "fibonacci list 2: {}\n"
          "fibonacci list 1 length: {:d}\n"
          "fibonacci list 2 length: {:d}\n"
          "number of digits fibonacci list 1 last item : {:d}\n"
          "number of digits fibonacci list 2 last item : {:d}\n"
          "time taken: {:f}\n"
          .format(multi_threading_results1, multi_threading_results2,
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
    queue_items = get_complete_queue_sorted(q)

    print("successfully finished: {}\nfibonacci list: {}\nfibonacci list length: {:d}\n"
          "number of digits fibonacci list last item : {:d}\ntime taken: {:f}\n"
          .format(result, queue_items, len(queue_items),
                  int(math.log10(queue_items[-1])) + 1, end))
