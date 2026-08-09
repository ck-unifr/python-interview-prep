# 🚪 Python Context Managers（上下文管理器）

> 适用 Python 3.8+。上下文管理器用 `with` 明确资源或状态的进入与退出边界，即使发生异常也能可靠清理。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

上下文管理协议由两个方法组成：

| 方法 | 作用 |
| --- | --- |
| `__enter__()` | 进入上下文，获取资源并返回 `as` 绑定的对象 |
| `__exit__(exc_type, exc_value, traceback)` | 退出上下文，释放资源并决定异常是否继续传播 |

`__exit__()` 返回真值会压制上下文中的异常；返回 `False` 或 `None` 则继续传播。

## 2. 核心用法

类形式适合需要保存状态的管理器：

```python
from time import perf_counter, sleep

class Timer:
    def __enter__(self):
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = perf_counter() - self.started_at
        return False

with Timer() as timer:
    sleep(0.01)

print(timer.elapsed > 0)  # True
```

`contextlib.contextmanager` 用单次 `yield` 分隔进入与退出逻辑：

```python
from contextlib import contextmanager

@contextmanager
def transaction(store):
    snapshot = store.copy()
    try:
        yield store
    except Exception:
        store.clear()
        store.update(snapshot)
        raise

account = {"balance": 100}
with transaction(account):
    account["balance"] -= 20

print(account)  # {'balance': 80}
```

文件、线程锁和数据库事务都是典型上下文资源：

```python
from threading import Lock

lock = Lock()
with lock:
    # 临界区结束后自动释放锁
    protected_value = 42
```

## 3. 关键机制

`with manager as value:` 的核心语义接近：先调用 `__enter__()`，再执行主体，最后在清理路径调用 `__exit__()`。如果 `__enter__()` 本身失败，尚未成功进入上下文，因此不会调用该对象的 `__exit__()`。

多个上下文管理器按从左到右进入、从右到左退出：

```python
with manager_a() as a, manager_b() as b:
    use(a, b)
```

动态数量的上下文管理器可使用 `contextlib.ExitStack` 注册，并统一按后进先出顺序清理。异步资源对应 `async with`、`__aenter__()`、`__aexit__()` 和 `AsyncExitStack`。

## 4. 常见陷阱与工程实践

- `__exit__()` 不应无条件返回 `True`，否则会静默吞掉所有异常。
- `@contextmanager` 生成器必须恰好 `yield` 一次，并把清理逻辑放入 `finally` 或明确异常路径。
- 不要只处理正常退出；清理逻辑必须覆盖异常和提前返回。
- 资源获取若分多步完成，应在失败时释放已经获取的部分，复杂场景使用 `ExitStack`。
- 上下文管理器负责生命周期，不应隐藏与生命周期无关的大量业务逻辑。
- 事务管理器压制异常前必须有明确契约，否则调用方可能误以为操作成功。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `as` 后的值来自哪里？ | `__enter__()` 的返回值 |
| `__exit__()` 的三个异常参数是什么？ | 异常类型、异常实例和 traceback；正常退出时都为 `None` |
| 如何让异常继续传播？ | `__exit__()` 返回 `False` 或 `None`，生成器管理器中重新抛出 |
| 多个管理器的退出顺序是什么？ | 与进入顺序相反，后进入先退出 |
| 类管理器与 `@contextmanager` 如何选择？ | 状态和复用复杂时用类；单一获取—释放流程可用生成器形式 |

## 6. 参考资料

- [Python 语言参考：The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
- [Python 数据模型：Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Python 官方文档：contextlib](https://docs.python.org/3/library/contextlib.html)
- [Python 官方文档：ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack)
- [参考 Notebook：21-Context manager.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/21-Context%20manager.ipynb)
