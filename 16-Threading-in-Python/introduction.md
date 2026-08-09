# 🧵 Threading in Python（多线程）

> 适用 Python 3.8+。`threading` 适合在单进程内并发处理 I/O 任务，共享状态必须通过同步原语或线程安全队列协调。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

同一进程中的线程共享内存、文件描述符和模块状态。共享降低了通信成本，也带来竞态、死锁和可见性问题。

| 原语 | 用途 |
| --- | --- |
| `Lock` | 同一时刻只允许一个线程进入临界区 |
| `RLock` | 同一线程可重复获取的可重入锁 |
| `Event` | 在线程间广播一个布尔状态 |
| `Condition` | 等待受锁保护的状态条件 |
| `Semaphore` | 限制同时访问资源的线程数量 |
| `queue.Queue` | 线程安全的任务或数据传递 |

## 2. 核心用法

`start()` 启动线程，`join()` 等待线程结束；`args` 必须是元组：

```python
from threading import Thread

results = [None, None, None]

def square(index, value):
    results[index] = value * value

threads = [
    Thread(target=square, args=(index, value))
    for index, value in enumerate([2, 3, 4])
]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(results)  # [4, 9, 16]
```

复合读改写必须保护整个临界区，锁优先作为上下文管理器使用：

```python
from threading import Lock, Thread

counter = 0
lock = Lock()

def increment(times):
    global counter
    for _ in range(times):
        with lock:
            counter += 1

threads = [Thread(target=increment, args=(1000,)) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(counter)  # 4000
```

## 3. 关键机制

生产者—消费者模式通常用 `Queue`，避免手动管理共享列表与条件变量：

```python
from queue import Queue
from threading import Thread

queue = Queue()
results = []

def worker():
    while True:
        item = queue.get()
        try:
            if item is None:
                return
            results.append(item * item)
        finally:
            queue.task_done()

thread = Thread(target=worker)
thread.start()

for value in range(4):
    queue.put(value)
queue.put(None)  # 哨兵通知退出

queue.join()
thread.join()
print(results)  # [0, 1, 4, 9]
```

`Queue.get()` 和 `put()` 可阻塞，`task_done()` 必须与每次成功的 `get()` 配对，`join()` 才能在全部任务完成后返回。

标准 CPython 构建的 GIL 限制 Python 字节码并行，但不会消除线程切换或数据竞争。I/O 操作和部分 C 扩展可释放 GIL。

## 4. 常见陷阱与工程实践

- 不依赖“看起来原子”的实现细节；共享不变量应由锁或消息传递保护。
- 多把锁应采用固定获取顺序，并缩短临界区，降低死锁风险。
- 不使用 `queue.empty()` 做并发终止判断；结果在检查后可能立即变化。
- 守护线程会在进程退出时被突然停止，不适合必须提交事务或释放资源的工作。
- `Thread` 中未处理异常不会自动在调用线程重新抛出；需要收集结果时优先 `ThreadPoolExecutor`。
- 阻塞操作应设置超时，并用 `Event`、哨兵或取消标志实现可控关闭。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `start()` 与直接调用 `run()` 有何区别？ | `start()` 创建并调度新线程；直接 `run()` 仍在当前线程执行 |
| `join()` 做什么？ | 阻塞调用线程，直到目标线程结束或超时 |
| 为什么 `counter += 1` 仍可能需要锁？ | 它是读、计算、写的复合操作，不能把 GIL 当业务锁 |
| `Lock` 与 `RLock` 有何区别？ | 后者允许同一线程重复获取，并要求对应次数释放 |
| Queue 为什么适合线程通信？ | 它封装了同步和阻塞，减少直接共享状态 |

## 6. 参考资料

- [Python 官方文档：threading](https://docs.python.org/3/library/threading.html)
- [Python 官方文档：queue](https://docs.python.org/3/library/queue.html)
- [Python 官方文档：ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
- [Python 官方文档：Synchronization primitives](https://docs.python.org/3/library/threading.html#lock-objects)
- [参考 Notebook：16-Threading in Python.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/16-Threading%20in%20Python.ipynb)
