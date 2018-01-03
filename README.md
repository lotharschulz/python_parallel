# Python parallel sample

execution example of a fibonacci function using 
- [threading](https://docs.python.org/3/library/threading.html#module-threading)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing)

## precondition
python 3.x installed

## set up
```
pip3 install pytest
```

## run
```
python test_python_parallel.py
```

## test
```
pytest -v
```

## note 

[CPython implementation detail](https://docs.python.org/3.6/library/threading.html#threading.Thread.setDaemon):

_CPython implementation detail: In CPython, due to the Global Interpreter Lock, only one thread can execute Python code at once (even though certain performance-oriented libraries might overcome this limitation). If you want your application to make better use of the computational resources of multi-core machines, you are advised to use multiprocessing or concurrent.futures.ProcessPoolExecutor. However, threading is still an appropriate model if you want to run multiple I/O-bound tasks simultaneously._