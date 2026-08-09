# 🏭 Multiprocessing in Python（多进程）

> 适用 Python 3.8+。`multiprocessing` 通过独立解释器进程执行任务，适合可拆分的纯 Python CPU 密集计算和需要故障隔离的工作。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

进程默认拥有独立地址空间和 Python 解释器。普通全局变量不会自动同步，数据需要通过序列化消息、共享内存或代理对象交换。

| 组件 | 用途 |
| --- | --- |
| `Process` | 显式创建和管理单个进程 |
| `Pool` | 复用固定数量工作进程并分发任务 |
| `Queue`、`Pipe` | 进程间消息传递 |
| `Value`、`Array`、`shared_memory` | 共享底层内存 |
| `Lock`、`Event`、`Semaphore` | 跨进程同步 |
| `Manager` | 通过服务进程提供共享代理对象 |

## 2. 核心用法

工作函数应定义在模块顶层，进程创建必须放在主入口保护下：

```python
from multiprocessing import Process, Queue

def square(value, output):
    output.put((value, value * value))

if __name__ == "__main__":
    output = Queue()
    processes = [
        Process(target=square, args=(value, output))
        for value in range(4)
    ]

    for process in processes:
        process.start()
    results = [output.get() for _ in processes]
    for process in processes:
        process.join()

    print(sorted(results))
    # [(0, 0), (1, 1), (2, 4), (3, 9)]
```

大量同构任务优先使用进程池：

```python
from multiprocessing import Pool

def cube(value):
    return value ** 3

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.map(cube, range(6))
    print(results)  # [0, 1, 8, 27, 64, 125]
```

共享值的复合更新必须显式加锁：

```python
from multiprocessing import Process, Value

def increment(counter, times):
    for _ in range(times):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)
    workers = [Process(target=increment, args=(counter, 1000)) for _ in range(4)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(counter.value)  # 4000
```

## 3. 关键机制

Python 支持 `spawn`、`fork` 和 `forkserver` 等启动方式，可用性及默认值取决于操作系统和 Python 版本：

- `spawn` 启动全新解释器并导入主模块，隔离清晰但启动较慢。
- `fork` 复制当前进程状态，启动快，但复制多线程进程可能不安全。
- `forkserver` 由单线程服务进程负责派生子进程。

不要依赖平台默认值。需要固定行为时，在程序入口尽早选择上下文：

```python
import multiprocessing as mp

if __name__ == "__main__":
    context = mp.get_context("spawn")
    with context.Pool(2) as pool:
        print(pool.map(abs, [-2, -1, 0, 1]))
```

任务、参数和返回值通常要经过 `pickle` 序列化。数据过大或任务过短时，序列化与 IPC 可能超过并行收益。

## 4. 常见陷阱与工程实践

- 缺少主入口保护会在 `spawn` 环境中递归创建进程。
- Lambda、局部函数和不可序列化资源通常不能直接作为进程任务或参数。
- `value += 1` 是读改写复合操作，即使 `Value` 带锁也应覆盖整个操作。
- 不依赖 `Queue.empty()` 或 `qsize()` 做正确性判断；并发状态会立即变化且部分平台不支持精确结果。
- 子进程异常必须通过结果对象、退出码或监控显式收集。
- 数据量大时优先减少传输、批量任务或使用共享内存；不要频繁往返发送细碎对象。
- 进程池应显式关闭；上下文管理器可以可靠完成清理。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 多进程如何绕开标准 CPython 的 GIL？ | 每个进程拥有独立解释器和 GIL，可在不同核心运行 |
| 为什么需要 `if __name__ == "__main__"`？ | 防止导入主模块时再次创建子进程，尤其是 `spawn` 模式 |
| 进程间为何不能直接共享普通全局变量？ | 进程拥有独立地址空间 |
| Pool 适合什么任务？ | 大量可序列化、相互独立且计算量足以抵消调度成本的任务 |
| 多进程一定更快吗？ | 不一定，启动、序列化、IPC 和调度都可能抵消收益 |

## 6. 参考资料

- [Python 官方文档：multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Python 官方文档：Contexts and start methods](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)
- [Python 官方文档：Process Pools](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool)
- [Python 官方文档：multiprocessing.shared_memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html)
- [参考 Notebook：17-Multiprocessing.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/17-Multiprocessing.ipynb)
