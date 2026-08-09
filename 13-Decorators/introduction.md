# 🎁 Python Decorators（装饰器）

> 适用 Python 3.8+。装饰器接收可调用对象并返回替代对象，用于在不修改核心实现的前提下复用横切逻辑。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

函数是第一类对象，可以被传入、返回和重新绑定。装饰器语法：

```python
@decorator
def target():
    pass
```

等价于：

```python
def target():
    pass

target = decorator(target)
```

装饰发生在函数定义执行时，通常也就是模块导入阶段；调用 `target()` 时实际调用装饰器返回的对象。

## 2. 核心用法

通用函数装饰器应透传参数、返回值，并用 `functools.wraps()` 保留元数据：

```python
from functools import wraps

def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__}")
        result = function(*args, **kwargs)
        print(f"returned {result!r}")
        return result
    return wrapper

@traced
def add(left, right=0):
    """Return the sum."""
    return left + right

print(add(2, right=3))  # 5
print(add.__name__)      # add
```

带参数装饰器需要再增加一层函数：

```python
from functools import wraps

def repeat(times):
    if times < 1:
        raise ValueError("times must be positive")

    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = function(*args, **kwargs)
            return result
        return wrapper
    return decorate

@repeat(3)
def greet(name):
    print(f"Hello, {name}")

greet("Ada")
```

## 3. 关键机制

多个装饰器从下向上应用：

```python
@outer
@inner
def target():
    pass

# 等价于 target = outer(inner(target))
```

调用时通常先进入 `outer` 的包装器，再进入 `inner`。应用顺序与运行时进入/退出顺序要分开理解。

类也可作为有状态装饰器，只需实例可调用：

```python
from functools import update_wrapper

class CountCalls:
    def __init__(self, function):
        update_wrapper(self, function)
        self.function = function
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.function(*args, **kwargs)

@CountCalls
def ping():
    return "pong"

ping()
ping()
print(ping.count)  # 2
```

常见用途包括鉴权、缓存、重试、指标、注册、事务和日志。标准库已经提供 `lru_cache`、`singledispatch`、`property` 等成熟装饰器。

## 4. 常见陷阱与工程实践

- 忘记返回被装饰函数的结果，会把正常返回值变成 `None`。
- 忘记 `wraps()` 会丢失 `__name__`、`__doc__`、签名关联和 `__wrapped__`。
- 装饰器导入时执行外层逻辑，不要在此进行昂贵 I/O 或依赖尚未初始化的全局状态。
- 同步包装器不能正确包装异步函数；`async def` 需要异步包装器并 `await` 原函数。
- 重试装饰器必须限制次数、区分可重试异常，并考虑幂等性和退避策略。
- 装饰层过多会隐藏控制流，应保持单一职责并提供测试。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 装饰器本质是什么？ | 接收对象并返回替代对象的可调用对象 |
| 为什么使用 `functools.wraps`？ | 保留原函数元数据并提供 `__wrapped__` 链接 |
| 带参数装饰器为什么有三层函数？ | 外层接收配置，中层接收被装饰函数，内层处理调用 |
| 多个装饰器按什么顺序应用？ | 从靠近函数的装饰器开始，由下向上应用 |
| 类装饰器适合什么场景？ | 需要跨调用保存状态时，但应注意方法绑定与线程安全 |

## 6. 参考资料

- [Python 语言参考：Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
- [Python 官方文档：functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- [Python 官方文档：functools](https://docs.python.org/3/library/functools.html)
- [参考 Notebook：13-Decoratos.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/13-Decoratos.ipynb)
