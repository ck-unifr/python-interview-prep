# 🚨 Python Exceptions（异常）

> 适用 Python 3.8+。异常用于报告和传播运行时失败，应在能够恢复、补充上下文或转换边界语义的位置处理。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

- `SyntaxError` 表示源码无法被正确解析，通常在程序运行前发现。
- 异常表示语法合法的代码在执行时无法完成操作，例如 `ValueError`、`TypeError`、`KeyError`。
- 大多数应用异常继承自 `Exception`；`SystemExit`、`KeyboardInterrupt` 等直接继承自 `BaseException`，通常不应被业务代码吞掉。
- `raise` 主动抛出异常，`try/except` 处理预期失败，`finally` 保证清理逻辑执行。

## 2. 核心用法

捕获范围应尽量小，并针对具体异常：

```python
def parse_port(raw):
    try:
        port = int(raw)
    except (TypeError, ValueError) as error:
        raise ValueError("port must be an integer") from error
    else:
        if not 1 <= port <= 65535:
            raise ValueError("port out of range")
        return port

print(parse_port("8080"))  # 8080
```

`else` 仅在 `try` 未抛异常时执行，可避免把后续代码意外纳入捕获范围。`finally` 无论是否发生异常都会执行：

```python
def divide(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return None
    finally:
        print("calculation finished")

print(divide(6, 2))  # 3.0
```

自定义异常用于表达领域语义，通常保持结构简单：

```python
class InsufficientBalanceError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"balance={balance}, amount={amount}")
        self.balance = balance
        self.amount = amount

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(balance, amount)
    return balance - amount
```

## 3. 关键机制

异常发生后，解释器沿调用栈向上查找匹配的处理器，这一过程称为栈展开。若没有处理器，程序打印 traceback 并终止当前执行流。

`raise NewError(...) from original` 建立显式异常链，保留底层原因并提供更合适的抽象：

```python
class ConfigError(Exception):
    pass

def load_timeout(config):
    try:
        return int(config["timeout"])
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigError("invalid timeout configuration") from error
```

在 `except` 中单独写 `raise` 会保留原 traceback 重新抛出；写 `raise error` 会改变 traceback 的重新抛出位置。

上下文管理器通常比手写 `try/finally` 更适合资源清理，例如文件、锁和数据库事务。

## 4. 常见陷阱与工程实践

- 避免裸 `except:`；它会捕获 `KeyboardInterrupt` 和 `SystemExit` 等控制流异常。
- 不要用过宽的 `except Exception` 静默忽略错误；至少记录上下文或重新抛出。
- `assert` 用于开发期不变量，不用于参数校验、权限或安全检查，因为优化模式可移除断言。
- 不要在 `finally` 中 `return`，否则可能覆盖正常返回值或压制异常。
- 异常消息应说明失败上下文，但不要泄露密码、令牌或敏感数据。
- 库代码应抛出异常，由应用边界决定记录、重试或转换响应，避免重复记录同一异常。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `else` 何时执行？ | `try` 块没有抛出异常时执行 |
| `finally` 何时执行？ | 正常返回、异常或提前退出时通常都会执行 |
| `raise` 与 `raise error` 有何区别？ | 前者保留当前 traceback 重新抛出；后者会改变重新抛出位置 |
| 为什么不建议裸 `except`？ | 它会捕获通常应继续传播的 `BaseException` 子类 |
| `assert` 能否代替业务校验？ | 不能，优化模式可能移除断言 |

## 6. 参考资料

- [Python 官方教程：Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python 官方文档：Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Python 语言参考：The try statement](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)
- [Python 官方文档：Exception context](https://docs.python.org/3/library/exceptions.html#exception-context)
- [参考 Notebook：09-Exceptions.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/09-Exceptions.ipynb)
