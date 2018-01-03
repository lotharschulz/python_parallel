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


def collect_fibs(ns):
    fibunaccies = fib(ns)
    fibs_list = []
    for fibunacci in fibunaccies:
        fibs_list.append(fibunacci)
    return fibs_list


def test_fib():
    fibs = fib(iterations)
    last_fib = 0
    for fs in fibs:
        last_fib = fs
    assert last_fib_number_digits <= int(math.log10(last_fib))+1


def test_collect_fibs():
    fs = collect_fibs(iterations)
    print("fs: {}".format(fs))
    assert last_fib_number_digits <= int(math.log10(fs[-1]))+1


if __name__ == "__main__":
    n = iterations
    print("sequential execution")
    start = time.time()
    f = fib(n)
    fib_list = []
    for x in f:
        fib_list.append(x)
    end = time.time()
    print("fib_list: {}, len(fib_list): {:d}, len(fib_list[-1]): {:d}, time taken: {:f}".
          format(fib_list, len(fib_list), len(str(fib_list[-1])), end))

    print("multi threading")
    start = time.time()
    p1 = Thread(target=fib, args=(n / 2,))
    p1.start()
    p2 = Thread(target=fib, args=(n / 2,))
    p2.start()
    # check return values
    end = time.time()
    print("time taken: {:f}".format(end))

    print("multi processing")
    start = time.time()
    p1 = Process(target=fib, args=(n / 2,))
    p1.start()
    p2 = Process(target=fib, args=(n / 2,))
    p2.start()
    p1.join()
    p2.join()
    result = p1.exitcode == 0 and p2.exitcode == 0
    # check return values
    end = time.time()
    print("successful: {}, time taken: {:f}".format(result, end))

#    print("##################")
#    test_collect_fibs()
#    test_fib()
