# ⚖️ Python Threading vs. Multiprocessing

> 适用 Python 3.8+。并发模型应根据任务瓶颈、状态共享、隔离需求和运行环境选择，而不是只比较线程与进程数量。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 维度 | 线程 | 进程 |
| --- | --- | --- |
| 地址空间 | 同一进程内共享 | 默认相互隔离 |
| 创建与切换成本 | 较低 | 较高 |
| 数据交换 | 共享对象，需同步 | 队列、管道、共享内存等 IPC |
| 故障隔离 | 较弱 | 较强 |
| 标准 CPython 的 CPU 密集型并行 | 通常受 GIL 限制 | 可利用多个 CPU 核心 |
| 典型场景 | 网络、磁盘等 I/O 密集任务 | 纯 Python CPU 密集计算 |

并发表示多个任务在时间上重叠推进；并行表示多个任务在同一时刻实际执行。线程可以提供并发，但在标准 GIL 构建的 CPython 中不一定提供 Python 字节码并行。

## 2. 核心用法

I/O 等待型任务可使用线程池：

```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def wait_and_return(value):
    sleep(0.01)  # 模拟 I/O 等待
    return value * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(wait_and_return, range(6)))

print(results)  # [0, 2, 4, 6, 8, 10]
```

纯 Python CPU 密集任务可使用进程池。进程入口必须受 `if __name__ == "__main__"` 保护：

```python
from concurrent.futures import ProcessPoolExecutor

def square(value):
    return value * value

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, range(6)))
    print(results)  # [0, 1, 4, 9, 16, 25]
```

高层 `concurrent.futures` API 统一了提交任务、获取结果和传播异常的方式；需要精细生命周期与 IPC 控制时再直接使用 `threading` 或 `multiprocessing`。

## 3. 关键机制

标准 CPython 构建中的 GIL 保证同一解释器内通常只有一个线程执行 Python 字节码。线程在阻塞 I/O 时会释放执行机会，许多 C 扩展也会在耗时原生计算期间释放 GIL，因此线程对某些任务仍可并行受益。

从 Python 3.13 起，CPython 提供可禁用 GIL 的 free-threaded 构建，但它不是所有安装的默认模式，第三方扩展兼容性也需单独确认。即使没有 GIL，共享可变状态仍可能产生数据竞争，锁和消息传递依然必要。

进程拥有独立解释器和 GIL，可在多个核心上执行 Python 代码；代价包括启动、序列化、IPC 和额外内存。任务过小可能无法抵消这些成本。

## 4. 常见陷阱与工程实践

- 先测量任务是 CPU、I/O、锁竞争还是外部服务瓶颈，再选择并发模型。
- 不要把线程安全等同于“有 GIL”；复合读改写操作仍需同步。
- 进程任务及参数通常必须可序列化，函数应定义在可导入模块顶层。
- 控制工作者数量，避免线程、进程与底层库线程叠加造成过度调度。
- 并发任务必须设置超时、取消和错误传播策略，不能只调用 `start()` 后忽略结果。
- 共享状态越少越容易推理；优先不可变数据、消息队列和明确所有权。
- 在目标操作系统和实际负载下基准测试，进程启动方式与性能会因平台不同。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| I/O 密集任务为何适合线程？ | 一个线程等待 I/O 时，其他线程可继续推进 |
| CPU 密集任务为何常用多进程？ | 每个进程有独立解释器，可绕开单个 GIL 的限制 |
| GIL 是否保证业务数据线程安全？ | 不保证，复合操作和共享状态仍需同步 |
| 多进程的主要成本是什么？ | 进程启动、内存、序列化和 IPC |
| free-threaded CPython 是否消除同步需求？ | 不会；并行共享访问反而更需要正确同步 |

## 6. 参考资料

- [Python 官方文档：threading](https://docs.python.org/3/library/threading.html)
- [Python 官方文档：multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Python 官方文档：concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Python 官方 HOWTO：Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html)
- [参考 Notebook：15-Threading vs Multiprocessing.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/15-Threading%20vs%20Multiprocessing.ipynb)
