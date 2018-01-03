#!/usr/bin/env python3
import time
from threading import Thread
from multiprocessing import Process
import math


iterations = 10  # 250000
last_fib_number_digits = 2  # 52247


def fib(n):
    curr, next_number, counter = 0, 1, 0
    while True:
        if counter >= n:
            return
        yield curr
        curr, next_number = next_number, curr + next_number
        counter += 1


def collect_fibs(ns, results):
    fibonaccies = fib(ns)
    for fibonacci in fibonaccies:
        results.append(fibonacci)
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


if __name__ == "__main__":
    print("sequential execution")
    start = time.time()
    f = fib(iterations)
    fib_list = []
    for x in f:
        fib_list.append(x)
    end = time.time()
    print("fib_list: {}, len(fib_list): {:d}, len(fib_list[-1]): {:d}, time taken: {:f}".
          format(fib_list, len(fib_list), len(str(fib_list[-1])), end))

    print("multi threading")
    start = time.time()
    p1 = Thread(target=fib, args=(iterations / 2,))
    p1.start()
    p2 = Thread(target=fib, args=(iterations / 2,))
    p2.start()
    p1.join()
    p2.join()
    # check return values
    end = time.time()
    print("time taken: {:f}".format(end))

    print("multi processing")
    start = time.time()
    p1 = Process(target=fib, args=(iterations / 2,))
    p1.start()
    p2 = Process(target=fib, args=(iterations / 2,))
    p2.start()
    p1.join()
    p2.join()
    result = p1.exitcode == 0 and p2.exitcode == 0
    # check return values
    end = time.time()
    print("successful: {}, time taken: {:f}".format(result, end))
